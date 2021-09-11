from fastapi import *
from fastapi.middleware.cors import CORSMiddleware
from common import *
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/data")
async def main():
    return get_all_question()


@app.get('/topic')
async def get_topic():
    return get_all_topic()


@app.get('/document')
async def get_document():
    return get_all_document()


@app.get('/point/{id}')
async def get_point(id: int):
    return get_point_db(id)


@app.get('/receive/{id_student}/{result_student}/{id_question}')
async def receive(id_student, result_student, id_question):
    check_ans_and_update_row(id_student, result_student, id_question)
    return {'id_student': id_student, 'result_student': result_student, 'id_question': id_question}


class user(BaseModel):
    user: str
    passw: str


@app.post('/login')
async def login(u: user):
    return check_user_and_pass(u.user, u.passw)


templates = Jinja2Templates(directory="templates")


@app.get("/items")
async def read_item(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
