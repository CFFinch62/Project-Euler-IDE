from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QPushButton,
                            QLabel, QTextEdit, QMessageBox, QProgressBar)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QColor

class TutorialDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Tutorial")
        self.setMinimumWidth(600)
        self.setMinimumHeight(400)
        
        # Create layout
        layout = QVBoxLayout()
        
        # Create title label
        self.title_label = QLabel()
        self.title_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(self.title_label)
        
        # Create content area
        self.content_label = QLabel()
        self.content_label.setWordWrap(True)
        layout.addWidget(self.content_label)
        
        # Create progress bar
        self.progress_bar = QProgressBar()
        layout.addWidget(self.progress_bar)
        
        # Create navigation buttons
        button_layout = QHBoxLayout()
        self.prev_button = QPushButton("Previous")
        self.prev_button.clicked.connect(self.previous_step)
        self.next_button = QPushButton("Next")
        self.next_button.clicked.connect(self.next_step)
        self.close_button = QPushButton("Close Tutorial")
        self.close_button.clicked.connect(self.close)
        button_layout.addWidget(self.prev_button)
        button_layout.addWidget(self.next_button)
        button_layout.addWidget(self.close_button)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        
        # Initialize tutorial state
        self.current_tutorial = None
        self.current_step = 0
        self.highlight_timer = QTimer()
        self.highlight_timer.timeout.connect(self.update_highlight)
        
        # Load tutorials
        self.load_tutorials()

    def load_tutorials(self):
        """Load tutorials from the tutorial manager."""
        from tutorial_manager import TutorialManager
        self.tutorial_manager = TutorialManager()
        self.tutorials = self.tutorial_manager.load_tutorials()

    def start_tutorial(self, tutorial_name):
        """Start a specific tutorial."""
        self.current_tutorial = self.tutorial_manager.get_tutorial(tutorial_name)
        if self.current_tutorial:
            self.current_step = 0
            self.update_display()
            self.show()

    def update_display(self):
        """Update the display with current tutorial step."""
        if not self.current_tutorial:
            return
            
        step = self.current_tutorial["steps"][self.current_step]
        self.title_label.setText(step["title"])
        self.content_label.setText(step["content"])
        
        # Update progress bar
        total_steps = len(self.current_tutorial["steps"])
        self.progress_bar.setMaximum(total_steps - 1)
        self.progress_bar.setValue(self.current_step)
        
        # Update button states
        self.prev_button.setEnabled(self.current_step > 0)
        self.next_button.setEnabled(self.current_step < total_steps - 1)
        
        # Handle step actions
        self.handle_step_action(step)

    def handle_step_action(self, step):
        """Handle the action specified in the current step."""
        action = step.get("action", "none")
        params = step.get("params", {})
        
        if action == "highlight_areas":
            self.highlight_interface_areas()
        elif action == "highlight_button":
            self.highlight_button(params.get("button"))
        elif action == "select_problem":
            self.parent().load_problem_by_number(params.get("problem_number"))

    def highlight_interface_areas(self):
        """Highlight different areas of the interface."""
        # Implementation would depend on your interface structure
        pass

    def highlight_button(self, button_name):
        """Highlight a specific button."""
        # Implementation would depend on your interface structure
        pass

    def previous_step(self):
        """Go to the previous step in the tutorial."""
        if self.current_step > 0:
            self.current_step -= 1
            self.update_display()

    def next_step(self):
        """Go to the next step in the tutorial."""
        if self.current_step < len(self.current_tutorial["steps"]) - 1:
            self.current_step += 1
            self.update_display()
        else:
            self.close()

    def update_highlight(self):
        """Update the highlight animation."""
        # Implementation would depend on your interface structure
        pass 