Tic Tac Toe AI with Commentary
Project Overview
This project is an interactive Tic Tac Toe game built with Python and Pygame. It uses Minimax with alpha-beta pruning for the AI moves, and Hugging Face Transformers combined with LangChain to give commentary on AI moves.

Features
Play Tic Tac Toe against an AI.
AI chooses moves using Minimax with alpha-beta pruning.
AI explains its moves using a Hugging Face model (such as gpt2).
Commentary is shown directly on the game screen.

Tech Stack
Python 3.9 or higher
Pygame for game rendering and interaction
Hugging Face Transformers for language generation
LangChain for prompt and model chaining

Setup Instructions
Clone the repository:
git clone <your-repo-url>

Install required dependencies:
pip install pygame transformers langchain torch

Run the game:
python game.py

Usage
The game starts with a Tic Tac Toe grid.
Click on the screen to make a move as the human player.
The AI will make its move and display commentary about its decision.
The game ends when one player wins or the game is a draw.

Improvements and Ideas
Try different Hugging Face models for better commentary.
Add voice output for AI commentary.
Export the game as a standalone app.
Integrate a database for move statistics or review.
