from src.geo import Country, World
import time

class Player:
    def __init__(self, country: Country, world: World, color: tuple) -> None:
        self.country = country
        self.world = world
        self.color = color
        self.country.color = self.color
        self.timer = time.time() * 1000  # Timer in milliseconds
        self.controlled_countries = [self.country.name]
        self.neighbours = self.get_neighbours()

        # moving units
        self.move_country_from = ""
        self.move_country_to = ""
        self.move_n_units = 0

        # attacking countries
        self.attack_country_from = ""
        self.attack_country_to = ""

    def update(self, phase: str) -> None:
        if phase == "place_units":
            self.place_units()
        elif phase == "move_units":
            self.move_units()
        elif phase == "attack_country":
            self.attack_country()

    def place_units(self, country_name: str, units: int) -> None:
        now = time.time() * 1000
        if (now - self.timer > 300) and (country_name in self.controlled_countries):
            self.timer = now
            self.world.countries[country_name].units += units

    def move_units(self, from_country: str, to_country: str, units: int) -> None:
        if from_country in self.controlled_countries and to_country in self.controlled_countries:
            c_from = self.world.countries[from_country]
            c_to = self.world.countries[to_country]
            if c_from.units >= units:
                c_from.units -= units
                c_to.units += units

    def attack_country(self, from_country: str, to_country: str) -> None:
        if from_country in self.controlled_countries:
            neighbours = self.world.countries[from_country].neighbours
            if to_country in neighbours and to_country not in self.controlled_countries:
                self.world.battle(from_country, to_country)

    def get_neighbours(self) -> list:
        neighbours = []
        for country in self.controlled_countries:
            for neighbour in self.world.countries[country].neighbours:
                if neighbour not in self.controlled_countries:
                    neighbours.append(neighbour)
        return set(neighbours)

    def conquer(self, country: str) -> None:
        self.world.countries[country].color = self.color
        self.world.countries[country].controlled_by = self.country.name
        self.controlled_countries.append(country)
        self.neighbours = self.get_neighbours()

    def reset_turn(self) -> None:
        self.timer = time.time() * 1000
        self.move_country_from = ""
        self.move_country_to = ""
        self.move_n_units = 0
        self.attack_country_from = ""
        self.attack_country_to = ""
        for country in self.controlled_countries:
            c = self.world.countries[country]
            c.has_attacked = False

    def to_dict(self):
        return {
            "controlled_countries": self.controlled_countries,
            "neighbours": list(self.neighbours),
        }
