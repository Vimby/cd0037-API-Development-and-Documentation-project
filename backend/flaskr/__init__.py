
import os
import sys
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

# Implement pagination
def paginate_questions(request, selection):
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    CORS(app, resource={"/": {"origins": "*"}})
    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Headers', 'GET, POST, PATCH, DELETE, OPTIONS')
        return response
    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    #curl  http://127.0.0.1:5000/categories

    @app.route("/categories", methods=['GET'])
    def get_categories():
        categories = Category.query.order_by(Category.id).all()
        formatted_category = {}
        for category in categories:
            formatted_category[category.id]= category.type
        
        
        return jsonify ({
            'success': True,
             'categories': formatted_category
        })

        

    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    """
   # curl  http://127.0.0.1:5000/questions?page=1
    @app.route("/questions",methods=['GET'])
    def get_questions():
        questions = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request, questions)
        categories=Category.query.all()
        formatted_category = {}
        for category in categories:
            formatted_category[category.id]= category.type
    
           
        if len(current_questions) == 0:
                abort(404)

        return jsonify({
                'success': True,
                'questions': current_questions,
                'total_questions': len(questions),
                 'categories':formatted_category,
                'current_category': None
                
            })


        """
    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.
    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    #curl -X DELETE http://127.0.0.1:5000/questions/30
    @app.route("/questions/<int:question_id>", methods=['DELETE'])
    def delete_questions(question_id):
      try:
        question = Question.query.get(question_id)

        if question is None:
            abort (404)

        question.delete()
        
        return jsonify({
                'success': True,
                 'deleted': question_id
            })

      except:
        abort(422)



    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    #curl -X POST -H "Content-Type: application/json" -d '{"question": "Where do you live", "answer":"Durban", "category": "5", "difficulty": "1"}' http://127.0.0.1:5000/questions
    @app.route("/questions", methods=["POST"])
    def create_question():
       data = request.get_json()

       new_question = data.get("question", None)
       new_answer = data.get("answer", None)
       new_category = data.get("category", None)
       new_difficulty = data.get("difficulty", None)

       try:
           question = Question(question=new_question, answer=new_answer, category=new_category, difficulty=new_difficulty)
           question.insert()

           selection = Question.query.order_by(Question.id).all()
           current_questions = paginate_questions(request, selection)

           return jsonify(
                {
                    "success": True,
                    "created": question.id,
                    "questions": current_questions,
                    "total_questions": len(Question.query.all()),
                }
            )

       except:
            abort(422)



    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """ 
    #curl -X POST -H "Content-Type: application/json" -d '{"searchTerm": "title"}' http://localhost:5000/questions/search
    @app.route("/questions/search", methods=["POST"])
    def search_questions():
        body = request.get_json()
        search_query = body.get("searchTerm" , None)

        try:
         if search_query == '':
           search_result = Question.query.order_by(Question.id).all()
         else:
            search_result = Question.query.order_by(Question.id).filter(Question.question.ilike(f'%{search_query}%')).all()
            limited_questions = paginate_questions(request, search_result)
            current_category = None
            
            return jsonify({
                'success': True, 
                'questions': limited_questions,
                'total_questions': len(search_result),
                'current_category': current_category  
            })
         
         
        except:
          print(sys.exc_info())
          abort(422)

 
    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    # curl  http://127.0.0.1:5000/categories/3/questions
    @app.route("/categories/<int:id>/questions", methods=["GET"])
    def get_questions_by_category(id):
        try:
         category_questions = Question.query.order_by(Question.id).filter(Question.category == id).all()
         current_category_questions = paginate_questions(request, category_questions)
         category= Category.query.get(id)
         
         return jsonify({
                'success': True,
                'questions': current_category_questions,
                'total_questions': len(category_questions),
                'current_category': category.type
            })
         
        except:
            abort(422)

  
    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
#curl -X POST 'http://127.0.0.1:5000/quizzes' -H 'Content-Type: application/json' -d '{"previous_questions": [1, 4, 20, 15], "quiz_category":{"id":"1", "type":"Science"}}'

   
    @app.route('/quizzes', methods=['POST'])
    def questions_to_play_quizz():

        try:
            body = request.get_json()
            #get prev questions
            previous_questions = body.get("previous_questions", None)
            #get category
            quiz_category = body.get("quiz_category", None)
            
             #get questions on the category selected
            if quiz_category['id'] != 0:
              category_qns = Question.query.filter(Question.category== quiz_category['id']).all()
               #if user selected "All" or no category
            else:
              category_qns = Question.query.all()

            #format
            available_ids = [question.id for question in category_qns]

            #generate a random id 
            random_num = random.choice([num for num in available_ids if num not in previous_questions])

            #fetch the random question 
            question = Question.query.filter(Question.id == random_num).one_or_none()

            previous_questions.append(question.id)
           
            return jsonify(
                {
                    'success': True,
                    'question': question.format()
                }
            )
        except:
            abort(404)
   

  
    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(404)
    def not_found(error):
     return jsonify({
        "success": False, 
        "error": 404,
        "message": "Not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
     return jsonify({
        "success": False, 
        "error": 422,
        "message": "The server was unable to process the request"
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
     return jsonify({
        "success": False, 
        "error": 400,
        "message": "Bad Request"
        }), 400 

    @app.errorhandler(500)
    def server_error(error):
     return jsonify({
        "success": False, 
        "error": 500,
        "message": "Internal server error"
        }), 500


    return app

