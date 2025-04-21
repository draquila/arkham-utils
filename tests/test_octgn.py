from arkham_utils.octgn import db

def test_find_card():
  card = db.find('Blackjack')
  assert card.name == 'Blackjack'

def test_card_image():
  card = db.find('Blackjack')
  assert card.image