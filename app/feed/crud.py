from sqlalchemy.orm import Session
from app.models import Note
from app.feed.schemas import NoteCreate, NoteUpdate


def get_notes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Note).order_by(Note.created_date.desc()).offset(skip).limit(limit).all()


def get_note(db: Session, note_id: int):
    return db.query(Note).filter(Note.id == note_id).first()


def create_note(db: Session, note: NoteCreate):
    db_note = Note(title=note.title, content=note.content)
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note


def update_note(db: Session, note_id: int, note: NoteUpdate):
    db_note = db.query(Note).filter(Note.id == note_id).first()
    if db_note:
        db_note.title = note.title
        db_note.content = note.content
        db.commit()
        db.refresh(db_note)
    return db_note


def delete_note(db: Session, note_id: int):
    db_note = db.query(Note).filter(Note.id == note_id).first()
    if db_note:
        db.delete(db_note)
        db.commit()
        return True
    return False
