## Ideation

We begin by creating a database for Users (containing their id, username, password, and a relationship with Scores) and a database for Scores (containing the id, score, total, difficulty, and user_id). Then, we have defined the URL’s for the easy, medium, and hard questions.

Things Learned
Python Libraries and Frameworks
Database
APIs
HTML and Templating
CSS and JavaScript
Concepts
Development Tools
Routes





## App.py

First I had to decide what python library I would use to handle interacting with my database. Because I didn’t want to work with raw SQL queries and wanted to relate databases together (Users and Score), I knew that I wanted to use a library which had Object Relational Mapping capabilities. Therefore, I decided to use SQLAlchemy

To encode and decode passwords, I used functions in the werkzeug.security library.

The fetch_questions function takes inputs of difficulty. It reads in the data and properly formatted it in terms of its id, question, correct answer, and incorrect answers and stores it.

If the user is still logged in from previous sessions, the program starts by transferring us to the beginning of the page. 

If you request questions too quickly from the API’s, the API itself will throw an error (429). Therefore, I have implemented 3 retries into the function, which 

## Index.html

So this page

## Analytics.html

I wanted to make the data visualizations interactive with the user, so instead of creating static visualizations through Python libraries such as Matplot or Seaborn, I used Chart.js, which is a javascript library. 



Analytics.js

Folder contains the logic behind 
