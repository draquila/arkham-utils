from typing import Dict, List
from arkham_utils.arkhamdb.card import ArkhamDBCard
from arkham_utils.arkhamdb.constants import API
import requests


class ArkhamDBPublicDeck(object):
  id: int
  data: object
  _cards: Dict[str, ArkhamDBCard]

  def __init__(self, id: int, is_decklist: bool = False):
    self.id = id
    key = 'decklist' if is_decklist else 'deck'
    r = requests.get(f"{API}/{key}/{self.id}.json")
    print(f"{API}/{key}/{self.id}.json")
    print(r.content)
    self.data = r.json()
    self._cards = None

  @property
  def cards(self):
    if self._cards is None:
      self._cards = {}
      for id in self.data['slots']:
        self._cards[id] = ArkhamDBCard.from_id(id)

    all_cards = []
    for id, count in self.data['slots'].items():
      all_cards.extend([self._cards[id]] * count)

    return all_cards

  def dump(self):
    self.cards
    print(f"{self.data['name']}")
    for id, count in self.data['slots'].items():
      print(f"  {self._cards[id].name} x{count}")
