from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import llm
from pydantic import BaseModel
from prisma import Prisma

app = FastAPI()
prisma = Prisma()


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


class UserLoginCred(BaseModel):
    username: int
    password: int


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    await prisma.connect()


@app.on_event("shutdown")
async def shutdown():
    await prisma.disconnect()


@app.get("/")
def hello():
    return {"hello": "world"}


@app.get("/user")
async def get_user(username):
    data = await prisma.user.find_unique(where={"username": username})
    return data


@app.post("/login")
async def login(user: UserLoginCred):
    # Fetch users from the database
    userData = await get_user(user.username)

    if userData is None:
        return {"status": "failed", "message": "Incorrect username or password"}

    if user.password == userData.password:
        return {"status": "success", "message": "Login successful!"}

    return {"status": "failed", "message": "Incorrect username or password"}


@app.post("/extract_pdf")
def extract_text_from_pdf(file: UploadFile):
    return llm.extract_text_from_pdf(file.file)


@app.post("/llm/extract_key_terms")
def extract_key_terms_from_retreived_text(text: Text):
    return llm.extract_key_terms_from_retreived_text(text.retrieved_text)


@app.post("/llm/generate_question")
def generate_question(user: User):
    print("hello generator 0")
    return llm.generate_questions(user)


@app.post("/llm/evaluate_answer")
def evaluate_answer(body: AnswerBody):
    return llm.evaluate_answer(body.question_number, body.user_answer)


@app.post("/transcribe")
def transcribe_audio(request):
    if "file" not in request.files:
        return {"error": "No file part"}

    file = request.files["file"]
    if file.filename == "":
        return {"error": "No selected file"}

    # Save the uploaded file temporarily
    file_path = "temp_audio.wav"
    file.save(file_path)

    try:
        text = llm.transcript(file_path)
        return {"text": text}
    except Exception as e:
        return {"error": str(e)}
