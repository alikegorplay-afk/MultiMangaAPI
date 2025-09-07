from typing import List, Dict

import httpx

from bs4 import BeautifulSoup, _IncomingMarkup

from manga_typing import Pagination, MiniManga
from tools import find_with_raise, raise_more

class SiteUrls:
    FIND_BY_QUOTE_URL = "https://multi-manga.today/index.php?do=search&subaction=search&search_start={}&full_search=0&story={}"

class MangaPagination(Pagination):
    def __init__(self, url: str, cache = True, engine: str = 'html.parser'):
        self.session = httpx.Client()
        self._cache: Dict[int, List[MiniManga]] = {}
        
        self.use_cache: str = cache
        self.engine = engine
        self.url: str = url
        
        super().__init__()
        
        self._load_page(1)
        #self.max_page = 
        
        
    def _load_page(self, num):
        if num in self._cache and self.use_cache:
            return self._cache[num]
        
        response = self.session.get(self.url.format(num))
        response.raise_for_status()
        
        data = self.parse_page(response.text, self.engine)

        if self._cache:
            self._cache[num] = data
        return data
        
    @staticmethod
    def parse_page(data: _IncomingMarkup, engine: str = 'html.parser'):
        soup = BeautifulSoup(data, engine)
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
                  
class MangaSearch:
    
    @staticmethod
    def find_manga(quote: str, cache = True, engine: str = 'html.parser'):
        result = MangaPagination(SiteUrls.FIND_BY_QUOTE_URL.format("{}", quote), cache, engine)
        return result
    
    
if __name__ == "__main__":
    a = MangaSearch.find_manga('Брат')
    print(a.next_page())