from fastapi import APIRouter, Depends, HTTPException
from Database.db import get_db_cursor

router = APIRouter(
    prefix='/api/v1/analyse',
    tags=['Ready PC Cost/TDP analyse']
)

@router.get('/{build_id}')
async def build_anlz(build_id: int, cur = Depends(get_db_cursor)):

    query = '''
            select 
            b.build_name,
            c.brand_cpu, c.name_cpu AS cpu_name, c.price AS cpu_price, c.tdp AS cpu_tdp,
            m.brand_mother, m.name_mother AS mb_name, m.price_mother AS mb_price,
            r.brand_ram, r.name_ram AS ram_name, r.price_ram AS ram_price,
            g.brand_gpu, g.name_gpu AS gpu_name, g.price_gpu AS gpu_price, g.tdp AS gpu_tdp,
            p.brand_psu, p.name_psu, p.wattage AS psu_wattage, p.price_psu AS psu_price,
            cs.brand_case, cs.name_case AS case_name, cs.price AS case_price,
            cl.brand_cooler, cl.name_cooler AS cooler_name, cl.price AS cooler_price
            from builds b
            LEFT JOIN cpu c ON b.cpu_id = c.id
            LEFT JOIN motherboard m ON b.motherboard_id = m.id
            LEFT JOIN ram r ON b.ram_id = r.id
            LEFT JOIN gpu g ON b.gpu_id = g.id
            LEFT JOIN psu p ON b.psu_id = p.id
            LEFT JOIN cases cs ON b.case_id = cs.id
            LEFT JOIN cooler cl ON b.cooler_id = cl.id
            where b.id = %s
    '''

    try:
        await cur.execute(query,(build_id,))
        build_data = await cur.fetchone()

        if not build_data:
            raise HTTPException(status_code=404, detail=f'Build with {build_id} not found')
        build_price = 0
        for key,value in build_data.items():
            if 'price' in key and value != None:
                build_price += float(value)

        cpu_tdp = float(build_data['cpu_tdp']) if build_data['cpu_tdp'] else 0
        gpu_tdp = float(build_data['gpu_tdp']) if build_data['gpu_tdp'] else 0
        total_tdp =  cpu_tdp + gpu_tdp
        rec_tdp = total_tdp + 100

        psu_status = 'PSU not selected'
        if build_data ['psu_wattage']:
            psu_watt = float(build_data['psu_wattage'])
            if psu_watt >= rec_tdp:
                psu_status = 'OK (Enough power)'
            else:
                psu_status = 'Warning! PSU is weak for this build'
        return {
            "status": "success",
            "build_name": build_data['build_name'],
            "summary": {
                "total_price": build_price,
                "total_tdp": total_tdp,
                "recommended_tdp": rec_tdp,
                "psu_check": psu_status
            },
            "components": build_data
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


