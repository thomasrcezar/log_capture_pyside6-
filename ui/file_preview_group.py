from PySide6.QtWidgets import (QGroupBox, QVBoxLayout, QListWidget, QPushButton)

class FilePreviewGroup(QGroupBox):
    def __init__(self):
        super().__init__("File Preview")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        
        self.create_ui()

    def create_ui(self):
        self.file_list = QListWidget()
        self.layout.addWidget(self.file_list)
        self.refresh_preview_btn = QPushButton("Refresh Preview")
        self.refresh_preview_btn.setObjectName("refresh_preview_btn")
        self.layout.addWidget(self.refresh_preview_btn)