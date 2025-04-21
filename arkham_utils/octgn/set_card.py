from arkham_utils.octgn.card import OctgnCard

class OctgnSetCard(OctgnCard):
    def get_property(self, key):
        return self.elem.find(f'property[@name="{key}"]').attrib['value']
    @property
    def name(self):
        return self.elem.attrib['name']
    @property
    def size(self):
        try:
            return self.elem.attrib['size']
        except:
            return None
    @property
    def set_number(self):
        return int(self.get_property("Card Number"))
    @property
    def quantity(self):
        return int(self.get_property("Quantity"))
    @property
    def type(self):
        return self.get_property("Type")
    @property
    def xp(self):
        try:
            return int(self.get_property("Level"))
        except:
            return 'n/a'
