from typing import Generator
from arkham_utils.card import ArkhamCard
from arkham_utils.pdf.builder import PDFBuilder
import fitz
from PIL import Image


class PDFImageReader(object):
    def __init__(self, filename, zoom=4):
        self.filename = filename
        self.zoom = zoom

    def get_images(self) -> Generator[Image.Image, None, None]:
        with fitz.open(self.filename) as pdf:
            mat = fitz.Matrix(self.zoom, self.zoom)
            for i in range(len(pdf)):
                page = pdf.load_page(i)
                pix = page.get_pixmap(matrix=mat)
                yield Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

    def build_pdf(self):
        return PDFBuilder([ArkhamCard(im) for im in self.get_images()])
