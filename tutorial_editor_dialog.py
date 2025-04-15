from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QPushButton,
                            QLabel, QLineEdit, QTextEdit, QListWidget, QMessageBox)
from PyQt6.QtCore import Qt
import json
import os

class TutorialEditorDialog(QDialog):
    def __init__(self, parent=None, tutorial_name=None):
        super().__init__(parent)
        self.tutorial_name = tutorial_name
        self.settings_manager = parent.settings_manager if parent else None
        self.setWindowTitle("Create Tutorial" if not tutorial_name else "Edit Tutorial")
        self.setMinimumWidth(800)
        self.setMinimumHeight(600)
        
        # Create layout
        layout = QVBoxLayout()
        
        # Name input
        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("Tutorial Name:"))
        self.name_input = QLineEdit()
        self.name_input.setStyleSheet("""
            QLineEdit {
                background-color: #000066;
                color: yellow;
                border: none;
                padding: 5px;
            }
        """)
        if tutorial_name:
            self.name_input.setText(tutorial_name)
            self.name_input.setReadOnly(True)  # Don't allow editing the name of existing tutorials
        name_layout.addWidget(self.name_input)
        
        # Add Load Tutorial button
        self.load_button = QPushButton("Load Tutorial")
        self.load_button.clicked.connect(self.load_tutorial_dialog)
        name_layout.addWidget(self.load_button)
        
        layout.addLayout(name_layout)
        
        # Title input
        title_layout = QHBoxLayout()
        title_layout.addWidget(QLabel("Tutorial Title:"))
        self.title_input = QLineEdit()
        self.title_input.setStyleSheet("""
            QLineEdit {
                background-color: #000066;
                color: yellow;
                border: none;
                padding: 5px;
            }
        """)
        title_layout.addWidget(self.title_input)
        layout.addLayout(title_layout)
        
        # Steps list and controls
        steps_layout = QVBoxLayout()
        steps_layout.addWidget(QLabel("Steps:"))
        
        # Steps list
        self.steps_list = QListWidget()
        self.steps_list.setStyleSheet("""
            QListWidget {
                background-color: #000066;
                color: yellow;
                border: none;
                padding: 5px;
            }
        """)
        self.steps_list.currentItemChanged.connect(self.load_step)
        steps_layout.addWidget(self.steps_list)
        
        # Step controls
        step_controls = QHBoxLayout()
        self.add_step_button = QPushButton("Add Step")
        self.add_step_button.clicked.connect(self.add_step)
        self.delete_step_button = QPushButton("Delete Step")
        self.delete_step_button.clicked.connect(self.delete_step)
        step_controls.addWidget(self.add_step_button)
        step_controls.addWidget(self.delete_step_button)
        steps_layout.addLayout(step_controls)
        
        layout.addLayout(steps_layout)
        
        # Step editor
        step_editor_layout = QVBoxLayout()
        step_editor_layout.addWidget(QLabel("Step Editor:"))
        
        # Step title
        step_title_layout = QHBoxLayout()
        step_title_layout.addWidget(QLabel("Title:"))
        self.step_title_input = QLineEdit()
        self.step_title_input.setStyleSheet("""
            QLineEdit {
                background-color: #000066;
                color: yellow;
                border: none;
                padding: 5px;
            }
        """)
        step_title_layout.addWidget(self.step_title_input)
        step_editor_layout.addLayout(step_title_layout)
        
        # Step content
        step_editor_layout.addWidget(QLabel("Content:"))
        self.step_content_input = QTextEdit()
        self.step_content_input.setStyleSheet("""
            QTextEdit {
                background-color: #000066;
                color: yellow;
                border: none;
                padding: 5px;
            }
        """)
        step_editor_layout.addWidget(self.step_content_input)
        
        # Step action
        step_action_layout = QHBoxLayout()
        step_action_layout.addWidget(QLabel("Action:"))
        self.step_action_input = QLineEdit()
        self.step_action_input.setStyleSheet("""
            QLineEdit {
                background-color: #000066;
                color: yellow;
                border: none;
                padding: 5px;
            }
        """)
        self.step_action_input.setPlaceholderText("none, highlight_areas, highlight_button, select_problem")
        step_action_layout.addWidget(self.step_action_input)
        step_editor_layout.addLayout(step_action_layout)
        
        # Step params
        step_params_layout = QHBoxLayout()
        step_params_layout.addWidget(QLabel("Params:"))
        self.step_params_input = QLineEdit()
        self.step_params_input.setStyleSheet("""
            QLineEdit {
                background-color: #000066;
                color: yellow;
                border: none;
                padding: 5px;
            }
        """)
        self.step_params_input.setPlaceholderText("JSON format, e.g., {\"button\": \"run\"}")
        step_params_layout.addWidget(self.step_params_input)
        step_editor_layout.addLayout(step_params_layout)
        
        # Save step button
        self.save_step_button = QPushButton("Save Step")
        self.save_step_button.clicked.connect(self.save_step)
        step_editor_layout.addWidget(self.save_step_button)
        
        layout.addLayout(step_editor_layout)
        
        # Dialog buttons
        button_layout = QHBoxLayout()
        self.save_button = QPushButton("Save Tutorial")
        self.save_button.clicked.connect(self.save_tutorial)
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        
        # Load tutorial if editing
        if tutorial_name:
            self.load_tutorial()

    def load_tutorial_dialog(self):
        """Show a dialog to select and load an existing tutorial."""
        try:
            # Get the tutorials directory
            tutorials_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tutorials")
            if not os.path.exists(tutorials_dir):
                QMessageBox.warning(self, "Warning", "No tutorials directory found")
                return
                
            # Get all JSON files in the tutorials directory
            tutorials = []
            for file in os.listdir(tutorials_dir):
                if file.endswith('.json'):
                    # Remove the .json extension to get the tutorial name
                    tutorial_name = file[:-5]
                    tutorials.append(tutorial_name)
                    
            if not tutorials:
                QMessageBox.warning(self, "Warning", "No tutorials found")
                return
                
            # Create dialog to select tutorial
            dialog = QDialog(self)
            dialog.setWindowTitle("Load Tutorial")
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
            for tutorial in sorted(tutorials):
                list_widget.addItem(tutorial)
            layout.addWidget(list_widget)
            
            # Add buttons
            button_layout = QHBoxLayout()
            load_button = QPushButton("Load")
            cancel_button = QPushButton("Cancel")
            button_layout.addWidget(load_button)
            button_layout.addWidget(cancel_button)
            layout.addLayout(button_layout)
            
            # Connect buttons
            load_button.clicked.connect(dialog.accept)
            cancel_button.clicked.connect(dialog.reject)
            
            dialog.setLayout(layout)
            
            if dialog.exec() == QDialog.DialogCode.Accepted:
                selected_item = list_widget.currentItem()
                if selected_item:
                    tutorial_name = selected_item.text()
                    self.tutorial_name = tutorial_name
                    self.name_input.setText(tutorial_name)
                    self.name_input.setReadOnly(True)
                    self.setWindowTitle(f"Edit Tutorial: {tutorial_name}")
                    self.load_tutorial()
                    
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load tutorials: {str(e)}")

    def load_tutorial(self):
        """Load an existing tutorial for editing."""
        try:
            # Load the tutorial file
            tutorial_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tutorials", f"{self.tutorial_name}.json")
            if not os.path.exists(tutorial_path):
                QMessageBox.warning(self, "Error", f"Tutorial file not found: {tutorial_path}")
                return
                
            with open(tutorial_path, 'r') as f:
                tutorial_data = json.load(f)
            
            # Set the title
            self.title_input.setText(tutorial_data.get("title", ""))
            
            # Clear and populate the steps list
            self.steps_list.clear()
            for step in tutorial_data.get("steps", []):
                self.steps_list.addItem(step.get("title", "Untitled Step"))
                
            # Select the first step if available
            if self.steps_list.count() > 0:
                self.steps_list.setCurrentRow(0)
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load tutorial: {str(e)}")

    def add_step(self):
        """Add a new step to the tutorial."""
        self.steps_list.addItem("New Step")
        self.steps_list.setCurrentRow(self.steps_list.count() - 1)
        self.step_title_input.clear()
        self.step_content_input.clear()
        self.step_action_input.clear()
        self.step_params_input.clear()

    def delete_step(self):
        """Delete the selected step."""
        current_row = self.steps_list.currentRow()
        if current_row >= 0:
            self.steps_list.takeItem(current_row)

    def load_step(self, current, previous):
        """Load the selected step for editing."""
        if current is None:
            return
            
        try:
            # Load the tutorial file
            tutorial_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tutorials", f"{self.tutorial_name}.json")
            if not os.path.exists(tutorial_path):
                return
                
            with open(tutorial_path, 'r') as f:
                tutorial_data = json.load(f)
            
            # Get the step index
            step_index = self.steps_list.row(current)
            if step_index < len(tutorial_data.get("steps", [])):
                step = tutorial_data["steps"][step_index]
                self.step_title_input.setText(step.get("title", ""))
                self.step_content_input.setPlainText(step.get("content", ""))
                self.step_action_input.setText(step.get("action", "none"))
                self.step_params_input.setText(json.dumps(step.get("params", {})))
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load step: {str(e)}")

    def save_step(self):
        """Save the current step."""
        current_row = self.steps_list.currentRow()
        if current_row < 0:
            return
            
        # Get step data
        title = self.step_title_input.text().strip()
        content = self.step_content_input.toPlainText().strip()
        action = self.step_action_input.text().strip()
        
        # Parse params if provided
        params = {}
        params_text = self.step_params_input.text().strip()
        if params_text:
            try:
                params = json.loads(params_text)
            except:
                QMessageBox.warning(self, "Warning", "Invalid params format. Use JSON format.")
                return
        
        # Update the step in the list
        self.steps_list.item(current_row).setText(title)

    def save_tutorial(self):
        """Save the tutorial and close the dialog."""
        name = self.name_input.text().strip()
        title = self.title_input.text().strip()
        
        if not name:
            QMessageBox.warning(self, "Warning", "Please enter a tutorial name")
            return
            
        if not title:
            QMessageBox.warning(self, "Warning", "Please enter a tutorial title")
            return
            
        # Collect all steps
        steps = []
        for i in range(self.steps_list.count()):
            item = self.steps_list.item(i)
            steps.append({
                "title": item.text(),
                "content": "",  # This would be filled with actual content
                "action": "none"
            })
        
        # Create tutorial data
        tutorial_data = {
            "title": title,
            "steps": steps
        }
        
        # Save to individual tutorial file
        try:
            # Ensure tutorials directory exists
            tutorials_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tutorials")
            os.makedirs(tutorials_dir, exist_ok=True)
            
            # Save the tutorial file
            tutorial_path = os.path.join(tutorials_dir, f"{name}.json")
            with open(tutorial_path, 'w') as f:
                json.dump(tutorial_data, f, indent=4)
                
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save tutorial: {str(e)}") 