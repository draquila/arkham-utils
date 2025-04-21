import csv
import re
import sys
from typing import List
import xml.etree.ElementTree as ET

from arkham_utils.octgn.set_card import OctgnSetCard


# check out repo https://github.com/GeckoTH/arkham-horror/tree/master/o8g
class OctgnSet(object):
    cards: List[OctgnSetCard]
    
    def __init__(self, set_xml='o8g/Sets/Core Set/set.xml'):
        self.xml = set_xml
        tree = ET.parse(set_xml)
        self.name = tree.getroot().attrib['name']
        self.cards = [OctgnSetCard(card) for card in tree.findall('.//card')]
        self.counts = {}
        for card in self.cards:
            try:
                self.counts[card.id] = card.quantity
            except AttributeError:
                self.counts[card.id] = 1
#                 logging.warning(f'{set_xml} card {card.name} ({card.id}) has no quantity')
        self.proxies = []
            
    def csv(self, fh=sys.stdout):
        writer = csv.writer(fh)
        for card in self.cards:
            writer.writerow([card.id, card.set_number, card.name, card.quantity, card.xp])
    
    def find(self, card_id):
        return next((x for x in self.cards if x.id == card_id), None)
    
    def find_by_regex(self, pattern, xp=None):
        return [x for x in self.cards if re.search(pattern, x.name) is not None and (xp is None or xp == x.xp)]
    
    def remove(self, card_id):
        if card_id in self.counts:
            self.counts[card_id] -= 1
#             print(f'ok removing {self.find(card_id).name}, {self.counts[card_id]} left')
            if self.counts[card_id] == 0:
                del self.counts[card_id]
            return True
        if not self.find(card_id):
            raise KeyError(f'Unknown card id: {card_id}')
        return False
    
    def remove_deck(self, deck):
        for card in deck.cards:
            for _ in range(card.quantity):
                ok = self.remove(card.id)
                if not ok:
#                     print(f'proxy: {card.name}')
                    self.proxies.append(card)