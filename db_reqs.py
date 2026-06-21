from aiomysql import Pool, DictCursor


class DB_commands:
    def __init__(self, pool: Pool):
        self.pool = pool

    async def select_all (self, sql : str, data: tuple = None):
        async with self.pool.acquire() as conn:
            async with conn.cursor(DictCursor) as cur:
                await cur.execute(sql,data)
            return await cur.fetchall()


