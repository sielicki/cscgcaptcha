#!/usr/bin/env python3
import requests
import time
from bs4 import BeautifulSoup
from base64 import b64decode


def get_one():
    s = requests.Session()
    t = s.get("http://hax1.allesctf.net:9200/captcha/0").text
    image = b64decode(
        BeautifulSoup(t, "html.parser").find("img").attrs["src"].split(",")[1]
    )
    time.sleep(1)
    solution = (
        list(
            filter(
                lambda x: "Because" in str(x),
                BeautifulSoup(
                    s.post(
                        "http://hax1.allesctf.net:9200/captcha/0", data={"0": "a"}
                    ).text,
                    "html.parser",
                ).find_all("p"),
            )
        )[0]
        .find("b")
        .text
    )
    with open("./training_data/{}.png".format(solution), "wb") as f:
        f.write(image)


for i in range(100):
    print(i)
    get_one()
