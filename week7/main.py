from PySide6.QtWidgets import (QMessageBox, QLabel, QFileDialog, QGridLayout, QHBoxLayout, QTimeEdit ,QPushButton, QTextEdit, QWidget, QApplication, QDateEdit)
from PySide6.QtCore import Qt
import sys

message = {'date':'2000-01-01', 'time': '12:00', 'message': 'this is my first journal'}

app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle("Journal maker")
window.resize(400, 300)
layout = QGridLayout(window)

window.setStyleSheet("""
    QPushButton {
        background-color: #e5c890;
        color: #4c4f69;
        border: none;
        border-radius: 6px;
        padding: 8px 16px;
    }
    QPushButton:hover {
        background-color: #f5a97f;
    }
    QLabel{

        font-size: 23px;
        color:  #91d7e3;   
                
    }
    QTextEdit{
        background-color: #babbf1;
        color: #292c3c;
    }
    QTimeEdit{
        background-color: #babbf1;
        color: #292c3c;
    }
    QDateEdit{
        background-color: #babbf1;
        color: #292c3c;
    }
""")

def save_file():
    folder = QFileDialog.getExistingDirectory(window, "Pick a folder to save journal in")
    with open(f'{folder}/journal.txt', "w") as f:
        f.write(f"Journal Created at {message['date']} on {message['time']} \n\njournal: {message['message']}")
    
    QMessageBox.information(window, "Saved", f"Your file has been saved, and can be found at {folder}/journal.txt !")

def update_file():
    path, _ = QFileDialog.getOpenFileName(
    window,
    "Open File",
    "", # indicates to use last directory that was used
    "Text Files (*.txt);;All Files (*)"
)
    if path:
        with open(path, 'r+') as f:
            content = f.read()+ f"\n____________________________________________________________________________________\nJournal Created at {message['date']} on {message['time']} \n\njournal: {message['message']}"
            f.seek(0)
            f.truncate(0)
            f.write(content)
    
    QMessageBox.information(window, "Updated", f"Your journal has been added to the file: {path}!")
    


def update_date(date_value):
    message['date'] = date_value.toString("yyyy-MM-dd")

def update_time(time_value):
    message['time'] = time_value.toString("HH:mm")

def update_journal():
    message['message'] = journal.toPlainText()


date = QDateEdit()
time = QTimeEdit()
journal = QTextEdit('Enter Journal')
title = QLabel("Journal Maker")
title.setAlignment(Qt.AlignCenter)
button_row = QHBoxLayout()
save = QPushButton("Create new journal")
add = QPushButton("Add to existing journal")


add.clicked.connect(update_file)
save.clicked.connect(save_file)
date.dateChanged.connect(update_date)
time.timeChanged.connect(update_time)
journal.textChanged.connect(update_journal)

button_row.addWidget(save)
button_row.addWidget(add)
layout.addWidget(date,1,0)
layout.addWidget(time,2,0)
layout.addWidget(journal,3,0)
layout.addLayout(button_row, 4,0)
layout.addWidget(title,0,0)
window.show()
app.exec()
