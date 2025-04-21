from arkham_utils.arkhamdb import db

def test_find_core_set():
  core = next(db.find_all_sets('Core'))
  assert core.name == 'Core Set'
  assert len(core.cards) == 182

def test_search():
  card = db.search('Blackjack')
  assert card.name == 'Blackjack'
  assert card.type == 'asset'
  assert card.image.size == (300, 419)
