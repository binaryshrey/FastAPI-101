from uuid import UUID
from typing import Optional
from pydantic import BaseModel, Field
from starlette.responses import JSONResponse
from fastapi import FastAPI, HTTPException, Request, status, Form, Header


# Response BaseModel
class Book(BaseModel):
    uid: UUID
    title: str = Field(min_length=1)
    author: str = Field(min_length=1)
    description: str = Field(title='description of the book', min_length=1, max_length=100)
    rating: int = Field(gt=-1, lt=11)

    # Default config override
    class Config:
        schema_extra = {
            'example': {
                "uid": "17c65688-aa68-42c2-bbe5-8a0854301abf",
                "title": "Harry Potter and the Prisoner of Azkaban",
                "author": "JK Rowling",
                "description": "3rd book in HP series",
                "rating": 10
            }
        }


class BookNoRating(BaseModel):
    uid: UUID
    title: str = Field(min_length=1)
    author: str = Field(min_length=1)
    description: str = Field(title='description of the book', min_length=1, max_length=100)


# Custom Exception
class NegativeNumberException(Exception):
    def __init__(self, number):
        self.number = number


app = FastAPI()
BOOKS = []


def create_dummy_books():
    book1 = Book(uid='bbab32e7-65a5-4694-8d78-7e3c1e7f9b8b', title='Harry Potter and the Sorcerer’s Stone',
                 author='JK Rowling', description='1st book in HP series', rating='10')
    book2 = Book(uid='039dc28a-a704-423c-bf7f-33957b8525f2', title='Harry Potter and the Chamber of Secrets',
                 author='JK Rowling', description='2nd book in HP series', rating='9')
    book3 = Book(uid='57c65688-aa68-42c2-bbe5-8a0854301abf', title='Harry Potter and the Prisoner of Azkaban',
                 author='JK Rowling', description='3rd book in HP series', rating='10')
    book4 = Book(uid='12814a0a-a3de-470f-812f-611a63133095', title='Harry Potter and the Goblet of Fire',
                 author='JK Rowling', description='4th book in HP series', rating='9')
    book5 = Book(uid='482bd3be-a6c0-418d-8285-21e2fb859c5c', title='Harry Potter and the Order of the Phoenix',
                 author='JK Rowling', description='5th book in HP series', rating='10')
    BOOKS.append(book1)
    BOOKS.append(book2)
    BOOKS.append(book3)
    BOOKS.append(book4)
    BOOKS.append(book5)


# Custom Exception handler
@app.exception_handler(NegativeNumberException)
async def handle_negative_number(request: Request, exception: NegativeNumberException):
    return JSONResponse(status_code=418, content={'message': 'Negative numbers not allowed'})


# Not found exception
def raise_uid_not_found_exception():
    return HTTPException(status_code=404, detail='UID not found', headers={'X-HEADER-ERROR': 'No matching UID found'})


@app.get('/')
def get_books(books_to_return: Optional[int] = None):
    if len(BOOKS) < 1:
        create_dummy_books()

    if books_to_return and books_to_return < 0:
        raise NegativeNumberException(books_to_return)
    elif books_to_return and books_to_return < len(BOOKS):
        return BOOKS[0:books_to_return]
    return BOOKS


@app.get('/uid/')
def get_book_by_uid(uid: UUID):
    for book in BOOKS:
        if uid == book.uid:
            return book
    raise raise_uid_not_found_exception()


# Custom response model
@app.get('/uid/no_rating/', response_model=BookNoRating)
def get_book_by_uid(uid: UUID):
    for book in BOOKS:
        if uid == book.uid:
            return book
    raise raise_uid_not_found_exception()


@app.post('/', status_code=status.HTTP_201_CREATED)
def add_book(book: Book):
    BOOKS.append(book)
    return BOOKS


@app.put('/')
def add_book(uid: UUID, book: Book):
    for i, b in enumerate(BOOKS):
        if uid == b.uid:
            BOOKS[i] = book
    raise raise_uid_not_found_exception()


@app.delete('/uid/')
def del_book_by_uid(uid: UUID):
    for i, book in enumerate(BOOKS):
        if uid == book.uid:
            del BOOKS[i]
            return {uid: 'Deleted'}
    raise raise_uid_not_found_exception()


# Form data post
@app.post('/books/login/')
async def books_login(username: str = Form(...), password: str = Form(...)):
    return {'username': username, 'password': password}


# Header
@app.get('/header')
async def get_header(random_header: Optional[str] = Header(None)):
    return {'header': random_header}
