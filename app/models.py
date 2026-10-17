"""Modelos relacionais que serão completados na atividade 2."""

from sqlalchemy import Integer, ForeignKey, UniqueConstraint, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Event(Base):
    __tablename__ = "events"
    __table_args__ = (
        CheckConstraint("capacity > 0", name="ck_events_capacity_positive"),
    )
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    # Complete os campos title, date e capacity e suas restrições.
    title: Mapped[str] = mapped_column(nullable=False)
    date: Mapped[int] = mapped_column(nullable=False)
    capacity: Mapped[int] = mapped_column(nullable=False)


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    # Complete os campos name e email.
    name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)


class Registration(Base):
    __tablename__ = "registrations"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    event_id: Mapped[int] = mapped_column(Integer)
    user_id: Mapped[int] = mapped_column(Integer)
    # Relacione event_id e user_id às tabelas corretas e impeça duplicatas.
    event_id: Mapped[int] = mapped_column(Integer, ForeignKey("events.id"))
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))

    __table_args__ = (
        UniqueConstraint('event_id', 'user_id', name='uq_event_user'),
    )

