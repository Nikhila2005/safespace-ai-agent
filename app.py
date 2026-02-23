from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello from SafeSpace AI Agent", "status": "ok"}

@app.get("/health")
def health():
    return {"status": "healthy"}
