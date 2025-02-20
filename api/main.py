from fastapi import FastAPI, UploadFile
# from pypdf import PdfReader
import llm
from pydantic import BaseModel


class User(BaseModel):
    name: str
    career_domain: str
    skills: list
    experience_years: str


class Text(BaseModel):
    retreived_text: str


class AnswerBody(BaseModel):
    question_number: int
    user_answer: str


app = FastAPI()


@app.get("/")
def hello():
    return {"hello": "world"}


@app.post("/extract_pdf")
def extract_text_from_pdf(file: UploadFile):
    return llm.extract_text_from_pdf(file.file)


@app.post("/llm/extract_key_terms")
def extract_key_terms_from_retreived_text(text: Text):
    return llm.extract_key_terms_from_retreived_text(text.retreived_text)


@app.post("/llm/generate_question")
def generate_question(user: User):
    return llm.generate_questions(user)


@app.post("/llm/evaluate_answer")
def evaluate_answer(body: AnswerBody):
    return llm.evaluate_answer(body.question_number, body.user_answer)
