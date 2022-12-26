from fastapi import APIRouter

router_index = APIRouter()


@router_index.get('/')
def index():
    return {'ok': True}
