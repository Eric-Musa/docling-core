from pydantic import BaseModel, AnyUrl
from pathlib import Path
import json
import jiter

class TestClass(BaseModel):
    text: str
    uri: AnyUrl
    path: Path


test_text = "test text//+ ///lorem ipsum//dolor/sit amet, //consectetur adipiscing elit.//+ ///"
uri = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAIAAAAlC+aJAAABNElEQVR4nO2ayw7DIAwEIf//z+nBErKAEBMe9rrMmYRZNr60xDCVW7AmTt1xwtsk0uu2H3rDiPosiY/PzlLnfFPpfmqFOqdXqGP9anWOXOsSrttp37WdKMBm+65NX7pSUc9oK7YasGAf3jQeAxixJxoy0iE2Sz2AqeMnnpQqAQzaE1WxPIBZe6LU8zUDxo+fyCQdNQBx/ARX9dIA0PETSdhFA3DHT5C2iwaggQ8QQQcgAd/ACaDNCaDNCaDNCaDNCaDNNfc/w81EDw1oC4ziIgDoGJC2iwYCYAlJ2EsDAaoEruqogQBSQibpq4FgvoRSr9KA2QxVsfonZDDDk5K7GUiYKqEh02rASIa2hkhS6xdsiZxoBlSqEG4qHeLNGeTb/dO1Sw7wxVcO8NVjDvDl75L91+9/ESIkdDQ3IX0AAAAASUVORK5CYII='
path = uri

gt = TestClass(text=test_text, uri=uri, path=path)

with open('test.json', 'w') as f:
    json.dump(gt.model_dump(mode='json'), f)

with open('test.json', 'r') as f: 
    test1 = TestClass.model_validate_json(f.read())

with open('test.json', 'r') as f: 
    test2 = TestClass(**json.load(f))

with open('test.json', 'r') as f: 
    test3 = TestClass(**jiter.from_json(bytes(f.read(), 'utf-8')))

assert gt == test1 == test2 == test3

from PIL import Image
# import BytesIO
from io import BytesIO

## load an image from gt.uri
import base64
encoded_img = str(gt.uri).split(",")[1]
decoded_img = base64.b64decode(encoded_img)
im = Image.open(BytesIO(decoded_img))
im.show()

encoded_img = str(test1.uri).split(",")[1]
decoded_img = base64.b64decode(encoded_img)
im = Image.open(BytesIO(decoded_img))
im.show()

encoded_img = str(test2.uri).split(",")[1]
decoded_img = base64.b64decode(encoded_img)
im = Image.open(BytesIO(decoded_img))
im.show()

encoded_img = str(test3.uri).split(",")[1]
decoded_img = base64.b64decode(encoded_img)
im = Image.open(BytesIO(decoded_img))
im.show()

