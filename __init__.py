from fastapi import FastAPI

app = FastAPI()

from app.routes import employees, departments, jobs, routes_1, routes_2

# Registrar las rutas
app.include_router(employees.router)
app.include_router(departments.router)
app.include_router(jobs.router)
app.include_router(routes_1.router)
app.include_router(routes_2.router)
