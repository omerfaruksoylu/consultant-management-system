import os
from datetime import date
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from starlette.middleware.sessions import SessionMiddleware

from app import constraints
from app.database import Consultant, Department, LeaveDay, SessionLocal, Task, User
from app.security import hash_password, verify_password

load_dotenv()                                   # read settings from backend/.env (not in Git)
if not os.environ.get("CMS_SECRET_KEY") or not os.environ.get("CMS_DEMO_PASSWORD"):
    raise RuntimeError("Missing settings: copy .env.example to .env and fill in the values.")

app = FastAPI(title="Consultant Management System")
app.add_middleware(SessionMiddleware, secret_key=os.environ["CMS_SECRET_KEY"])   # signs the login cookie
templates = Jinja2Templates(directory=Path(__file__).parent / "templates")


def add_demo_data():
    """Add invented demo data the first time the app starts. All demo users get CMS_DEMO_PASSWORD from .env."""
    with SessionLocal() as db:
        if db.scalars(select(Department)).first():
            return
        password = os.environ["CMS_DEMO_PASSWORD"]
        db.add_all([Department(id=1, name="IT"), Department(id=2, name="HR")])
        db.add(Consultant(id=1, name="Ayse Demo", department_id=1, working_weekdays="0,1,2",
                          weekly_limit=2, monthly_budget_days=6))
        db.add(Consultant(id=2, name="Mehmet Demo", department_id=2, working_weekdays="0,1,2,3,4",
                          weekly_limit=3, monthly_budget_days=10))
        db.add(LeaveDay(consultant_id=1, day=date(2026, 11, 18)))
        db.add_all([
            User(username="admin", role="admin", password_hash=hash_password(password)),
            User(username="planner_it", role="planner", department_id=1, password_hash=hash_password(password)),
            User(username="planner_hr", role="planner", department_id=2, password_hash=hash_password(password)),
            User(username="ayse", role="consultant", consultant_id=1, password_hash=hash_password(password)),
        ])
        db.commit()
        print("Demo users created: admin, planner_it, planner_hr, ayse (password: CMS_DEMO_PASSWORD in .env)")


add_demo_data()


# ---------- Login and roles (FR-01) ----------

HOME_PAGE = {"admin": "/departments", "planner": "/", "consultant": "/my-tasks"}


def get_user(request: Request, db, role: str):
    """Return the logged-in user if they have the given role, otherwise None."""
    user_id = request.session.get("user_id")
    user = db.get(User, user_id) if user_id else None
    return user if user and user.role == role else None


def go_home(request: Request, db):
    """Send a user who may not open this page to their own home page, or to the login page."""
    user_id = request.session.get("user_id")
    user = db.get(User, user_id) if user_id else None
    return RedirectResponse(HOME_PAGE[user.role] if user else "/login", status_code=303)


def render(request: Request, page: str, user, **data):
    return templates.TemplateResponse(request, page, {"user": user, **data})


@app.get("/login")
def login_page(request: Request):
    return render(request, "login.html", None)


@app.post("/login")
def login(request: Request, username: str = Form(), password: str = Form()):
    with SessionLocal() as db:
        user = db.scalars(select(User).where(User.username == username)).first()
        if not user or not verify_password(password, user.password_hash):
            return render(request, "login.html", None, message="Wrong username or password.", ok=False)
        request.session["user_id"] = user.id
        return RedirectResponse(HOME_PAGE[user.role], status_code=303)


@app.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/login", status_code=303)


# ---------- Admin: departments (FR-02) ----------

def show_departments(request: Request, db, user, message=None, ok=True):
    return render(request, "departments.html", user, message=message, ok=ok,
                  departments=db.scalars(select(Department)).all())


@app.get("/departments")
def departments_page(request: Request):
    with SessionLocal() as db:
        user = get_user(request, db, "admin")
        if not user:
            return go_home(request, db)
        return show_departments(request, db, user)


@app.post("/departments")
def add_department(request: Request, name: str = Form()):
    with SessionLocal() as db:
        user = get_user(request, db, "admin")
        if not user:
            return go_home(request, db)
        if not name.strip():
            return show_departments(request, db, user, "Rejected: Name cannot be empty.", ok=False)
        db.add(Department(name=name.strip()))
        db.commit()
        return show_departments(request, db, user, f"Department {name.strip()} added.")


# ---------- Planner: only the consultants of the planner's department (NFR-02) ----------

def department_consultants(db, user):
    return db.scalars(select(Consultant).where(Consultant.department_id == user.department_id)).all()


def find_consultant(db, user, consultant_id: int):
    """Return the consultant only if they belong to the planner's department."""
    consultant = db.get(Consultant, consultant_id)
    return consultant if consultant and consultant.department_id == user.department_id else None


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


def show_tasks(request: Request, db, user, message=None, ok=True):
    tasks = db.scalars(select(Task).join(Consultant).where(Consultant.department_id == user.department_id)
                       .order_by(Task.day)).all()
    return render(request, "index.html", user, message=message, ok=ok,
                  consultants=department_consultants(db, user), tasks=tasks)


@app.get("/")
def home(request: Request):
    with SessionLocal() as db:
        user = get_user(request, db, "planner")
        if not user:
            return go_home(request, db)
        return show_tasks(request, db, user)


@app.post("/tasks")
def assign_task(request: Request, consultant_id: int = Form(), day: date = Form(), title: str = Form()):
    with SessionLocal() as db:
        user = get_user(request, db, "planner")
        if not user:
            return go_home(request, db)
        if not title.strip():
            return show_tasks(request, db, user, "Rejected: Task title cannot be empty.", ok=False)
        consultant = find_consultant(db, user, consultant_id)
        if not consultant:
            return show_tasks(request, db, user, "Rejected: Consultant not found in your department.", ok=False)
        result = check(db, consultant, day)
        if result.allowed:
            db.add(Task(consultant_id=consultant_id, day=day, title=title))
            db.commit()
            return show_tasks(request, db, user, f"Task assigned to {consultant.name} on {day}.")
        return show_tasks(request, db, user, f"Rejected: {result.reason}.", ok=False)


def show_consultants(request: Request, db, user, message=None, ok=True):
    consultants = department_consultants(db, user)
    leave_days = db.scalars(select(LeaveDay).join(Consultant).where(Consultant.department_id == user.department_id)
                            .order_by(LeaveDay.day)).all()
    return render(request, "consultants.html", user, message=message, ok=ok,
                  consultants=consultants, leave_days=leave_days)


@app.get("/consultants")
def consultants_page(request: Request):
    with SessionLocal() as db:
        user = get_user(request, db, "planner")
        if not user:
            return go_home(request, db)
        return show_consultants(request, db, user)


@app.post("/consultants")
def add_consultant(request: Request, name: str = Form(), working_weekdays: list[int] = Form(default=[]),
                   weekly_limit: int = Form(), monthly_budget_days: int = Form()):
    with SessionLocal() as db:
        user = get_user(request, db, "planner")
        if not user:
            return go_home(request, db)
        if not name.strip():
            return show_consultants(request, db, user, "Rejected: Name cannot be empty.", ok=False)
        if not working_weekdays:
            return show_consultants(request, db, user, "Rejected: Select at least one working day.", ok=False)
        if weekly_limit < 1 or monthly_budget_days < 1:
            return show_consultants(request, db, user, "Rejected: Limits must be at least 1 day.", ok=False)
        db.add(Consultant(name=name.strip(), department_id=user.department_id,
                          working_weekdays=",".join(str(d) for d in sorted(working_weekdays)),
                          weekly_limit=weekly_limit, monthly_budget_days=monthly_budget_days))
        db.commit()
        return show_consultants(request, db, user, f"Consultant {name.strip()} added.")


@app.post("/leave-days")
def add_leave_day(request: Request, consultant_id: int = Form(), day: date = Form()):
    with SessionLocal() as db:
        user = get_user(request, db, "planner")
        if not user:
            return go_home(request, db)
        if not find_consultant(db, user, consultant_id):
            return show_consultants(request, db, user, "Rejected: Consultant not found in your department.", ok=False)
        db.add(LeaveDay(consultant_id=consultant_id, day=day))
        db.commit()
        return show_consultants(request, db, user, f"Leave day {day} added.")


# ---------- Consultant: own tasks only, read-only (FR-06) ----------

@app.get("/my-tasks")
def my_tasks(request: Request):
    with SessionLocal() as db:
        user = get_user(request, db, "consultant")
        if not user:
            return go_home(request, db)
        tasks = db.scalars(select(Task).where(Task.consultant_id == user.consultant_id).order_by(Task.day)).all()
        return render(request, "my_tasks.html", user, tasks=tasks)
