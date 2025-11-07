from fastapi import FastAPI, Request, Depends, HTTPException, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import os
from app.database import get_db, engine, Base
from app.feed.crud import get_notes, get_note, create_note, update_note, delete_note
from app.feed.schemas import NoteCreate, NoteUpdate

Base.metadata.create_all(bind=engine)

app = FastAPI(title="YourNotes", description="Микросервис для управления заметками")

current_dir = os.path.dirname(os.path.abspath(__file__))
templates_dir = os.path.join(current_dir, "templates")
static_dir = os.path.join(os.path.dirname(current_dir), "static")

app.mount("/static", StaticFiles(directory=static_dir), name="static")
templates = Jinja2Templates(directory=templates_dir)


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request, db: Session = Depends(get_db)):
    notes = get_notes(db)

    from datetime import timedelta

    for note in notes:
        tomsk_time = note.created_date + timedelta(hours=7) 
        note.formatted_time = tomsk_time.strftime("%d.%m.%Y %H:%M")

    return templates.TemplateResponse("index.html", {
        "request": request,
        "notes": notes,
        "editing_note": None
    })


@app.post("/notes/")
async def create_note_handler(
    title: str = Form(...),
    content: str = Form(...),
    db: Session = Depends(get_db)
):
    if not title.strip() or not content.strip():
        raise HTTPException(status_code=400, detail="Заголовок и содержание не могут быть пустыми")

    note_create = NoteCreate(title=title.strip(), content=content.strip())
    create_note(db=db, note=note_create)
    return RedirectResponse(url="/", status_code=303)


@app.get("/notes/{note_id}/edit", response_class=HTMLResponse)
async def edit_note_form(request: Request, note_id: int, db: Session = Depends(get_db)):
    note = get_note(db, note_id=note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Заметка не найдена")

    notes = get_notes(db)
    return templates.TemplateResponse("index.html", {
        "request": request,
        "notes": notes,
        "editing_note": note
    })


@app.post("/notes/{note_id}/edit")
async def update_note_handler(
    note_id: int,
    title: str = Form(...),
    content: str = Form(...),
    db: Session = Depends(get_db)
):
    if not title.strip() or not content.strip():
        raise HTTPException(status_code=400, detail="Заголовок и содержание не могут быть пустыми")

    note_update = NoteUpdate(title=title.strip(), content=content.strip())
    db_note = update_note(db, note_id=note_id, note=note_update)

    if not db_note:
        raise HTTPException(status_code=404, detail="Заметка не найдена")

    return RedirectResponse(url="/", status_code=303)


@app.post("/notes/{note_id}/delete")
async def delete_note_handler(
    note_id: int,
    db: Session = Depends(get_db)
):
    success = delete_note(db, note_id=note_id)
    if not success:
        raise HTTPException(status_code=404, detail="Заметка не найдена")

    return RedirectResponse(url="/", status_code=303)
