from PyQt5 import QtWidgets, QtCore, QtGui
from quiz_ui import Ui_MainWindow # Correctly importing Ui_MainWindow

class QuizUiForm(QtWidgets.QWidget):
    """
    Wrapper class for your quiz.ui.
    This class correctly embeds the content of a QMainWindow-designed UI
    into a QWidget, making it suitable for use within a QStackedWidget
    in the main application window.
    """
    def __init__(self):
        super().__init__()
        print("QuizUiForm: Initializing...") # Debug print

        # Set a larger minimum size for the QuizUiForm itself.
        # This is crucial to ensure it gets enough space when embedded in other layouts,
        # especially for the QToolBox content to be fully visible.
        self.setMinimumSize(620, 650) # Increased minimum size (width, height)
        print(f"QuizUiForm: Set minimum size to {self.minimumSize().width()}x{self.minimumSize().height()}.")


        self.ui = Ui_MainWindow() # Instantiate the auto-generated UI class for quiz.ui

        # Create a temporary QMainWindow instance. The Ui_MainWindow class (from quiz_ui.py)
        # is designed to set up its widgets on a QMainWindow.
        temp_quiz_window = QtWidgets.QMainWindow()
        try:
            # Set up the UI on this temporary QMainWindow. This populates it with all the
            # widgets defined in your quiz.ui file.
            self.ui.setupUi(temp_quiz_window)
            print("QuizUiForm: setupUi successful on temporary QMainWindow.") # Debug print
        except Exception as e:
            # If there's an error during UI setup, display a simple error message.
            print(f"QuizUiForm: Error during setupUi on temporary QMainWindow: {e}") # Debug print for errors
            layout = QtWidgets.QVBoxLayout(self)
            layout.addWidget(QtWidgets.QLabel("Error loading quiz UI. Check console for details."))
            self.setLayout(layout)
            return # Exit early if UI setup fails

        # After setupUi, the actual content of your quiz (the central widget)
        # is now inside `temp_quiz_window`. We need to extract it.
        quiz_content_widget = temp_quiz_window.centralWidget()

        if quiz_content_widget:
            # Reparent the extracted central widget to this QuizUiForm (which is a QWidget).
            # This effectively moves all the quiz's UI elements into this wrapper widget.
            quiz_content_widget.setParent(self)

            # Set the layout of this QuizUiForm to contain the extracted quiz content.
            # A QVBoxLayout is used to ensure the content fills the available space.
            layout = QtWidgets.QVBoxLayout(self)
            layout.addWidget(quiz_content_widget)
            layout.setContentsMargins(0, 0, 0, 0) # Remove extra margins around the content if desired
            self.setLayout(layout) # Apply the layout to this QuizUiForm widget
            print("QuizUiForm: Layout set with quiz content.") # Debug print
        else:
            # Handle the case where no central widget was found (unexpected).
            print("QuizUiForm: No central widget found in Ui_MainWindow setup for quiz.") # Debug print
            layout = QtWidgets.QVBoxLayout(self)
            layout.addWidget(QtWidgets.QLabel("Quiz content not found. Check quiz_ui.py."))
            self.setLayout(layout)

        # Ensure the temporary QMainWindow is explicitly deleted to free up resources.
        temp_quiz_window.deleteLater()
        print("QuizUiForm: Temporary QMainWindow deleted.") # Debug print

        # --- Internal Quiz Page Navigation ---
        # Your quiz_ui.py uses a QToolBox named 'toolBox' to manage its two pages.
        # Page 0: Settings (objectName 'widget')
        # Page 1: Question Display (objectName 'page_2')

        if hasattr(self.ui, 'toolBox'): # Check if the toolBox exists in quiz_ui
            print(f"QuizUiForm: Found toolBox with objectName: {self.ui.toolBox.objectName()}")
            print(f"QuizUiForm: toolBox has {self.ui.toolBox.count()} pages.")

            # The QToolBox itself should expand to fill available space
            self.ui.toolBox.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
            print("QuizUiForm: Set toolBox sizePolicy to Expanding, Expanding.")

            # Connect the "Get New Question" button (pushButton_4) on the settings page (Page 0)
            # to switch to the question display page (Page 1).
            if hasattr(self.ui, 'pushButton_4'):
                self.ui.pushButton_4.clicked.connect(lambda: self.ui.toolBox.setCurrentIndex(1))
                print("QuizUiForm: 'Get New Question' button (pushButton_4) connected to Quiz Question page (index 1).")
            else:
                print("QuizUiForm: 'pushButton_4' (Get New Question button) not found. Please check quiz.ui object names.")

            # Connect the "Try Again" button (pushButton) on the question page (Page 1)
            # to switch back to the settings page (Page 0).
            if hasattr(self.ui, 'pushButton'):
                self.ui.pushButton.clicked.connect(lambda: self.ui.toolBox.setCurrentIndex(0))
                print("QuizUiForm: 'Try Again' button (pushButton) connected to Quiz Settings page (index 0).")
            else:
                print("QuizUiForm: 'pushButton' (Try Again button) not found. Consider adding a way to return to settings.")

            # Set the initial page of the internal quiz toolBox to the settings page (Page 0)
            self.ui.toolBox.setCurrentIndex(0)
            print(f"QuizUiForm: Initial internal page set to Quiz Settings (index 0). Current index is now: {self.ui.toolBox.currentIndex()}")
        else:
            print("QuizUiForm: No internal 'toolBox' found in quiz_ui.py. Please ensure your quiz.ui uses a QToolBox for its pages.")

        print("QuizUiForm: Initialized and UI setup completed.") # Debug print
