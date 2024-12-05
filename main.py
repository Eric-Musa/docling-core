import json
import os
import time
from docling_core.types import DoclingDocument
from docling_core.types.doc.base import ImageRefMode
from pathlib import Path
import jiter
from test.test_docling_doc import _construct_doc, _verify_saved_output


document: DoclingDocument = _construct_doc()

image_dir = Path("./test/data/doc/constructed_images/")

doc_with_references = document._with_pictures_refs(
    image_dir=image_dir  # Path("./test/data/constructed_images/")
)

# paths will be different on different machines, so needs to be kept!
paths = doc_with_references._list_images_on_disk()
assert len(paths) == 1, "len(paths)!=1"

## USING EMBEDDED JSON AS TEST
filename = Path("test/data/doc/constructed_doc.embedded.json")
document.save_as_json(
    filename=filename, artifacts_dir=image_dir, image_mode=ImageRefMode.EMBEDDED
)
_verify_saved_output(filename=filename, paths=paths)

# filename = Path("test/data/doc/constructed_doc.referenced.json")
# document.save_as_json(
#     filename=filename, artifacts_dir=image_dir, image_mode=ImageRefMode.REFERENCED
# )
# _verify_saved_output(filename=filename, paths=paths)

# print('filename', filename)
with open(filename, 'r') as f:
    contents = f.read()
    document_json = DoclingDocument.model_validate_json(contents)

with open(filename, 'r') as f:
    document_py = DoclingDocument(**json.load(f))


import re

def _verify_objects_match(doc1: DoclingDocument, doc1_name, doc2: DoclingDocument, doc2_name):
    assert doc1 == doc2, f"""
doc1 ({doc1_name}) != doc2 ({doc2_name})
len({doc1_name}) = {len(str(doc1))}
len({doc2_name}) = {len(str(doc2))}
len({doc1_name} dict) = {len(json.dumps(doc1.export_to_dict()))}
len({doc2_name} dict) = {len(json.dumps(doc2.export_to_dict()))}
number of "//+" in {doc1_name} = {len(re.findall(r'//+', json.dumps(doc1.export_to_dict())))}
number of "//+" in {doc2_name} = {len(re.findall(r'//+', json.dumps(doc2.export_to_dict())))}
"""
# doc1 (Test Doc) != doc2 (JSON-loaded Doc)
# len(Test Doc) = 9149
# len(JSON-loaded Doc) = 9154
# len(Test Doc dict) = 8864
# len(JSON-loaded Doc dict) = 8863
# number of "//+" in Test Doc = 1
# number of "//+" in JSON-loaded Doc = 0
## Discrepancy in char count comes from the lack of "//+" in the JSON-loaded Doc along with "uri=PosixPath" instead of "uri=Url"
# JSON: uri=PosixPath('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAIAAAAlC+aJAAABNElEQVR4nO2ayw7DIAwEIf/z+nBErKAEBMe9rrMmYRZNr60xDCVW7AmTt1xwtsk0uu2H3rDiPosiY/PzlLnfFPpfmqFOqdXqGP9anWOXOsSrttp37WdKMBm+65NX7pSUc9oK7YasGAf3jQeAxixJxoy0iE2Sz2AqeMnnpQqAQzaE1WxPIBZe6LU8zUDxo+fyCQdNQBx/ARX9dIA0PETSdhFA3DHT5C2iwaggQ8QQQcgAd/ACaDNCaDNCaDNCaDNCaDNNfc/w81EDw1oC4ziIgDoGJC2iwYCYAlJ2EsDAaoEruqogQBSQibpq4FgvoRSr9KA2QxVsfonZDDDk5K7GUiYKqEh02rASIa2hkhS6xdsiZxoBlSqEG4qHeLNGeTb/dO1Sw7wxVcO8NVjDvDl75L91+9/ESIkdDQ3IX0AAAAASUVORK5CYII=')),
# ORIG: uri=Url('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAIAAAAlC+aJAAABNElEQVR4nO2ayw7DIAwEIf//z+nBErKAEBMe9rrMmYRZNr60xDCVW7AmTt1xwtsk0uu2H3rDiPosiY/PzlLnfFPpfmqFOqdXqGP9anWOXOsSrttp37WdKMBm+65NX7pSUc9oK7YasGAf3jQeAxixJxoy0iE2Sz2AqeMnnpQqAQzaE1WxPIBZe6LU8zUDxo+fyCQdNQBx/ARX9dIA0PETSdhFA3DHT5C2iwaggQ8QQQcgAd/ACaDNCaDNCaDNCaDNCaDNNfc/w81EDw1oC4ziIgDoGJC2iwYCYAlJ2EsDAaoEruqogQBSQibpq4FgvoRSr9KA2QxVsfonZDDDk5K7GUiYKqEh02rASIa2hkhS6xdsiZxoBlSqEG4qHeLNGeTb/dO1Sw7wxVcO8NVjDvDl75L91+9/ESIkdDQ3IX0AAAAASUVORK5CYII=')),
# "PosixPath" is 6 more characters than "Url", but the PosixPath has one less "/" than the Url, so the discrepancy is 5 characters
    
_verify_objects_match(document, "Test Doc", document_py, "Python-loaded Doc")
_verify_objects_match(document, "Test Doc", document_json, "JSON-loaded Doc")

# with open('test orig doc.txt', 'w') as f:
#     f.write('\n'.join(str(document).split(' ')))

# with open('test json doc.txt', 'w') as f:
#     f.write('\n'.join(str(document_json).split(' ')))

data = jiter.from_json(bytes(contents, 'utf-8'))
document_jiter = DoclingDocument(**data)

# uri: Union[AnyUrl, Path] = Field(union_mode='left_to_right')
# THIS ^^ fixes the problem.

# https://docs.pydantic.dev/latest/concepts/unions/#left-to-right-mode
# https://docs.pydantic.dev/latest/concepts/unions/#smart-mode