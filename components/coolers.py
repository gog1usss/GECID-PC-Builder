from fastapi import APIRouter, Depends
from Database.db import get_db_cursor

router = APIRouter(
    prefix='/api/v1/coolers',
    tags = ['Cooling']
)

@router.get('/')
async def get_all_routers(cpu_id: int = None, cur = Depends(get_db_cursor)):

    if cpu_id:
        query = '''
        select DISTINCT co.brand_cooler, co.name_cooler, co.max_tdp, co.price, co.image_url, cs.cooler_socket, c.name_cpu, c.tdp from cooler co 
        join cooler_socket cs ON (co.id = cs.cooler_id)
        join cpu c ON (cs.cooler_socket = c.socket_cpu)
        where c.id = %s AND co.max_tdp >= c.tdp;
        '''
        await cur.execute(query,(cpu_id))

    else:
        await cur.execute('select co.brand_cooler, co.name_cooler, co.max_tdp, co.price, co.image_url, cs.cooler_socket from cooler co '
                    'Join cooler_socket cs ON (co.id = cs.cooler_id);')

    coolers = await cur.fetchall()

    return {
        'status': 'success',
        'count': len(coolers),
        'data': coolers
    }

