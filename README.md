# Flappy Bird - Python Game

## Project Description
This is a Python implementation of the classic Flappy Bird game using the Pygame library. The objective of the game is to control a small bird that must fly between vertically moving obstacles (pipes) without hitting them. The game includes features like animated clouds, a scrolling ground, and sound effects for flapping, scoring, and crashing.

## Features
- **Animated Bird**: A yellow bird with 3 animated frames simulating flapping motion.
- **Dynamic Obstacles**: Vertically moving pipes that increase in difficulty as you progress.
- **Realistic Clouds**: Randomly generated, soft-edged clouds that move across the sky.
- **Scrolling Ground**: Continuously moving ground that enhances the illusion of forward motion.
- **Sound Effects**: Custom sounds for wing flaps, scoring, and collisions.
- **Progressive Difficulty**: The game speed increases slightly as the player scores more points.
- **Camera Scroll Effect**: The camera follows the bird horizontally, simulating infinite forward flight.

## Requirements
- Python 3.x
- Pygame 2.x
- NumPy (for sound generation)

## Installation
1. Clone this repository to your local machine:
   ```
   git clone https://github.com/yourusername/flappy-bird-python.git
   ```
2. Navigate to the project directory:
   ```
   cd flappy-bird-python
   ```
3. Install the required dependencies:
   ```
   pip install pygame numpy
   ```

## How to Play
- **Start**: Press the Spacebar (SPACE) to start the game.
- **Fly**: Press the Spacebar (SPACE) to make the bird flap and rise. The bird is affected by gravity and will fall if no input is given.
- **Avoid Obstacles**: Fly through the gaps between the vertical pipes. The game ends if the bird collides with a pipe or the ground.
- **Scoring**: Each time the bird successfully flies between two pipes, you score a point.
- **Game Over**: After a collision, the current score and the high score are displayed. Press the Spacebar (SPACE) to restart the game.

## Running the Game
To run the game, navigate to the project directory and execute the Python script:
python flappy_bird.py


## Code Overview
- `create_bird_images()`: Generates three animation frames for the bird. These frames are used to simulate flapping as the bird moves.
- `create_pipe_image()`: Creates the vertical pipe obstacles the bird must fly through.
- `Cloud Class`: This class generates animated clouds in the background. The clouds are composed of multiple ellipses, with highlights and shadows to give them a soft, realistic look.
- `create_sound()`: Generates sound effects (e.g., flapping, scoring, crashing) using NumPy to create sine waves that modulate different frequencies.
- `Bird Class`: Represents the bird controlled by the player. Handles movement, gravity, flapping, and collision detection.
- `Pipe Class`: Handles the generation and movement of the vertical pipe obstacles. Pipes are generated off-screen and move from right to left.
- `Camera Class`: Simulates a scrolling camera that follows the bird horizontally as it moves forward.
- `draw_background()`: Draws the moving background, including clouds and the scrolling ground.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Contact
For any issues or questions, feel free to reach out via GitHub or email.

Enjoy the game and have fun!
