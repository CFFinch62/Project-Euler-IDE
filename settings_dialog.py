from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                            QComboBox, QSpinBox, QPushButton, QColorDialog,
                            QGroupBox, QFormLayout, QScrollArea, QWidget,
                            QGridLayout, QFileDialog, QMessageBox, QLineEdit)
from PyQt6.QtGui import QFont, QFontDatabase, QColor
from PyQt6.QtCore import Qt
import json
import os

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.setMinimumWidth(1050)  # Increased from 1000 to 1050 pixels
        self.setMinimumHeight(600)  # Reduced height since we'll use more columns
        
        # Create main layout
        layout = QVBoxLayout(self)
        
        # Create scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        
        # Get system fonts
        system_fonts = QFontDatabase.families()
        
        # Create grid layout for settings groups
        settings_grid = QGridLayout()
        settings_grid.setSpacing(20)  # Add spacing between groups
        
        # First Column
        first_column = QVBoxLayout()
        
        # Problem Text Settings
        problem_group = QGroupBox("Problem Text")
        problem_layout = QFormLayout()
        self.problem_font_family = QComboBox()
        self.problem_font_family.addItems(system_fonts)
        problem_layout.addRow("Font:", self.problem_font_family)
        self.problem_font_size = QSpinBox()
        self.problem_font_size.setRange(8, 72)
        self.problem_font_size.setValue(12)
        problem_layout.addRow("Size:", self.problem_font_size)
        self.problem_text_color = QPushButton("Choose Color")
        self.problem_text_color.clicked.connect(lambda: self.choose_color("problem_text"))
        problem_layout.addRow("Text:", self.problem_text_color)
        self.problem_bg_color = QPushButton("Choose Color")
        self.problem_bg_color.clicked.connect(lambda: self.choose_color("problem_bg"))
        problem_layout.addRow("Background:", self.problem_bg_color)
        problem_group.setLayout(problem_layout)
        first_column.addWidget(problem_group)
        
        # Code Editor Settings
        code_group = QGroupBox("Code Editor")
        code_layout = QFormLayout()
        self.code_font_family = QComboBox()
        self.code_font_family.addItems(system_fonts)
        code_layout.addRow("Font:", self.code_font_family)
        self.code_font_size = QSpinBox()
        self.code_font_size.setRange(8, 72)
        self.code_font_size.setValue(12)
        code_layout.addRow("Size:", self.code_font_size)
        self.code_text_color = QPushButton("Choose Color")
        self.code_text_color.clicked.connect(lambda: self.choose_color("code_text"))
        code_layout.addRow("Text:", self.code_text_color)
        self.code_bg_color = QPushButton("Choose Color")
        self.code_bg_color.clicked.connect(lambda: self.choose_color("code_bg"))
        code_layout.addRow("Background:", self.code_bg_color)
        code_group.setLayout(code_layout)
        first_column.addWidget(code_group)
        
        # Second Column
        second_column = QVBoxLayout()
        
        # Helper Editor Settings
        helper_group = QGroupBox("Helper Editor")
        helper_layout = QFormLayout()
        self.helper_font_family = QComboBox()
        self.helper_font_family.addItems(system_fonts)
        helper_layout.addRow("Font:", self.helper_font_family)
        self.helper_font_size = QSpinBox()
        self.helper_font_size.setRange(8, 72)
        self.helper_font_size.setValue(12)
        helper_layout.addRow("Size:", self.helper_font_size)
        self.helper_text_color = QPushButton("Choose Color")
        self.helper_text_color.clicked.connect(lambda: self.choose_color("helper_text"))
        helper_layout.addRow("Text:", self.helper_text_color)
        self.helper_bg_color = QPushButton("Choose Color")
        self.helper_bg_color.clicked.connect(lambda: self.choose_color("helper_bg"))
        helper_layout.addRow("Background:", self.helper_bg_color)
        helper_group.setLayout(helper_layout)
        second_column.addWidget(helper_group)
        
        # Data Files Settings
        data_files_group = QGroupBox("Data Files")
        data_files_layout = QFormLayout()
        self.data_files_font_family = QComboBox()
        self.data_files_font_family.addItems(system_fonts)
        data_files_layout.addRow("Font:", self.data_files_font_family)
        self.data_files_font_size = QSpinBox()
        self.data_files_font_size.setRange(8, 72)
        self.data_files_font_size.setValue(12)
        data_files_layout.addRow("Size:", self.data_files_font_size)
        self.data_files_text_color = QPushButton("Choose Color")
        self.data_files_text_color.clicked.connect(lambda: self.choose_color("data_files_text"))
        data_files_layout.addRow("Text:", self.data_files_text_color)
        self.data_files_bg_color = QPushButton("Choose Color")
        self.data_files_bg_color.clicked.connect(lambda: self.choose_color("data_files_bg"))
        data_files_layout.addRow("Background:", self.data_files_bg_color)
        data_files_group.setLayout(data_files_layout)
        second_column.addWidget(data_files_group)
        
        # Third Column - Syntax Highlighting
        third_column = QVBoxLayout()
        
        # Syntax Highlighting Settings
        syntax_group = QGroupBox("Syntax Highlighting")
        syntax_layout = QFormLayout()
        
        self.keywords_color = QPushButton("Choose Color")
        self.keywords_color.clicked.connect(lambda: self.choose_color("keywords"))
        syntax_layout.addRow("Keywords:", self.keywords_color)
        
        self.strings_color = QPushButton("Choose Color")
        self.strings_color.clicked.connect(lambda: self.choose_color("strings"))
        syntax_layout.addRow("Strings:", self.strings_color)
        
        self.numbers_color = QPushButton("Choose Color")
        self.numbers_color.clicked.connect(lambda: self.choose_color("numbers"))
        syntax_layout.addRow("Numbers:", self.numbers_color)
        
        self.comments_color = QPushButton("Choose Color")
        self.comments_color.clicked.connect(lambda: self.choose_color("comments"))
        syntax_layout.addRow("Comments:", self.comments_color)
        
        self.operators_color = QPushButton("Choose Color")
        self.operators_color.clicked.connect(lambda: self.choose_color("operators"))
        syntax_layout.addRow("Operators:", self.operators_color)
        
        self.functions_color = QPushButton("Choose Color")
        self.functions_color.clicked.connect(lambda: self.choose_color("functions"))
        syntax_layout.addRow("Functions:", self.functions_color)
        
        self.punctuation_color = QPushButton("Choose Color")
        self.punctuation_color.clicked.connect(lambda: self.choose_color("punctuation"))
        syntax_layout.addRow("Punctuation:", self.punctuation_color)
        
        # Add spacing before theme controls
        syntax_layout.addRow("", QLabel(""))  # Empty row for spacing
        
        # Theme name input
        theme_name_layout = QHBoxLayout()
        self.theme_name_input = QLineEdit()
        self.theme_name_input.setPlaceholderText("Enter theme name")
        theme_name_layout.addWidget(self.theme_name_input)
        syntax_layout.addRow("Theme:", theme_name_layout)
        
        # Theme buttons on a new line
        theme_buttons_layout = QHBoxLayout()
        self.save_theme_button = QPushButton("Save Theme")
        self.save_theme_button.clicked.connect(self.save_theme)
        self.load_theme_button = QPushButton("Load Theme")
        self.load_theme_button.clicked.connect(self.load_theme)
        theme_buttons_layout.addWidget(self.save_theme_button)
        theme_buttons_layout.addWidget(self.load_theme_button)
        syntax_layout.addRow("", theme_buttons_layout)  # Empty label for the buttons row
        
        syntax_group.setLayout(syntax_layout)
        third_column.addWidget(syntax_group)
        
        # Add columns to the grid
        settings_grid.addLayout(first_column, 0, 0)
        settings_grid.addLayout(second_column, 0, 1)
        settings_grid.addLayout(third_column, 0, 2)
        
        scroll_layout.addLayout(settings_grid)
        
        # Add buttons at the bottom
        button_layout = QHBoxLayout()
        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.accept)
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.ok_button)
        button_layout.addWidget(self.cancel_button)
        
        scroll.setWidget(scroll_content)
        layout.addWidget(scroll)
        layout.addLayout(button_layout)
        
        # Store current colors
        self.current_colors = {}
        
    def choose_color(self, color_type):
        """Open color dialog and update button background."""
        color = QColorDialog.getColor()
        if color.isValid():
            # Get the color in a consistent format
            color_hex = color.name(QColor.NameFormat.HexRgb)
            button = getattr(self, f"{color_type}_color")
            button.setStyleSheet(f"background-color: {color_hex}")
            self.current_colors[color_type] = color_hex
            
            # If this is a syntax highlighting color, update the settings and highlighter
            if color_type in ["keywords", "strings", "numbers", "comments", 
                            "operators", "functions", "punctuation"]:
                # Get the parent window to access the code editor
                parent = self.parent()
                if parent and hasattr(parent, 'code_editor'):
                    # Update the settings manager with the new color
                    if hasattr(parent, 'settings_manager'):
                        settings = parent.settings_manager.get_settings()
                        if 'syntax_highlighting' not in settings:
                            settings['syntax_highlighting'] = {}
                        settings['syntax_highlighting'][color_type] = color_hex
                        parent.settings_manager.set_settings(settings)
                        parent.settings_manager.save_settings()
                        print(f"Updated settings manager with new {color_type} color: {color_hex}")  # Debug print
                    
                    # Update the highlighter
                    if hasattr(parent, 'highlighter'):
                        parent.highlighter.update_highlighting_rules()
                        parent.highlighter.rehighlight()
                        print(f"Updated main editor highlighter with new {color_type} color")  # Debug print
                    
                    # Also update the helper editor highlighter
                    if hasattr(parent, 'helpers_highlighter'):
                        parent.helpers_highlighter.update_highlighting_rules()
                        parent.helpers_highlighter.rehighlight()
                        print(f"Updated helper editor highlighter with new {color_type} color")  # Debug print
            
    def get_settings(self):
        """Get all settings from the dialog."""
        settings = {
            "problem_text": {
                "font_family": self.problem_font_family.currentText(),
                "font_size": self.problem_font_size.value(),
                "text_color": self.current_colors.get("problem_text", "#000000"),
                "background_color": self.current_colors.get("problem_bg", "#FFFFFF")
            },
            "code_editor": {
                "font_family": self.code_font_family.currentText(),
                "font_size": self.code_font_size.value(),
                "text_color": self.current_colors.get("code_text", "#000000"),
                "background_color": self.current_colors.get("code_bg", "#FFFFFF")
            },
            "helper_editor": {
                "font_family": self.helper_font_family.currentText(),
                "font_size": self.helper_font_size.value(),
                "text_color": self.current_colors.get("helper_text", "#000000"),
                "background_color": self.current_colors.get("helper_bg", "#FFFFFF")
            },
            "data_files": {
                "font_family": self.data_files_font_family.currentText(),
                "font_size": self.data_files_font_size.value(),
                "text_color": self.current_colors.get("data_files_text", "#FFFF00"),
                "background_color": self.current_colors.get("data_files_bg", "#000066")
            },
            "syntax_highlighting": {
                "keywords": self.current_colors.get("keywords", "#569CD6"),
                "strings": self.current_colors.get("strings", "#CE9178"),
                "numbers": self.current_colors.get("numbers", "#E07912"),
                "comments": self.current_colors.get("comments", "#6A9955"),
                "operators": self.current_colors.get("operators", "#DCDCAA"),
                "functions": self.current_colors.get("functions", "#DCDCAA"),
                "punctuation": self.current_colors.get("punctuation", "#D4D4D4")
            }
        }
        return settings
        
    def set_settings(self, settings):
        """Set all settings in the dialog."""
        # Set problem text settings
        if "problem_text" in settings:
            problem = settings["problem_text"]
            self.problem_font_family.setCurrentText(problem.get("font_family", "Arial"))
            self.problem_font_size.setValue(problem.get("font_size", 12))
            self.problem_text_color.setStyleSheet(f"background-color: {problem.get('text_color', '#000000')}")
            self.problem_bg_color.setStyleSheet(f"background-color: {problem.get('background_color', '#FFFFFF')}")
            self.current_colors["problem_text"] = problem.get("text_color", "#000000")
            self.current_colors["problem_bg"] = problem.get("background_color", "#FFFFFF")
            
        # Set code editor settings
        if "code_editor" in settings:
            code = settings["code_editor"]
            self.code_font_family.setCurrentText(code.get("font_family", "Courier New"))
            self.code_font_size.setValue(code.get("font_size", 12))
            self.code_text_color.setStyleSheet(f"background-color: {code.get('text_color', '#000000')}")
            self.code_bg_color.setStyleSheet(f"background-color: {code.get('background_color', '#FFFFFF')}")
            self.current_colors["code_text"] = code.get("text_color", "#000000")
            self.current_colors["code_bg"] = code.get("background_color", "#FFFFFF")
            
        # Set helper editor settings
        if "helper_editor" in settings:
            helper = settings["helper_editor"]
            self.helper_font_family.setCurrentText(helper.get("font_family", "Courier New"))
            self.helper_font_size.setValue(helper.get("font_size", 12))
            self.helper_text_color.setStyleSheet(f"background-color: {helper.get('text_color', '#000000')}")
            self.helper_bg_color.setStyleSheet(f"background-color: {helper.get('background_color', '#FFFFFF')}")
            self.current_colors["helper_text"] = helper.get("text_color", "#000000")
            self.current_colors["helper_bg"] = helper.get("background_color", "#FFFFFF")
            
        # Set data files settings
        if "data_files" in settings:
            data_files = settings["data_files"]
            self.data_files_font_family.setCurrentText(data_files.get("font_family", "Courier New"))
            self.data_files_font_size.setValue(data_files.get("font_size", 12))
            self.data_files_text_color.setStyleSheet(f"background-color: {data_files.get('text_color', '#FFFF00')}")
            self.data_files_bg_color.setStyleSheet(f"background-color: {data_files.get('background_color', '#000066')}")
            self.current_colors["data_files_text"] = data_files.get("text_color", "#FFFF00")
            self.current_colors["data_files_bg"] = data_files.get("background_color", "#000066")
            
        # Set syntax highlighting settings
        if "syntax_highlighting" in settings:
            syntax = settings["syntax_highlighting"]
            for element in ["keywords", "strings", "numbers", "comments", 
                          "operators", "functions", "punctuation"]:
                if element in syntax:  # Only process elements that exist in the settings
                    color = syntax.get(element, "#000000")
                    button = getattr(self, f"{element}_color")
                    button.setStyleSheet(f"background-color: {color}")
                    self.current_colors[element] = color

    def save_theme(self):
        """Save the current syntax highlighting colors to a theme file."""
        theme_name = self.theme_name_input.text().strip()
        if not theme_name:
            QMessageBox.warning(self, "Warning", "Please enter a theme name")
            return
            
        theme = {
            "name": theme_name,
            "colors": {
                "keywords": self.current_colors.get("keywords", "#569CD6"),
                "strings": self.current_colors.get("strings", "#CE9178"),
                "numbers": self.current_colors.get("numbers", "#E07912"),
                "comments": self.current_colors.get("comments", "#6A9955"),
                "operators": self.current_colors.get("operators", "#DCDCAA"),
                "functions": self.current_colors.get("functions", "#DCDCAA"),
                "punctuation": self.current_colors.get("punctuation", "#D4D4D4")
            }
        }
        
        # Get the themes directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        themes_dir = os.path.join(current_dir, "themes")
        print(f"Creating themes directory at: {themes_dir}")  # Debug print
        
        try:
            os.makedirs(themes_dir, exist_ok=True)
            # Create filename from theme name
            filename = f"{theme_name.lower().replace(' ', '_')}.json"
            file_path = os.path.join(themes_dir, filename)
            print(f"Saving theme to: {file_path}")  # Debug print
            
            with open(file_path, 'w') as f:
                json.dump(theme, f, indent=4)
            QMessageBox.information(self, "Success", f"Theme '{theme_name}' saved successfully!\nLocation: {file_path}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save theme: {str(e)}")
                
    def load_theme(self):
        """Load a syntax highlighting theme from a file."""
        # Get the themes directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        themes_dir = os.path.join(current_dir, "themes")
        print(f"Looking for themes in: {themes_dir}")  # Debug print
        
        try:
            # Create themes directory if it doesn't exist
            os.makedirs(themes_dir, exist_ok=True)
            
            # Get list of theme files
            theme_files = [f for f in os.listdir(themes_dir) if f.endswith('.json')]
            print(f"Found theme files: {theme_files}")  # Debug print
            
            if not theme_files:
                QMessageBox.information(
                    self, 
                    "No Themes Found", 
                    f"No theme files found in {themes_dir}\n\n"
                    "To create a theme:\n"
                    "1. Adjust the syntax highlighting colors\n"
                    "2. Enter a theme name\n"
                    "3. Click 'Save Theme'"
                )
                return
            
            # Create dialog to select theme
            theme_dialog = QDialog(self)
            theme_dialog.setWindowTitle("Select Theme")
            theme_dialog.setModal(True)
            
            layout = QVBoxLayout(theme_dialog)
            
            # Create theme list
            theme_list = QComboBox()
            theme_names = []
            theme_data = {}  # Store theme data for each file
            
            for theme_file in theme_files:
                try:
                    with open(os.path.join(themes_dir, theme_file), 'r') as f:
                        theme = json.load(f)
                        theme_name = theme.get('name', theme_file[:-5])
                        theme_names.append(theme_name)
                        theme_data[theme_name] = theme
                        print(f"Loaded theme '{theme_name}' from {theme_file}")  # Debug print
                except Exception as e:
                    print(f"Error loading theme {theme_file}: {str(e)}")  # Debug print
                    theme_names.append(theme_file[:-5])
            
            theme_list.addItems(theme_names)
            layout.addWidget(theme_list)
            
            # Add buttons
            button_layout = QHBoxLayout()
            load_button = QPushButton("Load")
            cancel_button = QPushButton("Cancel")
            button_layout.addWidget(load_button)
            button_layout.addWidget(cancel_button)
            layout.addLayout(button_layout)
            
            # Connect buttons
            load_button.clicked.connect(theme_dialog.accept)
            cancel_button.clicked.connect(theme_dialog.reject)
            
            if theme_dialog.exec() == QDialog.DialogCode.Accepted:
                selected_theme_name = theme_list.currentText()
                print(f"Selected theme: {selected_theme_name}")  # Debug print
                
                if selected_theme_name in theme_data:
                    theme = theme_data[selected_theme_name]
                    print(f"Applying theme colors: {theme['colors']}")  # Debug print
                    
                    # Update colors in the dialog
                    for element, color in theme['colors'].items():
                        if element in ["keywords", "strings", "numbers", "comments", 
                                     "operators", "functions", "punctuation"]:
                            button = getattr(self, f"{element}_color")
                            button.setStyleSheet(f"background-color: {color}")
                            self.current_colors[element] = color
                            print(f"Set {element} color to {color}")  # Debug print
                    
                    # Get the parent window to access the code editor
                    parent = self.parent()
                    if parent and hasattr(parent, 'code_editor'):
                        # Update the settings manager with the new colors
                        if hasattr(parent, 'settings_manager'):
                            settings = parent.settings_manager.get_settings()
                            if 'syntax_highlighting' not in settings:
                                settings['syntax_highlighting'] = {}
                            settings['syntax_highlighting'].update(theme['colors'])
                            parent.settings_manager.set_settings(settings)
                            parent.settings_manager.save_settings()
                            print("Updated settings manager with new colors")  # Debug print
                        
                        # Update the highlighter
                        if hasattr(parent, 'highlighter'):
                            parent.highlighter.update_highlighting_rules()
                            parent.highlighter.rehighlight()
                            print("Updated main editor highlighter")  # Debug print
                        
                        # Also update the helper editor highlighter
                        if hasattr(parent, 'helpers_highlighter'):
                            parent.helpers_highlighter.update_highlighting_rules()
                            parent.helpers_highlighter.rehighlight()
                            print("Updated helper editor highlighter")  # Debug print
                    
                    QMessageBox.information(self, "Success", f"Theme '{theme['name']}' loaded successfully!")
                else:
                    QMessageBox.critical(self, "Error", f"Could not find theme data for '{selected_theme_name}'")
        except Exception as e:
            print(f"Error in load_theme: {str(e)}")  # Debug print
            QMessageBox.critical(self, "Error", f"Failed to access themes directory: {str(e)}") 