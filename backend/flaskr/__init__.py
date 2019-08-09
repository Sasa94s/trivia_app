import os
from builtins import int

from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from sqlalchemy.sql.expression import func
from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app, resources={r"/*": {"origins": "*"}}, support_credentials=True)

    def paginate(records_per_page, page):
        return records_per_page * (page - 1), records_per_page * page


    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        return response


    @app.route('/api/categories')
    def get_categories():
        '''
        Create an endpoint to handle GET requests
        for all available categories.
        '''
        categories = Category.query.all()
        return jsonify({
            'categories': [category.id for category in categories],
            'success': True,
        })


    @app.route('/api/categories/<int:category_id>/questions', methods=['GET'])
    def get_category_questions(category_id):
        '''
        Create a GET endpoint to get questions based on category.
        '''
        page = request.args.get('page', 1, type=int)
        categories = [category.id for category in Category.query.with_entities(Category.id)]

        start, stop = paginate(QUESTIONS_PER_PAGE, page)
        questions = Question.query.filter(Question.category == category_id).slice(start, stop).all()

        total_questions = Question.query.count()
        return jsonify({
            'questions': [question.format() for question in questions],
            'total_questions': total_questions,
            'current_category': category_id,
            'categories': categories
        })


    @app.route('/api/questions', methods=['POST'])
    def create_question():
        '''
        Create an endpoint to POST a new question,
        which will require the question and answer text,
        category, and difficulty score.

        Get questions based on a search term.
        It should return any questions for whom the search term
        is a substring of the question.
        '''
        body = request.get_json()
        search_term = body.get('searchTerm', None)

        if search_term:
            categories = Category.query.all()
            questions = Question.query.filter(Question.question.ilike('%{}%'.format(search_term)))
            total_questions = questions.count()
            return jsonify({
                'questions': [question.format() for question in questions],
                'total_questions': total_questions,
                'categories': [category.id for category in categories],
                'current_category': [question.category for question in questions],
                'success': True
            })
        else:
            status = False
            question = Question(**request.json)
            if question:
                question.insert()
                status = True

            return jsonify({
                'question': question.id,
                'success': status
            })


    @app.route('/api/questions', methods=['GET'])
    def get_questions():
        '''
        Create an endpoint to handle GET requests for questions,
        including pagination (every 10 questions).
        This endpoint should return a list of questions,
        number of total questions, current category, categories.
        '''
        page = request.args.get('page', 1, type=int)
        categories = [category.id for category in Category.query.with_entities(Category.id)]
        current_category = request.args.get('category', 0, type=int)

        start, stop = paginate(QUESTIONS_PER_PAGE, page)
        questions = Question.query.slice(start, stop).all()

        total_questions = Question.query.count()
        return jsonify({
            'questions': [question.format() for question in questions],
            'total_questions': total_questions,
            'current_category': current_category,
            'categories': categories
        })


    @app.route('/api/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        '''
        Create an endpoint to DELETE question using a question ID.
        '''
        question = Question.query.filter(Question.id == question_id).one_or_none()
        status = False
        if question:
            Question.delete(question)
            status = True
        return jsonify({
            'deleted': question.id,
            'success': status
        })


    @app.route('/api/quizzes', methods=['POST'])
    def quizzes():
        '''
        Create a POST endpoint to get questions to play the quiz.
        This endpoint should take category and previous question parameters
        and return a random questions within the given category,
        if provided, and that is not one of the previous questions.
        '''
        body = request.get_json()
        previous_questions = body.get('previous_questions', [])
        quiz_category = body.get('quiz_category', None)

        if not quiz_category:
            abort(400)

        category_id = int(quiz_category['id'])

        if category_id < 0:
            abort(422)
        elif category_id == 0:
            current_question = Question.query.filter(Question.id.notin_(previous_questions))\
                .order_by(func.random()).first()
        else:
            current_question = Question.query.filter(Question.category == category_id)\
                .filter(~Question.id.in_(previous_questions)).order_by(func.random()).first()

        return jsonify({
            'question': current_question.format()
        })

    @app.errorhandler(422)
    def unprocessable_error_handler(error):
        '''
        Error handler for status code 422.
        '''
        return jsonify({
            'success': False,
            'message': 'unprocessable'
        }), 422

    @app.errorhandler(404)
    def resource_not_found_error_handler(error):
        '''
        Error handler for status code 404.
        '''
        return jsonify({
            'success': False,
            'message': 'resource not found'
        }), 404

    @app.errorhandler(400)
    def bad_request_error_handler(error):
        '''
        Error handler for status code 400.
        '''
        return jsonify({
            'success': False,
            'message': 'bad request'
        }), 400

    @app.errorhandler(405)
    def method_not_allowed_error_handler(error):
        '''
        Error handler for status code 405.
        '''
        return jsonify({
            'success': False,
            'message': 'method not allowed'
        }), 405

    @app.errorhandler(500)
    def internal_server_error_handler(error):
        '''
        Error handler for status code 500.
        '''
        return jsonify({
            'success': False,
            'message': 'unexpected error, please check server logs'
        }), 500

    return app
