from database import db
from sqlalchemy import Column,Integer,String
from flask_login import UserMixin

class User(db.Model,UserMixin):
    id = Column(Integer,primary_key=True)
    username = Column(String(80),nullable=False,unique=True)
    password = Column(String(80),nullable=False)
    role = Column(String(80),nullable=False,default='user')

