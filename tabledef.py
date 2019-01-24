import datetime
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, DateTime, Integer, String, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

engine = create_engine('sqlite:///deadsimple.db', echo=True)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    password = Column(String)
    phone = Column(Integer)

    def __init__(self, first_name, last_name, email, password, phone):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.phone = phone

class Exercise(Base):
    __tablename__ = "exercises"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    day = Column(Integer)
    type = Column(String)
    weight = Column(Integer)
    reps = Column(Integer)

    def __init__(self, user_id, day, type, weight, reps):
        self.user_id = user_id
        self.day = day
        self.type = type
        self.weight = weight
        self.reps = reps

# Create a scheduled exercises table with dates and Boolean "Done?".
class Scheduled_Exercise(Base):
    __tablename__ = "scheduled_exercises"

    id = Column(Integer, primary_key=True)
    exercise_id = Column(Integer, ForeignKey('exercises.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    day = Column(Integer)
    type = Column(String)
    weight = Column(Integer)
    reps = Column(Integer)
    date = Column(DateTime, default=datetime.datetime.utcnow)
    done = Column(Boolean)

    def __init__(self, user_id, day, type, weight, reps, exercise_id, date, done):
        self.user_id = user_id
        self.day = day
        self.type = type
        self.weight = weight
        self.reps = reps
        self.exercise_id = exercise_id
        self.date = date
        self.done = done

Base.metadata.create_all(engine)
