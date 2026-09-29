from fastapi.testclient import TestClient
from backend.main import app
client=TestClient(app)
def test_root():
    r=client.get("/"); assert r.status_code==200; assert r.json()["status"]=="ok"
def test_health():
    r=client.get("/health"); assert r.status_code==200; assert r.json()["status"]=="healthy"
def test_generate(monkeypatch):
    from backend.routes import generator
    monkeypatch.setattr(generator,"generate_document",lambda *a:("DRAFT TEST","demo"))
    r=client.post("/generate",json={"document_type":"NDA","parties":"A, B","terms":["Confidentiality"],"effective_date":"2026-09-28"})
    assert r.status_code==200 and r.json()["source"]=="demo"
def test_validation():
    r=client.post("/generate",json={"document_type":"NDA","parties":"","terms":[],"effective_date":"2026-09-28"}); assert r.status_code==422
