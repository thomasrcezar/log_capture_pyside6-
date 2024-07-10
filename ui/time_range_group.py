from PySide6.QtWidgets import (QGroupBox, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QDateTimeEdit)
from PySide6.QtCore import QDateTime

class TimeRangeGroup(QGroupBox):
    def __init__(self):
        super().__init__("Time Range")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        
        self.create_ui()
        self.setup_connections()

    def create_ui(self):
        start_layout = QHBoxLayout()
        self.start_time = QDateTimeEdit(QDateTime.currentDateTime())
        start_layout.addWidget(QLabel("Start Time:"))
        start_layout.addWidget(self.start_time)
        self.capture_start_btn = QPushButton("Capture Start")
        self.capture_start_btn.setObjectName("capture_start_btn")
        start_layout.addWidget(self.capture_start_btn)
        self.layout.addLayout(start_layout)
        
        end_layout = QHBoxLayout()
        self.end_time = QDateTimeEdit(QDateTime.currentDateTime())
        end_layout.addWidget(QLabel("End Time:"))
        end_layout.addWidget(self.end_time)
        self.capture_end_btn = QPushButton("Capture End")
        self.capture_end_btn.setObjectName("capture_end_btn")
        end_layout.addWidget(self.capture_end_btn)
        self.layout.addLayout(end_layout)

    def setup_connections(self):
        self.capture_start_btn.clicked.connect(self.capture_start)
        self.capture_end_btn.clicked.connect(self.capture_end)

    def capture_start(self):
        self.start_time.setDateTime(QDateTime.currentDateTime())

    def capture_end(self):
        self.end_time.setDateTime(QDateTime.currentDateTime())