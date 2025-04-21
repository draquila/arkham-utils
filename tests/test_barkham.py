from arkham_utils.octgn import db
from arkham_utils.pdf.builder import PDFBuilder, PDFBuilderConfig


def test_barkham():
  # write all the non-mini cards as a PDF
  barkham = db.find_set('Meowlathotep')
  PDFBuilder([c for c in barkham.cards if c.type != 'Mini']
             ).write('barkham.pdf')

  # write the mini investigator cards
  mini_cfg = PDFBuilderConfig()
  mini_cfg.cards_per_row = 4
  mini_cfg.rows_per_page = 4
  mini_cfg.card_height = 2.5
  mini_cfg.card_width = 1.625
  PDFBuilder([c for c in barkham.cards if c.type == 'Mini'],
             mini_cfg).write('barkham_minis.pdf')
