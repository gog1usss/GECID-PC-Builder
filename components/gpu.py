from fastapi import APIRouter,Depends
from Database.db import get_db_cursor

router = APIRouter(
    prefix='/api/v1/gpu',
    tags = ['GPUs']
)

@router.get("/")
async def get_all_gpu (chip: str = None, cur = Depends(get_db_cursor)):
    if chip:
        query = "SELECT * FROM gpu WHERE chip_prod = %s"
        await cur.execute(query, (chip))
    else:
        await cur.execute("select * from gpu")
    gpus = await cur.fetchall()

    return {
        'status': 'ok',
        'items': len(gpus),
        'values': gpus
    }

