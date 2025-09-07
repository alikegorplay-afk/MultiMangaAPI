from typing import List, Dict, Iterable
from logging import Logger, DEBUG

import httpx

from bs4 import BeautifulSoup

from manga_typing import Pagination, MiniManga
from tools import find_with_raise

logger = Logger('Manga Logger', DEBUG)

class SiteUrls:
    FIND_BY_QUOTE_URL = "https://multi-manga.today/index.php?do=search&subaction=search&search_start={}&full_search=0&story={}"
    FIND_WITH_GENRES = "https://multi-manga.today/f/n.m.tags={}/sort=date/order=desc/page/{}/"
    FIND_WITH_AUTHOR = "https://multi-manga.today/xfsearch/autor/{}/page/{}/"
    
class MangaPagination(Pagination):
    def __init__(self, url: str, cache = True, engine: str = 'html.parser'):
        self.session = httpx.Client(follow_redirects=True)
        self._cache: Dict[int, List[MiniManga]] = {}
        if not self.session.follow_redirects:
            logger.warning("Без follow_redirects многие функции не работают!")
        
        self.use_cache: str = cache
        self.engine = engine
        self.url: str = url
        
        super().__init__()
        
        self._load_page(1)
          
    def _load_page(self, num):
        if num in self._cache and self.use_cache:
            return self._cache[num]
        
        response = self.session.get(self.url.format(num))
        response.raise_for_status()
        
        soup = BeautifulSoup(response, self.engine)
        self.max_page = self.find_max_page(soup)
        
        data = self.parse_page(soup)

        if self.use_cache:
            self._cache[num] = data
        return data
    
    @staticmethod
    def find_max_page(soup: BeautifulSoup) -> int:
        section = soup.find('section')
        if section is None:
            return 1
        page_numbers = []

        for child in section.children:
            text = child.get_text(strip=True)
            if text and text.isdigit():
                page_numbers.append(int(text))

        return max(page_numbers) if page_numbers else -1
    
    @staticmethod
    def parse_page(soup: BeautifulSoup) -> List[MiniManga]:
        page_data: List[MiniManga] = []
        
        for article in soup.find_all("div", class_="gallery"):
            title = article.get_text(strip=True)
            url = find_with_raise(article, 'a').get('href', AttributeError("Атрибут href пустой или не найден"))
            poster = find_with_raise(article, 'img').get('data-src', AttributeError("Атрибут src пустой или не найден"))
            
            if isinstance(url, AttributeError): 
                raise url
            elif isinstance(poster, AttributeError): 
                raise poster
            
            else: page_data.append(MiniManga(title, url, poster))
            
        return page_data
    
    @property
    def page(self):
        if self.use_cache:
            return self._cache[self.page_now]
        logger.warning("Используйте кэш! в переменной 'use_cache' используйте True или оставтье по умолчанию!")
    
    def __str__(self):
        return (
            f"Вы на [{self.page_now} из {self.max_page}]"
        )   

class MangaSearch:
    
    @staticmethod
    def find_manga(quote: str, cache = True, engine: str = 'html.parser'):
        logger.info(f"Была создана поптыка поиска манги {quote}")
        result = MangaPagination(SiteUrls.FIND_BY_QUOTE_URL.format("{}", quote), cache, engine)
        return result
    
    @staticmethod
    def find_with_genres(genres: Iterable[str], cache = True, engine: str = 'html.parser'):
        logger.info(f"Была создана поптыка поиска манги с параметрами {', '.join(genres)}")
        result = MangaPagination(SiteUrls.FIND_WITH_GENRES.format(f"{','.join(genres)}", "{}"), cache, engine)
        return result
    
    @staticmethod
    def find_author_manga(author: str, cache = True, engine: str = 'html.parser'):
        logger.info(f"Была создана поптыка поиска манги автора {author}")
        result = MangaPagination(SiteUrls.FIND_WITH_AUTHOR.format(f"{author}", "{}"), cache, engine)
        return result
    
    @staticmethod
    def find_popular(session: httpx.Client):
        response = session.get("https://multi-manga.today/")