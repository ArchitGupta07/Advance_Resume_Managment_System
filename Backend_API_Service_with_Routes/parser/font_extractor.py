from pdfminer.layout import LAParams, LTTextBox, LTTextLine
from pdfminer.high_level import extract_pages
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFDevice

class PDFTextWithFontSize:
    def __init__(self):
        self.text_elements = []

    def process_lt_obj(self, lt_obj):
        if isinstance(lt_obj, (LTTextBox, LTTextLine)):
            for element in lt_obj:
                if hasattr(element, 'fontname'):
                    text = element.get_text()
                    fontname = element.fontname
                    fontsize = element.size
                    self.text_elements.append((text, fontname, fontsize))
                if hasattr(element, '_objs'):
                    self.process_lt_obj(element._objs)
        if hasattr(lt_obj, '_objs'):
            for obj in lt_obj._objs:
                self.process_lt_obj(obj)

    def extract_text_with_font_size(self, pdf_path):
        laparams = LAParams()
        rsrcmgr = PDFResourceManager()
        device = PDFDevice(rsrcmgr)
        interpreter = PDFPageInterpreter(rsrcmgr, device)

        with open(pdf_path, 'rb') as fp:
            for page in PDFPage.get_pages(fp):
                interpreter.process_page(page)
                layout = device.get_result()
                self.process_lt_obj(layout)

        return self.text_elements

# Usage example
pdf_extractor = PDFTextWithFontSize()
font_data = pdf_extractor.extract_text_with_font_size('D:/Ex2_Projects/Resumes/Anand_Flutter_and_React_Native.pdf')

for text, fontname, fontsize in font_data:
    print(f"Text: {text.strip()}, Font: {fontname}, Size: {fontsize}")