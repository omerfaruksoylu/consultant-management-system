"""Database connection and tables (SQLite + SQLAlchemy)."""
from datetime import date

from sqlalchemy import ForeignKey, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker

engine = create_engine("sqlite:///cms.db")      # the database is the file backend/cms.db
SessionLocal = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass


class Consultant(Base):
    __tablename__ = "consultants"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
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
