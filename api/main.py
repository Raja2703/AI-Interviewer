import json
from fastapi import FastAPI, HTTPException, Response, UploadFile, Request
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
    question_number: int
    question_details: str
    user_answer: str


class UserLogin(BaseModel):
    username: int
    password: str


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
async def get_user(user_id: int):
    data = await prisma.user.find_unique(where={"username": user_id})
    return data


@app.post("/login")
async def login(user: UserLogin, response: Response):
    user_data = await get_user(user.username)

    if not user_data or str(user_data.password) != str(user.password):
            return {"status":"failed","message": "Invalid Credentials"}
    else:   
            response.set_cookie(key="user_id", value=str(user_data.username))
            return {"status":"success","message": "Login successful"}


@app.post("/extract_pdf")
def extract_text_from_pdf(file: UploadFile):
    return llm.extract_text_from_pdf(file.file)


@app.post("/llm/extract_key_terms")
def extract_key_terms_from_retreived_text(text: Text):
    return llm.extract_key_terms_from_retreived_text(text.retrieved_text)


@app.post("/llm/generate_question")
async def generate_question(body: User, request: Request):
    user_id = int(request.cookies.get("user_id"))
    if not user_id:
        raise HTTPException(status_code=400, detail="User ID missing in cookies")
    user_details = await get_user(user_id)
    if not user_details:
        raise HTTPException(status_code=400, detail="User not found")
    
    generated_data = llm.generate_questions(body)

    interview = await prisma.interviews.create(
        data={
            "user_id": user_details.id,
            "isCompleted": False,
            "completedAt": None 
        }
    )

    for q in generated_data["questions"]:
        await prisma.questions.create(
            data={
                "questionNumber": q["questionNumber"],
                "questionText": q["questionText"],
                "difficulty": q["difficulty"],
                "relevantKeywords": q["relevantKeywords"],
                "interview_id": interview.id,
            }
        )
    
    interview_with_questions = await prisma.interviews.find_unique(
        where={"id": interview.id},
        include={"questions": True}
    )
    
    return interview_with_questions

@app.get("/user/latest_interview")
async def get_most_recent_interview_questions(request: Request):
    user_id = int(request.cookies.get("user_id"))
    if not user_id:
        raise HTTPException(status_code=400, detail="User ID missing in cookies")
    user_details = await get_user(user_id)
    if not user_details:
        raise HTTPException(status_code=400, detail="User not found")
    
    interview = await prisma.interviews.find_first(
        where={"user_id": user_details.id},
        order={"created_at": "desc"} 
    )
    
    if not interview:
        return {"message": "No interviews found for the user."}
    
    questions = await prisma.questions.find_many(
        where={"interview_id": interview.id}
    )
    
    if not questions:
        return {"message": "No questions found for the most recent interview."}
    
    return {
        "interview": interview,
        "questions": questions
    }

@app.get("/user/{interview_id}")
async def get_interview(request: Request, interview_id: int):
    user_id = int(request.cookies.get("user_id"))
    if not user_id:
        raise HTTPException(status_code=400, detail="User ID missing in cookies")
    
    user_details = await get_user(user_id)
    if not user_details:
        raise HTTPException(status_code=400, detail="User not found")

    interview = await prisma.interviews.find_first(
        where={
            "user_id": user_details.id,
            "id": interview_id 
        },
        order={"created_at": "desc"} 
    )

    if not interview:
        raise HTTPException(status_code=404, detail="Interview not found or does not belong to the user.")

    questions = await prisma.questions.find_many(
        where={"interview_id": interview.id}
    )

    unanswered_question = next((q for q in questions if not q.answered), None)
    
    if not questions:
        return {"message": "No questions found for the interview."}
    
    return {
        "interview": interview,
        "questions": questions,
        "nextQuestion": unanswered_question
    }

@app.post("/llm/evaluate_answer/{interview_id}")
async def evaluate_answer(body: AnswerBody, request: Request, interview_id: int):
    user_id = int(request.cookies.get("user_id"))
    if not user_id:
        raise HTTPException(status_code=400, detail="User ID missing in cookies")
    user_details = await get_user(user_id)
    if not user_details:
        raise HTTPException(status_code=400, detail="User not found")

    interview = await prisma.interviews.find_first(
        where={"user_id": user_details.id, "id": interview_id}
    )
    if not interview:
        raise HTTPException(status_code=404, detail="Interview not found or does not belong to the user.")
    
    question = await prisma.questions.find_first(
        where={"interview_id": interview.id, "questionNumber": body.question_number}
    )
    if not question:
        raise HTTPException(status_code=404, detail="Invalid Question")
    
    feedback = llm.evaluate_answer(body.question_details, body.user_answer)
    
    updated_question = await prisma.questions.update(
        where={"id": question.id},
        data={
            "overallAssessment": feedback["feedback"]["overallAssessment"],
            "qualityOfAnswer": feedback["feedback"]["qualityOfAnswer"],
            "grammarAndVocabulary": feedback["feedback"]["grammarAndVocabulary"],
            "constructiveFeedback": feedback["feedback"]["constructiveFeedback"],
            "suggestedAnswer": feedback["feedback"]["suggestedAnswer"],
            "userAnswer": body.user_answer
        }
    )
    
    # Return updated question with feedback
    return {"message": "Answer evaluated and question updated successfully", "question": updated_question}


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
