from arkham_utils.arkhamdb import db
from arkham_utils.octgn import db as octgn_db
from arkham_utils.pdf.builder import PDFBuilder

def test_build_proxy_pdf():
  cards = [db.search(name) for name in [
    'Blackjack',
    'Guts',
    'Emergency Cache',
    'Elder Sign',
    'Shrivelling',
    'Daisy Walker'
  ]]
  pdf = PDFBuilder(cards)
  pdf.write('test.pdf')

def test_octgn_proxy_pdf():
  cards = [octgn_db.find(name) for name in [
    'Blackjack',
    'Guts',
    'Emergency Cache',
    'Elder Sign',
    'Shrivelling',
    'Daisy Walker'
  ]]
  pdf = PDFBuilder(cards)
  pdf.write('octgn.pdf')
