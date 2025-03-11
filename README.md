# TAS-D04-2025
A git distribution for Test, Analysis, and Design. Project group D04 at TUDelft.

📂 File & Project Structure
Use virtual environments to manage dependencies (venv).
Exclude environment folders (venv) and sensitive files in .gitignore.
Store dependencies in requirements.txt, with pinned versions.
Split requirements into separate files (e.g., base.txt, dev.txt).

🟢 Variables
Use snake_case for variable names.
Be descriptive but concise: user_name, max_retries.
Use UPPERCASE for constants: PI, MAX_CONNECTIONS.
Avoid magic numbers — define meaningful constants.

🟠 Functions
Use snake_case for function names.
Keep functions small and focused on one task.
Add docstrings to explain functionality.
Set default values for optional arguments.

def greet(name="Guest"):
    """Greet a user by name."""
    print(f"Hello, {name}!")
    
🟡 Classes
Use PascalCase for class names.
Use self for instance variables.
Prefix private variables with _: self._mileage.
Add docstrings to describe the class and its methods.

class Dog:
    """A class representing a dog."""
    def __init__(self, name):
        self.name = name
        
🟣 Comments
Use inline comments for short explanations:

final_price = price * 0.9  # Apply 10% discount
Use block comments for longer descriptions.

Write meaningful comments — don’t state the obvious!

🟤 Formatting & Whitespace
Indentation: Use 4 spaces (not tabs).
Line length: Stick to 79–100 characters.
Blank lines:
2 lines around top-level functions/classes.
1 line inside class methods or smaller sections.
Trailing commas in multiline structures:

items = [
    "apple",
    "banana",
    "cherry",
]

🟠 Imports
Order imports:

Standard library modules
Third-party packages
Local modules
One import per line:

import os  
import sys

Avoid wildcard imports (*) — import only what you need.
