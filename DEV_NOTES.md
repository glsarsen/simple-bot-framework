 pip install viberbot
 pip install gspread
 pip install nltk
 pip install flask
 pip install flask-migrate
 pip install flask-login
 pip install python-dotenv
 pip install torch
 pip intall numpy
 pip install flask-wtf
 pip install email_validator
 pip install flask-sqlalchemy


download nltk punkt tokenizer:
>>> import nltk
>>> nltk.download('punkt')


Running bot on server:
>>> cd /home/testsix/new-user-bot
>>> source venv/bin/activate
>>> nohup python3.9 app.py &


Creating db:
>>> python -m flask shell
>>> from app import db
>>> db.create_all()
