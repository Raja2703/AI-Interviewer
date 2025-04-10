from pydantic import BaseModel
from pypdf import PdfReader
from google import genai
import json
from fastapi import UploadFile
from dotenv import load_dotenv
import os, io

load_dotenv()

client = genai.Client(api_key=os.getenv("API_KEY"))


class User(BaseModel):
    name: str
    career_domain: str
    skills: list
    experience_years: str


def generate_questions(user: User):
    prompt = f"""
    You are an experienced interview coach. Generate 5-7 interview questions in JSON format based on:
    - Candidate Name: {user.name}
    - Job Role: {user.career_domain}
    - Years of Experience: {user.experience_years}
    - Resume Keywords: {user.skills}

    Questions should progress from simple to advanced. Output JSON only.
    The output json should be able to be loaded in python using the method json.loads().
    format example:
    {{
    "candidateName": "{user.name}",
    "jobRole": "{user.career_domain}",
    "yearsOfExperience": years of experience in number,
    "resumeKeywords": {user.skills},
    "questions": [
        {{
        "questionNumber": 1,
        "questionText": "Question text here.  (Basic level question based on keywords and role)",
        "difficulty": "basic",
        "relevantKeywords": ["keyword1", "keyword2"]
        }},
        {{
        "questionNumber": 2,
        "questionText": "Question text here. (More specific question based on role and experience)",
        "difficulty": "intermediate",
        "relevantKeywords": ["keyword2", "keyword3"]
        }},
        {{
        "questionNumber": 3,
        "questionText": "Question text here. (Situational question, requires candidate to apply skills)",
        "difficulty": "intermediate",
        "relevantKeywords": ["keyword1"]
        }},
        {{
        "questionNumber": 4,
        "questionText": "Question text here. (Technical question, especially for technical roles)",
        "difficulty": "advanced",
        "relevantKeywords": ["keyword3"]
        }},
        {{
        "questionNumber": 5,
        "questionText": "Question text here. (Behavioral question, STAR method)",
        "difficulty": "intermediate",
        "relevantKeywords": ["keyword2"]
        }},
        {{
        "questionNumber": 6,
        "questionText": "Question text here. (Open-ended question about career goals)",
        "difficulty": "intermediate",
        "relevantKeywords": []
        }},
        {{
        "questionNumber": 7,
        "questionText": "Question text here. (Question testing for problem-solving)",
        "difficulty": "advanced",
        "relevantKeywords": ["keyword1","keyword3"]
        }}
    ]
    }}
    """
    response = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
    response_json = clean_json(response.text)
    return json.loads(response_json)


def generate_questions_from_book(book_content: str):
    prompt = f"""
    Generate 12 interview questions based on the content within the text variable {book_content}, covering the following aspects:
    * 3 questions about the foundational principles and underlying theories presented.
    * 3 questions exploring specific concepts, models, or frameworks detailed in the text.
    * 3 questions focusing on the practical applications and any real-world examples mentioned.
    * 3 questions discussing potential limitations, challenges, or areas for further research or understanding related to this content.
    
    Questions should progress from simple to advanced. Output JSON only.
    The output json should be able to be loaded in python using the method json.loads().
    format example:
    {{
    "questions": [
        {{
        "questionNumber": question_number here,
        "questionText": "Question text here.  (question type)",
        "difficulty": "difficulty level here,
        "relevantKeywords": ["keyword1", "keyword2"]
        }}
    ]
    }}
    """
    response = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
    response_json = clean_json(response.text)
    return json.loads(response_json)


def extract_key_terms_from_retreived_text(retreived_text: str):
    prompt = f"""{retreived_text}. From the above retreived text, extract the person's name, career domain, his/her 
    experience in the particular domain(number of years) for example 2 years, his/her skills. skills must be an array
    
    Return the output strictly in JSON format:
    {{
        "name": "Raja",
        "career_domain": "Identified career field (e.g., Software Engineering, Data Science, Marketing, etc.)",
        "skills": ["list of key skills extracted from resume"],
        "experience_years": "(number of years) for example 2 years"
    }}
    """

    response = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
    response_json = clean_json(response.text)
    return json.loads(response_json)


def extract_text_from_pdf(file: UploadFile):
    # Read the file into memory
    contents = file.file.read()

    # Convert to BytesIO for PdfReader
    reader = PdfReader(io.BytesIO(contents))

    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""

    return text


def clean_json(json_str):
    start = 0
    end = 0
    for idx, char in enumerate(json_str):
        if char == "{":
            start = idx
            break
    for idx, char in enumerate(json_str[::-1]):
        if char == "}":
            end = len(json_str) - idx
            break
    return json_str[start:end]


def evaluate_answer(questions_details, user_answer):
    prompt = f"""
    Evaluate the candidate's answer to question {questions_details}. Provide feedback in JSON format with:
    - Overall assessment (Excellent, Good, Fair, Poor)
    - Quality of answer (Strengths and weaknesses)
    - Grammar and vocabulary
    - Constructive feedback (How to improve)
    - Suggested answer (Best way to answer)

    User's answer: "{user_answer}"

    After the user provides an answer to a question, you will evaluate the answer and provide feedback in the following JSON format:

    {{
    "questionNumber": "Number",
    "userAnswer": "The candidate's answer text",
    "feedback": {{
        "overallAssessment": "Excellent, Good, Fair, Poor",
        "qualityOfAnswer": "Detailed explanation of strengths and weaknesses of the answer content.  Did the answer directly address the question?  Was the answer concise and relevant?",
        "grammarAndVocabulary": "Feedback on grammar, vocabulary, and clarity.  Identify specific areas for improvement.",
        "constructiveFeedback": "Specific and actionable advice on how the candidate could improve their answer.  Include examples.",
        "suggestedAnswer": "A model answer that the candidate can use as a guide.  This should be a concise, well-structured answer that directly addresses the question and incorporates relevant keywords."
    }}
    }}
    questionNumber: The number of the question being evaluated.
    userAnswer: The verbatim text of the candidate's answer.
    feedback: A JSON object containing detailed feedback:
    overallAssessment: A summary assessment (Excellent, Good, Fair, Poor).
    qualityOfAnswer: A detailed assessment of the content of the answer. Does it address the question directly? Is it accurate and relevant? Does it demonstrate the necessary skills and experience?
    grammarAndVocabulary: Feedback on grammar, vocabulary, and clarity.
    constructiveFeedback: Specific advice on how to improve the answer.
    suggestedAnswer: A model answer. This MUST be tailored to the question and the candidate's profile (as represented by the resume keywords, job role, and experience level).

    Important Considerations:
    Relevance: Ensure all questions and feedback are directly related to the resume keywords, job role, and years of experience.
    Specificity: Constructive feedback should be specific and actionable. Avoid vague statements.
    Accuracy: The suggested answers should be accurate and well-structured.
    Tone: Maintain a professional and encouraging tone throughout.
    STAR Method: Encourage the use of the STAR method (Situation, Task, Action, Result) when answering behavioral questions.

    Return only JSON output.
    """
    response = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
    response_json = clean_json(response.text)
    return json.loads(response_json)


# name = "Shazz"
# role = "Software Engineer"
# exp = "0 years"
# keywords = [
#     "Python",
#     "Golang",
#     "adonisjs",
#     "AWS",
#     "communication skills",
#     "problem-solving",
# ]

# text = extract_key_terms_from_retreived_text()
# name = text["name"]
# role = text["career_domain"]
# exp = text["experience_years"]
# keywords = text["skills"]

# questions = generate_questions(name, role, exp, keywords)

# for q in questions["questions"]:
#     print(f"\nQuestion {q['questionNumber']}: {q['questionText']}")
#     user_answer = input("\nYour Answer: ")

#     print("\nEvaluating answer...")

#     feedback = evaluate_answer(q["questionNumber"], user_answer)
#     print("\nFeedback:")
#     print(json.dumps(feedback, indent=2))
