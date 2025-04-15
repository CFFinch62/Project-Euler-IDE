import json
import os
import sys
from pathlib import Path
from PyQt6.QtGui import QFont, QColor

class SettingsManager:
    def __init__(self):
        self.settings_file = self._get_settings_path()
        self.settings = self._load_settings()

    def _get_settings_path(self):
        """Get the path to the settings file in a cross-platform way."""
        if sys.platform == 'win32':
            # Windows: %APPDATA%
            base_dir = os.environ.get('APPDATA')
        elif sys.platform == 'darwin':
            # macOS: ~/Library/Application Support
            base_dir = os.path.expanduser('~/Library/Application Support')
        else:
            # Linux and others: ~/.local/share
            base_dir = os.path.expanduser('~/.local/share')
        
        # Create app-specific directory
        app_dir = os.path.join(base_dir, 'project_euler_editor')
        os.makedirs(app_dir, exist_ok=True)
        
        return os.path.join(app_dir, 'settings.json')

    def _load_settings(self):
        """Load settings from file or return defaults if file doesn't exist."""
        default_settings = {
            "problem_text": {
                "font_family": "Arial",
                "font_size": 12,
                "text_color": "#000000",
                "background_color": "#FFFFFF"
            },
            "code_editor": {
                "font_family": "Courier New",
                "font_size": 12,
                "text_color": "#000000",
                "background_color": "#FFFFFF"
            },
            "helper_editor": {
                "font_family": "Courier New",
                "font_size": 12,
                "text_color": "#000000",
                "background_color": "#FFFFFF"
            },
            "data_files": {
                "font_family": "Courier New",
                "font_size": 12,
                "text_color": "#FFFF00",  # Yellow
                "background_color": "#000066"  # Dark blue
            },
            "syntax_highlighting": {
                "keywords": "#569CD6",
                "strings": "#CE9178",
                "numbers": "#E07912",
                "comments": "#6A9955",
                "operators": "#DCDCAA",
                "functions": "#DCDCAA",
                "punctuation": "#D4D4D4"
            }
        }
        
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r') as f:
                    loaded_settings = json.load(f)
                    # Ensure all default settings are present
                    for category, defaults in default_settings.items():
                        if category not in loaded_settings:
                            loaded_settings[category] = defaults
                        elif category == "syntax_highlighting":
                            # Ensure all syntax highlighting elements are present
                            for element, default_color in defaults.items():
                                if element not in loaded_settings[category]:
                                    loaded_settings[category][element] = default_color
                    return loaded_settings
        except Exception as e:
            print(f"Error loading settings: {e}")
        
        return default_settings

    def save_settings(self):
        """Save current settings to file."""
        try:
            with open(self.settings_file, 'w') as f:
                json.dump(self.settings, f, indent=4)
        except IOError:
            pass

    def get_problem_text_settings(self):
        """Get settings for problem text area."""
        return self.settings["problem_text"]

    def get_code_editor_settings(self):
        """Get settings for code editor area."""
        return self.settings["code_editor"]

    def get_helper_editor_settings(self):
        """Get helper editor settings."""
        return self.settings.get("helper_editor", {
            "font_family": "Courier New",
            "font_size": 12,
            "text_color": "#000000",
            "background_color": "#FFFFFF"
        })

    def get_data_files_settings(self):
        """Get the current data files settings."""
        return self.settings.get("data_files", {
            "font_family": "Courier New",
            "font_size": 12,
            "text_color": "#FFFF00",  # Yellow
            "background_color": "#000066"  # Dark blue
        })

    def get_highlighting_color(self, element):
        """Get the color for a specific syntax highlighting element."""
        if not hasattr(self, 'settings'):
            self.settings = self._load_settings()
        return self.settings.get("syntax_highlighting", {}).get(element, "#000000")

    def update_problem_text_settings(self, font_family, font_size, text_color, background_color):
        """Update problem text settings."""
        self.settings["problem_text"] = {
            "font_family": font_family,
            "font_size": font_size,
            "text_color": text_color,
            "background_color": background_color
        }
        self.save_settings()

    def update_code_editor_settings(self, font_family, font_size, text_color, background_color):
        """Update code editor settings."""
        self.settings["code_editor"] = {
            "font_family": font_family,
            "font_size": font_size,
            "text_color": text_color,
            "background_color": background_color
        }
        self.save_settings()

    def update_helper_editor_settings(self, font_family, font_size, text_color, background_color):
        """Update helper editor settings."""
        if "helper_editor" not in self.settings:
            self.settings["helper_editor"] = {}
        self.settings["helper_editor"].update({
            "font_family": font_family,
            "font_size": font_size,
            "text_color": text_color,
            "background_color": background_color
        })
        self.save_settings()

    def update_data_files_settings(self, settings):
        """Update the data files settings."""
        if "data_files" not in self.settings:
            self.settings["data_files"] = {}
        self.settings["data_files"].update(settings)
        self.save_settings()

    def update_highlighting_colors(self, colors):
        """Update syntax highlighting colors."""
        if "syntax_highlighting" not in self.settings:
            self.settings["syntax_highlighting"] = {}
        self.settings["syntax_highlighting"].update(colors)
        self.save_settings()

    def apply_problem_text_settings(self, text_edit):
        """Apply saved settings to a problem text QTextEdit."""
        settings = self.get_problem_text_settings()
        font = QFont(settings["font_family"], settings["font_size"])
        text_edit.setFont(font)
        text_edit.setStyleSheet(f"""
            QTextEdit {{
                color: {settings["text_color"]};
                background-color: {settings["background_color"]};
                border: none;
                padding: 10px;
            }}
        """)

    def apply_code_editor_settings(self, text_edit):
        """Apply saved settings to a code editor QTextEdit or QPlainTextEdit."""
        settings = self.get_code_editor_settings()
        font = QFont(settings["font_family"], settings["font_size"])
        text_edit.setFont(font)
        
        # Determine the widget type for the stylesheet
        widget_type = "QPlainTextEdit" if hasattr(text_edit, "setLineWrapMode") and hasattr(text_edit, "setTabStopDistance") else "QTextEdit"
        
        text_edit.setStyleSheet(f"""
            {widget_type} {{
                background-color: {settings["background_color"]};
                color: {settings["text_color"]};
                border: none;
                padding: 10px;
                font-family: '{settings["font_family"]}';
            }}
        """)

    def apply_helper_editor_settings(self, text_edit):
        """Apply saved settings to a helper editor QTextEdit."""
        settings = self.get_helper_editor_settings()
        
        # Set font
        font = QFont(settings["font_family"], settings["font_size"])
        text_edit.setFont(font)
        
        # Determine the widget type for the stylesheet
        widget_type = "QPlainTextEdit" if hasattr(text_edit, "setLineWrapMode") and hasattr(text_edit, "setTabStopDistance") else "QTextEdit"
        
        # Set colors with full styling
        text_edit.setStyleSheet(f"""
            {widget_type} {{
                background-color: {settings['background_color']};
                color: {settings['text_color']};
                border: none;
                padding: 10px;
                font-family: '{settings['font_family']}';
            }}
        """)

    def apply_data_files_settings(self, widget):
        """Apply data files settings to a widget."""
        settings = self.get_data_files_settings()
        font = QFont(settings["font_family"], settings["font_size"])
        widget.setFont(font)
        widget.setStyleSheet(f"""
            QTextEdit {{
                color: {settings["text_color"]};
                background-color: {settings["background_color"]};
                border: none;
                padding: 5px;
            }}
        """)

    def get_settings(self):
        """Get the current settings."""
        return self.settings

    def set_settings(self, settings):
        """Set new settings."""
        self.settings = settings
        self.save_settings() 