import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QMessageBox, QTextEdit, QFileDialog, QInputDialog,
                             QFontDialog, QColorDialog)
from PyQt6.QtGui import QIcon, QTextCursor, QColor, QAction
from PyQt6.QtCore import Qt
import pathlib

path = str(pathlib.Path(__file__).parent)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initializeUI()

    def initializeUI(self):
        """ set up the application's GUI"""
        self.setMinimumSize(750, 650)
        self.setWindowTitle("1.0 - Cloud 69 Text Editor")

        self.setUpMainWindow()
        self.createAction()
        self.createMenu()
        self.show()

    def setUpMainWindow(self):
        """Create and arrange widgets in the main window"""
        self.text_edit = QTextEdit()
        self.text_edit.textChanged.connect(self.removeHighlights)
        self.setCentralWidget(self.text_edit)

    def createAction(self):
        """ create the application's menu actions"""
        # create actions for File menu
        self.new_act = QAction(QIcon(path + "/images/new_file.png"), "&New")
        self.new_act.setShortcut("Ctrl+N")
        self.new_act.triggered.connect(self.clearText)

        self.open_act = QAction(QIcon(path + "/images/open_file.png"), "&Open")
        self.open_act.setShortcut("Ctrl+O")
        self.open_act.triggered.connect(self.openFile)

        self.save_act = QAction(QIcon(path + "/images/save_file.png"), "&Save")
        self.save_act.setShortcut("Ctrl+S")
        self.save_act.triggered.connect(self.saveFile)

        self.quit_act = QAction(QIcon(path + "/images/quit_file.png"), "&Quit")
        self.quit_act.setShortcut("Ctrl+Q")
        self.quit_act.triggered.connect(self.close)

        # create actions for Edit menu
        self.undo_act = QAction(QIcon(path + "/images/undo.png"), "&Undo")
        self.undo_act.setShortcut("Ctrl+Z")
        self.undo_act.triggered.connect(self.text_edit.undo)

        self.redo_act = QAction(QIcon(path + "/images/redo.png"), "&Redo")
        self.redo_act.setShortcut("Ctrl+Y")
        self.redo_act.triggered.connect(self.text_edit.redo)

        self.cut_act = QAction(QIcon(path + "/images/cut.png"), "&Cut")
        self.cut_act.setShortcut("Ctrl+X")
        self.cut_act.triggered.connect(self.text_edit.cut)

        self.copy_act = QAction(QIcon(path + "/images/copy.png"), "&Copy")
        self.copy_act.setShortcut("Ctrl+C")
        self.copy_act.triggered.connect(self.text_edit.copy)

        self.paste_act = QAction(QIcon(path + "/images/paste.png"), "&Paste")
        self.paste_act.setShortcut("Ctrl+V")
        self.paste_act.triggered.connect(self.text_edit.paste)

        self.find_act = QAction(QIcon(path + "/images/find.png"), "&Find All")
        self.find_act.setShortcut("Ctrl+F")
        self.find_act.triggered.connect(self.searchText)

        # Create actions for Tool menu
        self.font_act = QAction(QIcon(path + "/images/font.png"), "&Font")
        self.font_act.setShortcut("Ctrl+T")
        self.font_act.triggered.connect(self.chooseFont)

        self.color_act = QAction(QIcon(path + "/images/color.png"), "&Color")
        self.color_act.setShortcut("Ctrl+Shift+C")
        self.color_act.triggered.connect(self.chooseFontColor)

        self.highlight_act = QAction(QIcon(path + "/images/highlight.png"), "&Highlight")
        self.highlight_act.setShortcut("Ctrl+Shift+H")
        self.highlight_act.triggered.connect(self.chooseFontBackgroundColor)

        # create actions for Help Menu
        self.about_act = QAction("About")
        self.about_act.triggered.connect(self.aboutDialog)

    def createMenu(self):
        """ create the application's menu bar"""
        # self.menuBar().setNativeMenuBar(False)       # macOS
        # create file menu and add actions

        file_menu = self.menuBar().addMenu("File")
        file_menu.addAction(self.new_act)
        file_menu.addSeparator()
        file_menu.addAction(self.open_act)
        file_menu.addAction(self.save_act)
        file_menu.addSeparator()
        file_menu.addAction(self.quit_act)

        # create Edit menu and actions
        edit_menu = self.menuBar().addMenu("Edit")
        edit_menu.addAction(self.undo_act)
        edit_menu.addAction(self.redo_act)
        edit_menu.addSeparator()
        edit_menu.addAction(self.cut_act)
        edit_menu.addAction(self.copy_act)
        edit_menu.addAction(self.paste_act)
        edit_menu.addSeparator()
        edit_menu.addAction(self.find_act)

        # create Tools menu and add actions
        tool_menu = self.menuBar().addMenu("Tools")
        tool_menu.addAction(self.font_act)
        tool_menu.addAction(self.color_act)
        tool_menu.addAction(self.highlight_act)

        # create Help menu and add actions
        help_menu = self.menuBar().addMenu("Help")
        help_menu.addAction(self.about_act)

    def clearText(self):
        """ Clear the QTextEdit field"""
        answer = QMessageBox.question(self, "Clear Text", "Do you wan to clear the Text",
                                      QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                      QMessageBox.StandardButton.Yes)
        if answer == QMessageBox.StandardButton.Yes:
            self.text_edit.clear()

    def openFile(self):
        """ Open a text or html file and display it content in the text edit field"""
        file_name, _ = QFileDialog.getOpenFileName(self, "Open File", "", "HTML Files (*.html);;Text Files (*.txt)")
        if file_name:
            with open(file_name, mode="r") as f:
                notepad_txt = f.read()
                self.text_edit.setText(notepad_txt)

    def saveFile(self):
        """If the save button is clicked, display dialog asking user if they want to save the text in
        the text edit field to a text or rich text file."""
        file_name, _ = QFileDialog.getSaveFileName(self, "Save File", "", "Text Files (*.txt);;HTML Files (*.html)")
        if file_name.endswith(".txt"):
            notepad_text = self.text_edit.toPlainText()
            with open(file_name, mode="w") as f:
                f.write(notepad_text)

        elif file_name.endswith(".html"):
            notepad_text = self.text_edit.toHtml()
            with open(file_name, mode="w") as f:
                f.write(notepad_text)
        else:
            QMessageBox.information(self, "Not saved", "Text not saved", QMessageBox.StandardButton.Ok)

    def searchText(self):
        """ search for text"""
        # Display input dialog to ask user for text to find
        find_text, ok = QInputDialog.getText(self, "Search Text", "Find:")
        if ok:
            extra_selections = []
            # set the cursor to the beginning
            self.text_edit.moveCursor(QTextCursor.MoveOperation.Start)
            color = QColor(Qt.GlobalColor.gray)

            while self.text_edit.find(find_text):
                # use ExtraSelection() to mark the text you are searching for as gray
                selection = QTextEdit.ExtraSelection()
                selection.format.setBackground(color)

                # set the cursor of the selection
                selection.cursor = self.text_edit.textCursor()
                extra_selections.append(selection)

            # Highlight all selections in the QTextEdit widget
            self.text_edit.setExtraSelections(extra_selections)

    def removeHighlights(self):
        """ Reset extra selections after editing text."""
        self.text_edit.setExtraSelections([])

    def chooseFont(self):
        """ Select a font from the QFontDialog"""
        current = self.text_edit.currentFont()
        opt = QFontDialog.FontDialogOption.DontUseNativeDialog
        font, ok = QFontDialog.getFont(current, self, options=opt)
        if ok:
            self.text_edit.setFont(font)

    def chooseFontColor(self):
        """ select a font color from QColorDialog"""
        font_color = QColorDialog.getColor()
        if font_color.isValid():
            self.text_edit.setTextColor(font_color)

    def chooseFontBackgroundColor(self):
        """ Select a color for text's background"""
        text_background_color = QColorDialog.getColor()
        if text_background_color.isValid():
            self.text_edit.setTextBackgroundColor(text_background_color)

    def aboutDialog(self):
        """ Provide information about Application"""
        QMessageBox.about(self, "About Cloud 69",
                          """
                          <p>1.0 - Cloud 69</p>
                          <p>Made with love by Prince</p>
                          """
                          )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(path + "/images/3_watermelon.png"))
    window = MainWindow()
    sys.exit(app.exec())
