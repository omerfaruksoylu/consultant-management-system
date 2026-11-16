from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI(title="Consultant Management System")


@app.get("/", response_class=HTMLResponse)
def home():
    return "<h1>Consultant Management System</h1><p>Prototype is running.</p>"
