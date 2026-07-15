from fastapi import Request
import aiomysql


DB_config = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': 'sqladmin',
    'db': 'GECID_PC',
    'autocommit': True
}

async def get_db_cursor(request: Request):
    async with request.app.state.db_pool.acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cur:
            yield cur
