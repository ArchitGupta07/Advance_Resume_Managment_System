import gradio as gr
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from docx import Document

import spacy
from spacy.matcher import Matcher
import io
import requests
import re
from gradio_main import main


def process_file(file):
    # Process the uploaded file here
    # For demonstration purposes, just printing the file content
    # with open(file.name, 'r') as f:
    #     content = f.read()
    # text = extract_text_from_pdf(file)
    # print("adafwfwwwfwfwefwaa")
    try:
        data = main(file)

        return data
    except:
        return {}

with gr.Blocks() as demo:

    upload_button = gr.File(label="Upload File")
    submit_button = gr.Interface(fn=process_file, inputs=upload_button, outputs=gr.JSON(), title="File Upload")


if __name__ == "__main__":
    demo.launch(share=True)


# import gradio as gr

# def greet(name, intensity):
#     return "Hello, " + name + "!" * int(intensity)

# demo = gr.Interface(
#     fn=greet,
#     inputs=["text", "slider"],
#     outputs=["text"],
# )

# demo.launch()