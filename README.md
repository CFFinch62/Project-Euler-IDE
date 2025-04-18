# Project Euler Editor

A modern, user-friendly, cross-platform (Linux, Mac, Windows) editor/code runner for solving Project Euler problems. This application provides a comprehensive environment for working on Project Euler problems, with features for code editing, testing, and progress tracking.

![Screenshot 2025-04-14 at 9 32 31 PM](https://github.com/user-attachments/assets/60af99c9-73f2-4781-a8d8-d4d58e938ddb)

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
- Some helper files already available to try or edit
- Create and manage helper files for each problem
- Test helper functions independently
- Organize code into multiple files
- Automatic loading of helper files when running solutions

### Data File Management
- Centralized storage for problem data files
- Automatic loading of required data files
- Support for multiple problems using the same data file
- Helper methods for loading and processing data
- All support files below are already available, no dwonloading needed

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
python pe_editor.py
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
   - All necessary data files for problems 1-100 included, no downlaoding required
   - Use helper methods to load data

5. **Use Tutorials**
   - Access tutorials through the Help menu
   - Follow interactive guides to learn the editor
   - Create custom tutorials using the tutorial editor

## Data Files

If any data files for certain problems are missing or get deleted they can be downloaded from the Project Euler website. 
Place them in the `data` directory with the exact names specified in the problem descriptions.

See `data/README.md` for detailed information about required data files and how to obtain them.


## Screenshots

![Screenshot 2025-04-14 at 9 32 52 PM](https://github.com/user-attachments/assets/0eb7d98d-eabe-442c-9cba-245f839452a3)
![Screenshot 2025-04-14 at 9 33 07 PM](https://github.com/user-attachments/assets/51e092b2-3878-4edd-8676-88012126640a)
![Screenshot 2025-04-14 at 9 33 16 PM](https://github.com/user-attachments/assets/3ab7b6e7-d61e-483e-ba0a-1c4b89474ca4)
![Screenshot 2025-04-14 at 9 33 25 PM](https://github.com/user-attachments/assets/88730167-0694-445b-8ae2-0e3d99bb670e)
![Screenshot 2025-04-14 at 9 33 36 PM](https://github.com/user-attachments/assets/083135f0-0616-470c-a55c-d607d94ee761)
![Screenshot 2025-04-14 at 9 33 52 PM](https://github.com/user-attachments/assets/fbeda655-2cd5-42ea-83f5-45a674e054a5)
![Screenshot 2025-04-14 at 9 34 01 PM](https://github.com/user-attachments/assets/8e35e067-4849-4d06-b8b8-21b4ae75e4db)
![Screenshot 2025-04-14 at 9 34 09 PM](https://github.com/user-attachments/assets/e0066afe-d45b-48a6-8e0e-d23dc947e762)
![Screenshot 2025-04-14 at 9 34 19 PM](https://github.com/user-attachments/assets/8b547f1e-fb6d-42d0-891e-b209614c735f)


## License

This project is licensed under the MIT License - see the LICENSE file for details. 
