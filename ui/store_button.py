from PySide6.QtWidgets import QPushButton
class StoreButton(QPushButton):
    def __init__(self):
        super().__init__("Store Files")
        self.setObjectName("store_btn")
        self.setStyleSheet("""
            background-color: #008CBA;
            font-size: 16px;
            padding: 10px 20px;
        """)