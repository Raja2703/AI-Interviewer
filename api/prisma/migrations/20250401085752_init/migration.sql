-- CreateTable
CREATE TABLE "Interviews" (
    "id" SERIAL NOT NULL,
    "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "user_id" INTEGER NOT NULL,
    "isCompleted" BOOLEAN NOT NULL DEFAULT false,
    "completedAt" TIMESTAMP(3),

    CONSTRAINT "Interviews_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "Questions" (
    "id" SERIAL NOT NULL,
    "questionText" TEXT NOT NULL,
    "difficulty" TEXT NOT NULL,
    "relevantKeywords" TEXT[],
    "interview_id" INTEGER NOT NULL,
    "userAnswer" TEXT,
    "overallAssessment" TEXT,
    "qualityOfAnswer" TEXT,
    "grammarAndVocabulary" TEXT,
    "constructiveFeedback" TEXT,
    "suggestedAnswer" TEXT,

    CONSTRAINT "Questions_pkey" PRIMARY KEY ("id")
);

-- AddForeignKey
ALTER TABLE "Interviews" ADD CONSTRAINT "Interviews_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "User"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "Questions" ADD CONSTRAINT "Questions_interview_id_fkey" FOREIGN KEY ("interview_id") REFERENCES "Interviews"("id") ON DELETE RESTRICT ON UPDATE CASCADE;
