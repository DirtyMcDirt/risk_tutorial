from flask import Flask, jsonify, request
from src.geo import World
from src.player import Player
import time

app = Flask(__name__)

class Game:
    def __init__(self) -> None:
        self.phases = ["place_units", "move_units", "attack_country"]
        self.phase_idx = 0
        self.phase = self.phases[self.phase_idx]
        self.phase_timer = time.time() * 1000  # Milliseconds timer
        self.world = World()
        self.player = Player(self.world.countries.get("France"), self.world, (0, 0, 255))
        self.playing = True
        self.finish_phase_button_hovered = False

    def update(self):
        now = time.time() * 1000
        self.world.update()
        self.player.update(self.phase)
        if self.world.battle_res is not None:
            if self.world.battle_res["victory"]:
                if self.world.battle_res["attacking_country"] in self.player.controlled_countries:
                    self.player.conquer(self.world.battle_res["defending_country"])
            self.world.battle_res = None

        if self.finish_phase_button_hovered and (now - self.phase_timer > 500):
            self.phase_timer = now
            self.phase_idx = (self.phase_idx + 1) % len(self.phases)
            self.phase = self.phases[self.phase_idx]
            if self.phase == "place_units":
                self.player.reset_turn()

    def to_dict(self):
        return {
            "phase": self.phase,
            "world": self.world.to_dict(),
            "player": self.player.to_dict(),
            "phase_timer": self.phase_timer,
        }

game = Game()

@app.route('/api/game', methods=['GET'])
def get_game_state():
    return jsonify(game.to_dict())

@app.route('/api/game/update', methods=['POST'])
def update_game_state():
    game.update()
    return jsonify(success=True)

@app.route('/api/game/next_phase', methods=['POST'])
def next_phase():
    game.phase_timer = time.time() * 1000  # Reset the phase timer
    game.phase_idx = (game.phase_idx + 1) % len(game.phases)
    game.phase = game.phases[game.phase_idx]
    if game.phase == "place_units":
        game.player.reset_turn()
    return jsonify(success=True)

if __name__ == "__main__":
    app.run(debug=True)
