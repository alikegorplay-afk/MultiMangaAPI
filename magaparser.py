from logging import Logger, DEBUG
from urllib.parse import urljoin

import httpx

from bs4 import BeautifulSoup

from manga_typing import Manga, Config
from tools import find_with_raise, find_all_with_raise

logger = Logger('Manga Logger', DEBUG)

def parse_from_html(html: str, engine: str = Config.DEFAULT_ENGINE) -> Manga:
    """Парсит manga из HTML строки"""
    try:
        soup = BeautifulSoup(html, engine)
        return _parse_manga_soup(soup)
    except Exception as e:
        logger.exception()

def parse_from_url(url: str, engine: str = Config.DEFAULT_ENGINE,
                        session: httpx.Client = None) -> Manga:
    """Парсит manga из URL"""
from logging import Logger, DEBUG
from urllib.parse import urljoin
from typing import Optional

import httpx
from bs4 import BeautifulSoup

from manga_typing import Manga, Config
from tools import find_with_raise, find_all_with_raise

logger = Logger('Manga Logger', DEBUG)

def parse_from_html(html: str, engine: str = Config.DEFAULT_ENGINE) -> Optional[Manga]:
    """Парсит manga из HTML строки"""
    try:
        soup = BeautifulSoup(html, engine)
        return _parse_manga_soup(soup)
    except Exception as e:
        logger.exception("Ошибка при парсинге HTML")
        return None

def parse_from_url(url: str, 
                  engine: str = Config.DEFAULT_ENGINE,
                  session: Optional[httpx.Client] = None) -> Optional[Manga]:
    """Парсит manga из URL"""
    close_session = False
    if session is None:
        session = httpx.Client()
        close_session = True

    try:
        response = session.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, engine)
        return _parse_manga_soup(soup)
    except Exception as e:
        logger.error(f"Ошибка при запросе {url}: {str(e)}")
        return None
    finally:
        if close_session:
            session.close()

def _parse_manga_soup(soup: BeautifulSoup) -> Manga:
    """Внутренняя функция парсинга"""
    info = {"gallery": []}
    
    info_block = find_with_raise(soup, "div", id="info")
    tags = find_all_with_raise(info_block, 'div', class_="tag-container")
    gallery = find_all_with_raise(soup, "div", class_="thumb-container")

    cover_div = find_with_raise(soup, "div", id="cover")
    cover_img = find_with_raise(cover_div, "img")
    info["poster"] = urljoin(Config.BASE_URL, cover_img.get('data-src'))
    
    info["title"] = find_with_raise(info_block, 'h1').get_text(strip=True)
    
    for tag in tags:
        tag_text = tag.next_element.get_text(strip=True).lower()
        if tag_text == "теги":
            info["genres"] = _parse_tags(tag)
        elif tag_text == "автор":
            info["author"] = _parse_tags(tag)
        elif tag_text == "язык":
            info["language"] = _parse_tags(tag)
    
    for img in gallery:
        img_tag = find_with_raise(img, 'img')
        info["gallery"].append(img_tag.get('data-src'))
    
    canonical_link = find_with_raise(soup, "link", rel="canonical")
    info["url"] = canonical_link.get("href")
    
    return Manga(**info)
    
def _parse_tags(soup: BeautifulSoup) -> list:
    return [x.get_text(strip=True) for x in find_all_with_raise(soup, 'a', class_="tag")]