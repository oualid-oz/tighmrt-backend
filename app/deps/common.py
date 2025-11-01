from fastapi import Query

def common_pagination(skip: int = 0, limit: int = Query(10, le=100)):
    return {"skip": skip, "limit": limit}
