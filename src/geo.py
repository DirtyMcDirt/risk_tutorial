from flask import Flask, jsonify, request
import json
import random
from shapely.geometry import Point, Polygon

app = Flask(__name__)

class Country:
    def __init__(self, name: str, coords: list) -> None:
        self.name = name
        self.coords = coords
        self.polygon = Polygon(self.coords)
        self.center = self.get_center()
        self.units = random.randint(1, 3)
        self.color = (72, 126, 176)
        self.hovered = False
        self.neighbours = None
        self.has_attacked = False
        self.controlled_by = self.name

    def get_center(self) -> dict:
        xs = [x for x, y in self.coords]
        ys = [y for x, y in self.coords]
        return {"x": sum(xs) / len(xs), "y": sum(ys) / len(ys)}

    def to_dict(self):
        return {
            "name": self.name,
            "units": self.units,
            "color": self.color,
            "center": self.center,
            "controlled_by": self.controlled_by,
            "neighbours": self.neighbours
        }

class World:
    MAP_WIDTH = 2.05 * 4000
    MAP_HEIGHT = 1.0 * 4000

    def __init__(self) -> None:
        self.read_geo_data()
        self.countries = self.create_countries()
        self.create_neighbours()

    def read_geo_data(self) -> None:
        with open("./data/country_coords.json", "r") as f:
            self.geo_data = json.load(f)

    def create_countries(self) -> dict:
        countries = {}
        for name, coords in self.geo_data.items():
            xy_coords = [
                [(self.MAP_WIDTH / 360) * (180 + coord[0]), (self.MAP_HEIGHT / 180) * (90 - coord[1])]
                for coord in coords
            ]
            countries[name] = Country(name, xy_coords)
        return countries

    def create_neighbours(self) -> None:
        for name, country in self.countries.items():
            country.neighbours = self.get_country_neighbours(name)

    def get_country_neighbours(self, country_name: str) -> list:
        neighbours = []
        country_poly = self.countries[country_name].polygon
        for other_country_name, other_country in self.countries.items():
            if country_name != other_country_name and country_poly.intersects(other_country.polygon):
                neighbours.append(other_country_name)
        return neighbours

    def to_dict(self):
        return {name: country.to_dict() for name, country in self.countries.items()}

world = World()

@app.route('/api/countries', methods=['GET'])
def get_countries():
    return jsonify(world.to_dict())

if __name__ == "__main__":
    app.run(debug=True)
