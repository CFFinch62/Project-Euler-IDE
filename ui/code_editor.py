from PyQt6.QtWidgets import QPlainTextEdit, QWidget, QScrollArea, QToolTip
from PyQt6.QtGui import QFont, QTextCharFormat, QColor, QPainter, QTextFormat, QTextCursor
from PyQt6.QtCore import Qt, QRect, QSize, pyqtSignal, QPoint
import re
from ui.syntax_highlighter import PythonHighlighter

class LineNumberArea(QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.editor = editor
        self.setStyleSheet("""
            QWidget {
                background-color: #2d2d2d;
                border-right: 1px solid #3d3d3d;
            }
        """)
        self.show()  # Explicitly show the widget

    def sizeHint(self):
        return QSize(self.editor.line_number_area_width(), 0)

    def paintEvent(self, event):
        self.editor.line_number_area_paint_event(event)

class CodeEditor(QPlainTextEdit):
    def __init__(self, parent=None, settings_manager=None):
        super().__init__(parent)
        self.settings_manager = settings_manager
        
        # Set initial font and style
        self.setFont(QFont("Consolas", 12))
        self.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)
        self.setTabStopDistance(40)  # 4 spaces
        self.setStyleSheet("""
            QPlainTextEdit {
                background-color: #1e1e1e;
                border: none;
                padding: 10px;
            }
        """)
        
        # Line number area
        self.line_number_area = LineNumberArea(self)
        self.line_number_area.show()  # Explicitly show the line number area
        self.blockCountChanged.connect(self.update_line_number_area_width)
        self.updateRequest.connect(self.update_line_number_area)
        self.update_line_number_area_width(0)
        
        # Syntax highlighter
        self.highlighter = PythonHighlighter(self.document(), settings_manager)
        
        # Error highlighting
        self.error_lines = {}  # Dictionary to store error lines and their messages
        self.error_format = QTextCharFormat()
        self.error_format.setBackground(QColor("#4a1f1f"))
        self.error_format.setUnderlineColor(QColor("#ff6b6b"))
        self.error_format.setUnderlineStyle(QTextCharFormat.UnderlineStyle.WaveUnderline)
        
        # Auto-indentation
        self.textChanged.connect(self.handle_text_change)
        self.last_cursor_position = 0

    def line_number_area_width(self):
        digits = len(str(max(1, self.blockCount())))
        space = 3 + self.fontMetrics().horizontalAdvance('9') * digits
        return max(space, 30)  # Ensure minimum width of 30 pixels

    def update_line_number_area_width(self, _):
        width = self.line_number_area_width()
        self.setViewportMargins(width, 0, 0, 0)

    def update_line_number_area(self, rect, dy):
        if dy:
            self.line_number_area.scroll(0, dy)
        else:
            self.line_number_area.update(0, rect.y(), self.line_number_area.width(), rect.height())
        if rect.contains(self.viewport().rect()):
            self.update_line_number_area_width(0)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        width = self.line_number_area_width()
        self.line_number_area.setGeometry(QRect(cr.left(), cr.top(), width, cr.height()))

    def line_number_area_paint_event(self, event):
        painter = QPainter(self.line_number_area)
        painter.fillRect(event.rect(), QColor("#2d2d2d"))

        # Use the same font as the editor
        painter.setFont(self.font())
        
        block = self.firstVisibleBlock()
        block_number = block.blockNumber()
        offset = self.contentOffset()
        top = self.blockBoundingGeometry(block).translated(offset).top()
        bottom = top + self.blockBoundingRect(block).height()

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(block_number + 1)
                
                # Check if this line has an error
                if block_number in self.error_lines:
                    # Use red color for line numbers with errors
                    painter.setPen(QColor("#ff6b6b"))
                else:
                    # Use normal color for other line numbers
                    painter.setPen(QColor("#d4d4d4"))
                
                painter.drawText(0, int(top), self.line_number_area.width() - 5, self.fontMetrics().height(),
                               Qt.AlignmentFlag.AlignRight, number)

            block = block.next()
            top = bottom
            bottom = top + self.blockBoundingRect(block).height()
            block_number += 1

    def highlight_error_line(self, line_number, error_message):
        """Highlight a specific line with an error message."""
        # Convert line number to block number (0-based)
        block_number = line_number - 1
        
        # Store the error message
        self.error_lines[block_number] = error_message
        
        # Get the block
        block = self.document().findBlockByNumber(block_number)
        if block.isValid():
            # Create a cursor for the block
            cursor = QTextCursor(block)
            cursor.select(QTextCursor.SelectionType.LineUnderCursor)
            
            # Apply the error format
            cursor.mergeCharFormat(self.error_format)
            
            # Update the line number area
            self.line_number_area.update()

    def clear_error_highlights(self):
        """Clear all error highlights."""
        # Clear the error lines dictionary
        self.error_lines.clear()
        
        # Clear the formatting
        cursor = QTextCursor(self.document())
        cursor.select(QTextCursor.SelectionType.Document)
        cursor.setCharFormat(QTextCharFormat())
        
        # Clear the tooltip
        QToolTip.hideText()
        
        # Update the line number area
        self.line_number_area.update()

    def mouseMoveEvent(self, event):
        """Show error tooltip when hovering over error lines."""
        # Get the cursor position
        cursor = self.cursorForPosition(event.pos())
        block_number = cursor.blockNumber()
        
        # Check if this line has an error
        if block_number in self.error_lines:
            # Show the error message as a tooltip
            QToolTip.showText(event.globalPosition().toPoint(), self.error_lines[block_number])
        else:
            QToolTip.hideText()
        
        super().mouseMoveEvent(event)

    def get_indentation_level(self, text):
        """Calculate the indentation level of a line of text."""
        return len(text) - len(text.lstrip())

    def should_increase_indent(self, text):
        """Check if the current line should increase indentation for the next line."""
        # Remove comments and whitespace
        text = text.split('#')[0].strip()
        if not text:
            return False
        
        # Check for statements that should increase indentation
        increase_patterns = [
            r':\s*$',  # Ends with colon
            r'def\s+\w+\s*\(',  # Function definition
            r'class\s+\w+\s*\(?',  # Class definition
            r'if\s+.+:',  # If statement
            r'elif\s+.+:',  # Elif statement
            r'else\s*:',  # Else statement
            r'for\s+.+:',  # For loop
            r'while\s+.+:',  # While loop
            r'try\s*:',  # Try block
            r'except\s+.+:',  # Except block
            r'finally\s*:',  # Finally block
            r'with\s+.+:'  # With statement
        ]
        
        for pattern in increase_patterns:
            if re.search(pattern, text):
                return True
        return False

    def should_decrease_indent(self, text):
        """Check if the current line should decrease indentation for the next line."""
        # Remove comments and whitespace
        text = text.split('#')[0].strip()
        if not text:
            return False
        
        # Check for statements that should decrease indentation
        decrease_patterns = [
            r'^\s*(return|break|continue|pass)\s*$',  # Control flow statements
            r'^\s*raise\s+.+$',  # Raise statement
            r'^\s*return\s+.+$'  # Return with value
        ]
        
        for pattern in decrease_patterns:
            if re.search(pattern, text):
                return True
        return False

    def handle_text_change(self):
        """Handle text changes and implement auto-indentation."""
        cursor = self.textCursor()
        current_position = cursor.position()
        
        # Check if we just added a new line (Enter/Return was pressed)
        if current_position > self.last_cursor_position and self.toPlainText()[current_position-1] == '\n':
            # Get the current block (line)
            current_block = cursor.block()
            previous_block = current_block.previous()
            
            if previous_block.isValid():
                # Get the text of the previous line
                previous_text = previous_block.text()
                
                # Calculate base indentation
                base_indent = self.get_indentation_level(previous_text)
                
                # Check if we should increase or decrease indentation
                if self.should_increase_indent(previous_text):
                    base_indent += 4  # Increase by one level (4 spaces)
                elif self.should_decrease_indent(previous_text):
                    base_indent = max(0, base_indent - 4)  # Decrease by one level
                
                # Apply the indentation
                cursor.insertText(' ' * base_indent)
        
        # Update the last cursor position
        self.last_cursor_position = current_position 

    def update_highlighting(self):
        """Update syntax highlighting based on current settings."""
        if self.highlighter:
            self.highlighter.update_highlighting_rules()
            self.highlighter.rehighlight() 