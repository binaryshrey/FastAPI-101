from enum import Enum
from fastapi import FastAPI
from typing import Optional

app = FastAPI()

BOOKS = {
    'book_1': {'title': 'Book-One', 'author': 'Author-One'},
    'book_2': {'title': 'Book-Two', 'author': 'Author-Two'},
    'book_3': {'title': 'Book-Three', 'author': 'Author-Three'},
    'book_4': {'title': 'Book-Four', 'author': 'Author-Four'},
    'book_5': {'title': 'Book-Five', 'author': 'Author-Five'},

}


class BookName(str, Enum):
    book_1 = 'book_1'
    book_2 = 'book_2'
    book_3 = 'book_3'
    book_4 = 'book_4'
    book_5 = 'book_5'


@app.get('/')
async def get_all_books_with_query_params(skip_book: Optional[str] = None):
    if skip_book:
        new_book = BOOKS.copy()
        del new_book[skip_book]
        return new_book
    return BOOKS


@app.get('/bookName/{book_name}')
async def books_by_name(book_name: str):
    return BOOKS[book_name]


@app.get('/bookId/{book_id}')
async def books_by_id(book_id: int):
    return {list(BOOKS)[book_id]: BOOKS[list(BOOKS)[book_id]]}


@app.get('/books/{book_name}')
async def books_by_enum(book_name: BookName):
    if book_name == 'book_1':
        return {'title': 'Book-One', 'author': 'Author-One'}
    if book_name == 'book_2':
        return {'title': 'Book-Two', 'author': 'Author-Two'}
    if book_name == 'book_3':
        return {'title': 'Book-Three', 'author': 'Author-Three'}
    if book_name == 'book_4':
        return {'title': 'Book-Four', 'author': 'Author-Four'}
    return {'title': 'Book-Five', 'author': 'Author-Five'}


# post
@app.post('/')
async def add_book(book_title, book_author):
    new_book = {'title': book_title, 'author': book_author}
    BOOKS[f'book_{len(BOOKS) + 1}'] = new_book
    return {f'book_{len(BOOKS)}': new_book}


# put
@app.put('/{book_name}')
async def update_book(book_name: str, book_title: str, book_author: str):
    updated_book = {'title': book_title, 'author': book_author}
    BOOKS[book_name] = updated_book
    return {book_name: updated_book}


# delete
@app.delete('/{book_name}')
async def update_book(book_name):
    del BOOKS[book_name]
    return f'{book_name} deleted!'
