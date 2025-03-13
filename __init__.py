from fastapi import FastAPI

app = FastAPI()

from app.routes import employees, departments, jobs

# Registrar las rutas
app.include_router(employees.router)
app.include_router(departments.router)
app.include_router(jobs.router)
