# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
$ psql -U postgres
postgres=# create database trivia_test;
postgres=# \q
$ psql -d trivia_test -U postgres -f backend/trivia.psql
```

## Running the server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## Tasks

1. Use Flask-CORS to enable cross-domain requests and set response headers. 
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 
3. Create an endpoint to handle GET requests for all available categories. 
4. Create an endpoint to DELETE question using a question ID. 
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 
6. Create a POST endpoint to get questions based on category. 
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
9. Create error handlers for all expected errors including 400, 404, 422 and 500. 

## Endpoints

1. `GET '/api/categories'`
2. `GET '/api/categories/<int:category_id>/questions'`
3. `GET '/api/questions'`
4. `POST '/api/questions'`
5. `DELETE '/api/questions/<int:question_id>'`
6. `POST '/api/quizzes'`

### API Documentation
1. `GET '/api/categories'` -- Gets all available categories
    - Request Body: None
    - Response Body:
        ```
        {
            "categories": [1,2,3,4,5,6],
            "success": true
        }      
        ```
2. `GET '/api/categories/<int:category_id>/questions'` -- Gets all questions based on category
    - Request Body: None
    - Response Body:
    ```
   {
        "categories": [1,2,3,4,5,6],
        "current_category": 1,
        "questions": [
            {
                "answer": "The Liver",
                "category": 1,
                "difficulty": 4,
                "id": 20,
                "question": "What is the heaviest organ in the human body?"
            },
            ...
        ],
        "total_questions": 21
    }
    ```
3. `GET '/api/questions'` -- Gets all questions with pagination
    - Request Body: None
    - Query String Parameters:
        - `page`: integer -- number of requested page
        - `category`: integer -- number of requested category, if value equals `zero` then it will fetch by all categories
    - Response Body:
    ```
   {
        "categories": [1,2,3,4,5,6],
        "current_category": 0,
        "questions": [
            {
                "answer": "Maya Angelou",
                "category": 4,
                "difficulty": 2,
                "id": 5,
                "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
            },
            ...
        ],
        "total_questions": 21
    }
   ```
4. `POST '/api/questions'` -- Creates a new question
    
    - Request Body:
    ```
    { 
       "question":"Whats your name?",
       "answer":"Mostafa",
       "difficulty":1,
       "category":1
    }
    ```
    - Response Body:
    ```
    {
        "question": 33,
        "success": true
    }
    ```
     `POST '/api/questions'` -- Gets all available questions based on search term
    
    - Request Body:
    ```
    { 
       "searchTerm":"name"
    }
    ```
    - Response Body:
    ```{
    "categories": [1,2,3,4,5,6],
        "current_category": [4,6,1],
        "questions": [
            {
                "answer": "Muhammad Ali",
                "category": 4,
                "difficulty": 1,
                "id": 9,
                "question": "What boxer's original name is Cassius Clay?"
            },
            ...
        ],
        "success": true,
        "total_questions": 3
    }
    ```
5. `DELETE '/api/questions/<int:question_id>'` -- Deletes question by ID
    
    - Request Body: None
    - Response Body:
    ```
    {
        "deleted": 10,
        "success": true
    }
    ```
6. `POST '/api/quizzes'` -- Gets random question to play the quiz
    
    - Request Body: 
    ```
    { 
       "previous_questions":[ 
    
       ],
       "quiz_category":{ 
          "type":"click",
          "id":2
       }
    }
    ```
    - Response Body:
    ```
    {
        "question": {
            "answer": "Escher",
            "category": 2,
            "difficulty": 1,
            "id": 16,
            "question": "Which Dutch graphic artist–initials M C was a creator of optical illusions?"
        }
    }
    ```

## Testing
To run the tests, run
```
$ psql -U postgres
postgres=# drop database trivia_test;
postgres=# create database trivia_test;
postgres=# \q
$ psql -d trivia_test -U postgres -f backend/trivia.psql
$ python test_flaskr.py
```