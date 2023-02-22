import models
from fastapi import FastAPI, Depends, HTTPException
from database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get('/')
async def read_all(db: Session = Depends(get_db)):
    return db.query(models.TodoEntity).all()


@app.get('/todos/{todoID}')
async def get_todo_by_id(todoID: int, db: Session = Depends(get_db)):
    todo_model = db.query(models.TodoEntity).filter(models.TodoEntity.id == todoID).first()
    if todo_model:
        return todo_model
    raise HTTPException(status_code=404, detail="Todo not found")

