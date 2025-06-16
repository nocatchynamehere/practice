# fitness_tracker_app/app.py

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fitness.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define your data model
class DailyLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    weight = db.Column(db.Float, nullable=False)
    calories = db.Column(db.Integer, nullable=False)
    sleep_hours = db.Column(db.Float, nullable=True)
    mood = db.Column(db.Integer, nullable=True)

# Routes
@app.route('/')
def index():
    logs = DailyLog.query.order_by(DailyLog.date.desc()).all()
    return render_template('index.html', logs=logs)

@app.route('/add', methods=['GET', 'POST'])
def add_entry():
    if request.method == 'POST':
        date = datetime.strptime(request.form['date'], '%Y-%m-%d')
        weight = float(request.form['weight'])
        calories = int(request.form['calories'])
        sleep_hours = float(request.form['sleep_hours'])
        mood = int(request.form['mood'])

        entry = DailyLog(date=date, weight=weight, calories=calories,
                         sleep_hours=sleep_hours, mood=mood)
        db.session.add(entry)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('add.html')

@app.route('/delete/<int:id>')
def delete_entry(id):
    entry = DailyLog.query.get_or_404(id)
    db.session.delete(entry)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)