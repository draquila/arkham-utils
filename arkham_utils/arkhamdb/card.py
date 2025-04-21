import requests
from arkham_utils.card import ArkhamCard
from PIL import Image
import io
import requests
from arkham_utils.arkhamdb.constants import API


def _get_image_from_url(url) -> Image.Image:
    r = requests.get(url)
    return Image.open(io.BytesIO(r.content))


class ArkhamDBCard(ArkhamCard):
    def __init__(self, data):
        self.data = data
        self._images = None

    def _lazy_load_images(self):
        if self._images is not None:
            return
        if 'backimagesrc' in self.data:
            self._images = _get_image_from_url(f'https://arkhamdb.com{self.data["imagesrc"]}'), _get_image_from_url(
                f'https://arkhamdb.com{self.data["backimagesrc"]}')
        elif 'imagesrc' in self.data:
            self._images = _get_image_from_url(
                f'https://arkhamdb.com{self.data["imagesrc"]}'),
        else:
            self._images = []
            print(f"{self.name} has no images!")

    @property
    def code(self):
        return self.data['code']

    @property
    def name(self):
        return self.data['name']

    @property
    def image(self):
        self._lazy_load_images()
        return self._images[0]
    
    @property
    def faction(self):
        return self.data['faction_code']
    
    @property
    def type(self):
        return self.data['type_code']

    @property
    def images(self):
        self._lazy_load_images()
        return self._images

    @staticmethod
    def from_id(id: str):
        r = requests.get(f"{API}/card/{id}.json")
        return ArkhamDBCard(r.json())
