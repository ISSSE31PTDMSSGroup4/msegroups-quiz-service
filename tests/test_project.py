from tests import client
import json
from .const import HTTP_HEADER, NEW_QUIZ_DETAILS 

def test_index(client):
    response = client.get('/')
    assert response.status_code == 200

# def test_post_create_quiz(client):
#     response = client.post('/api/quiz/', data=json.dumps(NEW_QUIZ_DETAILS), headers=HTTP_HEADER)

#     response = client.post('/api/quiz/', data=json.dumps(NEW_QUIZ_DETAILS), headers=HTTP_HEADER)
#     assert response.status_code == 200

# def test_get_list_of_quizzes(client):
#     response = client.get('/api/quiz/list/', headers=HTTP_HEADER)
#     assert response.status_code == 200

# def test_get_quiz_detail(client):
#     response = client.get('/api/quiz/list/', headers=HTTP_HEADER)
#     quiz = response.json[0]
#     quiz_id = quiz['quiz_id']

#     response = client.get(f"/api/quiz/detail/?quiz_id={quiz_id}", headers=HTTP_HEADER)
#     assert response.status_code == 200
    
# def test_put_quiz_update(client):
#     response = client.get('/api/quiz/list/', headers=HTTP_HEADER)
#     quiz = response.json[0]
#     quiz_id = quiz['quiz_id']

#     request_body = {
#         "quiz_id" : quiz_id,
#         "title"   : "This is new quiz title"
#     }

#     response = client.put("/api/quiz/", data=json.dumps(request_body), headers=HTTP_HEADER)
#     assert response.status_code == 200

# def test_delete_quiz(client):
#     response = client.get('/api/quiz/list/', headers=HTTP_HEADER)
#     quiz = response.json[1]
#     quiz_id = quiz['quiz_id']

#     request_body = {
#         "quiz_id" : quiz_id,
#     }

#     response = client.delete("/api/quiz/", data=json.dumps(request_body), headers=HTTP_HEADER)
#     assert response.status_code == 200

# def test_post_create_question(client):
#     response = client.get('/api/quiz/list/', headers=HTTP_HEADER)
#     quiz = response.json[0]
#     quiz_id = quiz['quiz_id']

#     add_question = {
#         "quiz_id": quiz_id,
#         "index": 3,
#         "question": "Which is the largest city in the United States?",
#         "options": [
#             "New York",
#             "Los Angeles",
#             "Chicago",
#             "Houston"
#         ],
#         "answer": "New York",
#         "explanation": "New York is the largest city in the United States by population."
#     }

#     response = client.post("/api/quiz/question/", data=json.dumps(add_question), headers=HTTP_HEADER)
#     assert response.status_code == 200

# def test_put_modify_question(client):
#     response = client.get('/api/quiz/list/', headers=HTTP_HEADER)
#     quiz = response.json[0]
#     quiz_id = quiz['quiz_id']

#     add_question = {
#         "quiz_id": quiz_id,
#         "index": 0,
#         "question": "Which is the largest city in the United States?",
#         "options": [
#             "New York",
#             "Los Angeles",
#             "Chicago",
#             "Houston"
#         ],
#         "answer": "New York",
#         "explanation": "New York is the largest city in the United States by population."
#     }
#     client.post("/api/quiz/question/", data=json.dumps(add_question), headers=HTTP_HEADER)

#     response = client.get(f"/api/quiz/detail/?quiz_id={quiz_id}", headers=HTTP_HEADER)
#     quiz = response.json
#     question_id = quiz['questions'][0]['question_id']

#     modify_question = {
#         "quiz_id": quiz_id,
#         "question_id": question_id,
#         "question": "Which is the largest country in the world?",
#         "options": [
#             "Russia",
#             "Austrlia",
#             "Africa",
#             "United States of America"
#         ],
#         "answer": "Russia",
#         "explanation": "The rest are continents, not countries."
#     }
#     response = client.put("/api/quiz/question/", data=json.dumps(modify_question), headers=HTTP_HEADER)
#     assert response.status_code == 200

# def test_delete_question(client):
#     response = client.get('/api/quiz/list/', headers=HTTP_HEADER)
#     quiz = response.json[0]
#     quiz_id = quiz['quiz_id']

#     add_question = {
#         "quiz_id": quiz_id,
#         "index": 0,
#         "question": "Which is the largest city in the United States?",
#         "options": [
#             "New York",
#             "Los Angeles",
#             "Chicago",
#             "Houston"
#         ],
#         "answer": "New York",
#         "explanation": "New York is the largest city in the United States by population."
#     }
#     client.post("/api/quiz/question/", data=json.dumps(add_question), headers=HTTP_HEADER)

#     response = client.get(f"/api/quiz/detail/?quiz_id={quiz_id}", headers=HTTP_HEADER)
#     quiz = response.json
#     question_id = quiz['questions'][0]['question_id']

#     request_body = {
#         "quiz_id": quiz_id,
#         "question_id": question_id
#     }

#     response = client.delete("/api/quiz/question/", data=json.dumps(request_body), headers=HTTP_HEADER)
#     assert response.status_code == 200