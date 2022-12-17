import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate_questions(request, selection):
    page = request.args.get("page",1,type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions
    
def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    cors = CORS(app, resources = {r"/api/*" :{"origins": "*"}})

   

    #CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type, Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response
    
    #----------------------------------------------------------------------------#
    # Get all categories
    #----------------------------------------------------------------------------#

    #This is an endpoint to handle GET requests for all available categories.
    @app.route("/categories")
    def get_categories():
        # Query to get all categories from the trivia database
    
        categories = Category.query.all()

        formatted_categories = {category.id : category.type for category in categories}

        if len(categories) == 0:
            abort(404)

        return jsonify({
           "success": True,
           "categories": formatted_categories
        })


    #----------------------------------------------------------------------------#
    # Get all questions
    #----------------------------------------------------------------------------#


    #This is an endpoint to handle GET requests for all available questions.
    @app.route("/questions")
    def get_questions():
        
        # Query to get all questions from the trivia database
        selection = Question.query.order_by(Question.id).all()

        #Statement to display current questions in a page that is 10questions per page
        current_questions = paginate_questions(request, selection)

        if (len(current_questions) == 0):
            abort(404)
        
        # Get the total length of questions from the trivia database: 
        total_questions = len(selection)

        # Query to get all categories from the trivia database
        categories = Category.query.all()

        formatted_categories = {category.id : category.type for category in categories}

        # if no error returns the following
        return jsonify({
            "success": True,
            "questions": current_questions,
            "total_questions": total_questions,
            "categories": formatted_categories
        })

        #----------------------------------------------------------------------------#
    # Delete Question
    #----------------------------------------------------------------------------#

    #This is an endpoint to DELETE question using a question ID
    @app.route("/questions/<int:id>", methods=["DELETE"])
    def delete_question(id):
        try:
            question = Question.query.filter(Question.id == id).one_or_none()

            if question is None:
                abort(404)
            
            question.delete()
            selection = Question.query.order_by(Question.id).all()
            current_questions = paginate_questions(request, selection)

            return jsonify({
                "success": True,
                "delete": id,
                "questions": current_questions,
                "total_questions": len(Question.query.all())
                })

        # An idea gotten from udacity full stack channel, question asked by kinason
        except Exception:
                abort(422) 

    #----------------------------------------------------------------------------#
    # Create Question
    #----------------------------------------------------------------------------#

    #This is an endpoint to add new questions to the database using the POST method
    @app.route("/questions", methods=["POST"])
    def create_questions():

        body = request.get_json()

        new_question = body.get("question", None)
        new_answer = body.get("answer", None)
        new_difficulty = body.get("difficulty", None)
        new_category = body.get("category", None)

        try:
            question = Question(question = new_question,answer = new_answer,difficulty = new_difficulty,category = new_category)

            question.insert()

            selection = Question.query.order_by(Question.id).all()
            current_questions = paginate_questions(request,selection)

            return jsonify({
                "success": True,
                "created": question.id,
                "questions": current_questions,
                "total_questions": len(Question.query.all())
            })
        
        except:
            abort(422)

    #----------------------------------------------------------------------------#
    # Search Question
    #----------------------------------------------------------------------------#
    
    #This is an endpoint to search for any questions with the POST method
    @app.route("/search", methods=["POST"])
    def search_question():
        body = request.get_json()

        search = body.get("searchTerm", None)

        
        search_question = Question.query.filter(
        Question.question.ilike("%{}%".format(search)))   
        
        current_questions = [question.format() for question in search_question]

        
        if current_questions == []:
            abort(404)
        
        else: 
            return jsonify({
                "success": True,
                "questions":current_questions,
                "total_questions": len(search_question.all()),
                "current_category": None
            })
    
        

    #----------------------------------------------------------------------------#
    # Get Questions for Category
    #----------------------------------------------------------------------------#

    #This is an endpoint to handle GET requests for display questions for each category.
    @app.route("/categories/<int:category_id>/questions")
    def get_questions_based_on_category(category_id):
    

        # Query to get all questions based on category from the trivia database
        select_questions = Question.query.order_by(Question.id).filter(Question.category == category_id)

        #Statement to display current category in a page that is 10questions per page
        current_category = paginate_questions(request,select_questions)

        category_questions = [question.format() for question in select_questions]

        total_questions = len(select_questions.all())

        if category_questions == []:
            abort(404)
        
        else:
        # if no error returns the following
            return jsonify({
                "success": True,
                "questions": category_questions,
                "total_questions": total_questions,
                "current_category": category_id
            })
    
    
    #----------------------------------------------------------------------------#
    # Get Question Based on Categories to Play Game
    #----------------------------------------------------------------------------#

    #This is an endpoint to get questions based on categories to play quiz
    @app.route("/quizzes", methods=["POST"])
    def get_questions_to_play_quiz():
        body = request.get_json()
        previous_questions = body.get("previous_questions")
        quiz_category = body.get("quiz_category")

        all_questions = Question.query.filter(Question.category == quiz_category["id"]).all()

        questions = [question.format() for question in all_questions]
        randomIndex = random.randint(0, len(all_questions)-1)

        nextQuestion = questions[randomIndex]
        playTriva = True

        # if no question for a category that does not exist show not found

        if(all_questions == []):
            abort(404)

        else:
            while range(0, len(all_questions)-1):
                return jsonify({
                    "success":True,
                    "question": nextQuestion,
                    "previousQuestions": previous_questions
                    })



   
    #----------------------------------------------------------------------------#
    # Error Handlers
    #----------------------------------------------------------------------------#

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }),400
    
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }),404

    @app.errorhandler(405)
    def not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "method not allowed"
        }),405

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }),422

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "internal server error"
        }),422
    

    return app

