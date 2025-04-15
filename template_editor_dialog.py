from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QPushButton,
                            QLabel, QLineEdit, QTextEdit, QMessageBox)
from PyQt6.QtCore import Qt
from ui.code_editor import CodeEditor

class TemplateEditorDialog(QDialog):
    def __init__(self, parent=None, template_name=None, template_data=None):
        super().__init__(parent)
        self.template_name = template_name
        self.template_data = template_data
        self.settings_manager = parent.settings_manager if parent else None
        self.setWindowTitle("Create Template" if not template_name else "Edit Template")
        self.setMinimumWidth(600)
        self.setMinimumHeight(500)
        
        # Create layout
        layout = QVBoxLayout()
        
        # Name input
        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("Template Name:"))
        self.name_input = QLineEdit()
        self.name_input.setStyleSheet("""
            QLineEdit {
                background-color: #000066;
                color: yellow;
                border: none;
                padding: 5px;
            }
        """)
        if template_name:
            self.name_input.setText(template_name)
        name_layout.addWidget(self.name_input)
        layout.addLayout(name_layout)
        
        # Description input
        desc_layout = QVBoxLayout()
        desc_layout.addWidget(QLabel("Description:"))
        self.desc_input = QTextEdit()
        self.desc_input.setStyleSheet("""
            QTextEdit {
                background-color: #000066;
                color: yellow;
                border: none;
                padding: 5px;
            }
        """)
        if template_data and "description" in template_data:
            self.desc_input.setPlainText(template_data["description"])
        self.desc_input.setMaximumHeight(100)
        desc_layout.addWidget(self.desc_input)
        layout.addLayout(desc_layout)
        
        # Code editor
        layout.addWidget(QLabel("Template Code:"))
        self.code_editor = CodeEditor(settings_manager=self.settings_manager)
        
        # Apply settings using SettingsManager
        if self.settings_manager:
            # Temporarily update settings for the code editor
            self.settings_manager.update_code_editor_settings(
                font_family="Consolas",
                font_size=12,
                text_color="#FFFF00",  # Yellow
                background_color="#000066"  # Dark blue
            )
            self.settings_manager.apply_code_editor_settings(self.code_editor)
        
        if template_data and "code" in template_data:
            self.code_editor.setPlainText(template_data["code"])
        layout.addWidget(self.code_editor)
        
        # Buttons
        button_layout = QHBoxLayout()
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_template)
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)

    def save_template(self):
        """Save the template and close the dialog."""
        name = self.name_input.text().strip()
        description = self.desc_input.toPlainText().strip()
        code = self.code_editor.toPlainText().strip()
        
        if not name:
            QMessageBox.warning(self, "Warning", "Please enter a template name")
            return
            
        if not code:
            QMessageBox.warning(self, "Warning", "Please enter template code")
            return
            
        # Create template data
        template_data = {
            "name": name,
            "description": description,
            "code": code
        }
        
        # Save to user templates
        from templates_manager import TemplatesManager
        templates_manager = TemplatesManager()
        templates_manager.add_user_template(name, template_data)
        
        self.accept() 