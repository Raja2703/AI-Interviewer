/*
  Warnings:

  - Added the required column `questionNumber` to the `Questions` table without a default value. This is not possible if the table is not empty.

*/
-- AlterTable
ALTER TABLE "Questions" ADD COLUMN     "answered" BOOLEAN NOT NULL DEFAULT false,
ADD COLUMN     "questionNumber" INTEGER NOT NULL;
