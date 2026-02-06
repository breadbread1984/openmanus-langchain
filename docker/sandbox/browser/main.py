#!/usr/bin/python3

from os import environ
environ['DISPLAY'] = ':100'
import asyncio
from absl import flags, app
import gradio as gr
from gradio.routes import mount_gradio_app
from fastapi import FastAPI
from browser_manager import BrowserManager

FLAGS = flags.FLAGS

def add_options():
  flags.DEFINE_string('service_host', default = '127.0.0.1', help = 'service host')
  flags.DEFINE_integer('service_port', default = 8081, help = 'service port')

def create_interface(browser_manager):
  # interface definition
  with gr.Blocks(title = "Chromium Manager") as interface:
    with gr.Row():
      # line 1
      with gr.Column():
        # tool 1
        with gr.Row():
          gr.Markdown("# navigate to")
          navigate_to_url = gr.Textbox(label = 'url')
          navigate_to_btn = gr.Button(value = "navigate_to")
        navigate_to_btn.click(browser_manager.navigate_to, inputs = [navigate_to_url], outputs = [], concurrency_limit = 64)
      with gr.Column():
        # tool 2
        with gr.Row():
          gr.Markdown("# go back")
          go_back_btn = gr.Button(value = "go_back")
        go_back_btn.click(browser_manager.go_back, inputs = [], outputs = [], concurrency_limit = 64)
      with gr.Column():
        # tool 3
        with gr.Row():
          gr.Markdown("# wait")
          wait_seconds = gr.Number(label = "seconds", precision = 0)
          wait_btn = gr.Button(value = "wait")
        wait_btn.click(browser_manager.wait, inputs = [wait_seconds], outputs = [], concurrency_limit = 64)
      with gr.Column():
        # tool 4
        with gr.Row():
          gr.Markdown("# mouse click")
          mouse_click_x = gr.Number(label = "x", precision = 0)
          mouse_click_y = gr.Number(label = "y", precision = 0)
          mouse_click_btn = gr.Button(value = "mouse_click")
        mouse_click_btn.click(browser_manager.mouse_click, inputs = [mouse_click_x, mouse_click_y], outputs = [], concurrency_limit = 64)
    with gr.Row():
      # line 2
      with gr.Column():
        # tool 5
        with gr.Row():
          gr.Markdown("# mouse click then type")
          mouse_click_then_type_x = gr.Number(label = "x", precision = 0)
          mouse_click_then_type_y = gr.Number(label = "y", precision = 0)
          mouse_click_then_type_text = gr.Textbox(label = "text")
          mouse_click_then_type_btn = gr.Button(value = "mouse_click_then_type")
        mouse_click_then_type_btn.click(browser_manager.mouse_click_then_type, inputs = [mouse_click_then_type_x, mouse_click_then_type_y, mouse_click_then_type_text], outputs = [], concurrency_limit = 64)
      with gr.Column():
        # tool 6
        with gr.Row():
          gr.Markdown("# send keys")
          send_keys_keys = gr.Textbox(label = "keys")
          send_keys_btn = gr.Button(value = "send_keys")
        send_keys_btn.click(browser_manager.send_keys, inputs = [send_keys_keys], outputs = [], concurrency_limit = 64)
      with gr.Column():
        # tool 7
        with gr.Row():
          gr.Markdown("# switch tab")
          switch_tab_page_id = gr.Number(label = "page_id", precision = 0)
          switch_tab_btn = gr.Button(value = "switch_tab")
        switch_tab_btn.click(browser_manager.switch_tab, inputs = [switch_tab_page_id], outputs = [], concurrency_limit = 64)
      with gr.Column():
        # tool 8
        with gr.Row():
          gr.Markdown("# close tab")
          close_tab_page_id = gr.Number(label = "page_id", precision = 0)
          close_tab_btn = gr.Button(value = "close_tab")
        close_tab_btn.click(browser_manager.close_tab, inputs = [close_tab_page_id], outputs = [], concurrency_limit = 64)
    with gr.Row():
      # line 3
      with gr.Column():
        # tool 9
        with gr.Row():
          gr.Markdown("# scroll down")
          scroll_down_amount = gr.Number(label = "amount", precision = 0)
          scroll_down_btn = gr.Button(value = "scroll_down")
        scroll_down_btn.click(browser_manager.scroll_down, inputs = [scroll_down_amount], outputs = [], concurrency_limit = 64)
      with gr.Column():
        # tool 10
        with gr.Row():
          gr.Markdown("# scroll up")
          scroll_up_amount = gr.Number(label = "amount", precision = 0)
          scroll_up_btn = gr.Button(value = "scroll_up")
        scroll_up_btn.click(browser_manager.scroll_up, inputs = [scroll_up_amount], outputs = [], concurrency_limit = 64)
      with gr.Column():
        # tool 11
        with gr.Row():
          gr.Markdown("# take screenshot")
          take_screenshot_btn = gr.Button(value = "take_screenshot_btn")
          take_screenshot_img = gr.File(label = "download screen shot")
        take_screenshot_btn.click(browser_manager.take_screenshot, inputs = [], outputs = [take_screenshot_img], concurrency_limit = 64)
      with gr.Column():
        # tool 12
        with gr.Row():
          gr.Markdown("# drag and drop")
          drag_and_drop_x1 = gr.Number(label = "x1", precision = 0)
          drag_and_drop_y1 = gr.Number(label = "y1", precision = 0)
          drag_and_drop_x2 = gr.Number(label = "x2", precision = 0)
          drag_and_drop_y2 = gr.Number(label = "y2", precision = 0)
          drag_and_drop_btn = gr.Button(value = "drag_and_drop")
        drag_and_drop_btn.click(browser_manager.drag_and_drop, inputs = [drag_and_drop_x1, drag_and_drop_y1, drag_and_drop_x2, drag_and_drop_y2], outputs = [], concurrency_limit = 64)
  return interface

def main(unused_argv):
  browser_manager = BrowserManager()
  app = create_interface(browser_manager)
  app.launch(server_name = FLAGS.service_host, server_port = FLAGS.service_port, root_path = '/browser')

if __name__ == "__main__":
  add_options()
  app.run(main)
