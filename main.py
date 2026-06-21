from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import aiomysql
from db import DB_config
from components import cpu,gpu,motherboard, cases, coolers

@asynccontextmanager
async def lifespan (app:FastAPI):
    app.state.db_pool = await aiomysql.create_pool(**DB_config)
    print("Connection succesfull")

    yield

    app.state.db_pool.close()
    await app.state.db_pool.wait.closed()
    print("Connection broke")

app = FastAPI(lifespan=lifespan, title="GECID PC Builder")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(cpu.router)
app.include_router(gpu.router)
app.include_router(motherboard.router)
app.include_router(cases.router)
app.include_router(coolers.router)


@app.get("/test")
async def root():
    return {'status': 'ok', 'database': 'ok'}
