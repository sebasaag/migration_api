from fastapi import FastAPI
from app.routes import employees, departments, jobs, routes_1, routes_2

app = FastAPI()

# Incluir rutas
app.include_router(employees.router)
app.include_router(departments.router)
app.include_router(jobs.router)
app.include_router(routes_1.router)
app.include_router(routes_2.router)

@app.get("/")
def read_root():
    return {"message": "API for Database Migration is running!"}
