import json

file = r"/home/androide47/Documents/FastAPI-The-Complete-Course/Books2/books.json"

def load_books(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

result =  load_books(file)
print(result)