from fastapi import APIRouter, Depends
from db import get_db_cursor

router = APIRouter(
    prefix='/api/v1/cases',
    tags = ['CASE']
)

@router.get('/')
async def get_cases(mother_id: int = None, cur = Depends(get_db_cursor)):

    if mother_id:
        query = '''
        select c.brand_case, c.name_case, cf.form_factor, c.price, m.brand_mother, m.name_mother, m.price_mother from cases c 
        Join cases_form cf ON (c.id = cf.case_id)
        join motherboard m ON (cf.form_factor = m.form_factor)
        where m.id = %s   
        '''
        await cur.execute (query,(mother_id))

    else:
        await cur.execute('select c.*, cf.form_factor from cases c join cases_form cf ON (c.id = cf.case_id)')

    cases = await cur.fetchall()

    return {
        'status': 'success',
        'count': len(cases),
        'data': cases
    }



