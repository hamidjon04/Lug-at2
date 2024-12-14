import sqlite3
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QPushButton, QLineEdit,
    QLabel, QWidget, QHBoxLayout, QTableWidget, QTableWidgetItem, QMessageBox
)

# Database functions
def create_database():
    conn = sqlite3.connect('dictionary.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS dictionary (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            english_word TEXT NOT NULL,
            uzbek_word TEXT NOT NULL,
            category TEXT
        );
    ''')
    conn.commit()
    conn.close()

def add_word_to_db(english_word, uzbek_word, category):
    conn = sqlite3.connect('dictionary.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO dictionary (english_word, uzbek_word, category) VALUES (?, ?, ?)',
                   (english_word, uzbek_word, category))
    conn.commit()
    conn.close()

def get_all_words():
    conn = sqlite3.connect('dictionary.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM dictionary')
    rows = cursor.fetchall()
    conn.close()
    return rows

def search_word(search_query):
    conn = sqlite3.connect('dictionary.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM dictionary WHERE english_word LIKE ? OR uzbek_word LIKE ?', 
                   (f'%{search_query}%', f'%{search_query}%'))
    rows = cursor.fetchall()
    conn.close()
    return rows

# PyQt5 GUI
class DictionaryApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Lug'at")
        self.setGeometry(100, 100, 800, 600)

        # Main layout
        layout = QVBoxLayout()
        
        # Buttons
        self.add_word_button = QPushButton("Yangi so'z qo'shish")
        self.add_word_button.clicked.connect(self.show_add_word_dialog)
        
        self.search_word_button = QPushButton("So'zni qidirish")
        self.search_word_button.clicked.connect(self.show_search_dialog)
        
        self.show_all_button = QPushButton("Barcha so'zlarni ko'rish")
        self.show_all_button.clicked.connect(self.show_all_words)

        # Add buttons to layout
        layout.addWidget(self.add_word_button)
        layout.addWidget(self.search_word_button)
        layout.addWidget(self.show_all_button)

        # Main widget
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Store references to dialogs
        self.add_dialog = None
        self.search_dialog = None
        self.table_dialog = None

    # Function to add a new word
    def show_add_word_dialog(self):
        self.add_dialog = QWidget()
        self.add_dialog.setWindowTitle("Yangi so'z qo'shish")
        self.add_dialog.setGeometry(150, 150, 400, 200)

        layout = QVBoxLayout()

        # Input fields
        self.english_word_input = QLineEdit()
        self.english_word_input.setPlaceholderText("Inglizcha so'z")
        self.uzbek_word_input = QLineEdit()
        self.uzbek_word_input.setPlaceholderText("O'zbekcha so'z")
        self.category_input = QLineEdit()
        self.category_input.setPlaceholderText("Kategoriya")

        # Add button
        add_button = QPushButton("Qo'shish")
        add_button.clicked.connect(self.add_word)

        # Add inputs and button to layout
        layout.addWidget(self.english_word_input)
        layout.addWidget(self.uzbek_word_input)
        layout.addWidget(self.category_input)
        layout.addWidget(add_button)

        self.add_dialog.setLayout(layout)
        self.add_dialog.show()

    def add_word(self):
        english_word = self.english_word_input.text().strip()
        uzbek_word = self.uzbek_word_input.text().strip()
        category = self.category_input.text().strip()

        if english_word and uzbek_word:
            add_word_to_db(english_word, uzbek_word, category)
            QMessageBox.information(self, "Muvaffaqiyatli", "So'z muvaffaqiyatli qo'shildi!")
            self.add_dialog.close()
        else:
            QMessageBox.warning(self, "Xato", "Iltimos, barcha maydonlarni to'ldiring!")

    # Function to show all words
    def show_all_words(self):
        words = get_all_words()
        self.display_words_table(words)

    # Function to search for a word
    def show_search_dialog(self):
        self.search_dialog = QWidget()
        self.search_dialog.setWindowTitle("So'zni qidirish")
        self.search_dialog.setGeometry(150, 150, 400, 100)

        layout = QVBoxLayout()

        # Search input
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Qidiruv so'zini kiriting")

        # Search button
        search_button = QPushButton("Qidirish")
        search_button.clicked.connect(self.search_word)

        # Add input and button to layout
        layout.addWidget(self.search_input)
        layout.addWidget(search_button)

        self.search_dialog.setLayout(layout)
        self.search_dialog.show()

    def search_word(self):
        search_query = self.search_input.text().strip()
        if search_query:
            results = search_word(search_query)
            self.display_words_table(results)
            self.search_dialog.close()
        else:
            QMessageBox.warning(self, "Xato", "Iltimos, qidiruv so'zini kiriting!")

    # Function to display words in a table
    def display_words_table(self, words):
        self.table_dialog = QWidget()
        self.table_dialog.setWindowTitle("So'zlar ro'yxati")
        self.table_dialog.setGeometry(150, 150, 600, 400)

        layout = QVBoxLayout()

        table = QTableWidget()
        table.setRowCount(len(words))
        table.setColumnCount(4)
        table.setHorizontalHeaderLabels(["ID", "Inglizcha", "O'zbekcha", "Kategoriya"])

        for row_idx, row_data in enumerate(words):
            for col_idx, col_data in enumerate(row_data):
                table.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))

        layout.addWidget(table)
        self.table_dialog.setLayout(layout)
        self.table_dialog.show()

# Main
if __name__ == "__main__":
    create_database()
    app = QApplication([])
    window = DictionaryApp()
    window.show()
    app.exec_()
