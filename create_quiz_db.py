import sqlite3
import os

def create_quiz_database(db_name="quiz.db"):
    if os.path.exists(db_name):
        print(f"Database '{db_name}' already exists. Skipping creation.")
        return

    conn = None
    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        # Create Categories table
        cursor.execute('''
            CREATE TABLE Categories (
                CategoryID INTEGER PRIMARY KEY AUTOINCREMENT,
                CategoryName TEXT NOT NULL UNIQUE
            )
        ''')

        # Create Questions table
        cursor.execute('''
            CREATE TABLE Questions (
                QuestionID INTEGER PRIMARY KEY AUTOINCREMENT,
                CategoryID INTEGER,
                QuestionText TEXT NOT NULL,
                FOREIGN KEY (CategoryID) REFERENCES Categories(CategoryID)
            )
        ''')

        # Create Answers table
        cursor.execute('''
            CREATE TABLE Answers (
                AnswerID INTEGER PRIMARY KEY AUTOINCREMENT,
                QuestionID INTEGER,
                AnswerText TEXT NOT NULL,
                IsCorrect BOOLEAN NOT NULL, -- 0 for false, 1 for true
                FOREIGN KEY (QuestionID) REFERENCES Questions(QuestionID)
            )
        ''')

        # Insert some sample data
        cursor.execute("INSERT INTO Categories (CategoryName) VALUES ('General Knowledge')")
        cursor.execute("INSERT INTO Categories (CategoryName) VALUES ('Science')")
        cursor.execute("INSERT INTO Categories (CategoryName) VALUES ('History')")

        # Get Category IDs
        cursor.execute("SELECT CategoryID FROM Categories WHERE CategoryName = 'General Knowledge'")
        general_knowledge_id = cursor.fetchone()[0]

        cursor.execute("SELECT CategoryID FROM Categories WHERE CategoryName = 'Science'")
        science_id = cursor.fetchone()[0]

        # Insert General Knowledge Questions and Answers
        cursor.execute("INSERT INTO Questions (CategoryID, QuestionText) VALUES (?, ?)",
                       (general_knowledge_id, "What is the capital of France?"))
        q1_id = cursor.lastrowid
        cursor.execute("INSERT INTO Answers (QuestionID, AnswerText, IsCorrect) VALUES (?, ?, ?)", (q1_id, "Berlin", 0))
        cursor.execute("INSERT INTO Answers (QuestionID, AnswerText, IsCorrect) VALUES (?, ?, ?)", (q1_id, "Madrid", 0))
        cursor.execute("INSERT INTO Answers (QuestionID, AnswerText, IsCorrect) VALUES (?, ?, ?)", (q1_id, "Paris", 1))
        cursor.execute("INSERT INTO Answers (QuestionID, AnswerText, IsCorrect) VALUES (?, ?, ?)", (q1_id, "Rome", 0))

        cursor.execute("INSERT INTO Questions (CategoryID, QuestionText) VALUES (?, ?)",
                       (general_knowledge_id, "Which planet is known as the Red Planet?"))
        q2_id = cursor.lastrowid
        cursor.execute("INSERT INTO Answers (QuestionID, AnswerText, IsCorrect) VALUES (?, ?, ?)", (q2_id, "Earth", 0))
        cursor.execute("INSERT INTO Answers (QuestionID, AnswerText, IsCorrect) VALUES (?, ?, ?)", (q2_id, "Mars", 1))
        cursor.execute("INSERT INTO Answers (QuestionID, AnswerText, IsCorrect) VALUES (?, ?, ?)", (q2_id, "Jupiter", 0))
        cursor.execute("INSERT INTO Answers (QuestionID, AnswerText, IsCorrect) VALUES (?, ?, ?)", (q2_id, "Venus", 0))

        # Insert Science Question and Answers
        cursor.execute("INSERT INTO Questions (CategoryID, QuestionText) VALUES (?, ?)",
                       (science_id, "What is the chemical symbol for water?"))
        q3_id = cursor.lastrowid
        cursor.execute("INSERT INTO Answers (QuestionID, AnswerText, IsCorrect) VALUES (?, ?, ?)", (q3_id, "O2", 0))
        cursor.execute("INSERT INTO Answers (QuestionID, AnswerText, IsCorrect) VALUES (?, ?, ?)", (q3_id, "H2O", 1))
        cursor.execute("INSERT INTO Answers (QuestionID, AnswerText, IsCorrect) VALUES (?, ?, ?)", (q3_id, "CO2", 0))
        cursor.execute("INSERT INTO Answers (QuestionID, AnswerText, IsCorrect) VALUES (?, ?, ?)", (q3_id, "NaCl", 0))

        conn.commit()
        print(f"Database '{db_name}' created and populated with sample data successfully.")

    except sqlite3.Error as e:
        print(f"Error creating database: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    create_quiz_database("quiz.db")