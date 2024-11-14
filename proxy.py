import json
import os

from lxml import etree
import lxml.etree
import requests

from telebot.util import CustomRequestResponse


def custom_proxy(method, url, **kwargs):
    """The custom proxy via telegram
    It sends request from third-party website, and parses the results.
    """
    # print("Proxy({}:{}){}".format(method, url, kwargs))

    full_url = url
    query = "?"
    if kwargs.get("params", None) is not None:
        for param, value in kwargs["params"].items():
            query += "{}={}&".format(param, value)
        full_url += query[:-1]
    print(full_url)

    payload = {
        "UrlBox": full_url,
        "AgentList": "Opera",
        "MethodList": method.upper(),
    }

    html = requests.post(os.getenv("PROXY_URL"), payload)

    parser = etree.HTMLParser(encoding="utf-8")
    root = etree.fromstring(html.content, parser)
    elem = root.xpath(r'//*[@id="ResultData"]/pre')

    with open("index.html", "w") as f:  # It saves the parsed output
        f.writelines(full_url)
        f.writelines("-" * 100 + "\n\n")
        f.writelines(str(elem))
        f.write(elem[0].text)

    # It makes a payload inot proper response
    data = CustomRequestResponse(elem[0].text)
    # data = json.loads(elem[0].text)

    return data
