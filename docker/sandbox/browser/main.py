#!/usr/bin/python3

from os import environ
environ['DISPLAY'] = ':100'
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
        navigate_to_btn.click(browser_manager.navigate_to, inputs = [navigate_to_url], outputs = [])
      with gr.Column():
        # tool 2
        with gr.Row():
          gr.Markdown("# go back")
          go_back_btn = gr.Button(value = "go_back")
        go_back_btn.click(browser_manager.go_back, inputs = [], outputs = [])
      with gr.Column():
        # tool 3
        with gr.Row():
          gr.Markdown("# wait")
          wait_seconds = gr.Number(label = "seconds", precision = 0)
          wait_btn = gr.Button(value = "wait")
        wait_btn.click(browser_manager.wait, inputs = [wait_seconds], outputs = [])
      with gr.Column():
        # tool 4
        with gr.Row():
          gr.Markdown("# click element")
          click_element_index = gr.Number(label = "index", precision = 0)
          click_element_btn = gr.Button(value = "click_element")
        click_element_btn.click(browser_manager.click_element, inputs = [click_element_index], outputs = [])
    with gr.Row():
      # line 2
      with gr.Column():
        # tool 5
        with gr.Row():
          gr.Markdown("# input text")
          input_text_index = gr.Number(label = "index", precision = 0)
          input_text_text = gr.Textbox(label = "text")
          input_text_btn = gr.Button(value = "input_text")
        input_text_btn.click(browser_manager.input_text, inputs = [input_text_index, input_text_text], outputs = [])
      with gr.Column():
        # tool 6
        with gr.Row():
          gr.Markdown("# send keys")
          send_keys_keys = gr.Textbox(label = "keys")
          send_keys_btn = gr.Button(value = "send_keys")
        send_keys_btn.click(browser_manager.send_keys, inputs = [send_keys_keys], outputs = [])
      with gr.Column():
        # tool 7
        with gr.Row():
          gr.Markdown("# switch tab")
          switch_tab_page_id = gr.Number(label = "page_id", precision = 0)
          switch_tab_btn = gr.Button(value = "switch_tab")
        switch_tab_btn.click(browser_manager.switch_tab, inputs = [switch_tab_page_id], outputs = [])
      with gr.Column():
        # tool 8
        with gr.Row():
          gr.Markdown("# close tab")
          close_tab_page_id = gr.Number(label = "page_id", precision = 0)
          close_tab_btn = gr.Button(value = "close_tab")
        close_tab_btn.click(browser_manager.close_tab, inputs = [close_tab_page_id], outputs = [])
    with gr.Row():
      # line 3
      with gr.Column():
        # tool 9
        with gr.Row():
          gr.Markdown("# scroll down")
          scroll_down_amount = gr.Number(label = "amount", precision = 0)
          scroll_down_btn = gr.Button(value = "scroll_down")
        scroll_down_btn.click(browser_manager.scroll_down, inputs = [scroll_down_amount], outputs = [])
      with gr.Column():
        # tool 10
        with gr.Row():
          gr.Markdown("# scroll up")
          scroll_up_amount = gr.Number(label = "amount", precision = 0)
          scroll_up_btn = gr.Button(value = "scroll_up")
        scroll_up_btn.click(browser_manager.scroll_up, inputs = [scroll_up_amount], outputs = [])
      with gr.Column():
        # tool 11
        with gr.Row():
          gr.Markdown("# scroll to text")
          scroll_to_text_text = gr.Textbox(label = "text")
          scroll_to_text_btn = gr.Button(value = "scroll_to_text")
        scroll_to_text_btn.click(browser_manager.scroll_to_text, inputs = [scroll_to_text_text], outputs = [])
      with gr.Column():
        # tool 12
        with gr.Row():
          gr.Markdown("# get dropdown options")
          get_dropdown_options_index = gr.Number(label = "index", precision = 0)
          get_dropdown_options_btn = gr.Button(value = "get_dropdown_options")
          get_dropdown_options_options = gr.JSON(label = "options")
        get_dropdown_options_btn.click(browser_manager.get_dropdown_options, inputs = [get_dropdown_options_index], outputs = [get_dropdown_options_options])
    with gr.Row():
      with gr.Column():
        # tool 13
        with gr.Row():
          gr.Markdown("# select dropdown option")
          select_dropdown_option_index = gr.Number(label = "index", precision = 0)
          select_dropdown_option_text = gr.Textbox(label = "text")
          select_dropdown_option_btn = gr.Button(value = "select_dropdown_option")
        select_dropdown_option_btn.click(browser_manager.select_dropdown_option, inputs = [select_dropdown_option_index, select_dropdown_option_text], outputs = [])
      with gr.Column():
        # tool 14
        with gr.Row():
          gr.Markdown("# click coordinates")
          click_coordinates_x = gr.Number(label = "x", precision = 0)
          click_coordinates_y = gr.Number(label = "y", precision = 0)
          click_coordinates_btn = gr.Button(value = "click_coordinates")
        click_coordinates_btn.click(browser_manager.click_coordinates, inputs = [click_coordinates_x, click_coordinates_y], outputs = [])
      with gr.Column():
        # tool 15
        with gr.Row():
          gr.Markdown("# drag drop")
          drag_drop_element_source = gr.Textbox(label = "element_source")
          drag_drop_element_target = gr.Textbox(label = "element_target")
          drag_drop_btn = gr.Button(value = "drag_drop")
        drag_drop_btn.click(browser_manager.drag_drop, inputs = [drag_drop_element_source, drag_drop_element_target], outputs = [])
  return interface

application = FastAPI()

def main(unused_argv):
  global application
  import uvicorn
  browser_manager = BrowserManager()
  interface = create_interface(browser_manager)
  application = mount_gradio_app(app = application, blocks = interface, path = '/')
  uvicorn.run(
    application,
    host = FLAGS.service_host,
    port = FLAGS.service_port
  )

if __name__ == "__main__":
  add_options()
  app.run(main)
