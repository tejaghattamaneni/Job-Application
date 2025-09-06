from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///job.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# Define model matching form fields
class JobApplication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer)
    phone = db.Column(db.String(15))
    dob = db.Column(db.String(20))
    registration = db.Column(db.String(30))
    gender = db.Column(db.String(10))
    skills = db.Column(db.String(200))
    skillset_rating = db.Column(db.Integer)
    profile_url = db.Column(db.String(200))
    cover_letter = db.Column(db.Text)

    def __repr__(self):
        return f"<JobApplication {self.name}>"

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        skills_selected = request.form.getlist('skills')
        new_app = JobApplication(
            name=request.form['name'],
            email=request.form['email'],
            password=request.form['password'],
            age=request.form.get('age'),
            phone=request.form.get('phone'),
            dob=request.form.get('dob'),
            registration=request.form.get('registration'),
            gender=request.form.get('gender'),
            skills=", ".join(skills_selected),
            skillset_rating=request.form.get('skillset'),
            profile_url=request.form.get('profile'),
            cover_letter=request.form.get('cover')
        )
        db.session.add(new_app)
        db.session.commit()
        return redirect(url_for('thank_you'))
        
    return render_template('home1.html')

@app.route('/view')
def view_applications():
    applications = JobApplication.query.all()
    return render_template('view.html', applications=applications)

@app.route('/thank-you')
def thank_you():
    return render_template('thank.html')

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)