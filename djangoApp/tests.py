from django.test import TestCase

import os
import unittest
import json
from manage import main
from models import setup_db, Question, Category

class TriviaTestCase(unittest.TestCase):

    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = main()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}:{}@{}/{}".format('psotgres', '1111', 'localhost:5432', 'trivia')
        setup_db(self.app, self.database_path)

        self.new_question = {
            'question': 'What is the longest waterfall in the world?',
            'answer': 'Niagara',
            'difficulty': 2,
            'category': Category.query.first().id
        }

        with self.app.app_context():
            self.db.init_app(self.app)
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        print("Test Completed! \n")
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    # Check that a list of categories is output.

#--------------------------------------------------------------------------------#
# Get categories
#--------------------------------------------------------------------------------#

    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["categories"])

    def test_get_categories_for_404(self):
        res = self.client().get('/categories/1234/questions')  
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertTrue(data["error"], 404)
        self.assertEqual(data["message"], "Resource not found") 


#--------------------------------------------------------------------------------#
# Create category
#--------------------------------------------------------------------------------#

    def test_create_category(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["categories"])

    # def test_create_category_400(self):
    #     res = self.client().get('/categories') 
    #     data = json.loads(res.data)
    #     self.assertEqual(res.status_code, 400)
    #     self.assertEqual(data["success"], False)
    #     self.assertTrue(data["error"], 400)
    #     self.assertEqual(data["message"], "questions not found")


    def test_create_category(self):
        res = self.client().post('/categories', json={"type": "", "id": 0})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["success"], False)
        self.assertTrue(data["error"], 400)        


#--------------------------------------------------------------------------------#
# Get question
#--------------------------------------------------------------------------------#

    def test_get_question(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["total_questions"])
        self.assertTrue(data["questions"])

    def test_get_question_404(self):
        res = self.client().get('/questions/2389734899348879') 
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertFalse(data["success"])
        self.assertEqual(data["error"], 404)
        self.assertEqual(data["message"], "Resource not found")


#--------------------------------------------------------------------------------#
# Delete question
#--------------------------------------------------------------------------------#

    def test_delete_question(self):
        question = Question.query.first()
        res = self.client().delete('/questions/' + str(question.id))
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["deleted"], question.id)

    def test_404_delete_question(self):
        res = self.client().delete('/questions/2774626262646266376436276336363')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Resource not found")
        print(res.data)


#--------------------------------------------------------------------------------#
# New question
#--------------------------------------------------------------------------------#

    def test_post_new_question(self):
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
  

    def test_post_question_for_400(self):
        res = self.client().post('/questions', json={})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "Bad request")


#--------------------------------------------------------------------------------#
# Search questions
#--------------------------------------------------------------------------------#

    def test_search_questions(self):
        res = self.client().get('/questions', json={'searchTerm':'abc'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["questions"])
        
    
    def test_404_if_search_questions_fails(self):
        res = self.client().post('/questions/search', json={'searchTerm': 'gol'})  
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertTrue(data["error"], 404)
        self.assertTrue(data["message"], "resource not found")


#--------------------------------------------------------------------------------#
# Get questions by category
#--------------------------------------------------------------------------------#

    def test_get_questions_by_category(self):
        res = self.client().get('/questions?/categories/1')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["questions"])


    def test_get_questions_by_category_404(self):
        res = self.client().get('/questions/categories/100')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertTrue(data["error"], 404)
        self.assertTrue(data["message"], "bad request")
    

#--------------------------------------------------------------------------------#
# Play quiz
#--------------------------------------------------------------------------------#

    def test_post_play_quiz(self):
        res = self.client().post('/quizzes', json={
            "previous_questions":[],
            "quiz_category": {"id":0, "type":"All"}
            })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertNotEqual(data["question"], None)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
