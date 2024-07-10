from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout)
from ui.time_range_group import TimeRangeGroup
from ui.software_details_group import SoftwareDetailsGroup
from ui.file_preview_group import FilePreviewGroup
from ui.store_button import StoreButton
from utils.file_operations import FileOperations

class LogCaptureApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Advanced Log File Capture")
        self.setGeometry(100, 100, 800, 600)
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        
        self.file_ops = FileOperations()
        self.create_ui()
        self.setup_connections()
        self.setup_styling()

    def create_ui(self):
        self.time_range_group = TimeRangeGroup()
        self.layout.addWidget(self.time_range_group)
        
        self.software_details_group = SoftwareDetailsGroup()
        self.layout.addWidget(self.software_details_group)
        
        self.file_preview_group = FilePreviewGroup()
        self.layout.addWidget(self.file_preview_group)
        
        self.store_button = StoreButton()
        self.layout.addWidget(self.store_button)

    def setup_connections(self):
        self.software_details_group.config_browse_btn.clicked.connect(
            lambda: self.file_ops.browse_directory(self.software_details_group.config_path))
        self.software_details_group.log_browse_btn.clicked.connect(
            lambda: self.file_ops.browse_directory(self.software_details_group.log_path))
        self.file_preview_group.refresh_preview_btn.clicked.connect(self.refresh_preview)
        self.store_button.clicked.connect(self.store_files)

    def setup_styling(self):
        # Add styling code here (CSS file if preferred)
        pass

    def refresh_preview(self):
        self.file_ops.refresh_preview(self.file_preview_group.file_list, 
                                      self.software_details_group.log_path.text(),
                                      self.software_details_group.config_path.text())

    def store_files(self):
        self.file_ops.store_files(self.time_range_group.start_time,
                                  self.time_range_group.end_time,
                                  self.software_details_group.software_name.text(),
                                  self.software_details_group.config_path.text(),
                                  self.software_details_group.log_path.text())