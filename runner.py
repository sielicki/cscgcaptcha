import matplotlib.pyplot as plt
import time
import sys
import keras_ocr
import glob
import random
import string
import math
import itertools
import os
import numpy as np
import imgaug
import matplotlib.pyplot as plt
import tensorflow as tf
import sklearn.model_selection
import keras_ocr
import requests
import time
from bs4 import BeautifulSoup
from base64 import b64decode
import tempfile
import uuid


recognizer = keras_ocr.recognition.Recognizer(
    alphabet="abcdefghijklmnpqrstuvwxyz0123456789",
)
recognizer.model.load_weights("recognizer_512.h5")
recognizer.compile()

image_dir = tempfile.TemporaryDirectory()
print(image_dir.name)

##### stage 0

s = requests.Session()
t = s.get("http://hax1.allesctf.net:9200/captcha/0").text
b = BeautifulSoup(t, "html.parser").find("form")
raw_images = {
    i: b64decode(x.attrs["src"].split(",")[1]) for i, x in enumerate(b.find_all("img"))
}
images = {}
for k, v in raw_images.items():
    this_random_uuid = uuid.uuid4()
    with open("{}/{}.png".format(image_dir.name, this_random_uuid), "wb") as f:
        f.write(v)
    images[k] = "{}/{}.png".format(image_dir.name, this_random_uuid)

recognized = {}

for k, v in images.items():
    recognized[k] = recognizer.recognize(v)

print("stage 0: {}".format(recognized))

##### stage 1
posted = s.post("http://hax1.allesctf.net:9200/captcha/0", data=recognized)
t = posted.text
url = posted.url
b = None
try:
    b = BeautifulSoup(t, "html.parser").find("form")
    raw_images = {
        i: b64decode(x.attrs["src"].split(",")[1])
        for i, x in enumerate(b.find_all("img"))
    }
except Exception as e:
    print("Stage 0 Failed.")
    sys.exit(1)
print("Stage 0 succeeded")

images = {}
for k, v in raw_images.items():
    this_random_uuid = uuid.uuid4()
    with open("{}/{}.png".format(image_dir.name, this_random_uuid), "wb") as f:
        f.write(v)
    images[k] = "{}/{}.png".format(image_dir.name, this_random_uuid)

recognized = {}

for k, v in images.items():
    recognized[k] = recognizer.recognize(v)
print("Stage 1 Guess: {}".format(recognized))

posted = s.post(url, data=recognized)


t = posted.text
url = posted.url
try:
    b = BeautifulSoup(t, "html.parser").find("form")
    raw_images = {
        i: b64decode(x.attrs["src"].split(",")[1])
        for i, x in enumerate(b.find_all("img"))
    }
except Exception as e:
    print("Stage 1 Failed.")
    sys.exit(1)
print("Stage 1 succeeded")

images = {}
for k, v in raw_images.items():
    this_random_uuid = uuid.uuid4()
    with open("{}/{}.png".format(image_dir.name, this_random_uuid), "wb") as f:
        f.write(v)
    images[k] = "{}/{}.png".format(image_dir.name, this_random_uuid)

recognized = {}

for k, v in images.items():
    recognized[k] = recognizer.recognize(v)

print("Stage 2 Guess: {}".format(recognized))

posted = s.post(url, data=recognized)


t = posted.text
url = posted.url
try:
    b = BeautifulSoup(t, "html.parser").find("form")
    raw_images = {
        i: b64decode(x.attrs["src"].split(",")[1])
        for i, x in enumerate(b.find_all("img"))
    }
except Exception as e:
    print("Stage 2 Failed.")
    sys.exit(1)
print("Stage 2 succeeded")

images = {}
for k, v in raw_images.items():
    this_random_uuid = uuid.uuid4()
    with open("{}/{}.png".format(image_dir.name, this_random_uuid), "wb") as f:
        f.write(v)
    images[k] = "{}/{}.png".format(image_dir.name, this_random_uuid)

recognized = {}

for k, v in images.items():
    recognized[k] = recognizer.recognize(v)

print("Stage 3: {}".format(recognized))

posted = s.post(url, data=recognized)


t = posted.text
print(t)
