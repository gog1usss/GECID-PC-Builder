from fastapi import APIRouter, Request, Depends
from db import get_db_cursor

router = APIRouter(
    prefix='/api/v1/gpu',
    tags = ['GPUs']
)

@router.get("/")
async def get_all_gpu (cur = Depends(get_db_cursor)):
    await cur.execute("select * from gpu")
    gpus = await cur.fetchall()

    return {
        'status': 'ok',
        'items': len(gpus),
        'values': gpus
    }

