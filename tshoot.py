from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.uic import loadUiType
import sys

# backend class
from tshoot_backend import TshootBackend



ui, _ = loadUiType("tshoot_main.ui")

class Tshoot(QMainWindow, ui):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.button_handler()
        self.btn_exit.clicked.connect(self.on_exit)
        self.export_data = []
    
    def button_handler(self):
        self.btn_login_execute.clicked.connect(self.login_execute)
        self.btn_export.clicked.connect(self.export_to_file)
    
    def login_execute(self):
        username = self.edit_username.text()
        password = self.edit_password.text()
        devices = []
        self.export_data = []
        
        for device in self.edit_list_of_devices.text().split(','):
            devices.append(device.strip(' '))
        commands = self.edit_commands.text().split(',')
        
        tshoot = TshootBackend(username, password)      
        result = tshoot.get_config(commands, devices)
        if not result:
            error_msg = QMessageBox()
            error_msg.Icon(QMessageBox.Critical)
            error_msg.setWindowTitle("Error")
            error_msg.setText("""Connection could not be made to one of the devices, 
            check username/password and connectivity to devices""")
            error_msg.show()
            return
        
        # clear the output plain textedit box        
        self.ptedit_output.clear()
        for key,value in result.items():
            self.ptedit_output.appendPlainText("\n*********************")
            self.ptedit_output.appendPlainText(f"Device Name(ip): {key}")
            self.ptedit_output.appendPlainText("**********************\n")
            self.export_data.append("\n"+key)            
            # populate with new outputs
            for data in value:
                self.ptedit_output.appendPlainText(data.replace("\r","").strip("\n"))
                self.export_data.append(data.replace("\r","").strip("\n"))
    
    def export_to_file(self):
        with open("commands_output.txt", "w") as file:
            for data in self.export_data:
                file.write(data+"\n")
    
    def on_exit(self):
        sys.exit()

def main():
    app = QApplication(sys.argv)
    
    myclass = Tshoot()
    myclass.show()
    
    app.exec_()

if __name__ == "__main__":
    main()