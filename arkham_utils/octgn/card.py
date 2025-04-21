from xml.etree.ElementTree import Element
from arkham_utils.card import ArkhamCard
from arkham_utils.octgn.image_db import image_db

class OctgnCard(ArkhamCard):
    def __init__(self, card_elem: Element, image_db=image_db):
        self.elem = card_elem
        self.image_db = image_db
    @property
    def id(self):
        return self.elem.attrib['id']
    @property
    def name(self):
        return self.elem.text
    @property
    def image(self):
        return self.image_db.get_image(self.id)
    @property
    def images(self):
        return self.image_db.get_images(self.id)
    @property
    def quantity(self):
        return int(self.elem.attrib['qty'])
    def __str__(self):
        return f"[{self.id}] {self.name}"