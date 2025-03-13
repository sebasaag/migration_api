from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import get_db

router = APIRouter()

@router.get("/hired_employees/quarterly")
def get_hired_employees_by_quarter(db: Session = Depends(get_db)):
    """
    Devuelve el número de empleados contratados en 2021 por cada trabajo y departamento,
    dividido por trimestre y ordenado alfabéticamente por departamento y trabajo.
    """
    query = text('''
        SELECT 
            d.department, 
            j.job, 
            SUM(CASE WHEN MONTH(e.datetime) BETWEEN 1 AND 3 THEN 1 ELSE 0 END) AS Q1,
            SUM(CASE WHEN MONTH(e.datetime) BETWEEN 4 AND 6 THEN 1 ELSE 0 END) AS Q2,
            SUM(CASE WHEN MONTH(e.datetime) BETWEEN 7 AND 9 THEN 1 ELSE 0 END) AS Q3,
            SUM(CASE WHEN MONTH(e.datetime) BETWEEN 10 AND 12 THEN 1 ELSE 0 END) AS Q4
        FROM hired_employees e
        INNER JOIN jobs j ON e.job_id = j.id
        INNER JOIN departments d ON e.department_id = d.id
        WHERE YEAR(e.datetime) = 2021
        GROUP BY d.department, j.job
        ORDER BY d.department, j.job;
    ''')
    
    with db.begin():
        result = db.execute(query)
        return [dict(row._mapping) for row in result]

