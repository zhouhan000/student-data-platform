from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator
from .database import (
    get_all_students,
    add_student_to_db,
    delete_student_by_id,
    find_student_by_id,
    update_student_grade_by_id,
)
from .grading import get_grade


class StudentCreate(BaseModel):
    name: str
    score: float = Field(ge=0, le=100)
    @field_validator("name")
    @classmethod
    def normalize_name(cls,value:str)->str:
        cleaned = value.strip()
        if 0< len(cleaned) <=50:
            return cleaned
        raise ValueError("姓名长度只能在1到50之间")


class StudentUpdate(BaseModel):
    score: float = Field(ge=0, le=100)


class StudentResponse(BaseModel):
    id: int
    name: str
    score: float = Field(ge=0, le=100)
    grade: str


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
    grade = get_grade(student.score)
    student_id = add_student_to_db(
        student.name,
        student.score,
        grade,
    )

    return {
        "id": student_id,
        "name": student.name,
        "score": student.score,
        "grade": grade,
    }

@app.delete("/students/{student_id}", response_model=MessageResponse)
def delete_student(student_id: int):
    deleted = delete_student_by_id(student_id)
    if deleted:
        return {"message": "学生删除成功"}

    raise HTTPException(status_code=404, detail="未找到该学生")

@app.put("/students/{student_id}", response_model=MessageResponse)
def update_student(student_id: int, student: StudentUpdate):
    updated = update_student_grade_by_id(student_id, student.score)
    if updated:
        return {"message": "学生更新成功"}

    raise HTTPException(status_code=404, detail="未找到该学生")

@app.get("/students/stats")
def get_student_stats():
    students = get_all_students()
    total_students = len(students)

    grade_counts = {
        "不及格": 0,
        "及格": 0,
        "良好": 0,
        "优秀": 0,
    }

    if total_students == 0:
        return {
            "total_students": 0,
            "average_score": None,
            "passing_students": 0,
            "pass_rate": None,
            "grade_counts": grade_counts,
        }

    # get_all_students() 的每条记录是 (id, name, score, grade)
    scores = [student[2] for student in students]
    passing_students = sum(score >= 60 for score in scores)

    for score in scores:
        grade_counts[get_grade(score)] += 1

    return {
        "total_students": total_students,
        "average_score": round(sum(scores) / total_students, 2),
        "passing_students": passing_students,
        "pass_rate": round(passing_students / total_students * 100, 2),
        "grade_counts": grade_counts,
    }


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
