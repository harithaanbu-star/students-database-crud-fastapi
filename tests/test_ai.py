import pytest


def test_ai_query_count_and_filters(client):
    # Seed known students
    students = [
        {"student_id": "AI_1", "name": "Alice Smith", "date_of_birth": "2006-03-01", "email": "ai1@test.com", "course": "Data Science"},
        {"student_id": "AI_2", "name": "Bob Taylor", "date_of_birth": "2002-09-15", "email": "ai2@test.com", "course": "Computer Science"},
        {"student_id": "AI_3", "name": "Charlie Ray", "date_of_birth": "2007-07-20", "email": "ai3@test.com", "course": "Data Science"},
    ]
    for s in students:
        client.post("/students", json=s)

    # 1. Test count question
    res_count = client.post("/ai/query", json={"question": "How many students are there?"})
    assert res_count.status_code == 200
    data_count = res_count.json()
    assert data_count["records_analyzed"] >= 3
    assert "student" in data_count["answer"].lower()

    # 2. Test born after question
    res_born = client.post("/ai/query", json={"question": "List students born after 2005."})
    assert res_born.status_code == 200
    data_born = res_born.json()
    assert "Alice Smith" in data_born["answer"]
    assert "Charlie Ray" in data_born["answer"]
    assert "Bob Taylor" not in data_born["answer"]

    # 3. Test validation on empty question
    res_invalid = client.post("/ai/query", json={"question": ""})
    assert res_invalid.status_code == 422
