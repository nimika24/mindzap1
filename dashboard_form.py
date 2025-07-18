from PyQt5 import QtWidgets, QtCore, QtGui # Added QtGui for QFont

# IMPORTANT: The class name below now correctly matches the main UI class
# generated in your sidebar_ui.py file, which is Ui_MainWindow.
from sidebar_ui import Ui_MainWindow # Correctly importing Ui_MainWindow

class SidebarUiForm(QtWidgets.QWidget):
    """
    Wrapper class for your sidebar_ui.py (the dashboard UI).
    This class correctly embeds the content of a QMainWindow-designed UI.
    """
    def __init__(self):
        super().__init__()
        print("SidebarUiForm: Initializing...") # Debug print

        # Create an instance of the auto-generated UI class
        self.ui = Ui_MainWindow()

        # Create a temporary QMainWindow instance to set up the UI on.
        # This allows Ui_MainWindow.setupUi to correctly build its internal structure,
        # including its central widget, as it was designed for a QMainWindow.
        temp_main_window = QtWidgets.QMainWindow()
        try:
            self.ui.setupUi(temp_main_window)
            print("SidebarUiForm: setupUi successful on temporary QMainWindow.") # Debug print
        except Exception as e:
            print(f"SidebarUiForm: Error during setupUi on temporary QMainWindow: {e}") # Debug print for errors
            # Fallback in case of setupUi failure, though this shouldn't happen with correct Ui_MainWindow
            layout = QtWidgets.QVBoxLayout(self)
            layout.addWidget(QtWidgets.QLabel("Error loading sidebar UI. Check console."))
            self.setLayout(layout)
            return

        # Extract the central widget from the temporary QMainWindow.
        # This central widget contains all the actual visual elements of your dashboard.
        dashboard_content_widget = temp_main_window.centralWidget()

        if dashboard_content_widget:
            # Reparent the central widget to this SidebarUiForm.
            # This is important to ensure it's part of the correct widget hierarchy
            # and will be displayed when SidebarUiForm is shown.
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
        # This is safe to do after its central widget has been reparented.
        temp_main_window.deleteLater()
        print("SidebarUiForm: Temporary QMainWindow deleted.") # Debug print

        # --- NEW: Apply a stylesheet to ensure text visibility ---
        # This sets a default dark text color for all QLabels and QPushButtons
        # within this SidebarUiForm, overriding any default light colors.
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
            /* You can add more specific styling here if needed */
        """)
        print("SidebarUiForm: Applied stylesheet for text visibility.") # Debug print


        # You can add any specific logic, signal connections, or initializations
        # for your dashboard/sidebar here, referencing self.ui.
        # For example, if you have a button named 'home_btn_1' in your sidebar_ui.py:
        # self.ui.home_btn_1.clicked.connect(self.handle_home_button_click)

    # Example method for a button click (uncomment and adapt if needed)
    # def handle_home_button_click(self):
    #     print("Home button on sidebar clicked!")
    #     # You might emit a signal here to tell MainWindow to change page, etc.
