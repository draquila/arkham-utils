import csv
import sys
import xml.etree.ElementTree as ET

from arkham_utils.octgn.card import OctgnCard


class OctgnDeck(object):
    def __init__(self, o8d='starter-deck.o8d'):
        tree = ET.parse(o8d)
        self.cards = [OctgnCard(card) for card in tree.findall('.//card')]        
    def csv(self, fh=sys.stdout):
        writer = csv.writer(fh)
        for card in self.cards:
            writer.writerow([card.id, card.name, card.quantity])
            