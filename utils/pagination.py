from fastapi import Query
from pydantic import BaseModel


class Pagination(BaseModel):
    page_size: int
    page: int

def pagination_param(
        page: int = Query(ge= 1 , le=1000, default= 1 ),
        page_size: int = Query(ge= 1 , le= 100 , default= 1)
):
    return Pagination(page_size=page_size , page= page)