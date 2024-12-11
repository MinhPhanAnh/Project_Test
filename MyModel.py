from pydantic import BaseModel
from utils import clean_text
import streamlit as st
from openai import OpenAI
import os
import json

# Access the OpenAI API key
api_key = st.secrets["general"]["OPENAI_API_KEY"]

# Khởi tạo OpenAI client
client = OpenAI(api_key=api_key)

if not api_key:
    raise ValueError("API key không được cung cấp!")

client = OpenAI(api_key=api_key)

class QuizSample(BaseModel):
    question: str
    choices: list[str]
    answer: str

class Exam(BaseModel):
    quizes: list[QuizSample]

class BaseExtracter():
    def __init__(self):
        self.model_name = "gpt-4o"

    @staticmethod
    def ensure_unique_questions(questions):
        """Loại bỏ các câu hỏi trùng lặp dựa trên nội dung câu hỏi."""
        seen = set()
        unique_questions = []
        for q in questions:
            if q["question"] not in seen:
                seen.add(q["question"])
                unique_questions.append(q)
        return unique_questions

class ExtractA(BaseExtracter):
    def run(self, _input, num_questions):
        try:
            completion = client.beta.chat.completions.parse(
                model=self.model_name,
                messages=[
                    {
                        "role": "system",
                        "content": f"""
                            TASK: Extract {num_questions} questions of level A difficulty. 
                            Questions test your ability to remember and recognize information.
                            Direct question format, asking to select the correct information.
                            The answer is clear, not confusing.
                            Provide the output in the format of a list of dictionaries: 
                            question (text), choices (list of 4 options: A, B, C, D), and answer (correct answer).
                            RULE: Use Vietnamese for all questions, choices, and answers.
                            """
                    },
                    {
                        "role": "user",
                        "content": f"base on this document: {clean_text(_input)}"
                    },
                ],
                response_format=Exam,
            )
            res = json.loads(completion.choices[0].message.content)
            # Loại bỏ tiền tố "A.", "B.",... nếu có
            for quiz in res["quizes"]:
                quiz["choices"] = [choice.split(".", 1)[1].strip() if "." in choice else choice.strip() for choice in quiz["choices"]]
            print("Debug choices (trước khi làm sạch):", res["quizes"])
            res["quizes"] = BaseExtracter.ensure_unique_questions(res["quizes"])
            for i in range(len(res["quizes"])):
                res["quizes"][i]["level"] = "Nhận biết"
            return res
        except Exception as e:
            print(f"Lỗi khi xử lý: {e}")
            return {"quizes": []}

class ExtractB(ExtractA):
    def run(self, _input, num_questions):
        try:
            completion = client.beta.chat.completions.parse(
                model=self.model_name,
                messages=[
                    {
                        "role": "system",
                        "content": f"""
                            TASK: Extract {num_questions} questions of level B difficulty. 
                            Questions not only identify or repeat knowledge but also understand its nature and relationships.
                            The answer requires basic reasoning or comparison based on learned knowledge.
                            Provide the output in the format of a list of dictionaries: 
                            question (text), choices (list of 4 options: A, B, C, D), and answer (correct answer).
                            RULE: Use Vietnamese for all questions, choices, and answers.
                            """
                    },
                    {
                        "role": "user",
                        "content": f"base on this document: {clean_text(_input)}"
                    },
                ],
                response_format=Exam,
            )
            res = json.loads(completion.choices[0].message.content)
            for quiz in res["quizes"]:
                quiz["choices"] = [choice.split(".", 1)[1].strip() if "." in choice else choice.strip() for choice in quiz["choices"]]
            print("Debug choices (trước khi làm sạch):", res["quizes"])
            res["quizes"] = BaseExtracter.ensure_unique_questions(res["quizes"])
            for i in range(len(res["quizes"])):
                res["quizes"][i]["level"] = "Thông hiểu"
            return res
        except Exception as e:
            print(f"Lỗi khi xử lý: {e}")
            return {"quizes": []}

class ExtractC(ExtractA):
    def run(self, _input, num_questions):
        try:
            completion = client.beta.chat.completions.parse(
                model=self.model_name,
                messages=[
                    {
                        "role": "system",
                        "content": f"""
                            TASK: Extract {num_questions} questions of level C difficulty. 
                            Questions require applying knowledge to specific situations or exercises.
                            Real or hypothetical situation, with facts to make inferences.
                            The answer requires calculation or inference from knowledge.
                            Provide the output in the format of a list of dictionaries: 
                            question (text), choices (list of 4 options: A, B, C, D), and answer (correct answer).
                            RULE: Use Vietnamese for all questions, choices, and answers.
                            """
                    },
                    {
                        "role": "user",
                        "content": f"base on this document: {clean_text(_input)}"
                    },
                ],
                response_format=Exam,
            )
            res = json.loads(completion.choices[0].message.content)
            for quiz in res["quizes"]:
                quiz["choices"] = [choice.split(".", 1)[1].strip() if "." in choice else choice.strip() for choice in quiz["choices"]]
            print("Debug choices (trước khi làm sạch):", res["quizes"])
            res["quizes"] = BaseExtracter.ensure_unique_questions(res["quizes"])
            for i in range(len(res["quizes"])):
                res["quizes"][i]["level"] = "Vận dụng"
            return res
        except Exception as e:
            print(f"Lỗi khi xử lý: {e}")
            return {"quizes": []}

class ExtractD(ExtractA):
    def run(self, _input, num_questions):
        try:
            completion = client.beta.chat.completions.parse(
                model=self.model_name,
                messages=[
                    {
                        "role": "system",
                        "content": f"""
                            TASK: Extract {num_questions} questions of level D difficulty. 
                            Require students to apply knowledge and creativity to solve complex or new problems.
                            Questions often contain real-life or interdisciplinary situations.
                            The answer requires analyzing the situation or creating a solution.
                            Provide the output in the format of a list of dictionaries: 
                            question (text), choices (list of 4 options: A, B, C, D), and answer (correct answer).
                            RULE: Use Vietnamese for all questions, choices, and answers.
                            """
                    },
                    {
                        "role": "user",
                        "content": f"base on this document: {clean_text(_input)}"
                    },
                ],
                response_format=Exam,
            )
            res = json.loads(completion.choices[0].message.content)
            for quiz in res["quizes"]:
                quiz["choices"] = [choice.split(".", 1)[1].strip() if "." in choice else choice.strip() for choice in quiz["choices"]]
            print("Debug choices (trước khi làm sạch):", res["quizes"])
            res["quizes"] = BaseExtracter.ensure_unique_questions(res["quizes"])
            for i in range(len(res["quizes"])):
                res["quizes"][i]["level"] = "Vận dụng cao"
            return res
        except Exception as e:
            print(f"Lỗi khi xử lý: {e}")
            return {"quizes": []}

class ExamOneChain():
    def run(self, text, com=[]):
        print("INPUT: ", text, "\n", "---------" * 20)
        for x in com:
            res = x().run(text)
            for quiz in res['quizes']:
                print("question:", quiz["question"])
                print("choices:", quiz["choices"])
                print("answer:", quiz["answer"])
                print("level:", quiz["level"])
                print("\n")
