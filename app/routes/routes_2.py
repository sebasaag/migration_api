from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import get_db

router = APIRouter()

# Obtener departamentos que contrataron más empleados que la media en 2021
@router.get("/departments/hiring_above_average")
def get_departments_hiring_above_average(db: Session = Depends(get_db)):
    """
    Lista de departamentos con más empleados contratados en 2021 que la media de contratación general.
    """
    query = text('''
        WITH dept_hires AS (
            SELECT department_id, COUNT(id) AS hired
            FROM hired_employees
            WHERE YEAR(datetime) = 2021
            GROUP BY department_id
        ),
        average_hired AS (
            SELECT AVG(hired) AS avg_hired FROM dept_hires
        )
        SELECT d.id, d.department, dh.hired
        FROM dept_hires dh
        JOIN departments d ON dh.department_id = d.id
        WHERE dh.hired > (SELECT avg_hired FROM average_hired)
        ORDER BY dh.hired DESC;
    ''')
    
    with db.begin():
        result = db.execute(query)
        return [dict(row._mapping) for row in result]
