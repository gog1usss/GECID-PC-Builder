from fastapi import APIRouter, Depends
from Database.db import get_db_cursor

router = APIRouter(
    prefix='/api/v1/ram',
    tags = ['RAM']
)

@router.get('/')
async def get_all_ram(mother_id: int = None, cur = Depends(get_db_cursor)):

    if mother_id:
        query = '''
        select r.id, r.brand_ram, r.name_ram, r.ram_type, r.capacity_ram, r.frequency_mhz, r.price_ram, r.image_url, m.brand_mother, 
        m.name_mother, m.socket_mother, m.ram_type from ram r 
        Join motherboard m ON (r.ram_type = m.ram_type)
        WHERE m.id = %s
        '''
        await cur.execute(query, (mother_id,))
        ram_1 = await cur.fetchall() 
    else:
        await cur.execute('select r.id, r.brand_ram, r.name_ram, r.ram_type, r.capacity_ram, r.frequency_mhz, r.price_ram, image_url from ram r')
        ram_1 = await cur.fetchall()

    return {
        'status': 'success',
        'count': len(ram_1),
        'data': ram_1
    }