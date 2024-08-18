from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from passlib.context import CryptContext
from datetime import datetime

Base = declarative_base()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    questions = relationship("UserQuestion", back_populates="user")

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def set_password(self, password):
        self.password_hash = pwd_context.hash(password)

class Question(Base):
    __tablename__ = 'questions'
    id = Column(Integer, primary_key=True)
    question_text = Column(Text, nullable=False)
    ai_response = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    user_questions = relationship("UserQuestion", back_populates="question")

class UserQuestion(Base):
    __tablename__ = 'user_questions'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    question_id = Column(Integer, ForeignKey('questions.id'))
    user = relationship("User", back_populates="questions")
    question = relationship("Question", back_populates="user_questions")

#set up database
engine = create_engine('sqlite:///dashboard.db')
Base.metadata.create_all(engine)

#session management
Session = sessionmaker(bind=engine)
session = Session()

#user registration and authentication
def register_user(username, password):
    user = User(username=username)
    user.set_password(password)
    session.add(user)
    session.commit()
    return user

def authenticate_user(username, password):
    user = session.query(User).filter_by(username=username).first()
    if user and user.verify_password(password):
        return user
    return None

#Recording ai interactions
def record_question(user, question_text, ai_response):
    question = Question(question_text=question_text, ai_response=ai_response)
    session.add(question)
    session.commit()
    
    user_question = UserQuestion(user_id=user.id, question_id=question.id)
    session.add(user_question)
    session.commit()

#learning from the data
def get_user_questions(user):
    return session.query(Question).join(UserQuestion).filter(UserQuestion.user_id == user.id).all()

from sqlalchemy import create_engine, inspect

engine = create_engine('sqlite:///dashboard.db')
inspector = inspect(engine)
