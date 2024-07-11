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
        print(f"Debug: start_time={start_time.text()}, end_time={end_time.text()}")
        print(f"Debug: software_name={software_name}")
        print(f"Debug: config_path={config_path}")
        print(f"Debug: log_path={log_path}")

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

        print("Copying log files...")
        FileOperations.copy_log_files(logs_dir, log_path, start_time, end_time)
        print("Log files copied to", logs_dir)

        print("Copying ini files...")
        FileOperations.copy_ini_files(ini_dir, config_path)
        print("INI files copied to", ini_dir)

        print("Temporary directory contents:")
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                print(os.path.join(root, file))

        with open(os.path.join(temp_dir, "description.txt"), "w") as f:
            f.write(description)

        save_dir = QFileDialog.getExistingDirectory(None, "Select folder to save the zip file")
        if not save_dir:
            shutil.rmtree(temp_dir)
            QMessageBox.information(None, "Cancelled", "File storage cancelled")
            return

        zip_filename = os.path.join(save_dir, f"{start_time.text().replace('/', '')}_{software_name}.zip")
        print("Creating zip file at", zip_filename)

        try:
            with zipfile.ZipFile(zip_filename, 'w') as zipf:
                for root, dirs, files in os.walk(temp_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, temp_dir)
                        zipf.write(file_path, arcname)
                        print(f"Added {file_path} as {arcname}")
            print("Zip file created successfully")
            
            # Verify zip file contents
            with zipfile.ZipFile(zip_filename, 'r') as zipf:
                print("Zip file contents:")
                zipf.printdir()
            
            QMessageBox.information(None, "Success", f"Files stored in {zip_filename}")
        except Exception as e:
            print(f"Failed to create zip file: {e}")
            QMessageBox.critical(None, "Error", f"Failed to create zip file: {e}")

        # Check if the zip file was created successfully
        if os.path.exists(zip_filename):
            print(f"Zip file {zip_filename} created successfully")
        else:
            print(f"Failed to create zip file: {zip_filename}")

        shutil.rmtree(temp_dir)

    @staticmethod
    def copy_log_files(logs_dir, log_path, start_time, end_time):
        start_datetime = start_time.dateTime()
        end_datetime = end_time.dateTime()
        print(f"Debug: Searching for log files between {start_datetime} and {end_datetime}")
        for file in glob.glob(os.path.join(log_path, "Data_*.CSV")):
            file_time = QDateTime.fromString(os.path.basename(file)[5:18], "yyMMdd_hhmmss")
            print(f"Debug: Found file {file} with time {file_time}")
            if start_datetime <= file_time <= end_datetime:
                shutil.copy(file, logs_dir)
                print(f"Copied log file: {file}")
            else:
                print(f"Debug: File {file} outside date range")

    @staticmethod
    def copy_ini_files(ini_dir, config_path):
        print(f"Debug: Searching for INI files in {config_path}")
        for file in glob.glob(os.path.join(config_path, "*.ini")):
            shutil.copy(file, ini_dir)
            print(f"Copied INI file: {file}")