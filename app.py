from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from flask import session
from flask_migrate import Migrate


app = Flask(__name__, template_folder='C:/Users/richy/OneDrive - Dundalk Institute of Technology/Documents/project_database/SD3AIOTPROJECT/database_templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'  
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  
db = SQLAlchemy(app)
migrate = Migrate(app, db)

app.secret_key = 'Richy123'



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    plants = db.relationship('Plant', backref='user', lazy=True)

class PlantType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    water_requirement = db.Column(db.String(100), nullable=False)

class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)   


class Plant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    plant_type_id = db.Column(db.Integer, db.ForeignKey('plant_type.id'), nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'), nullable=False)
    date_planted = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    plant_type = db.relationship('PlantType', backref='plants')
    location = db.relationship('Location', backref='plants')
  
    def __repr__(self):
        return f'<Plant {self.name}, Type: {self.plant_type.name}, Water Requirement: {self.plant_type.water_requirement}>'


#with app.app_context():
  #  db.create_all()

@app.route('/')
def home():
    plant_types = PlantType.query.all() 
    return render_template('register.html', plant_types=plant_types)


@app.route('/mainPage')
def mainPage():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    plants = Plant.query.filter_by(user_id=user.id).all()
    return render_template('mainPage.html', user=user, plants=plants)

@app.route('/add_plant.html', methods=['GET', 'POST'])
def add_plant():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        name = request.form['name']
        plant_type_id = request.form['plant_type']
        location_id = request.form['location']
        date_planted = request.form['date_planted']

        user_id = session['user_id']
    

        new_plant = Plant(
            name=name,
            plant_type_id=plant_type_id,
            location_id=location_id,
            date_planted=date_planted,
            user_id=user_id 
        )

        db.session.add(new_plant)
        db.session.commit()

        return redirect(url_for('mainPage'))

    plant_types = PlantType.query.all()
    locations = Location.query.all()
    return render_template('add_plant.html', plant_types=plant_types, locations=locations)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])  

        new_user = User(name=name, email=email, password=password)
        hashed_password = generate_password_hash(password)

        db.session.add(new_user)
        db.session.commit()

        session['user_id'] = new_user.id
        return redirect(url_for('mainPage')) 

    return render_template('register.html')  


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id 
            return redirect(url_for('mainPage'))

        return "Invalid credentials, please try again."

    return render_template('login.html')  

if __name__ == "__main__":
    app.run(debug=True)