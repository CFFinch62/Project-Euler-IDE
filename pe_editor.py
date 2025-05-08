import sys
import re
import traceback
import time
import os
import tempfile
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QTextEdit, QPushButton, QLabel, 
                            QSplitter, QComboBox, QFrame, QMessageBox,
                            QProgressBar, QStatusBar, QTabWidget, QFileDialog,
                            QListWidget, QInputDialog, QLineEdit, QDialog, QToolBar,
                            QGroupBox)
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QFont, QTextCharFormat, QColor, QAction, QDesktopServices
from problem_manager import ProblemManager
from progress_grid import ProblemGrid
from settings_manager import SettingsManager
from settings_dialog import SettingsDialog
from ui.code_editor import CodeEditor
from ui.syntax_highlighter import PythonHighlighter

# Set Qt platform plugin path
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = '/opt/anaconda3/lib/python3.12/site-packages/PyQt6/Qt6/plugins/platforms'

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Initialize managers first
        self.settings_manager = SettingsManager()
        self.problem_manager = ProblemManager()
        
        # Set up the main window
        self.setWindowTitle("Project Euler Editor")
        self.setGeometry(100, 100, 1200, 800)
        
        # Create menu bar
        menu_bar = self.menuBar()
        
        # File menu
        file_menu = menu_bar.addMenu("File")
        settings_action = QAction("Settings", self)
        settings_action.triggered.connect(self.show_settings_dialog)
        file_menu.addAction(settings_action)
        
        # View menu
        view_menu = menu_bar.addMenu("View")
        progress_action = QAction("Progress", self)
        progress_action.triggered.connect(self.show_progress_dialog)
        view_menu.addAction(progress_action)
        
        # Help menu
        help_menu = menu_bar.addMenu("Help")
        welcome_action = QAction("Welcome", self)
        welcome_action.triggered.connect(self.show_welcome_dialog)
        help_menu.addAction(welcome_action)
        
        # Add Templates menu item
        templates_action = QAction("Code Templates", self)
        templates_action.triggered.connect(self.show_templates_dialog)
        help_menu.addAction(templates_action)
        
        # Add Tutorials menu item
        tutorials_action = QAction("Tutorials", self)
        tutorials_action.triggered.connect(self.show_tutorials_dialog)
        help_menu.addAction(tutorials_action)
        
        # Add Tutorial Editor menu item
        tutorial_editor_action = QAction("Tutorial Editor", self)
        tutorial_editor_action.triggered.connect(self.show_tutorial_editor_dialog)
        help_menu.addAction(tutorial_editor_action)
        
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about_dialog)
        help_menu.addAction(about_action)
        
        info_action = QAction("Info", self)
        info_action.triggered.connect(self.show_info_dialog)
        help_menu.addAction(info_action)
        
        # Create status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        
        # Add progress bar to status bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedWidth(100)
        self.progress_bar.setVisible(False)
        self.status_bar.addPermanentWidget(self.progress_bar)
        
        # Add execution time label to status bar
        self.execution_time_label = QLabel()
        self.execution_time_label.setVisible(False)
        self.status_bar.addPermanentWidget(self.execution_time_label)
        
        # Create main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)
        
        # Create splitter for left and right panels
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Left panel (Problem description and progress grid)
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        
        # Problem description
        self.problem_description = QTextEdit()
        self.problem_description.setReadOnly(True)
        left_layout.addWidget(self.problem_description)
        
        # Data file indicator
        self.data_file_indicator = QLabel()
        self.data_file_indicator.setStyleSheet("""
            QLabel {
                background-color: #2D2D2D;
                color: #569CD6;
                padding: 5px;
                border: 1px solid #3D3D3D;
                border-radius: 3px;
            }
        """)
        self.data_file_indicator.setVisible(False)
        self.data_file_indicator.mousePressEvent = self.handle_data_file_click
        left_layout.addWidget(self.data_file_indicator)
        
        # Store current download URL
        self.current_download_url = None
        
        # Progress grid
        self.progress_grid = ProblemGrid(self.problem_manager)
        self.progress_grid.setFixedHeight(400)  # Limit the height
        self.progress_grid.square_clicked_signal.connect(self.load_problem_by_number)
        left_layout.addWidget(self.progress_grid)
        
        # Right panel (Code editor and helper files)
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        
        # Tab widget for solution, helper files, and data files
        self.tab_widget = QTabWidget()
        
        # Solution tab
        solution_tab = QWidget()
        solution_layout = QVBoxLayout(solution_tab)
        self.code_editor = CodeEditor(settings_manager=self.settings_manager)
        solution_layout.addWidget(self.code_editor)
        self.tab_widget.addTab(solution_tab, "Solution")
        
        # Helper files tab
        helpers_tab = QWidget()
        helpers_layout = QVBoxLayout(helpers_tab)
        
        # Helper files list and controls
        helpers_controls = QHBoxLayout()
        self.add_helper_button = QPushButton("Add Helper File")
        self.delete_helper_button = QPushButton("Delete Helper File")
        self.test_helper_button = QPushButton("Test Helper Function")
        self.save_helper_button = QPushButton("Save Helper File")
        self.load_helper_button = QPushButton("Load Helper File")
        helpers_controls.addWidget(self.add_helper_button)
        helpers_controls.addWidget(self.delete_helper_button)
        helpers_controls.addWidget(self.test_helper_button)
        helpers_controls.addWidget(self.save_helper_button)
        helpers_controls.addWidget(self.load_helper_button)
        
        # Helper files list
        self.helper_files_list = QListWidget()
        self.helper_files_list.setStyleSheet("""
            QListWidget {
                background-color: #1E1E1E;
                color: #D4D4D4;
                border: none;
                padding: 5px;
            }
        """)
        self.helper_files_list.setFixedHeight(100)  # Set fixed height for the list
        
        # Helper editor
        self.helpers_editor = CodeEditor(settings_manager=self.settings_manager)
        helpers_layout.addLayout(helpers_controls)
        helpers_layout.addWidget(self.helper_files_list)
        helpers_layout.addWidget(self.helpers_editor)
        
        # Add helpers tab to tab widget
        self.tab_widget.addTab(helpers_tab, "Helper Files")
        
        # Connect helper files list selection to load helper file
        self.helper_files_list.currentItemChanged.connect(self.load_helper_file)
        
        # Apply initial settings to helper editor
        self.settings_manager.update_helper_editor_settings(
            font_family="Consolas",
            font_size=12,
            text_color="#FFFF00",  # Yellow
            background_color="#000066"  # Dark blue
        )
        self.settings_manager.apply_helper_editor_settings(self.helpers_editor)
        
        # Add data files tab
        data_files_tab = QWidget()
        data_files_layout = QVBoxLayout(data_files_tab)
        
        # Data preview section
        data_preview_widget = QWidget()
        data_preview_layout = QVBoxLayout(data_preview_widget)
        self.data_preview_label = QLabel("Data Preview:")
        self.data_preview_label.setStyleSheet("color: yellow;")
        data_preview_layout.addWidget(self.data_preview_label)
        self.data_preview_text = QTextEdit()
        self.data_preview_text.setReadOnly(True)
        self.data_preview_text.setStyleSheet("""
            QTextEdit {
                background-color: #000066;
                color: yellow;
                border: none;
                padding: 5px;
            }
        """)
        data_preview_layout.addWidget(self.data_preview_text)
        
        # Add widgets to splitter
        data_splitter = QSplitter(Qt.Orientation.Vertical)
        
        # Data info section
        data_info_widget = QWidget()
        data_info_layout = QVBoxLayout(data_info_widget)
        self.data_files_text = QTextEdit()
        self.data_files_text.setReadOnly(True)
        self.data_files_text.setFixedHeight(100)
        self.data_files_text.setStyleSheet("""
            QTextEdit {
                background-color: #000066;
                color: yellow;
                border: none;
                padding: 5px;
            }
        """)
        data_info_layout.addWidget(self.data_files_text)
        
        # Add insert code button
        self.insert_data_code_button = QPushButton("Insert Data Loading Code")
        self.insert_data_code_button.clicked.connect(self.insert_data_loading_code)
        data_info_layout.addWidget(self.insert_data_code_button)
        
        # Add widgets to splitter
        data_splitter.addWidget(data_info_widget)
        data_splitter.addWidget(data_preview_widget)
        data_files_layout.addWidget(data_splitter)
        
        # Set initial splitter sizes to give more space to preview
        data_splitter.setSizes([150, 450])  # Info area: 150, Preview area: 450
        
        self.tab_widget.addTab(data_files_tab, "Data Files")
        
        right_layout.addWidget(self.tab_widget)
        
        # Add panels to splitter
        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        
        # Set initial splitter sizes
        splitter.setSizes([400, 800])
        
        # Add splitter to main layout
        main_layout.addWidget(splitter)
        
        # Create bottom bar with buttons
        bottom_bar = QHBoxLayout()
        self.run_button = QPushButton("Run Code")
        self.hint_button = QPushButton("Get Hint")
        self.save_button = QPushButton("Save Solution")
        self.mark_solved_button = QPushButton("Mark as Solved")
        bottom_bar.addWidget(self.run_button)
        bottom_bar.addWidget(self.hint_button)
        bottom_bar.addWidget(self.save_button)
        bottom_bar.addWidget(self.mark_solved_button)
        
        # Add bottom bar to main layout
        main_layout.addLayout(bottom_bar)
        
        # Set up syntax highlighters
        self.highlighter = PythonHighlighter(self.code_editor.document(), self.settings_manager)
        self.helpers_highlighter = PythonHighlighter(self.helpers_editor.document(), self.settings_manager)
        
        # Connect signals
        self.run_button.clicked.connect(self.run_code)
        self.hint_button.clicked.connect(self.show_hint)
        self.save_button.clicked.connect(self.save_solution)
        self.mark_solved_button.clicked.connect(self.mark_problem_solved)
        self.add_helper_button.clicked.connect(self.add_helper_file)
        self.delete_helper_button.clicked.connect(self.delete_helper_file)
        self.test_helper_button.clicked.connect(self.test_helper_function)
        self.save_helper_button.clicked.connect(self.save_current_helper_file)
        self.load_helper_button.clicked.connect(self.load_shared_helper_file)
        self.helper_files_list.currentItemChanged.connect(self.load_helper_file)
        
        # Apply settings after all UI components are created
        self.apply_settings()
        
        # Force rehighlighting of both editors to apply saved settings
        if hasattr(self, 'highlighter'):
            self.highlighter.update_highlighting_rules()
            self.highlighter.rehighlight()
        if hasattr(self, 'helpers_highlighter'):
            self.helpers_highlighter.update_highlighting_rules()
            self.helpers_highlighter.rehighlight()
        
        # Load the first problem
        self.load_problem_by_number(1)

    def handle_data_file_click(self, event):
        """Handle click on data file indicator to download missing file."""
        if self.current_download_url:
            QDesktopServices.openUrl(QUrl(self.current_download_url))
        # Call the parent class's event handler
        super(QLabel, self.data_file_indicator).mousePressEvent(event)

    def load_problem_by_number(self, problem_number):
        """Load a problem by its number."""
        try:
            # Load problem description
            problem_data = self.problem_manager.load_problem(problem_number)
            self.problem_text = problem_data["text"]
            
            # Get difficulty information
            difficulty = self.problem_manager.get_problem_difficulty(problem_number)
            difficulty_percentage = self.problem_manager.get_problem_difficulty_percentage(problem_number)
            
            # Add difficulty information to the display
            difficulty_text = f"\n\nDifficulty: {'★' * difficulty}{'☆' * (5 - difficulty)} ({difficulty_percentage}%)"
            display_text = self.problem_text + difficulty_text
            
            # Extract hints from the problem text
            hint_start = self.problem_text.find("Hint:")
            if hint_start != -1:
                self.current_hints = self.problem_text[hint_start:].strip()
                display_text = display_text[:hint_start].strip() + difficulty_text
            else:
                self.current_hints = "No hints available for this problem."
            
            # Display the problem text with difficulty
            self.problem_description.setPlainText(display_text)
            
            # Update grid tooltips with difficulty information
            self.update_grid_tooltips()
            
            # Check for info file and add simple indicator
            info_path = os.path.join("info", f"{problem_number:03d}_overview.pdf")
            if os.path.exists(info_path):
                display_text += "\n\n📄 Additional information is available for this problem in the info directory."
            
            # Display the problem text
            self.problem_description.setPlainText(display_text)
            
            # Check for data file requirements
            self.current_data_info = self.problem_manager.get_problem_data_info(problem_number)
            if self.current_data_info['has_data']:
                # Check if the data file exists
                try:
                    status = self.problem_manager.check_data_file(self.current_data_info['file'])
                    if not status['exists']:
                        self.data_file_indicator.setText(
                            f"⚠️ This problem requires a data file that is missing:\n"
                            f"File: {self.current_data_info['file']}\n"
                            f"Click here to download it"
                        )
                        self.data_file_indicator.setStyleSheet("""
                            QLabel {
                                background-color: #2D2D2D;
                                color: #FF6B6B;
                                padding: 5px;
                                border: 1px solid #3D3D3D;
                                border-radius: 3px;
                            }
                        """)
                        self.current_download_url = status['download_url']
                        self.data_file_indicator.setCursor(Qt.CursorShape.PointingHandCursor)
                    else:
                        self.data_file_indicator.setText(
                            f"This problem uses external data: {self.current_data_info['description']}\n"
                            f"File: {self.current_data_info['file']}\n"
                            f"Use: {self.current_data_info['method']}()"
                        )
                        self.data_file_indicator.setStyleSheet("""
                            QLabel {
                                background-color: #2D2D2D;
                                color: #569CD6;
                                padding: 5px;
                                border: 1px solid #3D3D3D;
                                border-radius: 3px;
                            }
                        """)
                        self.current_download_url = None
                        self.data_file_indicator.setCursor(Qt.CursorShape.ArrowCursor)
                        
                        # Load and display data file preview
                        try:
                            data_content = self.problem_manager.load_data_file_preview(self.current_data_info['file'])
                            self.data_preview_text.setPlainText(data_content)
                        except Exception as e:
                            self.data_preview_text.setPlainText(f"Error loading data preview: {str(e)}")
                except Exception as e:
                    self.data_file_indicator.setText(f"Error checking data file: {str(e)}")
                    self.data_file_indicator.setStyleSheet("""
                        QLabel {
                            background-color: #2D2D2D;
                            color: #FF6B6B;
                            padding: 5px;
                            border: 1px solid #3D3D3D;
                            border-radius: 3px;
                        }
                    """)
                    self.current_download_url = None
                    self.data_file_indicator.setCursor(Qt.CursorShape.ArrowCursor)
                
                self.data_file_indicator.setVisible(True)
                
                # Update data files tab
                self.data_files_text.setPlainText(
                    f"Data File: {self.current_data_info['file']}\n"
                    f"Description: {self.current_data_info['description']}\n\n"
                    f"Example Code:\n{self.current_data_info['example']}"
                )
                self.tab_widget.setTabEnabled(2, True)  # Enable data files tab
            else:
                self.data_file_indicator.setVisible(False)
                self.data_files_text.setPlainText("This problem does not use external data files.")
                self.data_preview_text.setPlainText("No data file required for this problem.")
                self.tab_widget.setTabEnabled(2, False)  # Disable data files tab
            
            # Load solution if it exists
            solution = self.problem_manager.load_solution(problem_number)
            if solution:
                self.code_editor.setPlainText(solution)
            else:
                # Create a template for new problems
                template = f'''"""
Project Euler Problem {problem_number}
"""

def solve():
    """
    Your solution goes here.
    This function should return the answer to the problem.
    """
    # Your code here
    return None

# Note: The solve() function is required.
# Do not use print statements or other output methods.
# The function should return the final answer.
'''
                self.code_editor.setPlainText(template)
            
            # Load helper files list
            self.update_helper_files_list(problem_number)
            
            # Update status
            self.update_status_bar(problem_number)
            
            # Update the grid to show the current problem and its status
            self.progress_grid.current_square = problem_number
            self.update_progress()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load problem {problem_number}: {str(e)}")

    def run_code(self):
        """Run the current solution and display the result."""
        try:
            # Get the current problem number
            current_square = self.progress_grid.get_current_square()
            if not current_square:
                return
            problem_number = int(current_square.number_label.text())
            
            # Disable run button and show progress
            self.run_button.setEnabled(False)
            self.progress_bar.setVisible(True)
            self.progress_bar.setRange(0, 0)  # Indeterminate progress
            self.execution_time_label.setVisible(True)
            self.status_bar.showMessage("Initializing execution...")
            
            # Get the code from the editor
            code = self.code_editor.toPlainText()
            
            # Clear any previous error highlights
            self.code_editor.clear_error_highlights()
            
            # Get helper files
            helper_files = self.problem_manager.load_helper_files(problem_number)
            
            # Create a temporary directory for helper files
            with tempfile.TemporaryDirectory() as temp_dir:
                # Save helper files to temp directory
                for filename, content in helper_files.items():
                    with open(os.path.join(temp_dir, filename), 'w') as f:
                        f.write(content)
                
                # Add temp directory to Python path
                sys.path.insert(0, temp_dir)
                
                try:
                    self.status_bar.showMessage("Running solution...")
                    start_time = time.time()
                    result = self.problem_manager.run_solution(problem_number, code)
                    execution_time = time.time() - start_time
                    
                    # Update execution time display
                    self.execution_time_label.setText(f"Execution time: {execution_time:.2f}s")
                    
                    if result["success"]:
                        self.status_bar.showMessage("Processing results...")
                        # Save the solution with execution time
                        self.problem_manager.save_solution(problem_number, code, execution_time)
                        
                        # Show result with execution time
                        msg = QMessageBox()
                        msg.setWindowTitle("Success")
                        msg.setText(f"Result: {result['result']}\nExecution time: {execution_time:.6f} seconds")
                        
                        # Add warning if execution time is too long
                        if execution_time > 60:
                            msg.setInformativeText("⚠️ Warning: This solution takes more than 1 minute to run.\nConsider optimizing your code for better performance.")
                        
                        msg.exec()
                        
                        # Update progress
                        self.update_progress()
                        self.update_status_bar(problem_number)
                    else:
                        # Show error message
                        msg = QMessageBox()
                        msg.setWindowTitle("Error")
                        msg.setText(f"Error: {result['error']}")
                        
                        # If we have line number information, highlight the error line
                        if 'line_number' in result and result['line_number'] is not None:
                            self.code_editor.highlight_error_line(result['line_number'], result['error'])
                        
                        msg.exec()
                finally:
                    # Remove temp directory from Python path
                    sys.path.remove(temp_dir)
                    # Reset UI state
                    self.run_button.setEnabled(True)
                    self.progress_bar.setVisible(False)
                    self.execution_time_label.setVisible(False)
                    self.status_bar.showMessage("Ready")
                
        except FileNotFoundError as e:
            # Handle missing data file error
            error_msg = str(e)
            if hasattr(e, 'download_url'):
                msg = QMessageBox()
                msg.setWindowTitle("Missing Data File")
                msg.setText(error_msg)
                msg.setInformativeText("Would you like to download the required data file?")
                msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
                msg.setDefaultButton(QMessageBox.StandardButton.Yes)
                
                if msg.exec() == QMessageBox.StandardButton.Yes:
                    QDesktopServices.openUrl(QUrl(e.download_url))
        except Exception as e:
            msg = QMessageBox()
            msg.setWindowTitle("Error")
            msg.setText(f"Error running code: {str(e)}")
            msg.exec()
        finally:
            # Ensure UI is reset even if an error occurs
            self.run_button.setEnabled(True)
            self.progress_bar.setVisible(False)
            self.execution_time_label.setVisible(False)
            self.status_bar.showMessage("Ready")

    def show_hint(self):
        """Show the hint for the current problem."""
        if not self.current_hints:
            QMessageBox.information(self, "Hint", "No hints available for this problem.")
            return
            
        msg = QMessageBox()
        msg.setWindowTitle("Hint")
        msg.setText(self.current_hints)
        msg.exec()

    def save_solution(self):
        """Save the current solution."""
        current_square = self.progress_grid.get_current_square()
        if not current_square:
            QMessageBox.warning(self, "Warning", "No problem selected")
            return
            
        problem_number = int(current_square.number_label.text())
        code = self.code_editor.toPlainText()
        
        if self.problem_manager.save_solution(problem_number, code):
            msg = QMessageBox()
            msg.setWindowTitle("Success")
            msg.setText("Solution saved successfully!")
            msg.exec()
        else:
            msg = QMessageBox()
            msg.setWindowTitle("Error")
            msg.setText("Failed to save solution.")
            msg.exec()

    def mark_problem_solved(self):
        """Mark the current problem as solved."""
        current_square = self.progress_grid.get_current_square()
        if not current_square:
            QMessageBox.warning(self, "Warning", "No problem selected")
            return
            
        problem_number = int(current_square.number_label.text())
        self.problem_manager.mark_problem_solved(problem_number)
        
        # Update streak information
        from datetime import datetime
        today = datetime.now().strftime('%Y-%m-%d')
        last_solved_date = self.settings_manager.settings.get('last_solved_date', None)
        
        if last_solved_date:
            last_date = datetime.strptime(last_solved_date, '%Y-%m-%d')
            today_date = datetime.strptime(today, '%Y-%m-%d')
            if (today_date - last_date).days == 1:
                # Consecutive day
                self.settings_manager.settings['current_streak'] = self.settings_manager.settings.get('current_streak', 0) + 1
                if self.settings_manager.settings['current_streak'] > self.settings_manager.settings.get('longest_streak', 0):
                    self.settings_manager.settings['longest_streak'] = self.settings_manager.settings['current_streak']
            elif (today_date - last_date).days > 1:
                # Streak broken
                self.settings_manager.settings['current_streak'] = 1
        else:
            # First problem solved
            self.settings_manager.settings['current_streak'] = 1
            self.settings_manager.settings['longest_streak'] = 1
        
        self.settings_manager.settings['last_solved_date'] = today
        self.settings_manager.save_settings()
        
        self.update_progress()
        self.update_status_bar(problem_number)
        
        msg = QMessageBox()
        msg.setWindowTitle("Success")
        msg.setText(f"Problem {problem_number} marked as solved!")
        msg.exec()

    def update_progress(self):
        """Update the progress grid with solved and attempted problems."""
        progress = self.problem_manager.get_progress()
        self.progress_grid.update_progress(
            progress["solved_problems"],
            progress["attempted_problems"]
        )
        
        # Update the current square's color if it exists
        if self.progress_grid.current_square:
            current_number = self.progress_grid.current_square
            self.progress_grid.update_progress(
                progress["solved_problems"],
                progress["attempted_problems"]
            )

    def update_status_bar(self, problem_number):
        progress = self.problem_manager.get_progress()
        status = f"Problem {problem_number}"
        if self.problem_manager.is_problem_solved(problem_number):
            status += " ✓"
        self.status_bar.showMessage(status)

    def show_settings_dialog(self):
        """Show the settings dialog and apply changes if accepted."""
        dialog = SettingsDialog(self)
        dialog.set_settings(self.settings_manager.settings)
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            new_settings = dialog.get_settings()
            self.settings_manager.settings = new_settings
            self.settings_manager.save_settings()
            
            # Update syntax highlighting colors
            if "syntax_highlighting" in new_settings:
                self.settings_manager.update_highlighting_colors(new_settings["syntax_highlighting"])
            
            # Apply all settings
            self.apply_settings()
            
            # Force rehighlighting of both editors
            if hasattr(self, 'highlighter'):
                self.highlighter.update_highlighting_rules()
                self.highlighter.rehighlight()
            if hasattr(self, 'helpers_highlighter'):
                self.helpers_highlighter.update_highlighting_rules()
                self.helpers_highlighter.rehighlight()
    
    def apply_settings(self):
        """Apply current settings to the UI."""
        settings = self.settings_manager.settings
        
        # Apply problem text settings
        self.settings_manager.apply_problem_text_settings(self.problem_description)
        
        # Apply code editor settings
        self.settings_manager.apply_code_editor_settings(self.code_editor)
        # Force line number area update for code editor
        self.code_editor.update_line_number_area_width(0)
        
        # Apply helper editor settings
        self.settings_manager.apply_helper_editor_settings(self.helpers_editor)
        # Force line number area update for helper editor
        self.helpers_editor.update_line_number_area_width(0)
        
        # Apply data files settings
        self.settings_manager.apply_data_files_settings(self.data_files_text)
        self.settings_manager.apply_data_files_settings(self.data_preview_text)
        self.data_preview_label.setStyleSheet(f"color: {settings['data_files']['text_color']};")

    def add_helper_file(self):
        """Add a new helper file."""
        # Get filename from user
        filename, ok = QInputDialog.getText(
            self,
            "Add Helper File",
            "Enter filename (e.g., gpf.py):",
            QLineEdit.EchoMode.Normal,
            "gpf.py"
        )
        
        if ok and filename:
            if not filename.endswith('.py'):
                filename += '.py'
            
            # Create template content
            template = '''"""
Helper functions for Project Euler problems
"""

def example_function(arg1, arg2=None):
    """
    Example helper function.
    
    Args:
        arg1: First argument
        arg2: Optional second argument
        
    Returns:
        Result of the operation
    """
    # Your code here
    pass

# Add more helper functions below
'''
            
            # Save the helper file
            if self.problem_manager.save_helper_file(filename, template):
                QMessageBox.information(self, "Success", f"Helper file {filename} created successfully")
            else:
                QMessageBox.critical(self, "Error", "Failed to create helper file")

    def delete_helper_file(self):
        """Delete the selected helper file."""
        current_item = self.helper_files_list.currentItem()
        if current_item is None:
            QMessageBox.warning(self, "Warning", "No helper file selected")
            return
        
        current_square = self.progress_grid.get_current_square()
        if not current_square:
            QMessageBox.warning(self, "Warning", "No problem selected")
            return
            
        problem_number = int(current_square.number_label.text())
        filename = current_item.text()
        
        reply = QMessageBox.question(
            self,
            "Delete Helper File",
            f"Are you sure you want to remove {filename} from problem {problem_number}?\n"
            f"This will not delete the helper file itself, just remove it from this problem.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                if self.problem_manager.unassign_helper_from_problem(problem_number, filename):
                    self.update_helper_files_list(problem_number)
                    self.helpers_editor.clear()
                    QMessageBox.information(self, "Success", f"Helper file {filename} removed from problem {problem_number}")
                else:
                    QMessageBox.critical(self, "Error", f"Failed to remove helper file {filename}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error removing helper file: {str(e)}")

    def test_helper_function(self):
        """Test a function from the current helper file."""
        # Get the current problem number
        current_square = self.progress_grid.get_current_square()
        if not current_square:
            return
        problem_number = int(current_square.number_label.text())
        
        # Get the current helper file
        current_item = self.helper_files_list.currentItem()
        if current_item is None:
            QMessageBox.warning(self, "Warning", "No helper file selected")
            return
        
        # Get function name from user
        function_name, ok = QInputDialog.getText(
            self,
            "Test Helper Function",
            "Enter function name to test:",
            QLineEdit.EchoMode.Normal
        )
        
        if not ok or not function_name:
            return
        
        # Get function arguments from user
        args_text, ok = QInputDialog.getText(
            self,
            "Test Helper Function",
            "Enter function arguments (comma-separated):",
            QLineEdit.EchoMode.Normal
        )
        
        if not ok:
            return
        
        # Clear any previous error highlights
        self.helpers_editor.clear_error_highlights()
        
        # Parse arguments
        args = []
        kwargs = {}
        
        if args_text.strip():
            try:
                # Split by commas but preserve those within quotes
                parts = []
                current = ""
                in_quotes = False
                for char in args_text:
                    if char in ['"', "'"]:
                        in_quotes = not in_quotes
                        current += char
                    elif char == ',' and not in_quotes:
                        parts.append(current.strip())
                        current = ""
                    else:
                        current += char
                if current:
                    parts.append(current.strip())
                
                # Process each part
                for part in parts:
                    if '=' in part and not any(c in part for c in ['"', "'", '(', ')']):
                        # Keyword argument
                        key, value = part.split('=', 1)
                        kwargs[key.strip()] = eval(value.strip())
                    else:
                        # Positional argument
                        args.append(eval(part.strip()))
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Invalid arguments: {str(e)}")
                return
        
        # Test the function
        result = self.problem_manager.test_helper_function(problem_number, function_name, *args, **kwargs)
        
        msg = QMessageBox()
        msg.setWindowTitle("Test Result")
        
        if result["success"]:
            msg.setText(f"Result: {result['result']}\nExecution Time: {result['execution_time']}")
        else:
            error_msg = f"Error: {result['error']}"
            if 'traceback' in result:
                error_msg += f"\n\nTraceback:\n{result['traceback']}"
            msg.setText(error_msg)
            
            # If we have line number information, highlight the error line
            if 'line_number' in result and result['line_number'] is not None:
                self.helpers_editor.highlight_error_line(result['line_number'], result['error'])
        
        msg.exec()

    def load_helper_file(self, current, previous):
        """Load the selected helper file into the editor."""
        # Clear the editor if no file is selected
        if current is None:
            self.helpers_editor.clear()
            return
        
        # Load the new file
        current_square = self.progress_grid.get_current_square()
        if not current_square:
            return
            
        problem_number = int(current_square.number_label.text())
        filename = current.text()
        
        # Get helper files for this problem
        helper_files = self.problem_manager.load_helper_files(problem_number)
        if filename in helper_files:
            self.helpers_editor.setPlainText(helper_files[filename])
            # Apply settings after loading the content
            self.settings_manager.apply_helper_editor_settings(self.helpers_editor)

    def save_current_helper_file(self):
        """Save the current helper file."""
        current_item = self.helper_files_list.currentItem()
        if current_item is None:
            QMessageBox.warning(self, "Warning", "No helper file selected")
            return
            
        filename = current_item.text()
        content = self.helpers_editor.toPlainText()
        
        if self.problem_manager.save_helper_file(filename, content):
            QMessageBox.information(self, "Success", f"Helper file {filename} saved successfully")
        else:
            QMessageBox.critical(self, "Error", f"Failed to save helper file {filename}")

    def update_helper_files_list(self, problem_number):
        """Update the helper files list for the current problem."""
        self.helper_files_list.clear()
        helper_files = self.problem_manager.load_helper_files(problem_number)
        for filename in helper_files.keys():
            self.helper_files_list.addItem(filename)
        if self.helper_files_list.count() > 0:
            self.helper_files_list.setCurrentRow(0)

    def copy_data_example(self):
        """Copy the data file example code to clipboard."""
        if self.current_data_info and self.current_data_info['has_data']:
            QApplication.clipboard().setText(self.current_data_info['example'])
            self.status_bar.showMessage("Example code copied to clipboard", 3000)

    def show_welcome_dialog(self):
        """Show welcome dialog for first-time users."""
        welcome_text = """
        <h2>Welcome to Project Euler Editor!</h2>
        <p>This application helps you solve Project Euler problems and build your coding portfolio.</p>
        
        <h3>Getting Started:</h3>
        <ol>
            <li>Click on any problem number in the grid to load it</li>
            <li>Read the problem description carefully</li>
            <li>Write your solution in the code editor</li>
            <li>Click "Run Code" to test your solution</li>
            <li>Save your solution to build your portfolio</li>
        </ol>
        
        <h3>Features:</h3>
        <ul>
            <li>Syntax highlighting for better code readability</li>
            <li>Helper files to organize your code</li>
            <li>Progress tracking to see your improvement</li>
            <li>Hints when you get stuck</li>
            <li>Data file management for problems that need external data</li>
        </ul>
        
        <p>Click "OK" to start your coding journey!</p>
        """
        
        msg = QMessageBox()
        msg.setWindowTitle("Welcome")
        msg.setTextFormat(Qt.TextFormat.RichText)
        msg.setText(welcome_text)
        msg.exec()

    def show_progress_dialog(self):
        """Show progress dialog."""
        progress = self.problem_manager.get_progress()
        solved = progress["solved_problems"]
        attempted = progress["attempted_problems"]
        execution_times = progress.get("execution_times", {})
        
        # Calculate statistics
        total_solved = len(solved)
        total_attempted = len(attempted)
        success_rate = (total_solved / total_attempted * 100) if total_attempted > 0 else 0
        
        # Get streak information
        streak = self.settings_manager.settings.get('current_streak', 0)
        longest_streak = self.settings_manager.settings.get('longest_streak', 0)
        last_solved_date = self.settings_manager.settings.get('last_solved_date', None)
        
        # Check if streak is still active
        if last_solved_date:
            from datetime import datetime, timedelta
            last_date = datetime.strptime(last_solved_date, '%Y-%m-%d')
            today = datetime.now().date()
            if (today - last_date.date()) > timedelta(days=1):
                streak = 0
                self.settings_manager.settings['current_streak'] = 0
                self.settings_manager.save_settings()
        
        # Calculate execution time statistics
        if execution_times:
            avg_time = sum(execution_times.values()) / len(execution_times)
            slow_solutions = [p for p, t in execution_times.items() if t > 60]  # Solutions taking more than 60 seconds
        else:
            avg_time = 0
            slow_solutions = []
        
        # Generate achievements
        achievements = []
        if total_solved >= 10:
            achievements.append("🎯 Novice Solver: Solved 10 problems")
        if total_solved >= 25:
            achievements.append("🏆 Intermediate Solver: Solved 25 problems")
        if total_solved >= 50:
            achievements.append("🌟 Advanced Solver: Solved 50 problems")
        if total_solved >= 100:
            achievements.append("💫 Master Solver: Solved all problems!")
        if success_rate >= 80:
            achievements.append("🎯 High Accuracy: Maintained 80% success rate")
        if streak >= 3:
            achievements.append("🔥 3-Day Streak: Solved problems for 3 consecutive days")
        if streak >= 7:
            achievements.append("⚡ 7-Day Streak: Solved problems for a week straight")
        if streak >= 30:
            achievements.append("🌟 Monthly Streak: Solved problems for a month straight")
        if longest_streak >= 100:
            achievements.append("💫 Century Streak: Maintained a 100-day streak")
        if avg_time < 1 and execution_times:
            achievements.append("⚡ Speed Demon: Average solution time under 1 second")
        
        # Create custom dialog
        dialog = QDialog(self)
        dialog.setWindowTitle("Progress")
        dialog.setMinimumWidth(800)  # Set minimum width for landscape orientation
        dialog.setMinimumHeight(400)
        
        # Create main layout
        main_layout = QHBoxLayout(dialog)
        
        # Left column (Statistics)
        left_column = QVBoxLayout()
        
        # Progress Summary
        summary_group = QGroupBox("Progress Summary")
        summary_layout = QVBoxLayout()
        summary_layout.addWidget(QLabel(f"Total Problems Solved: {total_solved}"))
        summary_layout.addWidget(QLabel(f"Total Problems Attempted: {total_attempted}"))
        summary_layout.addWidget(QLabel(f"Success Rate: {success_rate:.1f}%"))
        summary_layout.addWidget(QLabel(f"Current Streak: {streak} days"))
        summary_layout.addWidget(QLabel(f"Longest Streak: {longest_streak} days"))
        if execution_times:
            summary_layout.addWidget(QLabel(f"Average Execution Time: {avg_time:.3f} seconds"))
        summary_group.setLayout(summary_layout)
        left_column.addWidget(summary_group)
        
        # Add OK button below progress summary
        ok_button = QPushButton("OK")
        ok_button.clicked.connect(dialog.accept)
        left_column.addWidget(ok_button)
        
        # Slow Solutions
        if slow_solutions:
            slow_group = QGroupBox("Slow Solutions (over 60 seconds)")
            slow_layout = QVBoxLayout()
            for problem in slow_solutions:
                time = execution_times[problem]
                slow_layout.addWidget(QLabel(f"Problem {problem}: {time:.1f} seconds"))
            slow_group.setLayout(slow_layout)
            left_column.addWidget(slow_group)
        
        left_column.addStretch()
        main_layout.addLayout(left_column)
        
        # Middle column (Problems)
        middle_column = QVBoxLayout()
        
        # Solved Problems
        solved_group = QGroupBox("Solved Problems")
        solved_layout = QVBoxLayout()
        solved_list = QListWidget()
        for problem in sorted(solved):
            time = execution_times.get(str(problem), "N/A")
            time_str = f" ({time:.3f}s)" if isinstance(time, (int, float)) else ""
            solved_list.addItem(f"Problem {problem}{time_str}")
        solved_layout.addWidget(solved_list)
        solved_group.setLayout(solved_layout)
        middle_column.addWidget(solved_group)
        
        # Attempted Problems
        attempted_group = QGroupBox("Attempted Problems")
        attempted_layout = QVBoxLayout()
        attempted_list = QListWidget()
        for problem in sorted(attempted):
            if problem not in solved:
                attempted_list.addItem(f"Problem {problem}")
        attempted_layout.addWidget(attempted_list)
        attempted_group.setLayout(attempted_layout)
        middle_column.addWidget(attempted_group)
        
        middle_column.addStretch()
        main_layout.addLayout(middle_column)
        
        # Right column (Achievements)
        right_column = QVBoxLayout()
        
        # Achievements
        achievements_group = QGroupBox("Achievements")
        achievements_layout = QVBoxLayout()
        achievements_list = QListWidget()
        for achievement in achievements:
            achievements_list.addItem(achievement)
        achievements_layout.addWidget(achievements_list)
        achievements_group.setLayout(achievements_layout)
        right_column.addWidget(achievements_group)
        
        # Tip
        tip_label = QLabel("Tip: Try solving at least one problem each day to maintain your streak!")
        tip_label.setWordWrap(True)
        right_column.addWidget(tip_label)
        
        right_column.addStretch()
        main_layout.addLayout(right_column)
        
        dialog.exec()

    def load_shared_helper_file(self):
        """Load a helper file and assign it to the current problem."""
        current_square = self.progress_grid.get_current_square()
        if not current_square:
            QMessageBox.warning(self, "Warning", "No problem selected")
            return
            
        problem_number = int(current_square.number_label.text())
        
        # Get list of available helper files
        available_files = self.problem_manager.get_available_helper_files()
        if not available_files:
            QMessageBox.information(self, "Info", "No helper files available")
            return
            
        # Create dialog to select helper file
        dialog = QDialog(self)
        dialog.setWindowTitle("Load Helper File")
        layout = QVBoxLayout(dialog)
        
        # Create list widget for helper files
        list_widget = QListWidget()
        for filename in available_files:
            list_widget.addItem(filename)
        layout.addWidget(list_widget)
        
        # Add buttons
        button_box = QHBoxLayout()
        load_button = QPushButton("Load")
        cancel_button = QPushButton("Cancel")
        button_box.addWidget(load_button)
        button_box.addWidget(cancel_button)
        layout.addLayout(button_box)
        
        # Connect buttons
        load_button.clicked.connect(dialog.accept)
        cancel_button.clicked.connect(dialog.reject)
        
        # Show dialog
        if dialog.exec() == QDialog.DialogCode.Accepted:
            selected_item = list_widget.currentItem()
            if selected_item:
                filename = selected_item.text()
                # Assign the helper file to the problem
                if self.problem_manager.assign_helper_to_problem(problem_number, filename):
                    self.update_helper_files_list(problem_number)
                    QMessageBox.information(self, "Success", f"Helper file {filename} assigned to problem {problem_number}")
                else:
                    QMessageBox.critical(self, "Error", f"Failed to assign helper file {filename}")

    def insert_data_loading_code(self):
        """Insert the data loading code into the code editor."""
        if not self.current_data_info or not self.current_data_info['has_data']:
            return
            
        # Get the loading method from the data info
        method = self.current_data_info['method']
        
        # Create the loading code
        loading_code = f"# Load the data file\n{method} = problem_manager.{method}()\n"
        
        # Get current cursor position
        cursor = self.code_editor.textCursor()
        
        # Find the solve function
        document = self.code_editor.document()
        find_cursor = document.find("def solve():", 0)
        if not find_cursor.isNull():
            # Move cursor to the start of the solve function
            cursor.setPosition(find_cursor.position())
            cursor.movePosition(cursor.MoveOperation.Down)
            cursor.movePosition(cursor.MoveOperation.EndOfLine)
            cursor.insertText("\n" + loading_code)
        else:
            # If solve function not found, insert at cursor position
            cursor.insertText(loading_code)
        
        # Update the cursor
        self.code_editor.setTextCursor(cursor)

    def update_grid_tooltips(self):
        """Update tooltips for all grid squares with difficulty information."""
        for i in range(1, 101):
            difficulty = self.problem_manager.get_problem_difficulty(i)
            percentage = self.problem_manager.get_problem_difficulty_percentage(i)
            self.progress_grid.update_tooltip(i, difficulty, percentage)

    def filter_by_difficulty(self, star_number):
        """Filter grid squares by difficulty when a star is clicked."""
        self.progress_grid.filter_by_difficulty(star_number)

    def show_about_dialog(self):
        """Show the About dialog."""
        about_text = """
        <h2>Project Euler Code Editor</h2>
        <p>Version 1.0</p>
        <p>A specialized editor for solving Project Euler problems in Python.</p>
        <p>© 2024 Fragillidae Software</p>
        """
        
        msg = QMessageBox()
        msg.setWindowTitle("About")
        msg.setTextFormat(Qt.TextFormat.RichText)
        msg.setText(about_text)
        msg.exec()

    def show_info_dialog(self):
        """Show the Info dialog with README.md contents."""
        try:
            with open("README.md", "r") as f:
                readme_content = f.read()
        except FileNotFoundError:
            readme_content = "README.md file not found."
        
        dialog = QDialog(self)
        dialog.setWindowTitle("Info")
        dialog.setMinimumSize(600, 400)
        
        layout = QVBoxLayout(dialog)
        
        text_edit = QTextEdit()
        text_edit.setReadOnly(True)
        text_edit.setPlainText(readme_content)
        layout.addWidget(text_edit)
        
        close_button = QPushButton("Close")
        close_button.clicked.connect(dialog.accept)
        layout.addWidget(close_button)
        
        dialog.exec()

    def show_templates_dialog(self):
        """Show the templates dialog."""
        from templates_dialog import TemplatesDialog
        dialog = TemplatesDialog(self)
        dialog.exec()

    def show_tutorials_dialog(self):
        """Show the tutorials dialog with a list of available tutorials."""
        from tutorial_dialog import TutorialDialog
        from tutorial_manager import TutorialManager
        
        # Create tutorial manager to get available tutorials
        tutorial_manager = TutorialManager()
        tutorials = tutorial_manager.load_tutorials()
        
        if not tutorials:
            QMessageBox.warning(self, "Warning", "No tutorials available")
            return
            
        # Create dialog to select tutorial
        dialog = QDialog(self)
        dialog.setWindowTitle("Select Tutorial")
        dialog.setMinimumWidth(400)
        dialog.setMinimumHeight(300)
        layout = QVBoxLayout()
        
        # Create list widget for tutorials
        list_widget = QListWidget()
        list_widget.setStyleSheet("""
            QListWidget {
                background-color: #000066;
                color: yellow;
                border: none;
                padding: 5px;
            }
        """)
        for tutorial_name, tutorial_data in tutorials.items():
            list_widget.addItem(f"{tutorial_name} - {tutorial_data['title']}")
        layout.addWidget(list_widget)
        
        # Add buttons
        button_layout = QHBoxLayout()
        start_button = QPushButton("Start Tutorial")
        cancel_button = QPushButton("Cancel")
        button_layout.addWidget(start_button)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)
        
        # Connect buttons
        start_button.clicked.connect(dialog.accept)
        cancel_button.clicked.connect(dialog.reject)
        
        dialog.setLayout(layout)
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            selected_item = list_widget.currentItem()
            if selected_item:
                # Extract tutorial name from the selected item
                tutorial_name = selected_item.text().split(" - ")[0]
                # Create and show the tutorial dialog
                tutorial_dialog = TutorialDialog(self)
                tutorial_dialog.start_tutorial(tutorial_name)

    def show_tutorial_editor_dialog(self):
        """Show the tutorial editor dialog."""
        from tutorial_editor_dialog import TutorialEditorDialog
        dialog = TutorialEditorDialog(self)
        dialog.exec()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle('Fusion')
    
    # Set dark theme
    palette = app.palette()
    palette.setColor(palette.ColorRole.Window, QColor(53, 53, 53))
    palette.setColor(palette.ColorRole.WindowText, Qt.GlobalColor.white)
    palette.setColor(palette.ColorRole.Base, QColor(25, 25, 25))
    palette.setColor(palette.ColorRole.AlternateBase, QColor(53, 53, 53))
    palette.setColor(palette.ColorRole.ToolTipBase, Qt.GlobalColor.white)
    palette.setColor(palette.ColorRole.ToolTipText, Qt.GlobalColor.white)
    # Remove the default text color to allow syntax highlighting to work
    palette.setColor(palette.ColorRole.Text, Qt.GlobalColor.white)
    palette.setColor(palette.ColorRole.Button, QColor(53, 53, 53))
    palette.setColor(palette.ColorRole.ButtonText, Qt.GlobalColor.white)
    palette.setColor(palette.ColorRole.BrightText, Qt.GlobalColor.red)
    palette.setColor(palette.ColorRole.Link, QColor(42, 130, 218))
    palette.setColor(palette.ColorRole.Highlight, QColor(42, 130, 218))
    palette.setColor(palette.ColorRole.HighlightedText, Qt.GlobalColor.black)
    app.setPalette(palette)
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec()) 