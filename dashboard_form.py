from PyQt5 import QtWidgets, QtCore, QtGui
import webbrowser # NEW: Import the webbrowser module

# IMPORTANT: The class name below now correctly matches the main UI class
# generated in your sidebar_ui.py file, which is Ui_MainWindow.
from sidebar_ui import Ui_MainWindow # Correctly importing Ui_MainWindow

class SidebarUiForm(QtWidgets.QWidget):
    """
    Wrapper class for your sidebar_ui.py (the dashboard UI).
    This class correctly embeds the content of a QMainWindow-designed UI.
    """
    # Define signals to communicate with MainWindow for logout
    logout_requested = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()
        print("SidebarUiForm: Initializing...") # Debug print

        # Create an instance of the auto-generated UI class
        self.ui = Ui_MainWindow()

        # Create a temporary QMainWindow instance to set up the UI on.
        temp_main_window = QtWidgets.QMainWindow()
        try:
            self.ui.setupUi(temp_main_window)
            print("SidebarUiForm: setupUi successful on temporary QMainWindow.") # Debug print
        except Exception as e:
            print(f"SidebarUiForm: Error during setupUi on temporary QMainWindow: {e}") # Debug print for errors
            layout = QtWidgets.QVBoxLayout(self)
            layout.addWidget(QtWidgets.QLabel("Error loading sidebar UI. Check console."))
            self.setLayout(layout)
            return

        # Extract the central widget from the temporary QMainWindow.
        dashboard_content_widget = temp_main_window.centralWidget()

        if dashboard_content_widget:
            # Reparent the central widget to this SidebarUiForm.
            dashboard_content_widget.setParent(self)

            # Set the layout of this SidebarUiForm (which is a QWidget)
            # to contain the extracted dashboard content.
            layout = QtWidgets.QVBoxLayout(self)
            layout.addWidget(dashboard_content_widget)
            layout.setContentsMargins(0, 0, 0, 0) # Remove extra margins if desired
            self.setLayout(layout) # Set the layout for SidebarUiForm
            print("SidebarUiForm: Layout set with dashboard content.") # Debug print
        else:
            print("SidebarUiForm: No central widget found in Ui_MainWindow setup.") # Debug print
            layout = QtWidgets.QVBoxLayout(self)
            layout.addWidget(QtWidgets.QLabel("Dashboard content not found. Check sidebar_ui.py."))
            self.setLayout(layout)


        # Ensure the temporary QMainWindow is deleted to free up resources.
        temp_main_window.deleteLater()
        print("SidebarUiForm: Temporary QMainWindow deleted.") # Debug print

        # Apply a stylesheet to ensure text visibility AND adjust header position
        self.setStyleSheet("""
            QLabel {
                color: #333333; /* Dark gray for labels */
            }
            QPushButton {
                color: #333333; /* Dark gray for button text */
            }
            QLineEdit {
                color: #333333; /* Dark gray for line edit text */
            }

            /* --- Header Positioning Adjustments --- */
            /* Target the main widget holding the header content (widget_3) */
            #widget_3 {
                padding-top: 0px;
                margin-top: 0px;
            }
            /* Target the horizontal widget inside widget_3 that contains header elements */
            #widget { /* This is the widget with horizontalLayout_4 in your sidebar_ui.py */
                padding-top: 0px;
                margin-top: 0px;
                min-height: 40px; /* Ensure it has a minimum height to display content */
                max-height: 50px; /* Optional: cap maximum height */
            }
            /* Adjust spacing of the horizontal layout itself if needed */
            #widget > QHBoxLayout { /* This targets the layout directly */
                spacing: 0px;
                margin: 0px;
                padding: 0px;
            }
        """)
        print("SidebarUiForm: Applied stylesheet for text visibility and header positioning.") # Debug print

        # Connect sidebar buttons to internal stackedWidget pages
        self.ui.home_btn_1.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(0)) # Home Page (page)
        self.ui.home_btn_2.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(0))

        # Connect Profile button (user_btn) to Profile Page (page_7) at index 1
        self.ui.user_btn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(1))

        self.ui.flash_btn_1.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(2)) # Flashcard Page (page_2)
        self.ui.flash_btn_2.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(2))

        self.ui.quizze_btn_1.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(3)) # Quizze Page (page_3)
        self.ui.quizze_btn_2.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(3))

        self.ui.about_btn_1.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(4)) # About us Page (page_4)
        self.ui.about_btn_2.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(4))

        self.ui.setting_1.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(5)) # Settings Page (page_5)
        self.ui.setting_2.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(5))

        # Connect Search button (search_btn) to Search Page (page_6) at index 6
        self.ui.search_btn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(6))

        # --- NEW: Connect search button to open Google search ---
        self.ui.search_btn.clicked.connect(self.perform_google_search)
        self.ui.search_input.returnPressed.connect(self.perform_google_search) # Also search on Enter key press

        # Connect logout buttons to emit logout_requested signal with debug print
        self.ui.logout_btn_1.clicked.connect(lambda: (print("Logout btn 1 clicked. Emitting logout_requested."), self.logout_requested.emit()))
        self.ui.logout_btn_2.clicked.connect(lambda: (print("Logout btn 2 clicked. Emitting logout_requested."), self.logout_requested.emit()))

        print("SidebarUiForm: Button signals connected.") # Debug print

    # --- NEW: Method to perform Google search ---
    def perform_google_search(self):
        search_query = self.ui.search_input.text().strip()
        if search_query:
            google_url = f"https://www.google.com/search?q={search_query}"
            webbrowser.open(google_url)
            print(f"Opened Google search for: {search_query}")
        else:
            print("Search input is empty.")
            QtWidgets.QMessageBox.information(self, "Search", "Please enter a search query.")
        self.ui.search_input.clear() # Clear the search input after searching
