from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'  
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  
db = SQLAlchemy(app)


class PlantType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)   


class Plant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    plant_type_id = db.Column(db.Integer, db.ForeignKey('plant_type.id'), nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'), nullable=False)
    date_planted = db.Column(db.String(100), nullable=False)

    plant_type = db.relationship('PlantType', backref='plants')
    location = db.relationship('Location', backref='plants')
    def __repr__(self):
        return f'<Plant {self.name}>'


with app.app_context():
    db.create_all()

@app.route('/add_plant', methods=['GET', 'POST'])
def add_plant():
    if request.method == 'POST':
        name = request.form['name']
        plant_type_id = request.form['plant_type']
        location_id = request.form['location']
        date_planted = request.form['data.planted']

        new_plant = Plant(name=name, plant_type_id=plant_type_id, location_id=location_id, date_planted=date_planted)


        db.session.add(new_plant)
        db.session.commit()

        return redirect(url_for('home'))

        plant_types = PlantType.query.all()
        locations = Location.query.all()



    return render_template('add_plant.html', plant_types=plant_types, locations=locations)

@app.route('/')
def home():
    return "Welcome to the HydraBloom"

if __name__ == "__main__":
    app.run(debug=True)