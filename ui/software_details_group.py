from PySide6.QtWidgets import (QGroupBox, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton)

class SoftwareDetailsGroup(QGroupBox):
    def __init__(self):
        super().__init__("Software Details")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        
        self.create_ui()

    def create_ui(self):
        self.software_name = QLineEdit()
        self.layout.addWidget(QLabel("Software Name:"))
        self.layout.addWidget(self.software_name)
        
        config_layout = QHBoxLayout()
        self.config_path = QLineEdit()
        config_layout.addWidget(QLabel("Ini files Path:"))
        config_layout.addWidget(self.config_path)
        self.config_browse_btn = QPushButton("Browse")
        self.config_browse_btn.setObjectName("config_browse_btn")
        config_layout.addWidget(self.config_browse_btn)
        self.layout.addLayout(config_layout)
        
        log_layout = QHBoxLayout()
        self.log_path = QLineEdit()
        log_layout.addWidget(QLabel("Log Path:"))
        log_layout.addWidget(self.log_path)
        self.log_browse_btn = QPushButton("Browse")
        self.log_browse_btn.setObjectName("log_browse_btn")
        log_layout.addWidget(self.log_browse_btn)
        self.layout.addLayout(log_layout)