from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from db import get_db_cursor
from JWT import get_user


router = APIRouter(
    prefix='/api/v1/build',
    tags = ['Ready Build']
)

class Build(BaseModel):
    build_name: str = 'My PC'
    cpu_id: Optional[int] = None
    motherboard_id: Optional[int] = None
    ram_id: Optional[int] = None
    gpu_id: Optional[int] = None
    psu_id: Optional[int] = None
    case_id: Optional[int] = None
    cooler_id: Optional[int] = None

class BuildUpdate(BaseModel):
    build_name: Optional[str] = None
    cpu_id: Optional[int] = None
    motherboard_id: Optional[int] = None
    ram_id: Optional[int] = None
    gpu_id: Optional[int] = None
    psu_id: Optional[int] = None
    case_id: Optional[int] = None
    cooler_id: Optional[int] = None

@router.post('/')
async def create_build(build: Build, cur = Depends(get_db_cursor), user_id: int = Depends(get_user)):

    query = '''
        INSERT INTO builds 
        (user_id, build_name, cpu_id, motherboard_id, ram_id, gpu_id, psu_id, case_id, cooler_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    '''

    values = (
        user_id, build.build_name, build.cpu_id, build.motherboard_id,
        build.ram_id, build.gpu_id, build.psu_id, build.case_id, build.cooler_id
    )
    try:
        await cur.execute(query,values)

        return {
            "status": "success",
            "message": f"Your build '{build.build_name}' has been successfully saved"
        }
    except:
        raise HTTPException(
            status_code=400,
            detail=f"Error"
        )


@router.get('/{user_id}')
async def user_builds(cur = Depends(get_db_cursor), user_id: int = Depends(get_user)):
    try:
        await cur.execute('SELECT * FROM builds WHERE user_id = %s', (user_id,))
        builds = await cur.fetchall()

        if not builds:
            return {
                'status': 'success',
                'data': 'this user doesnt have any builds'
            }

        for b in builds:
            if 'created_at' in b and b['created_at']:
                b['created_at'] = str(b['created_at'])
            if 'updated_at' in b and b['updated_at']:
                b['updated_at'] = str(b['updated_at'])

        return {
            'status': 'success',
            'user_build_count': len(builds),
            'data': builds
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete('/{build_id}')
async def delete_build(build_id: int, cur = Depends(get_db_cursor), user_id: int = Depends(get_user)):

    try:
        await cur.execute('Delete from builds Where id=%s and user_id = %s',(build_id,user_id,))

        if cur.rowcount == 0:
            raise HTTPException(status_code=404,detail=f'Build with {build_id} not found')
        return {
            "status": "success",
            "message": f"Build {build_id} has been successfully deleted"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.patch('/{build_id}')
async def update_bld(build_id:int,build_data: BuildUpdate, cur=Depends(get_db_cursor), user_id: int = Depends(get_user)):
    try:
        update_fields = build_data.dict(exclude_unset= True)

        if not update_fields:
            return {'status':'success','message':'There is no builds to update'}
        set_clauses = []
        values = []

        for field_name,field_value in update_fields.items():
            set_clauses.append(f'{field_name}=%s')
            values.append(field_value)

        set_q_str = ', '.join(set_clauses)

        values.extend([build_id, user_id])
        #set_q_str = gpu_id = x, ram_id = x
        final_q = f'UPDATE builds SET {set_q_str} where id = %s and user_id = %s'

        await cur.execute(final_q,tuple(values))

        await cur.execute("SELECT * FROM builds WHERE id = %s", (build_id,))
        updated_build = await cur.fetchone()

        if not updated_build:
            raise HTTPException(status_code=404, detail=f"Build with ID {build_id} not found")

        if cur.rowcount == 0:
            raise (
                HTTPException(status_code=404,detail='Build not found. No data has been changed')
            )
        for key, value in updated_build.items():
            if value is not None and not isinstance(value, (int, float, str, bool)):
                updated_build[key] = str(value)
        return {
            "status": "success",
            "message": f"Build {build_id} has benn successfully updated",
            "data": updated_build
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

