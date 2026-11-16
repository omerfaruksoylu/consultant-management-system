"""Database connection and tables (SQLite + SQLAlchemy)."""
from datetime import date
from typing import Optional

from sqlalchemy import ForeignKey, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker

engine = create_engine("sqlite:///cms.db")      # the database is the file backend/cms.db
SessionLocal = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass


class Department(Base):
    __tablename__ = "departments"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    password_hash: Mapped[str]                  # never the password itself (NFR-01)
    role: Mapped[str]                           # "admin", "planner" or "consultant"
    department_id: Mapped[Optional[int]] = mapped_column(ForeignKey("departments.id"))   # planners
    consultant_id: Mapped[Optional[int]] = mapped_column(ForeignKey("consultants.id"))   # consultants


class Consultant(Base):
    __tablename__ = "consultants"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    department_id: Mapped[int] = mapped_column(ForeignKey("departments.id"))
    working_weekdays: Mapped[str]               # e.g. "0,1,2" = Monday, Tuesday, Wednesday
    weekly_limit: Mapped[int]
    monthly_budget_days: Mapped[int]


class LeaveDay(Base):
    __tablename__ = "leave_days"
    id: Mapped[int] = mapped_column(primary_key=True)
    consultant_id: Mapped[int] = mapped_column(ForeignKey("consultants.id"))
    day: Mapped[date]


class Task(Base):
    __tablename__ = "tasks"
    id: Mapped[int] = mapped_column(primary_key=True)
    consultant_id: Mapped[int] = mapped_column(ForeignKey("consultants.id"))
    day: Mapped[date]
    title: Mapped[str]


Base.metadata.create_all(engine)                # create the tables if they do not exist
