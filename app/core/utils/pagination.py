import math
from dataclasses import dataclass

from fastapi import HTTPException, status

from schemas import PaginationSchema


@dataclass
class Pagination:
    page: int = 1
    page_size: int = 10
    _max_page: int = 0
    _max_rows: int = 0

    def __post_init__(self):
        self.page = self.page - 1
        self.limit = self.page_size
        self.offset = self.page_size * self.page

    @property
    def max_page(self):
        if not self._max_page:
            raise Exception('max_page does not init')
        return self._max_page

    @property
    def max_rows(self):
        if not self._max_rows:
            raise Exception('max_rows does not init')
        return self._max_rows

    def check_set_max_page(self, page: int, max_rows: int):
        self._max_rows = max_rows
        self._max_page = math.ceil(max_rows / self.page_size)
        if page > self._max_page:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'bad page {page},max={self._max_page}')

    def to_dict(self) -> dict:
        return {'limit': self.limit, 'offset': self.offset}

    @property
    def schema(self) -> PaginationSchema:
        return PaginationSchema(
            page=self.page + 1,
            page_size=self.page_size,
            max_rows=self.max_rows,
            max_page=self.max_page,
        )
