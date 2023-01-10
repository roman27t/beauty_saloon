from fastapi import APIRouter

router_index = APIRouter()


@router_index.get('/')
def view_index():
    return {'ok': True}
