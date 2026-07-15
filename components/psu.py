from fastapi import APIRouter, Depends
from Database.db import get_db_cursor

router = APIRouter(
    prefix='/api/v1/psu',
    tags = ['PSU']
)

@router.get('/')
async def get_all_psus(cpu_id: int = None, gpu_id: int = None, cur = Depends(get_db_cursor)):

    total_tdp = 0

    if cpu_id:
        await cur.execute('select tdp from cpu where id = %s', (cpu_id))
        cpu_data = await cur.fetchone()
        if cpu_data:
            total_tdp += cpu_data['tdp']

    if gpu_id:
        await cur.execute('select tdp from gpu where id = %s',(gpu_id))
        gpu_data = await cur.fetchone()
        if gpu_data:
            total_tdp += gpu_data['tdp']

    if total_tdp > 0:

        req_w = total_tdp + 100
        query = (
            'select * from psu where wattage >= %s Order by wattage ASC'
        )
        await cur.execute(query,(req_w))
    else:
        await cur.execute('select * from psu')

    psu_data = await cur.fetchall()

    return {
        'status': 'success',
        'count': len(psu_data),
        'system_tdp': total_tdp,
        'recommended_wattage': total_tdp + 100 if total_tdp > 0 else 0,
        'data': psu_data
    }