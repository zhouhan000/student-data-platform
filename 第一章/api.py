from fastapi import FastAPI, HTTPException
from database import (
    get_all_students,
    add_student_to_db,
    delete_student_by_id,
    find_student_by_id,
    update_student_grade_by_id,
)
from pydantic import BaseModel, Field

class StudentBase(BaseModel):
    name: str
    score: float = Field(ge=0, le=100)
    grade: str


class StudentCreate(StudentBase):
    pass


class StudentUpdate(BaseModel):
    score: float = Field(ge=0, le=100)
    grade: str

class StudentResponse(StudentCreate):
    id: int

class MessageResponse(BaseModel):
    message: str
app = FastAPI(title="学生管理系统 API")

@app.get("/", response_model=MessageResponse)
def home():
    return {"message": "API运行正常"}
@app.get("/students", response_model=list[StudentResponse])
def list_students():
    students = get_all_students()
    return [
        {
            "id": student_id,
            "name": name,
            "score": score,
            "grade": grade,
        }
        for student_id, name, score, grade in students
    ]

@app.post(
    "/students",
    status_code=201,
    response_model=StudentResponse,
)
def create_student(student: StudentCreate):
    student_id = add_student_to_db(
        student.name,
        student.score,
        student.grade
    )

    return {
        "id": student_id,
        "name": student.name,
        "score": student.score,
        "grade": student.grade,
    }
@app.delete("/students/{student_id}",response_model=MessageResponse)
def delete_student(student_id: int):
    deleted = delete_student_by_id(student_id)
    if deleted:
        return {"message": "学生删除成功"}

    raise HTTPException(status_code=404, detail="未找到该学生")

@app.put("/students/{student_id}",response_model=MessageResponse)
def update_student(student_id:int,student: StudentUpdate):
    updated = update_student_grade_by_id(student_id,student.score, student.grade)
    if updated:
        return {"message":"学生更新成功"}

    raise HTTPException(status_code=404, detail="未找到该学生")

@app.get(
    "/students/{student_id}",
    response_model=StudentResponse,
)
def find_student(student_id: int):
    student = find_student_by_id(student_id)

    if not student:
        raise HTTPException(status_code=404, detail="未找到该学生")

    student_id, name, score, grade = student

    return {
        "id": student_id,
        "name": name,
        "score": score,
        "grade": grade,
    }