from datetime import date
from pathlib import Path

from fastapi import FastAPI, Form, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy import select

from app import constraints
from app.database import Consultant, LeaveDay, SessionLocal, Task

app = FastAPI(title="Consultant Management System")
templates = Jinja2Templates(directory=Path(__file__).parent / "templates")


def add_demo_data():
    """Add two invented consultants the first time the app starts."""
    with SessionLocal() as db:
        if db.scalars(select(Consultant)).first():
            return
        db.add(Consultant(id=1, name="Ayse Demo", working_weekdays="0,1,2", weekly_limit=2, monthly_budget_days=6))
        db.add(Consultant(id=2, name="Mehmet Demo", working_weekdays="0,1,2,3,4", weekly_limit=3, monthly_budget_days=10))
        db.add(LeaveDay(consultant_id=1, day=date(2026, 11, 18)))
        db.commit()


add_demo_data()


def check(db, consultant: Consultant, day: date) -> constraints.CheckResult:
    """Read the consultant's data from the database and run the restriction check."""
    rules = constraints.Consultant(
        id=consultant.id,
        working_weekdays={int(d) for d in consultant.working_weekdays.split(",")},
        weekly_limit=consultant.weekly_limit,
        monthly_budget_days=consultant.monthly_budget_days,
        leave_days=set(db.scalars(select(LeaveDay.day).where(LeaveDay.consultant_id == consultant.id))),
    )
    existing = [constraints.Assignment(t.consultant_id, t.day)
                for t in db.scalars(select(Task).where(Task.consultant_id == consultant.id))]
    return constraints.check_assignment(rules, existing, day)


def show_page(request: Request, db, message=None, ok=True):
    return templates.TemplateResponse(request, "index.html", {
        "consultants": db.scalars(select(Consultant)).all(),
        "tasks": db.scalars(select(Task).order_by(Task.day)).all(),
        "message": message,
        "ok": ok,
    })


@app.get("/")
def home(request: Request):
    with SessionLocal() as db:
        return show_page(request, db)


@app.post("/tasks")
def assign_task(request: Request, consultant_id: int = Form(), day: date = Form(), title: str = Form()):
    with SessionLocal() as db:
        consultant = db.get(Consultant, consultant_id)
        result = check(db, consultant, day)
        if result.allowed:
            db.add(Task(consultant_id=consultant_id, day=day, title=title))
            db.commit()
            return show_page(request, db, f"Task assigned to {consultant.name} on {day}.")
        return show_page(request, db, f"Rejected: {result.reason}.", ok=False)
