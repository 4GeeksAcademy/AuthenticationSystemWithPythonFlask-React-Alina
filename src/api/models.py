from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<Users %r>' % self.id
    def new_user(self, email, password, name, is_active):
        self.email = email
        self.password = password
        self.name = name
        self.is_active = is_active
        db.session.add(self)
        db.session.commit()
        

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "name":self.name
            # do not serialize the password, its a security breach
        }
    
class Characters(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=False, nullable=False)
    hair_color = db.Column(db.String(120), unique=False, nullable=False)
    eye_color = db.Column(db.String(120), unique=False, nullable=False)
    height = db.Column(db.String(120), unique=False, nullable=False)

    def __repr__(self):
        return f'<Characters {self.name}>'

    def serialize(self):
        return {
            "id": self.id,
            "name" : self.name,
            "hair_color": self.hair_color,
            "eye_color": self.eye_color,
            "height": self.height
        }

class Planets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=False, nullable=False)
    biome = db.Column(db.String(120), unique=False, nullable=False)
    diameter = db.Column(db.String(120), unique=False, nullable=False)
    temp = db.Column(db.String(120), unique=False, nullable=False)
    
    def __repr__(self):
        return f'<Planets {self.name}>'

    def serialize(self):
        return {
            "id": self.id,
            "name" : self.name,
            "biome": self.biome,
            "diameter": self.diameter,
            "temp": self.temp
        }

class Vehicles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=False, nullable=False)
    seats = db.Column(db.String(120), unique=False, nullable=False)
    something = db.Column(db.String(120), unique=False, nullable=False)
    brand = db.Column(db.String(120), unique=False, nullable=False)
    
    def __repr__(self):
        return f'<Vehicles {self.name}>'

    def serialize(self):
        return {
            "id": self.id,
            "name" : self.name,
            "seats": self.seats,
            "something": self.something,
            "brand": self.brand
        }

class Fav_vehicles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_relation = db.Column(db.Integer, db.ForeignKey(Users.id, ondelete="CASCADE"), nullable=False)
    vehicles_relation = db.Column(db.Integer, db.ForeignKey(Vehicles.id, ondelete="CASCADE"), nullable=False)

    def __repr__(self):
        return f'<Vehicles {self.name}>'

    def serialize(self):
        return {
            "id": self.id,
            "user_relation" : self.user_relation,
            "vehicles_relation": self.vehicles_relation,
        }
    
class Fav_characters(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_relation = db.Column(db.Integer, db.ForeignKey(Users.id, ondelete="CASCADE"), nullable=False)
    characters_relation = db.Column(db.Integer, db.ForeignKey(Characters.id, ondelete="CASCADE"), nullable=False)

    def __repr__(self):
        return f'<Vehicles {self.name}>'

    def serialize(self):
        return {
            "id": self.id,
            "user_relation" : self.user_relation,
            "characters_relation": self.characters_relation,
        }
    
class Fav_planets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_relation = db.Column(db.Integer, db.ForeignKey(Users.id, ondelete="CASCADE"), nullable=False)
    planets_relation = db.Column(db.Integer, db.ForeignKey(Planets.id, ondelete="CASCADE"), nullable=False)

    def __repr__(self):
        return f'<Vehicles {self.name}>'

    def serialize(self):
        return {
            "id": self.id,
            "user_relation" : self.user_relation,
            "planets_relation": self.planets_relation,
        }