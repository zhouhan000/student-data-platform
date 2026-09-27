import sys
from pathlib import Path

from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "第一章"))
from api import app


def test_home():
    client = TestClient(app)
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "API运行正常"}

def test_reject_invalid_score():
    client = TestClient(app)
    response = client.post("/students",
                           json={
                               "name":"测试学生",
                               "score":200,
                               "grade":"测试",
                           },

                           )
    assert response.status_code == 422

def test_get_missing_student():
    client = TestClient(app)
    response = client.get("/students/-1")
    assert response.status_code == 404
    assert response.json() == {"detail":"未找到该学生"}

def test_student_crud(tmp_path, monkeypatch):
    import database

    monkeypatch.setattr(database, "DB_PATH", tmp_path / "students.db")
    database.init_db()
    client = TestClient(app)
    response = client.post(
        "/students",
        json={"name": "王五", "score": 88, "grade": "良好"},
    )

    assert response.status_code == 201
    assert response.json()["name"] == "王五"
    assert isinstance(response.json()["id"], int)
    student_id = response.json()["id"]
    get_response = client.get(f"/students/{student_id}")

    list_response = client.get("/students")
    assert list_response.status_code == 200
    assert any(
        student["id"] == student_id
        for student in list_response.json()
    )

    assert get_response.status_code == 200
    assert get_response.json() == response.json()
    update_response = client.put(
        f"/students/{student_id}",
        json={"score": 92, "grade": "优秀"},
    )

    assert update_response.status_code == 200

    updated_student = client.get(f"/students/{student_id}")
    assert updated_student.json()["score"] == 92
    assert updated_student.json()["grade"] == "优秀"
    invalid_update = client.put(
        f"/students/{student_id}",
        json={"score": 200, "grade": "优秀"},
    )

    assert invalid_update.status_code == 422

    student_after_rejection = client.get(f"/students/{student_id}")
    assert student_after_rejection.json()["score"] == 92

    delete_response = client.delete(f"/students/{student_id}")
    assert delete_response.status_code == 200

    missing_response = client.get(f"/students/{student_id}")
    assert missing_response.status_code == 404

    second_delete_response = client.delete(f"/students/{student_id}")
    assert second_delete_response.status_code == 404

    list_after_delete = client.get("/students")
    assert all(
        student["id"] != student_id
        for student in list_after_delete.json()
    )

    missing_update = client.put(
        f"/students/{student_id}",
        json={"score": 75, "grade": "良好"},
    )

    assert missing_update.status_code == 404
    assert missing_update.json() == {"detail": "未找到该学生"}