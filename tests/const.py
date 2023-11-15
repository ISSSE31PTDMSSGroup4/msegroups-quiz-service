USER_ID = 'testuser@testuser.com'

HTTP_HEADER = {
        'Content-Type': 'application/json',
        'X-USER': USER_ID
    }

NEW_QUIZ_DETAILS = {
        "title": "New Quiz",
        "questions": [
            {
                "index": 1,
                "question": "Which is the greatest fortification in history?",
                "options": [
                    "Great Wall of China",
                    "Machu Picchu",
                    "Chichen Itza",
                    "Colosseum"
                ],
                "answer": "Great Wall of China",
                "explanation": "The Great Wall of China is a historic fortification built to protect against invasions."
            },
            {
                "index": 2,
                "question": "Who was known for research on radioactivity?",
                "options": [
                    "Marie Curie",
                    "Rosalind Franklin",
                    "Jane Goodall",
                    "Dorothy Crowfoot Hodgkin"
                ],
                "answer": "Marie Curie",
                "explanation": "Marie Curie was a pioneering physicist and chemist known for her research on radioactivity."
            }
        ],
        "remark": "It is new quiz"
    }
