from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.auth import router as auth_router
from app.api.routes.notifikasi import router as notifikasi_router
from app.api.routes.produk import router as produk_router
from app.api.routes.transaksi import router as transaksi_router
from app.core.database import Base, engine
from app.models import *  # noqa: F401,F403

Base.metadata.create_all(bind=engine)

app = FastAPI(title='SegarChain API', version='1.0.0', description='Backend prototype untuk SegarChain')

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(auth_router)
app.include_router(produk_router)
app.include_router(notifikasi_router)
app.include_router(transaksi_router)


@app.get('/')
def root():
    return {'message': 'SegarChain API aktif', 'docs': '/docs'}
