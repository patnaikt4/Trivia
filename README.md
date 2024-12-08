# Trivia Quiz App
 
Video Implementation: https://www.youtube.com/watch?v=nTC91s9u_IQ

## Hosted Website: 
https://trivia-1-rpqp.onrender.com/ (Note that I'm using the free plan, which has this warning: Your free instance will spin down with inactivity, which can delay requests by 50 seconds or more.)

Just in case the hosted website does not work, below are instructions for running the Trivia Quiz app locally with Flask once one has the files

## Requirements to Run Locally
- Python 3.6 or newer
- Virtual environment (optiona)

## Setup Instructions (If the hosted website does not work) 
1. **Cloning the Repository**:
   - Open a terminal and run these commands:
 	```bash
   git clone https://github.com/patnaikt4/Trivia.git
   cd Trivia
  
2. **Install Dependencies**:
   - Install required libraries:
 	```bash
 	pip install -r requirements.txt
 	```

3. **Setting the Database**:
   - Initialize the database:
 	```bash
 	flask db init
 	flask db migrate -m "Initial migration"
 	flask db upgrade
 	```

4. **Run the App**:
   - Set environment variables:
 	```bash
 	export FLASK_APP=app.py
 	export FLASK_ENV=development  # On Windows: set FLASK_APP=app.py && set FLASK_ENV=development
 	```
   - Start the Flask server:
 	```bash
 	flask run
 	```
   - Open the app in a browser:
 	```
 	http://127.0.0.1:5000
 	```

## Code Files in This Project
- `app.py`: Main application file.
- `templates/`: Contains HTML templates.
- `static/`: Contains JavaScript files.
- `requirements.txt`: Lists project dependencies.
- `migrations/`: Contains database migration files

## Contact
For issues or questions, please contact tejaspatnaik@college.harvard.edu.

## Credits

When doing this project, I got help from the following sources:

- [Boostrap Documentation]([url](https://getbootstrap.com/docs/5.3/getting-started/introduction/))
- [Werkzeug Documentation]([url](https://werkzeug.palletsprojects.com/en/stable/utils/))




