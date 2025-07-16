from fastapi import FastAPI, Body, Path, Query, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from starlette import status
import json 

class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    year: int
    
    def __init__(self, id, title, author, description, rating, year):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.year = year

class BookRequest(BaseModel):
    id: Optional[int] = Field(description='ID is not needed on create', default=None)
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=0, lt=6)
    year: int = Field(min_length=1)

    model_config ={
        "json_schema_extra": {
           "example": {
               "title": "A new book",
               "author": "Sample title",
               "description": "A new description of a book",
               "rating": 5,
               "year": 1990
           } 
        }
    }
    

app = FastAPI()

BOOKS = [
    Book(1, 'Computer Science Pro', 'Coding', 'A very nice book!', 5, 2020),
    Book(2, 'Python Basics', 'John Doe', 'Learn Python from scratch.', 4, 2018),
    Book(3, 'Advanced Python', 'Jane Smith', 'Master advanced Python concepts.', 5, 2019),
    Book(4, 'Data Structures and Algorithms', 'Alice Johnson', 'A comprehensive guide to DSA.', 5, 2017),
    Book(5, 'Machine Learning 101', 'Bob Brown', 'An introduction to machine learning.', 4, 2021),
    Book(6, 'Deep Learning with Python', 'Carol White', 'A deep dive into deep learning.', 5, 2020),
    Book(7, 'FastAPI for Beginners', 'David Green', 'Learn FastAPI step by step.', 4, 2022),
    Book(8, 'RESTful APIs with Python', 'Eve Black', 'Build RESTful APIs using Python.', 5, 2021),
    Book(9, 'Database Design', 'Frank Blue', 'Learn how to design databases effectively.', 4, 2016),
    Book(10, 'Cloud Computing Essentials', 'Grace Red', 'An introduction to cloud computing.', 3, 2015)
]

@app.get("/books", status_code=status.HTTP_200_OK)
async def read_all_books():
    return BOOKS


@app.get("/books/{id}", status_code=status.HTTP_200_OK)
async def singlebook(id: int = Path(gt=0)):
    for book in BOOKS:
        if book.id == id:
            return book
    raise HTTPException(status_code=404, detail='Item not found')

@app.get("/books/", status_code=status.HTTP_200_OK)
async def rated_books(raiting: int = Query(gt=0, lt=6)):
    result = []
    for book in BOOKS:
        if book.rating == raiting:
            result.append(book)
    return result

@app.get("/books/year/", status_code=status.HTTP_200_OK)
async def book_by_year(year: int = Query(gt=1999, lt=2026)):
    result = []
    for book in BOOKS:
        if book.year == year:
            result.append(book.year)
    return result 

@app.put("/books/update-book", status_code=status.HTTP_204_NO_CONTENT)
async def uppdate_book(book_update: BookRequest):
    book_change = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_update.id:
            BOOKS[i] = book_update
            book_change = True
    if book_change:
        raise HTTPException(status_code=404, detail='No item found')
            
@app.delete("/book/delete/{id}")
async def delete_book(id: int = Path(gt=0)):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == id:
            BOOKS.pop(i)     
            break 
    
@app.post("/create-book", status_code=status.HTTP_201_CREATED)
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.model_dump())
    BOOKS.append(find_book_id(new_book))
    
def find_book_id(book: Book):
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    
    return book
    