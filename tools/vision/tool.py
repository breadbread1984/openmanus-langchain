#!/usr/bin/python3

from os.path import getsize, splitext
from io import BytesIO
import base64
from typing import Type, List, Optional, Annotated, Literal, Union
from pydantic import BaseModel, Field, ValidationError, model_validator
from langchain_core.tools.structured import StructuredTool
from langchain_core.callbacks.manager import CallbackManagerForToolRun
from PIL import Image

DEFAULT_MAX_WIDTH = 1920
DEFAULT_MAX_HEIGHT = 1080
DEFAULT_JPEG_QUALITY = 85
DEFAULT_PNG_COMPRESS_LEVEL = 6

def load_see_image_tool(configs):
  class SeeImageInput(BaseModel):
    file_path: str = Field(description = "path to image")
  class SeeImageOutput(BaseModel):
    mime_type: str = Field(description = "MIME type of the image")
    base64: str = Field(description = "base64 encoding of the image's bytes")
  class SeeImageTool(StructuredTool):
    name: str = "see_image"
    description: str = "a vision tool that allows agent to read image files. the base64 encoding of the image's bytes is returned. supported formats: JPG, PNG, GIF, WEBP, maximum size: 10MB"
    args_schema: Type[BaseModel] = SeeImageInput
    def _run(self, file_path, run_manager: Optional[CallbackManagerForToolRun] = None):
      file_size_bytes = getsize(file_path)
      if file_size_bytes / 1024**2 > 10:
        raise Exception("image over 10MB is not supported!")
      ext = splitext(file_path)[-1].lower()
      if ext in {'.jpg', '.jpeg'}:
        mime_type = "image/jpeg"
      elif ext in {'.png'}:
        mime_type = "image/png"
      elif ext in {'.gif'}:
        mime_type = "image/gif"
      elif ext in {'.webp'}:
        mime_type = "image/webp"
      else:
        raise Exception("image in format other than JPG, PNG, GIF and WEBP is not supported!")
      # compress image content
      with open(file_path, 'rb') as f:
        img_bytes = f.read()
      img = Image.open(BytesIO(img_bytes))
      if img.mode in ("RGBA", "LA", "P"):
        background = Image.new("RGB", img.size, (255, 255, 255))
        if img.mode == "P":
          img = img.convert("RGBA")
        background.paste(img, mask=img.split()[-1] if img.mode == "RGBA" else None)
        img = background
      width, height = img.size
      if width > DEFAULT_MAX_WIDTH or height > DEFAULT_MAX_HEIGHT:
        ratio = min(DEFAULT_MAX_WIDTH / width, DEFAULT_MAX_HEIGHT / height)
        new_width = int(width * ratio)
        new_height = int(height * ratio)
        img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
      output = BytesIO()
      if mime_type == "image/gif":
        img.save(output, format="GIF", optimize=True)
        output_mime = "image/gif"
      elif mime_type == "image/png":
        img.save(
          output,
          format="PNG",
          optimize=True,
          compress_level=DEFAULT_PNG_COMPRESS_LEVEL,
        )
        output_mime = "image/png"
      else:
        img.save(output, format="JPEG", quality=DEFAULT_JPEG_QUALITY, optimize=True)
        output_mime = "image/jpeg"
      compressed_bytes = output.getvalue()
      base64_image = base64.b64encode(compressed_bytes).decode('utf-8')
      return SeeImageOutput(base64 = base64_image, mime_type = output_mime)
    async def _arun(self, file_path, run_manager: Optional[CallbackManagerForToolRun] = None):
      raise NotImplementedError("Async execution is not supported!")
  return SeeImageTool()
