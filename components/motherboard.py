from fastapi import APIRouter, Depends
from Database.db import get_db_cursor

router = APIRouter(
    prefix='/api/v1/motherboard',
    tags = ['Motherboards']
)

@router.get('/')
async def motherboard_gets(cpu_id: int = None, cur = Depends(get_db_cursor)):

        if cpu_id:
            query = """
                select m.* from motherboard m 
                join cpu c ON m.socket_mother = c.socket_cpu
                where c.id = %s              
            """
            await cur.execute(query,(cpu_id),)  

        else:
            await cur.execute('select * from motherboard')
        motherboards = await cur.fetchall()

        return {
            'status': 'success',
            'count': len(motherboards),
            'data': motherboards
        }


