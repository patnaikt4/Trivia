## Ideation

We begin by creating a database for Users (containing their id, username, password, and a relationship with Scores) and a database for Scores (containing the id, score, total, difficulty, and user_id). Then, we have defined the URL’s for the easy, medium, and hard questions.

Things Learned
- Python Libraries and Frameworks
- Database
- APIs
- HTML and Templating
- CSS and JavaScript
- Concepts
- Development Tools
- Routes





## App.py Overview

First I had to decide what python library I would use to handle interacting with my database. Because I didn’t want to work with raw SQL queries and wanted to relate databases together (Users and Score), I knew that I wanted to use a library which had Object Relational Mapping capabilities. Therefore, I decided to use SQLAlchemy. To encode and decode passwords, I used functions in the werkzeug.security library.

The fetch_questions function takes inputs of difficulty. It reads in the data and properly formatted it in terms of its id, question, correct answer, and incorrect answers and stores it. This is reference in later functions to determine the score of the user.


## Index.html and Index Function in App.py

So this page documents the main page of the website. It has a drop down menu to select the difficulty of questions you want to obtain. Using Jinga

In order to process question submissions, I decided to loop through the user answers to the questions and check if it matches the correct answer for the question. Then, I save the score to the database by creating a Score object and appending it to the Score table. Once that has happened, we redirect the user to the result.html page, because the questions have been logged and calculated.

In order to handle GET requests, we get the difficulty, and fetch the questions.


## Analytics.html, Analytics.js, and Analytics Function in App.py

I wanted to make the data visualizations interactive with the user, so instead of creating static visualizations through Python libraries such as Matplot or Seaborn, I used Chart.js, which is a javascript library. 

For creating the difficulty chart (the first one that renders), I gathered statistics by creating labels for the graph and computing statistics from the scoresData. Then, a bar chart is created with that information. For creating the performance chart (the second one that renders), I have done virtually the same method andline chart instead.

## Base.html

This file contains the basic Bootstrap and CSS used for the Styling of the Navigation bar and the page content. It is located in this separate file because it is a commonality among most templates and it abstracts the process.
