from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean,  ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

db = SQLAlchemy()

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)


    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
    
class People(db.Model):
    __tablename__ = "people"
    id: Mapped[int] = mapped_column(primary_key=True) 
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    skin_color: Mapped[str] = mapped_column(String(120))
    hair_color: Mapped[str] = mapped_column(String(120))
    height:  Mapped[str] = mapped_column(String(120))
    eye_color: Mapped[str] = mapped_column(String(120))
    mass: Mapped[str] = mapped_column(String(120))
    birth_year: Mapped[str] = mapped_column(String(120), nullable=False)
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "birth_year": self.birth_year,
            "height": self.height,
            "skin_color": self.skin_color,
            "hair_color": self.hair_color,
            "mass": self.mass
        }

class Planets(db.Model):
    __tablename__ = "planets"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    climate: Mapped[str] = mapped_column(String(120), nullable=False)
    diameter: Mapped[str] = mapped_column(String(120))
    gravity: Mapped[str] = mapped_column(String(120), nullable=False)
    terrain: Mapped[str] = mapped_column(String(120), nullable=False)
    surface_water: Mapped[str] = mapped_column(String(120))
    population: Mapped[str] = mapped_column(String(120))
    orbital_period: Mapped[str] = mapped_column(String(120))
    rotation_period: Mapped[str] = mapped_column(String(120))
    def serialize(self):
     return {
        "id": self.id,
        "name": self.name,
        "climate": self.climate,
        "diameter": self.diameter,
        "gravity": self.gravity,
        "terrain": self.terrain,
        "surface_water": self.surface_water,
        "population": self.population,
        "orbital_period": self.orbital_period,
        "rotation_period": self.rotation_period
    }

class FavoritePlanet(db.Model):
    __tablename__ = "favorite_planets"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    planet_id: Mapped[int] = mapped_column(ForeignKey("planets.id"), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planet_id": self.planet_id
        }


    
class FavoritePeople(db.Model):
    __tablename__ = "favorite_people"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    people_id: Mapped[int] = mapped_column(ForeignKey("people.id"), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "people_id": self.people_id
        }