from typing import List, Dict

import httpx

from bs4 import BeautifulSoup, _IncomingMarkup

from manga_typing import Pagination, MiniManga

class MangaPagination(Pagination):
    def __init__(self, url: str, cache = True, engine: str = 'html.parser'):
        self.session = httpx.Client()
        self._cache: Dict[int, List[MiniManga]] = {}
        
        self.use_cache: str = cache
        self.engine = engine
        self.url: str = url
        
        super().__init__(cache)
        
        
    def _load_page(self, num):
        if num in self._cache and self.use_cache:
            return self._cache[num]
        
        response = self.session.get(self.url.format(num))
        response.raise_for_status()
    
    @staticmethod
    def parse_page(data: _IncomingMarkup, engine: str = 'html.parser'):
        soup = BeautifulSoup(data, engine)
        
        soup.find_all("div", class_="gallery")
    
class MangaSearch(MangaPagination):
    FIND_BY_QUOTE_URL = "https://multi-manga.today/index.php?do=search&subaction=search&search_start={}&full_search=0&story={}"
    
    #def
    
    def find_manga(self, quote: str):
        super().__init__(self.FIND_BY_QUOTE_URL.format("{}", quote))
    
    
if __name__ == "__main__":
    a = MangaPagination()
    a.max_page = 3
    a.next_page()
    print(a.page_now)