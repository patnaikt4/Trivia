## Ideation

The idea was to create a Trivia based quiz application that could track user statistics, hopefully leading to increased training and improvement over time. Hence why I wanted to create an analytical dashboard for this project -  as a way to keep users motivated and see their progress.

Below, I broke down sections of my code, explaining what each section is meant to accomplish.

We begin by creating a database for Users (containing their id, username, password, and a relationship with Scores) and a database for Scores (containing the id, score, total, difficulty, and user_id). Then, we have defined the URL’s for the easy, medium, and hard questions originating from the API.

Things Learned
- Python Libraries and Frameworks (Flask, Flask-SQLAlchemy, Flask-Migrate)
- Database
- APIs (Trivia Database API)
- HTML and Templating (Jinga2)
- CSS and JavaScript (Bootstrap and Chart.js)
- Development Tools (VSCode and Github)
- Routing


## App.py Overview

First I had to decide what python library I would use to handle interacting with my database. Because I didn’t want to work with raw SQL queries and wanted to relate databases together (Users and Score), I knew that I wanted to use a library which had Object Relational Mapping capabilities. Therefore, I decided to use SQLAlchemy. To encode and decode passwords, I used functions in the werkzeug.security library.

The fetch_questions function takes inputs of difficulty. It reads in the data and properly formatted it in terms of its id, question, correct answer, and incorrect answers and stores it. This is reference in later functions to determine the score of the user. I decided to use an API, which stored all the trivia questions based on difficulty. This function requests the questions from said API in order to use them for our program


## Index.html and Index Function in App.py

So this page documents the main page of the website. It has a drop down menu to select the difficulty of questions you want to obtain. Using Jinga

In order to process question submissions, I decided to loop through the user answers to the questions and check if it matches the correct answer for the question. Then, I save the score to the database by creating a Score object and appending it to the Score table. Once that has happened, we redirect the user to the result.html page, because the questions have been logged and calculated.

In order to handle GET requests, we get the difficulty, and fetch the questions.


## Analytics.html, Analytics.js, and Analytics Function in App.py

In the analytics function in app.py, I create a dictionary of stats based on each difficulty, which holds the total number of quizzes, total score, and average score for each level of difficulty. I also created a performance_data that has a key with the difficulty and the values are the scores. This is used in the line chart for the second graph.

I wanted to make the data visualizations interactive with the user, so instead of creating static visualizations through Python libraries such as Matplot or Seaborn, I used Chart.js, which is a javascript library. 

In the html file, I render the existing statistics with Bootstrap to keep everything in containers. I then use the Canvas tag utillized by Chart.js to create and render the data visualizations.

For creating the difficulty chart (the first one that renders), I gathered statistics by creating labels for the graph and computing statistics from the scoresData. Then, a bar chart is created with that information. For creating the performance chart (the second one that renders), I have done virtually the same method andline chart instead.


## Base.html

This file contains the basic Bootstrap and CSS used for the Styling of the Navigation bar and the page content. It is located in this separate file because it is a commonality among most templates and it abstracts the process.
