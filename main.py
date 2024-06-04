import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from fastapi import FastAPI
app = FastAPI()

from process import router as process_router
app.include_router(process_router)

from thread import router as thread_router
app.include_router(thread_router)

from hetcom import router as hetcom_router
app.include_router(hetcom_router)


