from bs4 import BeautifulSoup

def find_with_raise(soup: BeautifulSoup, *args, **kwargs):
    if (result := soup.find(*args, **kwargs)) is None:
        raise AttributeError("Не был найден атрибут{}{}".format(
            ' <' + ', '.join(args) + '>' if args else '',
            ' с параметрами ' + ', '.join([f"{k}: {v}" for k, v in kwargs.items()]) if kwargs else '' 
        ))
    return result

