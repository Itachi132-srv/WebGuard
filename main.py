from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any
from blueprint import BlueprintRunner
from scanner import run_security_scan

app = FastAPI(title="Shardex WebGuard AI", version="1.2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class BlueprintRequest(BaseModel):
    target_url: str
    steps: List[Dict[str, Any]]

class SecurityScanRequest(BaseModel):
    target_url: str

@app.post("/api/test/functional")
def run_functional_blueprint(req: BlueprintRequest):
    runner = BlueprintRunner(req.target_url, req.steps)
    return runner.execute()

@app.post("/api/test/security")
def run_security(req: SecurityScanRequest):
    return run_security_scan(req.target_url)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
