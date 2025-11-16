import sys
import requests
from PyQt5 import QtWidgets
from crud_usuarios_ui import Ui_MainWindow

API_URL = "http://127.0.0.1:8000/api/usuarios/"

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.load_data()

        self.btnAgregar.clicked.connect(self.agregar_usuario)
        self.btnEditar.clicked.connect(self.editar_usuario)
        self.btnEliminar.clicked.connect(self.eliminar_usuario)
        self.btnActualizar.clicked.connect(self.load_data)

    def load_data(self):
        response = requests.get(API_URL)
        if response.status_code == 200:
            usuarios = response.json()
            self.tableWidget.setRowCount(len(usuarios))
            for i, usuario in enumerate(usuarios):
                self.tableWidget.setItem(i, 0, QtWidgets.QTableWidgetItem(str(usuario["codigo"])))
                self.tableWidget.setItem(i, 1, QtWidgets.QTableWidgetItem(usuario["nombre"]))

    def agregar_usuario(self):
        data = {
            "codigo": self.lineCodigo.text(),
            "nombre": self.lineNombre.text()
        }
        requests.post(API_URL, data=data)
        self.load_data()

    def editar_usuario(self):
        codigo = self.lineCodigo.text()
        data = {"nombre": self.lineNombre.text()}
        requests.put(API_URL + f"{codigo}/", data=data)
        self.load_data()

    def eliminar_usuario(self):
        codigo = self.lineCodigo.text()
        requests.delete(API_URL + f"{codigo}/")
        self.load_data()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

