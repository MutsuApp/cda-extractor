import json
import requests

from bs4 import BeautifulSoup
from urllib.parse import unquote

def decrypt_file(a: str):
    words = ["_XDDD", "_CDA", "_ADC", "_CXD", "_QWE", "_Q5", "_IKSDE"]

    # first replace very cringy joke and other bad obfuscation
    for i in words:
        a = a.replace(i, "")

    # then apply decodeURIComponent using urllib.parse
    a = unquote(a)

    # store decrypted characters
    b = []

    for e in range(len(a)):
        f = ord(a[e])
        b.append(chr(33 + (f + 14) % 94) if 33 <= f and 126 >= f else chr(f))

    # decrypted URL
    a = "".join(b)

    # more "obfuscation" to deal with
    a = a.replace(".cda.mp4", "")
    a = a.replace(".2cda.pl", ".cda.pl")
    a = a.replace(".3cda.pl", ".cda.pl")

    # return extracted file as URL to video file
    return "https://" + a + ".mp4"


def extract_video(id: str):
    headers = {
        "Referer": "http://www.cda.pl",
        "User-Agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36"
    }

    url = f"https://www.cda.pl/video/{id}"
    res = requests.get(url, headers=headers)
    bs4 = BeautifulSoup(res.content, "lxml")
    try:
        quality = [
            tag.string for tag in bs4.find_all("a", {"class": "quality-btn"})
        ][-1]
        url = f"https://www.cda.pl/video/{id}?wersja={quality}"
    except IndexError:
        pass
    
    res = requests.get(url, headers=headers)
    bs4 = BeautifulSoup(res.content, "lxml")
    data = bs4.find("div", {"player_data": True})["player_data"]
    player_data = json.loads(data)
    return decrypt_file(player_data["video"]["file"])
