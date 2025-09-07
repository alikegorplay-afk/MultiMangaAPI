from typing import List, Optional, Dict, Callable
from dataclasses import dataclass

from abc import ABC, abstractmethod

@dataclass(frozen=True)
class MiniManga:
    title: str
    url: str
    poster: str
    
@dataclass(frozen=True)
class Manga(MiniManga):
    gallery: List[str]
    genres: Optional[List[str]] = None
    author: Optional[List[str]] = None
    language: Optional[List[str]] = None
    
class Pagination(ABC):
    def __init__(self):
        self.page_now = 1
        self.max_page = -1
    
    def next_page(self):
        return self.select_page(self.page_now + 1)
    
    def back_page(self):
        return self.select_page(self.page_now - 1)
    
    def select_page(self, num: int) -> List[MiniManga] | None:
        if not (0 < num <= self.max_page):
            return None
        data = self._load_page(num)
        
        self.page_now = num
        return data
    
    @abstractmethod
    def _load_page(self, num: int):
        pass
    
