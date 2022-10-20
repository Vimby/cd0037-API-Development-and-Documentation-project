TRIVIA APP FULL STACK PROJECT

Trivia is a game created for Udacity employees and students. It is a part of the Full Stack Nano degree project testing students grasp of API Development and Documentantion course. On completion  of the app one can do the following:
1. Display questions - both all questions and by category. Questions show the question, category and difficulty rating by default and can show/hide the answer.
2. Delete questions.
3. Add questions and require that they include question and answer text.
4. Search for questions based on a text query string.
5. Play the quiz game, randomizing either all questions or within a specific category.

Completing the trivia app  gives students the ability to structure, plan, implement, and test an API.


GETTING STARTED

Prerequisites and Installation
-This project requires Python3 version, pip and node modules to be installed to your local machine 
-We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virtual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

-To fork the project on your local machine [clone ]()

Backend
-From the backend folder run the below to install all dependencies
-The [Backend README](./backend/README.md) contain further details for working on the backend of the project

```bash
pip install -r requirements.txt

```
Running the server
-Firstly execute the below commands on git bash
export FLASK_APP=flaskr
export FLASK_ENV=development

-To run the server, execute:

 flask run --reload

The application is run on http://127.0.0.1:5000/ by default and is a proxy in the frontend configuration.

Frontend
From the frontend folder, execute the below commands to install the requirements
  npm install // only once to install dependencies

To start the server 
     npm start 

By default, the frontend will run on localhost:3000.

Tests
To deploy the tests, run

```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

API REFERANCE

Getting Started

Base URL
 At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, http://127.0.0.1:5000/, which is set as a proxy in the frontend configuration.

 Aunthentication
 This version of the application does not require authentication or API keys.

Error Handling
Errors are returned as JSON objects in the following format:

{
    "success": False, 
    "error": 400,
    "message": "Bad Request"
}

The API will return four error types when requests fail:

400: Bad Request
404:  Not found
422: The server was unable to process the request
500: Internal server error

Endpoints
GET '/categories'
curl http://127.0.0.1:5000/categories

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains an object of id: category_string key:value pairs.

```Response
{
"categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "success": true
}

GET '/questions?page=${integer}'
curl http://127.0.0.1:5000/questions?page=1

- Fetches a paginated set of questions, a total number of questions, all categories and current category string.
- Request Arguments: `page` - integer
- Returns: An object with 10 paginated questions, total questions, object including all categories, and current category string

```Response
"categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "current_category": null,
  "questions": [
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    "success": true,
  "total_questions": 19
    {

GET '/categories/${id}/questions'
curl  http://127.0.0.1:5000/categories/3/questions

- Fetches questions for a cateogry specified by id request argument
- Request Arguments: `id` - integer
- Returns: An object with questions for the specified category, total questions, and current category string

```Response
"current_category": "Geography",
  "questions": [
    {
      "answer": "Lake Victoria",
      "category": 3,
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"
    },
    {
      "answer": "The Palace of Versailles",
      "category": 3,
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }
  ],
  "success": true,
  "total_questions": 2
}


DELETE '/questions/${id}'
curl -X DELETE http://127.0.0.1:5000/questions/11
- Deletes a specified question using the id of the question
- Request Arguments: `id` 
-Returns deleted question id

```Response
"deleted": 9,
  "success": true
}

POST '/questions'
curl -X POST -H "Content-Type: application/json" -d '{"question": "Who is the richest singer in the world", "answer":"Paul MCCartney", "category": "5", "difficulty": "1"}' http://127.0.0.1:5000/questions
- Sends a post request in order to add a new question
- Returns the id of a created question, length of total questions and current paginated questions

```Response
 "created": 38,
  "questions": [
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    "success": true,
    "total_questions": 19

   
POST '/questions/search'
curl -X POST -H "Content-Type: application/json" -d '{"searchTerm": "title"}' http://localhost:5000/questions/search
- Sends a post request in order to search for a specific question by search term
-Returns any array of questions, a number of totalQuestions that met the search term and the current category string

```Response
 "current_category": null,
  "questions": [
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }
  ],
  "success": true,
  "total_questions": 2
}


POST '/quizzes'
curl -X POST 'http://127.0.0.1:5000/quizzes' -H 'Content-Type: application/json' -d '{"previous_questions": [1, 4, 20, 15], "quiz_category":{"id":"1", "type":"Science"}}'
- Sends a post request in order to get the next question
- Returns a single new question object

```Response
 "question": {
    "answer": "Blood",
    "category": 1,
    "difficulty": 4,
    "id": 22,
    "question": "Hematology is a branch of medicine involving the study of what?"
  },
  "success": true
}

DEPLOYMENT
N/A

Authors
This project was completed by Vimbai Rusike

ACKNOWLEDGMENTS
The awesome team at Udacity and our mentors who made this journey easy.
 