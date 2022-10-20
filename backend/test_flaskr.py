import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
dotenv_path = os.path.abspath(os.path.dirname(__file__))
load_dotenv(dotenv_path+'/.env') or load_dotenv(dotenv_path)



from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.host= os.getenv('DB_HOST')
        self.port=  os.getenv('DB_PORT')
        self.user = os.getenv('DB_USER')
        self.password= os.getenv('DB_PASSWORD')   
        self.database_name = os.getenv('TEST_DB')
        self.database_path = "postgresql://{}:{}@{}:{}/{}".format(self.user, self.password, self.host, self.port, self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    

        # test get paginated questions

    def test_get_paginated_questions(self):
        res = self.client().get('/questions?page=1')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data ['questions'])

    def test_404_sent_requesting_beyond_valid_page(self):
        res = self.client().get('/questions?page=500')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data ['message'], 'Not found')
    
    new_question = {
        'question': 'How many planets are they?',
        'answer': '8',
        'category': '1',
        'difficulty': 2,
        }
    # test create new question
    def test_create_new_question(self):
        res = self.client().post("/questions", json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["created"])
        self.assertTrue(data["questions"])

    #  test Delete 
    def test_delete_question(self):
        res = self.client().delete("/questions/10")
        data = json.loads(res.data)

        question = Question.query.filter(Question.id == 10).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["deleted"], 10)
        self.assertEqual(question, None)

    def test_422_if_question_is_none(self):
        res = self.client().delete("/questions/0")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "The server was unable to process the request")

     # test get categories
    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])    

# test Search
    def search_question(self):
        res = self.client().post('questions/search', json={"searchTerm": "title"})
        data = json.loads(res.data)

        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])

    def test_400_no_search_term(self):
        res = self.client().post('questions/search')
        data = json.loads(res.data)

        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'], 400)
        self.assertEqual(data["message"], "Bad Request")

        # test get question by category
    def test_get_questions_by_category(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data ['questions'])

    def test_422_category_questions_out_of_range(self):
        res = self.client().get('categories/50000/questions')
        data = json.loads(res.data)

        self.assertEqual(data['error'], 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data["message"], "The server was unable to process the request")

# test Quiz
    def test_questions_to_play_quizz(self):
        questions = {
            'previous_questions':[1, 4, 20, 15],
            'quiz_category': {
                'id': 1,
                'type': 'Science'
            }
        }

        res = self.client().post('/quizzes', json=questions)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])

        self.assertNotEqual(data['question']['id'], 1)
        self.assertNotEqual(data['question']['id'], 4)

        self.assertEqual(data['question']['category'], 1)




# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()