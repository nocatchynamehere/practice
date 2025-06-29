# fitness_tracker_app

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from dotenv import load_dotenv
import os
import enum

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

    # Relationships to other tables
    sleep_logs = db.relationship('SleepLog', backref='user', lazy=True)
    food_logs = db.relationship('FoodLog', backref='user', lazy=True)
    hydration_logs = db.relationship('HydrationLog', backref='user', lazy=True)
    measurements = db.relationship('Measurement', backref='user', lazy=True)
    workouts = db.relationship('Workout', backref='user', lazy=True)

class SleepLog(db.Model):
    __tablename__ = 'sleep_logs'

    log_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=True)
    sleep_date = db.Column(db.Date, nullable=True)
    hours_slept = db.Column(db.Numeric(4, 2), nullable=True)
    sleep_quality = db.Column(db.Integer, nullable=True)
    notes = db.Column(db.Text, nullable=True)

class Exercise(db.Model):
    __tablename__ = 'exercises'

    exercise_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    category = db.Column(db.String(50), nullable=True)
    is_bodyweight = db.Column(db.Boolean, nullable=True)

class SetType(enum.Enum):
    warmup = "warmup"
    working = "working"
    drop = "drop"
    failure = "failure"

class WorkoutSet(db.Model):
    __tablename__ = 'workout_sets'

    set_id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey('workouts.workout_id'), nullable=True)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.exercise_id'), nullable=True)
    set_number = db.Column(db.Integer, nullable=True)
    reps = db.Column(db.Integer, nullable=True)
    weight_used = db.Column(db.Numeric(5, 2), nullable=True)
    rest_seconds = db.Column(db.Integer, nullable=True)
    set_type = db.Column(db.String(20), nullable=True)

    exercise = db.relationship('Exercise', backref='workout_sets', lazy=True)

class FoodLog(db.Model):
    __tablename__ = 'food_logs'

    food_log_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=True)
    log_date = db.Column(db.Date, nullable=True)
    meal_type = db.Column(db.String(20), nullable=True)
    calories = db.Column(db.Integer, nullable=True)
    protein_g = db.Column(db.Numeric(5, 2), nullable=True)
    carbs_g = db.Column(db.Numeric(5, 2), nullable=True)
    fat_g = db.Column(db.Numeric(5, 2), nullable=True)
    sodium_mg = db.Column(db.Integer, nullable=True)
    sugar_g = db.Column(db.Numeric(5, 2), nullable=True)
    notes = db.Column(db.Text, nullable=True)

class HydrationLog(db.Model):
    __tablename__ = 'hydration_logs'

    hydration_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=True)
    log_date = db.Column(db.Date, nullable=True)
    total_water_oz = db.Column(db.Integer, nullable=True)
    electrolyte_mix_used = db.Column(db.Boolean, nullable=True)
    notes = db.Column(db.Text, nullable=True)

class Measurement(db.Model):
    __tablename__ = 'measurements'

    measurement_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=True)
    measurement_date = db.Column(db.Date, nullable=True)
    weight = db.Column(db.Numeric(5, 2), nullable=True)
    body_fat_pct = db.Column(db.Numeric(4, 2), nullable=True)
    hips_inches = db.Column(db.Numeric(4, 2), nullable=True)
    waist_inches = db.Column(db.Numeric(4, 2), nullable=True)
    chest_inches = db.Column(db.Numeric(4, 2), nullable=True)
    thigh_inches = db.Column(db.Numeric(4, 2), nullable=True)
    arm_inches = db.Column(db.Numeric(4, 2), nullable=True)
    resting_heart_rate = db.Column(db.Integer, nullable=True)
    mood = db.Column(db.Integer, nullable=True)
    pain_level = db.Column(db.Integer, nullable=True)

class Workout(db.Model):
    __tablename__ = 'workouts'

    workout_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=True)
    workout_date = db.Column(db.Date, nullable=True)
    workout_type = db.Column(db.String(50), nullable=True)
    duration_minutes = db.Column(db.Integer, nullable=True)
    rpe = db.Column(db.Integer, nullable=True)
    notes = db.Column(db.Text, nullable=True)

    workout_sets = db.relationship('WorkoutSet', backref='workout', lazy=True)

# Routes

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_measurement', methods=['GET', 'POST'])
def add_measurement():
    if request.method == 'POST':
        # Parse form data
        measurement_date = datetime.strptime(request.form['measurement_date'], '%Y-%m-%d')
        weight = request.form.get('weight')
        body_fat_pct = request.form.get('body_fat_pct')
        hips_inches = request.form.get('hips_inches')
        waist_inches = request.form.get('waist_inches')
        chest_inches = request.form.get('chest_inches')
        thigh_inches = request.form.get('thigh_inches')
        arm_inches = request.form.get('arm_inches')
        resting_heart_rate = request.form.get('resting_heart_rate')
        mood = request.form.get('mood')
        pain_level = request.form.get('pain_level')

        # Create Measurement object
        new_entry = Measurement(
            user_id=1,  # Temporary placeholder; replace with logged-in user's ID
            measurement_date=measurement_date,
            weight=weight,
            body_fat_pct=body_fat_pct,
            hips_inches=hips_inches,
            waist_inches=waist_inches,
            chest_inches=chest_inches,
            thigh_inches=thigh_inches,
            arm_inches=arm_inches,
            resting_heart_rate=resting_heart_rate,
            mood=mood,
            pain_level=pain_level
        )

        db.session.add(new_entry)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('add_measurement.html')