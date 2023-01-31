pip install viberbot
pip install gspread
pip install nltk
pip install flask
pip install flask-sqlalchemy
pip install python-dotenv
pip install torch
pip intall numpy

download nltk punkt tokenizer:
>>> import nltk
>>> nltk.download('punkt')


Running bot on server:
>>> cd /home/testsix/new-user-bot
>>> source venv/bin/activate
>>> nohup python3 app.py &


Creating db:
>>> python -m flask shell
>>> from app import db
>>> db.create_all()

