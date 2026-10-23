"""Rota de inscrição a completar na atividade 3."""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db_session import get_session
from sqlalchemy import select
from app.db_session import get_session
from app.models import Event, Registration, User

router = APIRouter()


class RegistrationInput(BaseModel):
    user_id: int


@router.post("/events/{event_id}/registrations", status_code=201)
def register(event_id: int, data: RegistrationInput, session: Session = Depends(get_session)):
    # Atividade 3: verifique evento, usuário, duplicidade e vagas. Só então
    # grave Registration e responda com event_id e user_id.
    event = session.get(Event, event_id)
    if event is None:
        raise HTTPException(status_code=404)

    user = session.get(User, data.user_id)
    if user is None:
        raise HTTPException(status_code=404)

    ja_inscrito = session.scalars(
        select(Registration).where(
            Registration.event_id == event_id,
            Registration.user_id == data.user_id,
        )
    ).first()
    if ja_inscrito is not None:
        raise HTTPException(status_code=409, detail="Usuário já inscrito")

    inscritos = len(session.scalars(
        select(Registration).where(Registration.event_id == event_id)
    ).all())
    if inscritos >= event.capacity:
        raise HTTPException(status_code=409, detail="Evento lotado")
    
    session.add(Registration(event_id=event_id, user_id=data.user_id))
    session.commit()
    return {"event_id": event_id, "user_id": data.user_id}
