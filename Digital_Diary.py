import os
import re
import sys
import time
from datetime import datetime

from PyQt5.QtCore import QStringListModel, Qt
from PyQt5.QtGui import QImage, QFont, QTextCursor, QIcon, \
    QPixmap
from PyQt5.QtWidgets import QTextBrowser, QPushButton, QListView, QGridLayout, QApplication, QMainWindow, \
    QWidget, QSplitter, QDialog, QTextEdit, QLineEdit, QLabel, QFileDialog, QMessageBox, QComboBox


# 3nd try
class ToDoPyQt5(QMainWindow):
    def __init__(self):
        # setup
        super().__init__()
        self.setGeometry(100, 100, 1000, 600)
        self.setWindowIcon(QIcon("journal_data/icons/diary.png"))
        self.setWindowTitle("Digital Diary")
        # central widget
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        central_widget.setLayout(QGridLayout())
        # sub windows
        index_windows = QWidget(central_widget)
        index_windows.setLayout(QGridLayout())
        index_windows.setStyleSheet("background-color: #9bc472;")
        view_windows = QWidget(central_widget)
        view_windows.setLayout(QGridLayout())
        view_windows.setStyleSheet("background-color: #9bc472;")
        button_windows = QWidget(central_widget)
        button_windows.setLayout(QGridLayout())
        button_windows.setStyleSheet("background-color: #9bc472;")
        # splitter
        splitter = QSplitter()
        splitter.setStyleSheet("QSplitter::handle { background-color: #9bc472; }")
        splitter.addWidget(index_windows)
        splitter.addWidget(view_windows)
        splitter.addWidget(button_windows)

        # element adding
        # index window
        entry_label = QLabel("<font face = 'Aclonica' size = '4'>Entries</font>",index_windows)
        index_windows.layout().addWidget(entry_label)
        # list: to show the entry
        self.index = QListView(index_windows)
        index_windows.layout().addWidget(self.index)
        self.index.setStyleSheet("background-color: #cdf6db;")
        self.populateListView()
        # view window
        self.view_label = QLabel("<font face = 'Aclonica' size = '4'>None</font>", index_windows)
        view_windows.layout().addWidget(self.view_label)
        self.view = QTextBrowser()
        view_windows.layout().addWidget(self.view)
        self.view.setStyleSheet("background-color: #cdf6db;")
        # button Window
        # open button
        self.open_button = QPushButton(button_windows)
        button_windows.layout().addWidget(self.open_button)
        self.open_button.clicked.connect(self.open_click)
        self.open_button.setStyleSheet("background-color: #9bc472;")
        self.open_button.setIcon(QIcon(r"journal_data/icons/folder.png"))
        self.open_button.setToolTip("Open Entry")
        # Add button
        self.add_button = QPushButton(button_windows)
        button_windows.layout().addWidget(self.add_button)
        self.add_button.clicked.connect(self.add_click)
        self.add_button.setStyleSheet("background-color: #9bc472;")
        self.add_button.setIcon(QIcon(r"journal_data/icons/plus-symbol-button.png"))
        self.add_button.setToolTip("Add New Entry")
        # Edit button
        self.edit_button = QPushButton(button_windows)
        button_windows.layout().addWidget(self.edit_button)
        self.edit_button.clicked.connect(self.edit_click)
        self.edit_button.setStyleSheet("background-color: #9bc472;")
        self.edit_button.setIcon(QIcon(r"journal_data/icons/editing.png"))
        self.edit_button.setToolTip("Edit Entry")
        # delete button
        self.delete_button = QPushButton(button_windows)
        button_windows.layout().addWidget(self.delete_button)
        self.delete_button.clicked.connect(self.delete_click)
        self.delete_button.setStyleSheet("background-color: #9bc472;")
        self.delete_button.setIcon(QIcon(r"journal_data/icons/trash.png"))
        self.delete_button.setToolTip("Delete Entry")
        # about button
        self.about_button = QPushButton(button_windows)
        button_windows.layout().addWidget(self.about_button)
        self.about_button.clicked.connect(self.about_click)
        self.about_button.setStyleSheet("background-color: #9bc472;")
        self.about_button.setIcon(QIcon(r"journal_data/icons/info.png"))
        self.about_button.setToolTip("About")

        # Set the stretch factors to make view_windows take max space
        splitter.setStretchFactor(0, 1)  # Index window
        splitter.setStretchFactor(1, 3)  # View window
        splitter.setStretchFactor(2, 1)  # Button window

        # splitter set
        self.setCentralWidget(splitter)


    def about_click(self):
        about_windows = QDialog()
        about_windows.setLayout(QGridLayout())
        about_windows.setGeometry(400, 150, 400, 300)
        about_windows.setWindowIcon(QIcon("journal_data/icons/info.png"))
        about_windows.setWindowTitle("About")
        about_windows.setStyleSheet("background-color: #3a6b35;")
        image_path = "journal_data/icons/diary.png"  # Replace with the actual path to your image
        pixmap = QPixmap(image_path)
        pixmap = pixmap.scaled(200, 200, Qt.KeepAspectRatio)

        # Create a QLabel to display the image
        image_label = QLabel()
        image_label.setPixmap(pixmap)
        about_label = QLabel("<font face = 'Aclonica' size = '4'>Made by Md. Tahir Amin Ansari<br>Contact: "
                             "rk9401424@gmail.com",about_windows)

        about_windows.layout().addWidget(image_label)
        about_windows.layout().setAlignment(image_label, Qt.AlignCenter)
        about_windows.layout().addWidget(about_label)
        about_windows.layout().setAlignment(about_label, Qt.AlignCenter)
        # Create a button to close the dialog
        close_button = QPushButton("Close",about_windows)
        close_button.clicked.connect(about_windows.accept)
        # Add the close button to the layout
        about_windows.layout().addWidget(close_button)
        about_windows.layout().setAlignment(close_button, Qt.AlignCenter)
        close_button.setStyleSheet("background-color: #e3b448;")
        about_windows.exec_()
    def delete_click(self):
        try:
            file_to_be_deleted = self.selection()
            user_response = self.warning(f"Are sure you want to delete <b>{file_to_be_deleted}</b> ?")
            if user_response == "ok":
                os.remove(f"journal_data/{file_to_be_deleted}.html")
                self.warning(f"<b>{file_to_be_deleted}</b> was deleted.")
                self.populateListView()
        except:
            self.warning("No Files Selected!<br>Select a file to delete.")

    def edit_click(self):

        existing_title = self.selection()

        try:
            if existing_title:
                with open(f"journal_data/{existing_title}.html", 'r') as file:
                    existing_entry = file.read()
            self.editor(mode="edit", existing_title=existing_title, existing_entry=existing_entry)
        except:
            self.warning("<h3>Cannot Open File.<br>Please select a valid file to open!")

    def add_click(self):
        self.editor(mode="new", existing_title=None, existing_entry=None)

    def editor(self, mode="new", existing_title=None, existing_entry=None):
        self.add_window = QDialog()  # open a new window
        self.add_window.setLayout(QGridLayout())
        self.add_window.setGeometry(140, 150, 900, 500)
        self.add_window.setWindowIcon(QIcon("journal_data/icons/editing.png"))
        self.add_window.setWindowTitle("Editor")
        self.add_window.setStyleSheet("background-color: #3a6b35;")
        # widget
        # title label
        title_label = QLabel("<font face = 'Aclonica' size = '5'>Title</font>", self.add_window)
        self.add_window.layout().addWidget(title_label, 0, 0, 1, -1)
        # title field
        title_field = QLineEdit(self.add_window)
        self.add_window.layout().addWidget(title_field, 1, 0, 1, -1)
        title_field.setStyleSheet("background-color: #cbd18f;")
        # body label
        body_label = QLabel("<font face = 'Aclonica' size = '5'>Body</font>", self.add_window)
        self.add_window.layout().addWidget(body_label, 2, 0, 1, -1)
        # we will enter here
        entry_field = QTextEdit(self.add_window)
        self.add_window.layout().addWidget(entry_field, 3, 0, 1, -1)
        entry_field.setStyleSheet("background-color: #cbd18f;")

        # if mode is editing
        if mode == "edit":
            title_field.setText(existing_title)
            entry_field.setHtml(existing_entry)
        # buttons
        # save button
        save_button = QPushButton(self.add_window)
        self.add_window.layout().addWidget(save_button, 4, 0)
        save_button.setStyleSheet("background-color: #e3b448;")
        save_button.setIcon(QIcon(r"journal_data/icons/diskette.png"))
        save_button.setToolTip("Save")

        if mode == "edit":
            save_button.clicked.connect(lambda: self.save_click(title_field, entry_field, mode="edit"))
        else:
            save_button.clicked.connect(lambda: self.save_click(title_field, entry_field, mode="new"))
        # image button
        image_button = QPushButton(self.add_window)
        self.add_window.layout().addWidget(image_button, 4, 1)
        image_button.clicked.connect(lambda: self.image_click(entry_field))
        image_button.setStyleSheet("background-color: #e3b448;")
        image_button.setIcon(QIcon(r"journal_data/icons/photo.png"))
        image_button.setToolTip("Add Image")
        # editing buttons
        # bold
        bold_button = QPushButton(self.add_window)
        self.add_window.layout().addWidget(bold_button, 4, 2)
        bold_button.clicked.connect(lambda: self.bold_click(entry_field))
        bold_button.setStyleSheet("background-color: #e3b448;")
        bold_button.setIcon(QIcon(r"journal_data/icons/bold.png"))
        bold_button.setToolTip("Bold Button")


        # italic
        italic_button = QPushButton(self.add_window)
        self.add_window.layout().addWidget(italic_button, 4, 3)
        italic_button.clicked.connect(lambda: self.italic_click(entry_field))
        italic_button.setStyleSheet("background-color: #e3b448;")
        italic_button.setIcon(QIcon(r"journal_data/icons/italics.png"))
        italic_button.setToolTip("Italic Button")
        # underline
        underline_button = QPushButton(self.add_window)
        self.add_window.layout().addWidget(underline_button, 4, 4)
        underline_button.clicked.connect(lambda: self.underline_click(entry_field))
        underline_button.setStyleSheet("background-color: #e3b448;")
        underline_button.setIcon(QIcon(r"journal_data/icons/underlined-text.png"))
        underline_button.setToolTip("Underline")
        # change font combobox
        self.font_list(entry_field)
        # (lambda: self.change_font(entry_field, font_name="Aclonica", font_size=10))  # func to
        # change font)
        self.add_window.exec_()  # runs in non-main window interactive way

    def font_list(self, entry_field):
        font_combobox = QComboBox(self.add_window)
        self.add_window.layout().addWidget(font_combobox,4,5)
        font_combobox.setStyleSheet("background-color: #e3b448;")
        font_combobox.addItem("Arial")
        font_combobox.addItem("Bahnschrift")
        font_combobox.addItem("Calibri Light")
        font_combobox.addItem("Comic Sans MS")
        font_combobox.addItem("Consolas")
        font_combobox.addItem("Constantia")
        font_combobox.addItem("Georgia")
        font_combobox.addItem("Gadugi")
        font_combobox.addItem("Gabriola")
        font_combobox.addItem("Franklin Gothic Medium")
        font_combobox.addItem("Ebrima")
        font_combobox.addItem("Courier New")
        font_combobox.activated[str].connect(lambda font_name: self.change_font(entry_field, font_name))

    def change_font(self, entry_field, font_name):
        # Store the current cursor position and selected text
        cursor = entry_field.textCursor()
        cursor_position = cursor.position()
        selected_text = cursor.selectedText()

        # Apply the font change to the selected text
        font_text = f"<font face='{font_name}' size='5'>" + selected_text + "</font>"
        cursor.insertHtml(font_text)

        # Restore the selection
        new_cursor = QTextCursor(entry_field.document())
        new_cursor.setPosition(cursor_position)
        new_cursor.setPosition(cursor_position + len(font_text), QTextCursor.KeepAnchor)
        entry_field.setTextCursor(new_cursor)

    def bold_click(self, entry_field):
        format = entry_field.currentCharFormat()
        is_bold = format.fontWeight() == QFont.Bold
        format.setFontWeight(QFont.Bold if not is_bold else QFont.Normal)
        entry_field.mergeCurrentCharFormat(format)

    def italic_click(self, entry_field):
        format = entry_field.currentCharFormat()
        is_italic = format.fontItalic()
        format.setFontItalic(not is_italic)
        entry_field.mergeCurrentCharFormat(format)

    def underline_click(self, entry_field):
        format = entry_field.currentCharFormat()
        is_underline = format.fontUnderline()
        format.setFontUnderline(not is_underline)
        entry_field.mergeCurrentCharFormat(format)

    def save_click(self, title_field, entry_field, mode="new"):
        # logic for saving file
        # retrieving content from text edit
        title = title_field.text()
        file_name = self.file_name_sanitizer(title)
        doc_content = entry_field.document()
        html_content = doc_content.toHtml()

        if mode == "edit":
            if title and html_content:
                with open(f"journal_data/{file_name}.html", "w", encoding="utf-8") as file:
                    file.write(html_content)
                self.add_window.accept()
                self.populateListView()
        else:
            if title and html_content and self.duplicate_check(file_name):
                with open(f"journal_data/{file_name}.html", "w", encoding="utf-8") as file:
                    file.write(f"Date:{self.time_now()}")
                    file.write(f"<center><h1>{title}<h/1></center>")
                    file.write("<font face='Arial' size='5'>")
                    file.write(html_content)
                    file.write("</font>")
                self.add_window.accept()
                self.populateListView()

    def duplicate_check(self, title):
        if title in self.getFiles_list():
            self.warning("<h3>File name already Exist!")
            return False
        else:
            return True

    def file_name_sanitizer(self, title):
        title = title.strip()
        title = re.sub(r'[\/:*?"<>|]', '_', title)
        if len(title) > 10:
            title = title[:10]
        return title

    def image_click(self, entry_field):
        image = self.load_image()  # load image using dialog
        if image:
            resized_image = self.resize_image(image)  # resize image
            entry_field.insertHtml(f"<br><center><img src={resized_image}></center><br>")  # enter image

    def resize_image(self, image):
        temp_image = QImage(image)
        temp_image = temp_image.scaled(200, 150, aspectRatioMode=Qt.KeepAspectRatio)
        time_stamp = str(int(time.time()))
        temp_image.save(f"journal_data/resized_image{time_stamp}.jpg")
        return f"journal_data/resized_image{time_stamp}.jpg"

    def time_now(self):
        # Get the current date and time
        current_datetime = datetime.now()
        # Format the date and time as required
        formatted_datetime = current_datetime.strftime("%d_%m_%Y__%H_%M")
        # Print the formatted date and time
        return formatted_datetime

    def load_image(self):
        # Create an options object for the file dialog
        options = QFileDialog().options()
        # Create an instance of QFileDialog
        file_dialog = QFileDialog()
        image_path, _ = file_dialog.getOpenFileNames(self, "Select an image", r"C:\Users\Administrator\Pictures",
                                                     "Image Files (*.jpeg *.jpg *.gif)",
                                                     options=options)
        if image_path:
            return image_path[0]

    def open_click(self):
        self.load_file()

    # hmm mm...?
    def selection(self):
        selected_file_index = self.index.currentIndex()
        return selected_file_index.data()

    def load_file(self):
        try:

            selected_file = self.selection()
            if selected_file:
                with open(f"journal_data/{selected_file}.html", 'r') as file:
                    html_content = file.read()
                    self.view.setHtml(html_content)
                    self.view_label.setText(f"<font face = 'Aclonica' size = '4'>{selected_file}</font>")

        except:
            self.warning("<h3> Cannot OPen File")

    def warning(self, warning_message):

        message_box = QMessageBox()
        message_box.setIcon(QMessageBox.Warning)
        message_box.setText(warning_message)
        message_box.setWindowTitle("Warning")
        message_box.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        result = message_box.exec_()

        if result == QMessageBox.Ok:
            return "ok"
        else:
            return "cancel"

    def getFiles_list(self):
        file_list = []
        files = os.listdir("journal_data")
        for file in files:
            if file.endswith(".html"):
                #  remove the html extension
                base_name = os.path.splitext(file)[0]
                file_list.append(base_name)
        return file_list

    def populateListView(self):
        # populate  the list with file names
        # Get the list of file names
        file_list = self.getFiles_list()

        # Create a QStringListModel and set the data
        self.model = QStringListModel(file_list)
        self.index.setModel(self.model)


if __name__ == "__main__":
    app = QApplication([])
    main_window = ToDoPyQt5()
    main_window.show()
    sys.exit(app.exec_())
