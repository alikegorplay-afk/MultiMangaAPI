from manga_typing import Pagination

class MangaPagination(Pagination):
    def __init__(self, cache = True):
        super().__init__(cache)
        
    def _load_page(self, num):
        pass