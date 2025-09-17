import os

basedir = os.path.abspath(os.path.dirname(__file__))

config = {
    "SQLALCHEMY_DATABASE_URI": f"sqlite:///{os.path.join(basedir, 'db.sqlite')}",
    "SQLALCHEMY_TRACK_MODIFICATIONS": False,
    "SMTP_SERVER": "smtp.gmail.com",
    "SMTP_PORT": 587,
    "SMTP_USER": "thenilap16052003@gmail.com",           # Gmail email
    "SMTP_PASSWORD": "hzhngyssbxgplqaj",     # Gmail app password
    "EMAIL_FROM": "thenilap16052003@gmail.com",
    "BATCH_SIZE": 10,
    "LOG_JSON": True
}
