from fastapi.testclient import TestClient

from app import database
from app.api import app


def test_home():
    client = TestClient(app)
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "API运行正常"}

def test_reject_invalid_score(tmp_path, monkeypatch):
    monkeypatch.setattr(database, "DB_PATH", tmp_path / "students.db")
    database.init_db()
    client = TestClient(app)
    response = client.post("/students",
                           json={
                               "name":"测试学生",
                               "score":200,
                           },

                           )
    assert response.status_code == 422

def test_get_missing_student(tmp_path, monkeypatch):

    monkeypatch.setattr(database, "DB_PATH", tmp_path / "students.db")
    database.init_db()
    client = TestClient(app)
    response = client.get("/students/-1")
    assert response.status_code == 404
    assert response.json() == {"detail":"未找到该学生"}

def test_student_crud(tmp_path, monkeypatch):

    monkeypatch.setattr(database, "DB_PATH", tmp_path / "students.db")
    database.init_db()
    client = TestClient(app)
    student_data = {
        "name":"王五",
        "score":95,
    }
    response = client.post("/students",json=student_data)
    assert response.status_code == 201
    result = response.json()
    assert result["grade"] == "优秀"
    assert result["score"] == 95
    student_id = result["id"]
    assert result["name"] == student_data["name"]
    assert isinstance(result["id"], int), "创建响应的 ID 不是整数"

    get_response = client.get(f"/students/{student_id}")
    assert get_response.status_code == 200
    get_result = get_response.json()
    assert get_result == result

    update_response = client.put(
        f"/students/{student_id}",
        json={"score": 75},
    )
    assert update_response.status_code == 200
    update_result = update_response.json()
    assert update_result == {"message": "学生更新成功"}
    get_response = client.get(f"/students/{student_id}")
    assert get_response.status_code == 200
    get_result = get_response.json()
    assert get_result["score"] == 75
    assert get_result["name"] ==student_data["name"]
    assert get_result["id"] == student_id
    assert get_result["grade"] == "及格"
    update_response = client.put(
        f"/students/{student_id}",
        json={"score":200},
    )
    assert update_response.status_code == 422
    get_response = client.get(f"/students/{student_id}")
    assert get_response.status_code == 200
    get_result = get_response.json()
    assert get_result["score"] == 75
    assert get_result["grade"] == "及格"

    get_response = client.get("/students")
    assert get_response.status_code == 200
    get_result = get_response.json()
    found = False
    for student in get_result:
        if student["id"] == student_id:
            found = True
            break
    assert found, "列表里没有找到刚创建的学生"

    delete_response = client.delete(f"/students/{student_id}")
    assert delete_response.status_code == 200
    delete_result = delete_response.json()
    assert delete_result == {"message":"学生删除成功"}
    get_response = client.get(f"/students/{student_id}")
    assert get_response.status_code == 404
    delete_response = client.delete(f"/students/{student_id}")
    assert delete_response.status_code == 404
    delete_result = delete_response.json()
    assert delete_result == {"detail":"未找到该学生"}
    update_response = client.put(
        f"/students/{student_id}",
        json={"score":100},
    )
    assert update_response.status_code == 404
    update_result = update_response.json()
    assert update_result == {"detail":"未找到该学生"}


    get_response = client.get("/students")
    assert get_response.status_code == 200
    get_result = get_response.json()
    found = False
    for student in get_result:
        if student["id"] == student_id:
            found = True
            break
    assert not found, "删除后，列表里仍然存在该学生"

def test_student_name_trim(tmp_path, monkeypatch):
    monkeypatch.setattr(database, "DB_PATH", tmp_path / "students.db")
    database.init_db()
    client = TestClient(app)
    student_data = {
        "name":" 王 五 ",
        "score":95
    }
    response = client.post("/students",json=student_data)
    assert response.status_code ==201
    result = response.json()
    assert result["name"] == "王 五"
    student_id = result["id"]
    get_response = client.get(f"/students/{student_id}")
    assert get_response.status_code == 200
    get_result = get_response.json()
    assert get_result["name"] == "王 五"

def test_reject_blank_name(tmp_path, monkeypatch):
    monkeypatch.setattr(database, "DB_PATH", tmp_path / "students.db")
    database.init_db()
    client = TestClient(app)
    before = client.get("/students").json()
    student_data = {
        "name": " ",
        "score": 95
    }
    response = client.post("/students", json=student_data)
    assert response.status_code == 422
    after = client.get("/students").json()
    assert after == before

    before = client.get("/students").json()
    student_data = {
        "name": "",
        "score": 95
    }
    response = client.post("/students", json=student_data)
    assert response.status_code == 422
    after = client.get("/students").json()
    assert after == before

def test_student_name_length_boundaries(tmp_path, monkeypatch):
    monkeypatch.setattr(database, "DB_PATH", tmp_path / "students.db")
    database.init_db()
    client = TestClient(app)
    student_data = {
        "name":"王",
        "score":90
    }
    response = client.post("/students", json=student_data)
    assert response.status_code == 201
    result = response.json()

    assert result["name"] == "王"
    student_data = {
        "name": "王"*50,
        "score": 91
    }
    response = client.post("/students", json=student_data)
    assert response.status_code == 201
    result = response.json()
    assert result["name"] == "王"*50

    before = client.get("/students").json()
    student_data = {
        "name": "王"*51,
        "score": 92
    }
    response = client.post("/students", json=student_data)
    assert response.status_code == 422
    after = client.get("/students").json()
    assert after == before

def test_allow_duplicate_student_names(tmp_path, monkeypatch):
    monkeypatch.setattr(database, "DB_PATH", tmp_path / "students.db")
    database.init_db()
    client = TestClient(app)
    student_data1 = {
        "name": "王五",
        "score": 91
    }
    response = client.post("/students", json=student_data1)
    assert response.status_code == 201
    result = response.json()
    id1 = result["id"]
    student_data2 = {
        "name": "王五",
        "score": 93
    }
    response = client.post("/students", json=student_data2)
    assert response.status_code == 201
    result = response.json()
    id2 = result["id"]
    assert id1 != id2
    get_response = client.get(f"/students/{id1}")
    assert get_response.status_code == 200
    get_result = get_response.json()
    assert get_result["name"] == "王五"
    assert get_result["score"] == 91
    get_response = client.get(f"/students/{id2}")
    assert get_response.status_code == 200
    get_result = get_response.json()
    assert get_result["name"] == "王五"
    assert get_result["score"] == 93