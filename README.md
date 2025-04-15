# Project Euler Editor

A modern, user-friendly, cross-platform (Linux, Mac, Windows) editor/code runner for solving Project Euler problems. This application provides a comprehensive environment for working on Project Euler problems, with features for code editing, testing, and progress tracking.

## Features

### Problem Management
- Browse and select problems from 1 to 100
- View problem descriptions and hints
- Track progress with visual indicators (solved (green), attempted (yellow), unsolved (grey))
- Save and load solutions
- Run solutions and view results
- Automatic progress tracking
- Problem difficulty ratings (1-5 stars)
- Difficulty-based problem filtering
- Project Euler difficulty percentages

### Code Editor
- Advanced syntax highlighting for Python code with customizable colors:
  - Keywords (e.g., def, if, for)
  - Strings and string literals
  - Numbers and numeric literals
  - Comments
  - Operators (+, -, *, /, etc.)
  - Functions and method calls
  - Punctuation (commas, semicolons)
- Customizable color scheme through settings
- Custom syntax highlighting themes:
  - Save and load custom color themes
  - Theme management through settings dialog
  - Default themes included
- Line numbers
- Auto-indentation
- Error highlighting
- Dark theme support

### Code Templates
- Pre-built code templates for common problem patterns
- Template management system:
  - Create and edit templates
  - Organize templates by category
  - Quick insertion of templates into code
- Template preview functionality
- Template editor with syntax highlighting

### Tutorial System
- Interactive tutorials for learning the editor
- Step-by-step guided learning:
  - Welcome tutorial
  - First problem tutorial
  - Running code tutorial
- Tutorial editor for creating custom tutorials
- Tutorial actions:
  - Interface highlighting
  - Button highlighting
  - Problem selection
  - Dialog opening
  - Template insertion
  - Code execution
  - Helper file loading
- Tutorial management through settings

### Helper Files
- Create and manage helper files for each problem
- Test helper functions independently
- Organize code into multiple files
- Automatic loading of helper files when running solutions

### Data File Management
- Centralized storage for problem data files
- Automatic loading of required data files
- Support for multiple problems using the same data file
- Helper methods for loading and processing data

Supported data files:
- `triangle.txt` (Problem 67)
- `names.txt` (Problem 22)
- `words.txt` (Problems 42 and 98)
- `poker.txt` (Problem 54)
- `cipher.txt` (Problem 59)
- `keylog.txt` (Problem 79)
- `matrix.txt` (Problems 81, 82, and 83)
- `roman.txt` (Problem 89)
- `sudoku.txt` (Problem 96)
- `base_exp.txt` (Problem 99)

### User Interface
- Modern, dark-themed interface
- Problem selection grid with difficulty indicators
- Difficulty filter toolbar with star ratings
- Split view for problem description and code editor
- Progress tracking visualization
- Status bar with problem information
- Error and result display
- Problem difficulty tooltips

### Progress Tracking
- Visual indicators for problem status:
  - Green: Solved
  - Yellow: Attempted
  - Gray: Unsolved
- Automatic saving of progress
- Progress statistics
- Last attempted problem tracking
- Achievement system with badges
- Streak tracking

### Difficulty System
- 1-5 star difficulty rating for each problem
- Project Euler difficulty percentages
- Difficulty-based problem filtering
- Visual difficulty indicators in the problem grid
- Difficulty information in problem descriptions
- Tooltips showing difficulty ratings and percentages

## Directory Structure
```
project_euler_editor/
├── data/                           # Additional data files for problems
├── problems/                       # Problem descriptions
│   └── difficulty.json             # Problem difficulty ratings
├── solutions/                      # User solutions
├── helpers/                        # Helper files
│   └── readme.md                   # Helper file systen usage info
│   └── helpers.md                  # Helper file details
│   └── problem_assingments.json    # Helper file assingments to problems
├── info/                           # Additional problem study info
├── themes/                         # Syntax highlighting themes
│   └── chuck.json                  # Example theme file
├── tutorials/                      # Tutorial files
│   ├── tutorials.json              # Tutorial definitions
│   └── tutorial_editor_guide.md    # Tutorial creation guide
├── main.py                         # Main application
├── problem_manager.py              # Problem management
├── progress_grid.py                # Progress grid with difficulty support
├── run_programs.py                 # Code runner
├── settings_manager.py             # Settings handling
├── settings_dialog.py              # Settgins GUI
├── progress.json                   # User progress storage
├── requirements.txt                # Python requirements for app to run properly
├── ui/                             # UI components
│   ├── main_window.py
│   ├── code_editor.py
│   ├── problem_grid.py
│   ├── syntax_highlighter.py
│   └── theme.py
├── templates_dialog.py             # Template management
├── template_editor_dialog.py       # Template editor
├── tutorial_dialog.py              # Tutorial viewer
├── tutorial_editor_dialog.py       # Tutorial editor
├── tutorial_manager.py             # Tutorial management
├── README.md                       # Main app instructions
└── future_plans.md                 # Future feature map
```

## Installation

1. Download the software from our github page:
https://github.com/CFFinch62?tab=repositories

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python main.py
```

## Usage

1. **Select a Problem**
   - Click on a problem number in the grid
   - View problem description, hints, and difficulty rating
   - Use the difficulty filter to find problems matching your skill level
   - Start coding your solution

2. **Write Your Solution**
   - Use the code editor to write Python code
   - Create helper files if needed
   - Test helper functions independently
   - Save your progress
   - Use code templates for common patterns
   - Customize syntax highlighting themes

3. **Run Your Solution**
   - Click the "Run" button
   - View results and execution time
   - Check for errors
   - Track your progress

4. **Manage Data Files**
   - Place required data files in the `data` directory
   - Use helper methods to load data
   - Access data files through the ProblemManager

5. **Use Tutorials**
   - Access tutorials through the Help menu
   - Follow interactive guides to learn the editor
   - Create custom tutorials using the tutorial editor

## Data Files

Data files required for certain problems can be downloaded from the Project Euler website. Place them in the `data` directory with the exact names specified in the problem descriptions.

See `data/README.md` for detailed information about required data files and how to obtain them.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 
