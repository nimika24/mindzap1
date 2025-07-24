from PyQt5 import QtWidgets, QtCore, QtGui
import webbrowser

from sidebar_ui import Ui_MainWindow
from quiz_form import QuizUiForm  # Import your QuizUiForm wrapper

class SidebarUiForm(QtWidgets.QWidget):
    logout_requested = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()
        print("SidebarUiForm: Initializing...")

        self.setMinimumSize(1024, 768)
        print(f"SidebarUiForm: Set minimum size to {self.minimumSize().width()}x{self.minimumSize().height()}.")

        self.ui = Ui_MainWindow()

        temp_main_window = QtWidgets.QMainWindow()
        self.ui.setupUi(temp_main_window)

        dashboard_content_widget = temp_main_window.centralWidget()
        if dashboard_content_widget:
            dashboard_content_widget.setParent(self)
            layout = QtWidgets.QVBoxLayout(self)
            layout.addWidget(dashboard_content_widget)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)
            self.setLayout(layout)
            print("SidebarUiForm: Layout set with dashboard content.")
        else:
            print("SidebarUiForm: No central widget found in Ui_MainWindow setup.")
            layout = QtWidgets.QVBoxLayout(self)
            layout.addWidget(QtWidgets.QLabel("Dashboard content not found."))
            self.setLayout(layout)

        temp_main_window.deleteLater()
        print("SidebarUiForm: Temporary QMainWindow deleted.")

        # Set size policy for stackedWidget
        if hasattr(self.ui, 'stackedWidget'):
            self.ui.stackedWidget.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
            print("SidebarUiForm: Set stackedWidget sizePolicy to Expanding.")

            # --- REPLACE placeholder page_3 with real QuizUiForm ---
            quiz_placeholder = self.ui.stackedWidget.findChild(QtWidgets.QWidget, "page_3")
            self.quiz_form_widget = QuizUiForm()

            if quiz_placeholder:
                quiz_page_index = self.ui.stackedWidget.indexOf(quiz_placeholder)
                self.ui.stackedWidget.removeWidget(quiz_placeholder)
                self.ui.stackedWidget.insertWidget(quiz_page_index, self.quiz_form_widget)
                print(f"Replaced placeholder 'page_3' with QuizUiForm at index {quiz_page_index}")
            else:
                quiz_page_index = self.ui.stackedWidget.addWidget(self.quiz_form_widget)
                print(f"'page_3' not found; added QuizUiForm at index {quiz_page_index}")

            # Connect quiz buttons to switch to quiz page
            if hasattr(self.ui, 'quizze_btn_1'):
                self.ui.quizze_btn_1.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(quiz_page_index))
                print("Connected quizze_btn_1 to quiz page.")
            if hasattr(self.ui, 'quizze_btn_2'):
                self.ui.quizze_btn_2.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(quiz_page_index))
                print("Connected quizze_btn_2 to quiz page.")

            # Connect other sidebar buttons to their pages (update indices as per your design)
            if hasattr(self.ui, 'home_btn_1'):
                self.ui.home_btn_1.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(0))
            if hasattr(self.ui, 'home_btn_2'):
                self.ui.home_btn_2.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(0))

            if hasattr(self.ui, 'user_btn'):
                self.ui.user_btn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(1))

            if hasattr(self.ui, 'flash_btn_1'):
                self.ui.flash_btn_1.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(2))
            if hasattr(self.ui, 'flash_btn_2'):
                self.ui.flash_btn_2.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(2))

            if hasattr(self.ui, 'about_btn_1'):
                self.ui.about_btn_1.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(4))
            if hasattr(self.ui, 'about_btn_2'):
                self.ui.about_btn_2.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(4))

            if hasattr(self.ui, 'setting_1'):
                self.ui.setting_1.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(5))
            if hasattr(self.ui, 'setting_2'):
                self.ui.setting_2.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(5))

            if hasattr(self.ui, 'search_btn'):
                self.ui.search_btn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(6))

            # Connect logout buttons to emit signal
            if hasattr(self.ui, 'logout_btn_1'):
                self.ui.logout_btn_1.clicked.connect(lambda: (print("Logout btn 1 clicked."), self.logout_requested.emit()))
            if hasattr(self.ui, 'logout_btn_2'):
                self.ui.logout_btn_2.clicked.connect(lambda: (print("Logout btn 2 clicked."), self.logout_requested.emit()))

            # Connect search functionality
            if hasattr(self.ui, 'search_btn'):
                self.ui.search_btn.clicked.connect(self.perform_google_search)
            if hasattr(self.ui, 'search_input'):
                self.ui.search_input.returnPressed.connect(self.perform_google_search)

        else:
            print("SidebarUiForm: stackedWidget not found in UI!")

        print("SidebarUiForm: Initialization complete.")

    def perform_google_search(self):
        if hasattr(self.ui, 'search_input'):
            search_query = self.ui.search_input.text().strip()
            if search_query:
                url = f"https://www.google.com/search?q={search_query}"
                webbrowser.open(url)
                print(f"Performed Google search for: {search_query}")
            else:
                QtWidgets.QMessageBox.information(self, "Search", "Please enter a search query.")
            self.ui.search_input.clear()
        else:
            print("search_input not found in UI.")

