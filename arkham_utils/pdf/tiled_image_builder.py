from typing import List, Tuple
import math

from fpdf import FPDF

from PIL import Image

a4_width = 210
a4_height = 297


class PDFTiledImageBuilder(object):
    def __init__(self, image_width_mm, image_height_mm, image_files: List[str], bleed_color: Tuple[int, int, int] = (0, 0, 0), space_between: int = 0.2):
        self.image_width = image_width_mm
        self.image_height = image_height_mm
        self.images = [Image.open(fname) for fname in image_files]
        self.bleed_thickness = 0.5
        self.minimum_page_padding = 5
        self.bleed_color = bleed_color  # rgb
        self.space_between = space_between

    def write(self, filename: str):
        # work out which orientation maximizes tiling
        printable_width = a4_width - 2 * \
            (self.bleed_thickness + self.minimum_page_padding)
        printable_height = a4_height - 2 * \
            (self.bleed_thickness + self.minimum_page_padding)
        rows0 = int(printable_height //
                    (self.image_height + self.space_between))
        cols0 = int(printable_width // (self.image_width + self.space_between))
        tiles_per_page0 = rows0 * cols0
        rows1 = int(printable_height //
                    (self.image_width + self.space_between))
        cols1 = int(printable_width //
                    (self.image_height + self.space_between))
        tiles_per_page1 = rows1 * cols1

        self.rotate_90deg = tiles_per_page1 > tiles_per_page0
        if not self.rotate_90deg:
            self.rows_per_page = rows0
            self.cols_per_page = cols0
            self.tiles_per_page = tiles_per_page0
            self.tile_width = self.image_width
            self.tile_height = self.image_height
            self.pages = math.ceil(len(self.images) / tiles_per_page0)
        else:
            self.rows_per_page = rows1
            self.cols_per_page = cols1
            self.tiles_per_page = tiles_per_page1
            self.tile_width = self.image_height
            self.tile_height = self.image_width
            self.pages = math.ceil(len(self.images) / tiles_per_page1)
        print(
            f"max tiles_per_page (rotated? {self.rotate_90deg}):{self.tiles_per_page} ({self.cols_per_page}x{self.rows_per_page}) pages:{self.pages}")

        # work out padding
        self.padding_left = (a4_width - self.cols_per_page * self.tile_width -
                             (self.cols_per_page - 1) * self.space_between) / 2
        self.padding_top = (a4_height - self.rows_per_page * self.tile_height -
                            (self.rows_per_page - 1) * self.space_between) / 2
        print(f"padding left:{self.padding_left} top:{self.padding_top}")

        pdf = FPDF(orientation='P', format='A4', unit='mm')
        for p in range(self.pages):
            pdf.add_page()
            # add bleed bg if needed
            if self.bleed_thickness > 0:
                for row in range(self.rows_per_page):
                    for col in range(self.cols_per_page):
                        idx = p * self.tiles_per_page + row * self.cols_per_page + col
                        if idx < len(self.images):
                            pdf.set_fill_color(*self.bleed_color)
                            pdf.rect(w=self.tile_width + 2 * self.bleed_thickness,
                                     h=self.tile_height + 2 * self.bleed_thickness,
                                     x=self.padding_left + col *
                                     (self.tile_width + self.space_between) -
                                     self.bleed_thickness,
                                     y=self.padding_top + row *
                                     (self.tile_height + self.space_between) -
                                     self.bleed_thickness,
                                     style='F')
            # add images
            for row in range(self.rows_per_page):
                for col in range(self.cols_per_page):
                    idx = p * self.tiles_per_page + row * self.cols_per_page + col
                    if idx < len(self.images):
                        print('adding image', idx + 1)
                        img = self.images[idx]
                        if self.rotate_90deg:
                            img = img.rotate(-90, expand=True)
                        pdf.image(img, w=self.tile_width, h=self.tile_height, x=self.padding_left +
                                  col * (self.tile_width + self.space_between), y=self.padding_top + row * (self.tile_height + self.space_between))

    #         # add bleed bg
    #         for row in range(3):
    #             for col in range(3):
    #                 if (p, row, col) in self.layout:
    #                     image = self.layout[(p, row, col)]
    #                     if image.width > image.height:
    #                         image = image.rotate(-90, expand=True)
    #                     pdf.image(image, w=card_width, h=card_height, x=padding_left +
    #                               col * card_width, y=padding_top + row * card_height)
        pdf.output(filename)

    # def get_layout(self) -> Dict[Tuple[int, int, int], Image.Image]:
    #     layout = {}
    #     twosided = [c for c in self.cards if len(c.images) == 2]
    #     onesided = [c for c in self.cards if len(c.images) == 1]
    #     for card in twosided:
    #         self.layout_2side(layout, card)
    #     for card in onesided:
    #         self.layout_1side(layout, card)
    #     return layout

    # @staticmethod
    # def layout_2side(layout, card: ArkhamCard):
    #     front, back = card.images
    #     if front.width < front.height:
    #         front = front.rotate(180)
    #     for p in range(MAX_PAGES):
    #         for c in range(3):
    #             if (p, 0, c) not in layout:
    #                 layout[(p, 0, c)] = back
    #                 layout[(p, 1, c)] = front
    #                 return
    #     raise RuntimeError('Exceeded last page')

    # @staticmethod
    # def layout_1side(layout, card: ArkhamCard):
    #     for p in range(MAX_PAGES):
    #         for r in range(3):
    #             for c in range(3):
    #                 if (p, r, c) not in layout:
    #                     layout[(p, r, c)] = card.image
    #                     return
    #     raise RuntimeError('Exceeded last page')

    # def write(self, filename: str):
    #     pdf = FPDF(orientation='P', format='A4', unit='in')
    #     pages = max([p for (p, r, c) in self.layout]) + 1
    #     for p in range(pages):
    #         pdf.add_page()
    #         # add bleed bg
    #         for row in range(3):
    #             for col in range(3):
    #                 if (p, row, col) in self.layout:
    #                     pdf.rect(w=card_width + 2 * bleed_thickness,
    #                              h=card_height + 2 * bleed_thickness,
    #                              x=padding_left + col * card_width - bleed_thickness,
    #                              y=padding_top + row * card_height - bleed_thickness,
    #                              style='F')
    #         # add bleed bg
    #         for row in range(3):
    #             for col in range(3):
    #                 if (p, row, col) in self.layout:
    #                     image = self.layout[(p, row, col)]
    #                     if image.width > image.height:
    #                         image = image.rotate(-90, expand=True)
    #                     pdf.image(image, w=card_width, h=card_height, x=padding_left +
    #                               col * card_width, y=padding_top + row * card_height)
    #     pdf.output(filename)
