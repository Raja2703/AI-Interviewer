# Interview Helper using AI

**Team Members:**  
- Raja  
- Shazz  
- Monikashri

## 💡 Overview

**Interview Helper using AI** is a web application that helps students practice mock interviews through an AI-driven experience. By leveraging Google Gemini AI, the app creates realistic interview questions based on either the student's uploaded resume or a book of their choice. The system then evaluates the student’s answers and provides detailed feedback to help improve interview performance.

---

## 🚀 Features

- **🔐 College-Based Login**
  - Students log in with their Register Number and Password, validated through the college library database.

- **📄 Resume/Book Upload**
  - Upload a **resume** for key term extraction and domain-based question generation.
  - Optionally upload a **book** and let Gemini AI ask intelligent questions from its content.

- **🧠 AI-Powered Interview**
  - 7–8 questions per session, varying from easy to hard.
  - Students can answer via **text or voice input**.
  - Gemini reads questions aloud in an **interviewer tone** for a real-time experience.

- **📝 Smart Answer Evaluation**
  - Evaluates **grammar**, **relevance**, and offers **suggested improvements**.
  - Provides performance ratings like _Poor, Fair, Good, Excellent, Amazing_.

- **📈 Interview History**
  - Tracks previous interviews.
  - Students can resume incomplete interviews.

- **🔒 Secure Authentication**
  - Uses **JWT** tokens for session management and route protection.

---

## 🛠️ Tech Stack

| Layer     | Technology        |
|-----------|-------------------|
| Frontend  | [Vue.js](https://vuejs.org/)           |
| Backend   | [FastAPI](https://fastapi.tiangolo.com/)        |
| Database  | [PostgreSQL](https://www.postgresql.org/)      |
| ORM       | [Prisma](https://www.prisma.io/)          |
| AI Engine | [Gemini AI](https://deepmind.google/technologies/gemini/)       |
| Auth      | JWT + College Library Database |

---

## 📁 Project Structure (Example)

```bash
interview-helper/
├── client/                # Vue.js frontend
│   └── ...
├── api/                   # FastAPI backend
│   ├── prisma/            # Prisma schema & migrations
│   └── schema.prisma
│   ├── app/
│   ├── routes/
│   ├── models/
│   └── ...

├── README.md
└── .env
```
---  
## ⚙️ Setup Instructions
### 1. Clone the repository
```
git clone https://github.com/your-username/interview-helper.git
cd AI-Interviewer
```
### 2. Setup environment variables
Create a .env file in both client/ and api/ directories with required credentials.

### 3. Install dependencies
- Frontend:
```
cd client
npm install
```
- Backend:
```
cd api
pip install -r requirements.txt
```

### 4. Run the development servers
- Start Frontend:
```
npm run dev
```
- Start Backend:
```
uvicorn main:app --reload
```

### 5. Apply Prisma Migrations
```
cd server
npx prisma migrate dev
```
---
## 📦 TODO / Future Enhancements
 - Add analytics dashboard for student performance
 - Mentor/peer review integration
 - Real-time AI feedback voice response
 - Admin panel for interview question curation

---
## 📄 License
This project is for educational purposes. Licensing information to be added based on team decision.

---
