from fastapi import FastAPI

import fabric_related, ca_related, ethereum_related
import os
from config import STORAGE_PATH

def init_and_check():
    if not os.path.exists(STORAGE_PATH):
        os.mkdir(STORAGE_PATH)
    if not os.path.exists(f'{STORAGE_PATH}/fabric-ca-servers'):
        os.mkdir(f'{STORAGE_PATH}/fabric-ca-servers')

init_and_check()

app = FastAPI()

app.include_router(router=fabric_related.router)
app.include_router(router=ca_related.router)
# app.include_router(router=ethereum_related.router)



