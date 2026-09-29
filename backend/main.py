from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.config import APP_TITLE
from backend.routes import router
app=FastAPI(title=APP_TITLE,description="AI-assisted legal document drafting backend.",version="1.0.0")
app.add_middleware(CORSMiddleware,allow_origins=["*"],allow_credentials=False,allow_methods=["*"],allow_headers=["*"])
app.include_router(router)
@app.get("/")
def root(): return {"status":"ok","service":APP_TITLE,"message":"LegalEase backend is running."}
@app.get("/health")
def health(): return {"status":"healthy"}
