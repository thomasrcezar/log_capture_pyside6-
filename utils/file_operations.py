import os
import glob
import shutil
import zipfile
from PySide6.QtWidgets import QFileDialog, QMessageBox, QInputDialog
from PySide6.QtCore import QDateTime

class FileOperations:
    @staticmethod
    def browse_directory(line_edit):
        directory = QFileDialog.getExistingDirectory(None, "Select Directory")
        if directory:
            line_edit.setText(directory)

    @staticmethod
    def refresh_preview(file_list, log_path, config_path):
        file_list.clear()
        if log_path:
            log_files = glob.glob(os.path.join(log_path, "Data_*.CSV"))
            file_list.addItems([os.path.basename(f) for f in log_files[:10]])
            if len(log_files) > 10:
                file_list.addItem("...")
        if config_path:
            config_files = glob.glob(os.path.join(config_path, "*.ini"))
            file_list.addItems([os.path.basename(f) for f in config_files])

    @staticmethod
    def store_files(start_time, end_time, software_name, config_path, log_path):
        if not all([start_time.text(), end_time.text(), software_name, config_path, log_path]):
            QMessageBox.critical(None, "Error", "All fields must be filled")
            return

        description, ok = QInputDialog.getText(None, "Enter Description", "Description:")
        if not ok:
            return

        temp_dir = "temp_storage"
        logs_dir = os.path.join(temp_dir, "Logs")
        ini_dir = os.path.join(temp_dir, "Ini")
        os.makedirs(logs_dir, exist_ok=True)
        os.makedirs(ini_dir, exist_ok=True)

        FileOperations.copy_log_files(logs_dir, log_path, start_time, end_time)
        FileOperations.copy_ini_files(ini_dir, config_path)

        with open(os.path.join(temp_dir, "description.txt"), "w") as f:
            f.write(description)

        save_dir = QFileDialog.getExistingDirectory(None, "Select folder to save the zip file")
        if not save_dir:
            shutil.rmtree(temp_dir)
            QMessageBox.information(None, "Cancelled", "File storage cancelled")
            return

        zip_filename = os.path.join(save_dir, f"{start_time.text().replace('/', '')}_{software_name}.zip")
        with zipfile.ZipFile(zip_filename, 'w') as zipf:
            for root, dirs, files in os.walk(temp_dir):
                for file in files:
                    zipf.write(os.path.join(root, file), 
                               os.path.relpath(os.path.join(root, file), temp_dir))

        shutil.rmtree(temp_dir)
        QMessageBox.information(None, "Success", f"Files stored in {zip_filename}")

    @staticmethod
    def copy_log_files(logs_dir, log_path, start_time, end_time):
        start_datetime = start_time.dateTime()
        end_datetime = end_time.dateTime()
        for file in glob.glob(os.path.join(log_path, "Data_*.CSV")):
            file_time = QDateTime.fromString(os.path.basename(file)[5:18], "yyMMdd_hhmmss")
            if start_datetime <= file_time <= end_datetime:
                shutil.copy(file, logs_dir)

    @staticmethod
    def copy_ini_files(ini_dir, config_path):
        for file in glob.glob(os.path.join(config_path, "*.ini")):
            shutil.copy(file, ini_dir)