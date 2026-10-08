import pytest
from datetime import date


def test_root_endpoint(client):
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["project"] == "Students Database CRUD Application"
    assert data["status"] == "online"


def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


def test_create_student_success(client):
    payload = {
        "student_id": "STU101",
        "name": "Alex Johnson",
        "date_of_birth": "2004-03-15",
        "email": "alex.johnson@example.com",
        "phone": "+1-555-0199",
        "course": "Computer Science",
        "address": "123 University Ave",
        "enrollment_date": "2023-09-01"
    }
    response = client.post("/students", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["student_id"] == "STU101"
    assert data["name"] == "Alex Johnson"
    assert data["email"] == "alex.johnson@example.com"
    assert data["course"] == "Computer Science"
    assert "id" in data
    assert "created_at" in data


def test_create_student_duplicate_id(client):
    payload = {
        "student_id": "STU102",
        "name": "Maria Garcia",
        "date_of_birth": "2005-01-10",
        "email": "maria1@example.com"
    }
    res1 = client.post("/students", json=payload)
    assert res1.status_code == 201

    # Attempt to insert with duplicate student_id
    payload_dup = {
        "student_id": "STU102",
        "name": "Maria Dup",
        "date_of_birth": "2005-01-10",
        "email": "maria2@example.com"
    }
    res2 = client.post("/students", json=payload_dup)
    assert res2.status_code == 400
    assert "already exists" in res2.json()["detail"]


def test_create_student_duplicate_email(client):
    payload = {
        "student_id": "STU103",
        "name": "David Kim",
        "date_of_birth": "2003-07-22",
        "email": "david.kim@example.com"
    }
    res1 = client.post("/students", json=payload)
    assert res1.status_code == 201

    payload_dup = {
        "student_id": "STU104",
        "name": "David Other",
        "date_of_birth": "2003-07-22",
        "email": "david.kim@example.com"
    }
    res2 = client.post("/students", json=payload_dup)
    assert res2.status_code == 400
    assert "already exists" in res2.json()["detail"]


def test_create_student_validation_errors(client):
    # Invalid email
    invalid_email_payload = {
        "student_id": "STU105",
        "name": "John Doe",
        "date_of_birth": "2004-01-01",
        "email": "not-an-email"
    }
    res = client.post("/students", json=invalid_email_payload)
    assert res.status_code == 422

    # Future date of birth
    future_dob_payload = {
        "student_id": "STU106",
        "name": "Future Person",
        "date_of_birth": "2099-01-01",
        "email": "future@example.com"
    }
    res = client.post("/students", json=future_dob_payload)
    assert res.status_code == 422


def test_get_student_by_id_and_custom_id(client):
    payload = {
        "student_id": "STU201",
        "name": "Emma Watson",
        "date_of_birth": "2002-04-15",
        "email": "emma.watson@example.com",
        "course": "Data Science"
    }
    create_res = client.post("/students", json=payload)
    assert create_res.status_code == 201
    created = create_res.json()
    pk_id = created["id"]

    # Retrieve by custom student_id
    res1 = client.get("/students/STU201")
    assert res1.status_code == 200
    assert res1.json()["name"] == "Emma Watson"

    # Retrieve by primary key id
    res2 = client.get(f"/students/{pk_id}")
    assert res2.status_code == 200
    assert res2.json()["student_id"] == "STU201"


def test_get_nonexistent_student(client):
    res = client.get("/students/NON_EXISTENT_ID")
    assert res.status_code == 404


def test_list_students_and_filtering(client):
    # Insert multiple students
    students_to_add = [
        {"student_id": "F1", "name": "Alice Bob", "date_of_birth": "2006-05-10", "email": "alice@filter.com", "course": "Physics"},
        {"student_id": "F2", "name": "Charlie Brown", "date_of_birth": "2004-08-15", "email": "charlie@filter.com", "course": "Computer Science"},
        {"student_id": "F3", "name": "David Copper", "date_of_birth": "2007-02-20", "email": "david@filter.com", "course": "Physics"},
    ]
    for s in students_to_add:
        client.post("/students", json=s)

    # List all
    res = client.get("/students")
    assert res.status_code == 200
    data = res.json()
    assert data["total"] >= 3
    assert len(data["items"]) >= 3

    # Filter by course
    res_course = client.get("/students?course=Physics")
    assert res_course.status_code == 200
    assert all(item["course"] == "Physics" for item in res_course.json()["items"])

    # Search keyword
    res_search = client.get("/students?search=Charlie")
    assert res_search.status_code == 200
    assert any(item["name"] == "Charlie Brown" for item in res_search.json()["items"])

    # Filter born after 2005
    res_dob = client.get("/students?born_after=2005-01-01")
    assert res_dob.status_code == 200
    for item in res_dob.json()["items"]:
        assert date.fromisoformat(item["date_of_birth"]) > date(2005, 1, 1)


def test_update_student_put(client):
    payload = {
        "student_id": "PUT_STU",
        "name": "Initial Name",
        "date_of_birth": "2004-01-01",
        "email": "initial@example.com",
        "course": "Math"
    }
    client.post("/students", json=payload)

    # Full update
    update_payload = {
        "name": "Updated Name",
        "date_of_birth": "2004-02-02",
        "email": "updated@example.com",
        "phone": "+1-888-9999",
        "course": "Advanced Mathematics",
        "address": "456 Updated St",
        "enrollment_date": "2024-01-10"
    }
    res = client.put("/students/PUT_STU", json=update_payload)
    assert res.status_code == 200
    data = res.json()
    assert data["name"] == "Updated Name"
    assert data["email"] == "updated@example.com"
    assert data["course"] == "Advanced Mathematics"
    assert data["phone"] == "+1-888-9999"


def test_patch_student(client):
    payload = {
        "student_id": "PATCH_STU",
        "name": "Sam Original",
        "date_of_birth": "2003-03-03",
        "email": "sam.orig@example.com",
        "course": "Chemistry"
    }
    client.post("/students", json=payload)

    # Partial update - only update course and phone
    patch_payload = {
        "course": "Biochemistry",
        "phone": "+1-222-3333"
    }
    res = client.patch("/students/PATCH_STU", json=patch_payload)
    assert res.status_code == 200
    data = res.json()
    assert data["name"] == "Sam Original"  # Unchanged
    assert data["course"] == "Biochemistry"  # Changed
    assert data["phone"] == "+1-222-3333"  # Changed


def test_delete_student(client):
    payload = {
        "student_id": "DEL_STU",
        "name": "Delete Me",
        "date_of_birth": "2005-05-05",
        "email": "del.me@example.com"
    }
    client.post("/students", json=payload)

    # Verify exists
    res = client.get("/students/DEL_STU")
    assert res.status_code == 200

    # Delete
    del_res = client.delete("/students/DEL_STU")
    assert del_res.status_code == 200
    assert "deleted successfully" in del_res.json()["message"]

    # Verify 404 after deletion
    res_after = client.get("/students/DEL_STU")
    assert res_after.status_code == 404
