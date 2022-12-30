from typing import Union

from fastapi import APIRouter

router_index = APIRouter()


@router_index.get('/')
def index():
    return {'ok': True}


@router_index.get('/items/{item_id}')
def read_item(item_id: int, q: Union[str, None] = None):
    return {'item_id': item_id, 'q': q}
