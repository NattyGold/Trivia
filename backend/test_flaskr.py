import os
import unittest
import json
from urllib import response
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia"
        self.database_path = 'postgresql://{}:{}@{}/{}'.format("postgres","natty","localhost:5432", self.database_name)
        setup_db(self.app, self.database_path)

        self.new_question  ={
            "question": "Who is the best player in the world?",
            "answer": "Christiano Ronaldo",
            "difficulty": 2,
            "category": 6
        }

        self.search_question = {
            "searchTerm": "what is"
        }

        self.invalid_search_question = {
            "searchTerm": "zxexxec ews"
        }

        self.quiz_question = {
                "previous_questions": [1],
                "quiz_category" :{
                    "id": "6",
                    "type": "sports"
                }
        }

        self.invalid_quiz_question = {
                "previous_questions": [10],
                "quiz_category" :{
                    "id": "a",
                    "type": "sports"
                }
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    # def test_paginate_questions(self):
    #     res = self.client().get("/questions")
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertTrue(data['questions'])
    #     self.assertTrue(data['total_questions'])
    #     self.assertTrue(data['categories'])
    
    # def test_404_request_beyound_valid_page(self):
    #     res = self.client().get("/questions?page=1000")
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 404)
    #     self.assertEqual(data['success'], False)
    #     self.assertEqual(data['message'], 'resource not found')

    # def test_get_categories(self):
    #     res = self.client().get("/categories")
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertTrue(data['categories'])
    
    # def test_delete_questions(self):
    #     res = self.client().delete("/questions/5")
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    
    # def test_404_delete_questions_not_found(self):
    #     res = self.client().delete("/questions/1000")
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 404)
    #     self.assertEqual(data['success'], False)
    #     self.assertEqual(data['message'], 'resource not found')

    # def test_create_new_questions(self):
    #     res = self.client().post("/questions", json= self.new_question)
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertTrue(data['created'])
    #     self.assertTrue(data['questions'])
    #     self.assertTrue(data['total_questions'])
    
    # def test_search_question(self):
    #     res = self.client().post("/search", json=self.search_question)
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertTrue(data['questions'])
    #     self.assertTrue(data['total_questions'])
    
    # def test_404_search_question_not_found(self):
    #     res = self.client().post("/search", json= self.invalid_search_question)
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 404)
    #     self.assertEqual(data['success'], False)
    #     self.assertEqual(data['message'], 'resource not found')

    # def test_get_questions_based_category(self):
    #     res = self.client().get("/categories/1/questions")
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertTrue(data['questions'])
    #     self.assertTrue(data['total_questions'])
    #     self.assertTrue(data['current_category'])
    
    # def test_404_get_questions_based_on_category_not_found(self):
    #     res = self.client().get("/categories/1000/questions")
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 404)
    #     self.assertEqual(data['success'], False)
    #     self.assertEqual(data['message'], 'resource not found')
    
    # def test_play_quiz(self):
    #     res = self.client().post("/quizzes", json= self.quiz_question)
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertTrue(data['question'])
    #     self.assertTrue(data['previousQuestions'])
    
    def tesT_404_play_quiz_not_found(self):
        res = self.client().post("/quizzmes", json= self.invalid_search_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
       



# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()