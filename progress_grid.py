from PyQt6.QtWidgets import (QWidget, QGridLayout, QLabel, QFrame, QVBoxLayout)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor, QPalette
import re

class ProblemGrid(QWidget):
    problem_selected = pyqtSignal(int)  # Signal emitted when a problem is selected
    square_clicked_signal = pyqtSignal(int)  # Renamed signal
    
    def __init__(self, problem_manager, parent=None):
        super().__init__(parent)
        self.problem_manager = problem_manager  # Store the problem manager
        self.setup_ui()
        
        # Set tooltip style for the entire widget
        self.setStyleSheet("""
            QToolTip {
                background-color: #2D2D2D;
                color: #D4D4D4;
                border: 1px solid #3D3D3D;
                padding: 5px;
            }
        """)
        
    def setup_ui(self):
        self.layout = QGridLayout()
        self.layout.setSpacing(0)  # Remove spacing between grid items
        self.setLayout(self.layout)
        self.problem_squares = {}
        self.current_square = None  # Track the current square
        self.solved_problems = set()  # Track solved problems
        self.attempted_problems = set()
        self.original_colors = {}  # Store original colors for filtering
        
        # Create 10x10 grid of problem squares
        for i in range(10):
            for j in range(10):
                problem_number = i * 10 + j + 1
                square = QFrame()
                square.setFrameShape(QFrame.Shape.Box)
                square.setLineWidth(1)
                square.setMinimumSize(40, 40)  # Set minimum size for better visibility
                square.setStyleSheet("""
                    QFrame {
                        background-color: #2D2D2D;
                        border: 1px solid #3D3D3D;
                    }
                    QFrame:hover {
                        background-color: #3D3D3D;
                    }
                """)
                
                # Create layout for the square
                square_layout = QVBoxLayout(square)
                square_layout.setContentsMargins(0, 0, 0, 0)  # Remove all margins
                square_layout.setSpacing(0)  # Remove spacing between labels
                
                # Add problem number label
                number_label = QLabel(str(problem_number))
                number_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                number_label.setStyleSheet("""
                    QLabel {
                        color: #A0A0A0;
                        font-size: 14px;
                        font-weight: bold;
                        padding: 0px;
                        margin: 0px;
                    }
                """)
                square_layout.addWidget(number_label)
                
                # Store references
                self.problem_squares[problem_number] = square
                square.number_label = number_label
                
                # Add to grid
                self.layout.addWidget(square, i, j)
                
                # Connect click event
                square.mousePressEvent = lambda event, pn=problem_number: self.square_clicked(pn)
        
    def square_clicked(self, problem_number):
        """Handle square click event."""
        # Update the current square
        self.current_square = problem_number
        
        # Update the grid to show the current problem while preserving progress colors
        for square in self.problem_squares.values():
            square_number = int(square.number_label.text())
            
            # Base style for the square
            if square_number in self.solved_problems:
                base_color = "#4CAF50"  # Green for solved
                hover_color = "#45A049"
            elif square_number in self.attempted_problems:
                base_color = "#FFC107"  # Yellow for attempted
                hover_color = "#FFB300"
            else:
                base_color = "#2D2D2D"  # Gray for not attempted
                hover_color = "#3D3D3D"
            
            # If this is the selected square, add a highlight border
            if square_number == problem_number:
                square.setStyleSheet(f"""
                    QFrame {{
                        background-color: {base_color};
                        border: 2px solid #569CD6;
                    }}
                    QFrame:hover {{
                        background-color: {hover_color};
                    }}
                """)
            else:
                square.setStyleSheet(f"""
                    QFrame {{
                        background-color: {base_color};
                        border: 1px solid #3D3D3D;
                    }}
                    QFrame:hover {{
                        background-color: {hover_color};
                    }}
                """)
            
            # Store original color if not already stored
            if square_number not in self.original_colors:
                self.original_colors[square_number] = base_color
        
        # Emit the signal
        self.square_clicked_signal.emit(problem_number)
    
    def get_current_square(self):
        """Get the currently selected problem square."""
        if self.current_square is None:
            return None
        return self.problem_squares.get(self.current_square)

    def update_progress(self, solved_problems, attempted_problems):
        """Update the visual state of problem squares based on progress."""
        self.solved_problems = set(solved_problems)  # Store solved problems
        self.attempted_problems = set(attempted_problems)  # Store attempted problems
        
        for problem_number, square in self.problem_squares.items():
            if problem_number in solved_problems:
                color = "#4CAF50"  # Green for solved
                hover_color = "#45A049"
            elif problem_number in attempted_problems:
                color = "#FFC107"  # Yellow for attempted
                hover_color = "#FFB300"
            else:
                color = "#2D2D2D"  # Gray for not attempted
                hover_color = "#3D3D3D"
            
            # Store original color if not already stored
            if problem_number not in self.original_colors:
                self.original_colors[problem_number] = color
            
            # If this is the current square, add highlight border
            if problem_number == self.current_square:
                square.setStyleSheet(f"""
                    QFrame {{
                        background-color: {color};
                        border: 2px solid #569CD6;
                    }}
                    QFrame:hover {{
                        background-color: {hover_color};
                    }}
                """)
            else:
                square.setStyleSheet(f"""
                    QFrame {{
                        background-color: {color};
                        border: 1px solid #3D3D3D;
                    }}
                    QFrame:hover {{
                        background-color: {hover_color};
                    }}
                """)
    
    def update_tooltip(self, problem_number, difficulty, percentage):
        """Update the tooltip for a specific problem square."""
        square = self.problem_squares.get(problem_number)
        if square:
            difficulty_stars = '★' * difficulty + '☆' * (5 - difficulty)
            square.setToolTip(f"Problem {problem_number}\nDifficulty: {difficulty_stars} ({percentage}%)")
    
    def filter_by_difficulty(self, difficulty):
        """Filter grid squares by difficulty."""
        for problem_number, square in self.problem_squares.items():
            if square:
                # Get the difficulty from the problem manager
                current_difficulty = self.problem_manager.get_problem_difficulty(problem_number)
                
                if current_difficulty == difficulty:
                    # Highlight matching difficulty
                    square.setStyleSheet("""
                        QFrame {
                            background-color: #FFD700;
                            border: 1px solid #3D3D3D;
                        }
                        QFrame:hover {
                            background-color: #FFC000;
                        }
                    """)
                else:
                    # Restore original color based on problem status
                    if problem_number in self.solved_problems:
                        color = "#4CAF50"  # Green for solved
                        hover_color = "#45A049"
                    elif problem_number in self.attempted_problems:
                        color = "#FFC107"  # Yellow for attempted
                        hover_color = "#FFB300"
                    else:
                        color = "#2D2D2D"  # Gray for not attempted
                        hover_color = "#3D3D3D"
                    
                    square.setStyleSheet(f"""
                        QFrame {{
                            background-color: {color};
                            border: 1px solid #3D3D3D;
                        }}
                        QFrame:hover {{
                            background-color: {hover_color};
                        }}
                    """) 