import models
from fastapi import FastAPI, Depends, HTTPException, status
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


class Todo(BaseModel):
    title: str
    description: str
    priority: int = Field(lt=6, gt=-1)
    complete: bool


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


@app.post('/', status_code=status.HTTP_201_CREATED)
async def add_todo(todo: Todo, db: Session = Depends(get_db)):
    todo_model = models.TodoEntity()
    todo_model.title = todo.title
    todo_model.description = todo.description
    todo_model.priority = todo.priority
    todo_model.complete = todo.complete

    db.add(todo_model)
    db.commit()
    return {'message': 'todo added!'}


@app.put('/', status_code=status.HTTP_202_ACCEPTED)
async def update_todo(todoId: int, todo: Todo, db: Session = Depends(get_db)):
    todo_model = db.query(models.TodoEntity).filter(models.TodoEntity.id == todoId).first()

    if not todo_model:
        raise HTTPException(status_code=404, detail="Todo not found")

    todo_model.title = todo.title
    todo_model.description = todo.description
    todo_model.priority = todo.priority
    todo_model.complete = todo.complete

    db.add(todo_model)
    db.commit()
    return {'message': 'todo updated!'}



@app.delete('/', status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(todoId: int, db: Session = Depends(get_db)):
    todo_model = db.query(models.TodoEntity).filter(models.TodoEntity.id == todoId).first()

    if not todo_model:
        raise HTTPException(status_code=404, detail="Todo not found")

    db.query(models.TodoEntity).filter(models.TodoEntity.id == todoId).delete()
    db.commit()
    return {'message': 'todo deleted!'}