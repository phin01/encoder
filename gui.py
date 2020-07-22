from PyQt5 import QtCore, QtWidgets, QtGui, uic
from PyQt5.QtWidgets import QFileDialog, QMessageBox
import os
import sys
import pandas as pd
from encodecode import EncoDeco



class EncoderGUI(QtWidgets.QWidget):

    def __init__(self):
        """ 

        """
        QtWidgets.QWidget.__init__(self)
        ui_path = os.path.join(os.path.dirname(__file__), "form.ui")
        self.ui = uic.loadUi(ui_path, self)

        # set button functions to encode, decode and get source file
        self.btnCode.clicked.connect(self.start_enconding)
        self.btnDecode.clicked.connect(self.start_decoding)
        self.btnGetSourceFile.clicked.connect(self.get_csv_filename)

        self.encodecode = EncoDeco()

        # self.spinBoxInterval.setValue(default_interval) # set spinbox value as default interval from config.json file
        # self.sysTray = parent # systray parent object that will run start/stop functions

        self.show()


    def get_csv_filename(self):
        """
            Opens File Dialog to select .csv file that will be encoded or decoded
            If file is .csv, sets UI textbox to filename
            Displays error message box in case selected file is not .csv
        """
        self.lblResult.setText('')
        options = QFileDialog.Options()
        # options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"Buscar CSV", "","CSV Files (*.csv)", options=options)
        if fileName:
            self.set_csv_path(fileName) if self.check_csv_extension(fileName) else self.show_msgbox('Erro', 'Favor selecionar um arquivo .csv')


    def encode_decode(self, encode: bool):
        self.lblResult.setText('Processando...')
        fileName = self.txtPath.toPlainText()
        separator = self.txtSeparator.toPlainText()

        if self.check_csv_extension(fileName) and separator:
            data = self.encodecode.load_csv(fileName, separator)

            if not data.empty:
                if encode:
                    encoded_df = self.encodecode.encode(data, p64=True)
                    output_csv = fileName.replace('.csv', '_convertido.csv')
                    output_result = self.encodecode.store_csv(encoded_df, output_csv, ';')
                else:
                    decoded_df = self.encodecode.decode(data, separator, p64=True)
                    output_csv = fileName.replace('.csv', '_original.csv')
                    output_result = self.encodecode.store_csv(decoded_df, output_csv, ';')
        
        if output_result:
            self.lblResult.setText('Arquivo salvo com sucesso em {0}'.format(output_csv))
            self.set_csv_path('')
        else:
            self.lblResult.setText('Erro na operação')
            self.show_msgbox('Erro', 'Não foi possível abrir arquivo .csv')



    """
    def load_csv(self, filename: str, separator: str):
        try:
            data = pd.read_csv(filename, sep=separator)
        except:
            data = None
        return data
    """

    def start_enconding(self):
        """ Calls encode_decode function with Encode flag """
        self.encode_decode(encode=True)
    
    
    def start_decoding(self):
        """ Calls encode_decode function with Decode flag """
        self.encode_decode(encode=False)


    def set_csv_path(self, fileName: str):
        """ Sets Text Box in UI to filename string received as parameter """
        try:
            self.txtPath.setPlainText(fileName)
        except:
            self.show_msgbox('Erro', 'Não foi possível selecionar o arquivo!')


    def check_csv_extension(self, fileName: str) -> bool:
        """ 
            Checks if the supplied filename has .csv extension 
            Args:
                filename (str): Name of file to be converted
            Returns:
                bool: True if file has .csv extentsion
        """
        return True if fileName[-4:] == ".csv" else False


    def show_msgbox(self, msgbox_title:str, msgbox_message: str):
        """ 
            Shows simple Message Box with supplied parameters. 
            Message box is displayed with Information icon and single OK button to close it

            Args:
                msgbox_title (str): Title of message box
                msgbox_message (str): Message displayed in message box
        """
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(msgbox_message)
        msg.setWindowTitle(msgbox_title)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    encodergui = EncoderGUI()
    sys.exit(app.exec_())        

    