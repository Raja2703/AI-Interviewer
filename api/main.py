from fastapi import FastAPI, UploadFile, File
import shutil

# from pypdf import PdfReader
from fastapi.middleware.cors import CORSMiddleware
import llm
from pydantic import BaseModel


class User(BaseModel):
    name: str
    career_domain: str
    skills: list
    experience_years: str


class Text(BaseModel):
    retrieved_text: str


class AnswerBody(BaseModel):
    question_number: str
    user_answer: str


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def hello():
    return {"hello": "world"}


@app.post("/extract_pdf")
def extract_text_from_pdf(file: UploadFile):
    return llm.extract_text_from_pdf(file.file)


@app.post("/llm/extract_key_terms")
def extract_key_terms_from_retreived_text(text: Text):
    return llm.extract_key_terms_from_retreived_text(text.retrieved_text)


@app.post("/llm/generate_question")
def generate_question(user: User):
    return llm.generate_questions(user)


@app.post("/llm/evaluate_answer")
def evaluate_answer(body: AnswerBody):
    return llm.evaluate_answer(body.question_number, body.user_answer)


@app.post("/transcribe")
async def transcribe_audio(file: UploadFile = File(...)):
    if not file:
        return {"error": "No file uploaded"}

    file_path = "temp_audio.wav"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        text = llm.transcript(file_path)
        return {"text": text}
    except Exception as e:
        return {"error": str(e)}
