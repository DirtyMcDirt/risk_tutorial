from flask import Flask, render_template, jsonify  # Added jsonify import
from src.game import Game
import time  # Added time import

app = Flask(__name__)

# Initialize the game
game = Game()

@app.route('/')
def index():
    """Serve the main HTML page."""
    return render_template('index.html')

@app.route('/api/game', methods=['GET'])
def get_game_state():
    """API endpoint to get the current game state."""
    return jsonify(game.to_dict())

@app.route('/api/game/next_phase', methods=['POST'])
def next_phase():
    """API endpoint to move to the next phase."""
    game.phase_timer = time.time() * 1000  # Reset the phase timer
    game.phase_idx = (game.phase_idx + 1) % len(game.phases)
    game.phase = game.phases[game.phase_idx]
    if game.phase == "place_units":
        game.player.reset_turn()
    return jsonify(success=True)

if __name__ == "__main__":
    app.run(debug=True)
