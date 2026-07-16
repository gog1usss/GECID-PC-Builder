from fastapi import APIRouter, Depends
from Database.db import get_db_cursor

router = APIRouter(
    prefix= '/api/v1/cpu',
    tags = ['CPUs']
)

@router.get("/")
async def get_all_processors(cur = Depends(get_db_cursor)):
    await cur.execute ('select * from cpu')
    processors = await cur.fetchall()

    return {
        'status': 'ok',
        'processors found': len(processors),
        'data': processors
    }
