__author__ = 'popka'


def normalize_urls(url):

    url = url.split("?")[0]
    url = url.split("#")[0]
    url.replace("//m.", "//")

    if url[-1] == "/":
        url = url[:-1]

    return url

