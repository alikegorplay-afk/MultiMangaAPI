from typing import Iterable

from bs4 import BeautifulSoup

def find_with_raise(soup: BeautifulSoup, *args, **kwargs):
    if (result := soup.find(*args, **kwargs)) is None:
        raise AttributeError("Не был найден атрибут{}{}".format(
            ' <' + ', '.join(args) + '>' if args else '',
            ' с параметрами ' + ', '.join([f"{k}: {v}" for k, v in kwargs.items()]) if kwargs else '' 
        ))
    return result


def raise_more(attrs: Iterable, attr_type: type, error: BaseException):
    if not all(isinstance(attr, attr_type) for attr in attrs):
        raise error