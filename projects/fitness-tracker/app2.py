# fitness_tracker_app

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import enum

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fitness.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)

class SleepLog(db.Model):
    __tablename__ = 'sleep_logs'
    
    log_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    sleep_date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    hours_slept = db.Column(db.Float, nullable=False)
    sleep_quality = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text, nullable = True)

class Exercises(db.Model):
    __tablename__ = 'exercises'

    exercise_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    is_bodyweight = db.Column(db.Boolean, nullable=False, default=False)

class SetType(enum.Enum):
    warmup = "warmup"
    working = "working"
    drop = "drop"
    failure = "failure"

class WorkoutSet(db.Model):
    __tablename__ = 'workout_sets'

    set_id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey('workouts.workout_id'), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.exercise_id'), nullable=False)
    set_number = db.Column(db.Integer, nullable=False)
    reps = db.Column(db.Integer, nullable=False)
    weight_used = db.Column(db.Float, nullable=False)
    rest_seconds = db.Column(db.Integer, nullable=True)
    set_type = db.Column(db.Enum(SetType), nullable=False)