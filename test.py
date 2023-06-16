import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
import json
import os

class WidgetOne(QtWidgets.QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.size = 2
        self.state = 1 #1 - старт программы, 2 - новое вычисление c пустым значением, 3 - новое вычисление
        self.color = Qt.red
        self.line_style = Qt.DashLine
        self.setStyleSheet('background-color: grey;')
        self.rect_coords = [[10, 10, 400, 400], [55, 55, 310, 310]]
        self.vertical_line_coords = []
        self.horizontal_line_coords = []
        self.pen = QtGui.QPen(self.color, self.size, self.line_style)
       
    def paintEvent(self, event):
        #self.painter.setPen(QtCore.Qt.red)
        #self.painter.setBrush(QtCore.Qt.green)
        self.pen = QtGui.QPen(self.color, self.size, self.line_style)
        painter = QtGui.QPainter(self)
        painter.setPen(self.pen)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        if self.state == 1:
            painter.drawText(10,10, 'Для старта программы введите ширину и высоту знака')
        elif self.state == 2:
            painter.drawRect(* self.rect_coords[0])
            painter.drawRect(* self.rect_coords[1])
            painter.drawText(self.rect_coords[0][2]+10,self.rect_coords[0][3]//2, ' У:45')

    def minimumSizeHint(self):
        return QtCore.QSize(30000, 30000)

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        widget = QtWidgets.QWidget()
        #layout = QtWidgets.QGridLayout(widget)
        layout = QtWidgets.QVBoxLayout(widget)
        self.widget_one = WidgetOne(self)
        # or
        # widget_one.setFixedSize(1000, 1000)
        # or
        # widget_one.setMinimumSize(1000, 1000)
        scroll = QtWidgets.QScrollArea(widgetResizable=True)
        scroll.setWidget(self.widget_one)
        layout.addWidget(scroll, 50)
        # layout.addWidget(WidgetTwo(), 1, 1)
        self.setCentralWidget(widget)
        self.resize(500, 500)
        self.button_1 = QtWidgets.QPushButton('Рассчитать', self)
        self.button_2 = QtWidgets.QPushButton('Сохранить параметры', self)
        self.button_1.clicked.connect(self.draw)
        self.widthInput = QtWidgets.QLineEdit()
        self.heightInput = QtWidgets.QLineEdit()
        self.widthInput.setPlaceholderText(
            'Введите ширину (мм):')
        self.heightInput.setPlaceholderText(
            'Введите высоту (мм):')
        self.widthInput.setValidator(QtGui.QIntValidator(0, 99999))
        self.heightInput.setValidator(QtGui.QIntValidator(0, 99999))
        layout2 = QtWidgets.QHBoxLayout()
        
        layout3 = QtWidgets.QVBoxLayout()
        layout4 = QtWidgets.QVBoxLayout()
        layout5 = QtWidgets.QHBoxLayout()
        layout6 = QtWidgets.QHBoxLayout()
        self.combobox2 = QtWidgets.QComboBox()
        self.combobox3 = QtWidgets.QComboBox()
        self.combobox2.addItems(['Красный', 'Синий', 'Зелёный', 'Чёрный'])
        self.combobox3.addItems(['Прерывистая','Сплошная', 'Точками'])

        self.mySlider = QtWidgets.QSlider(Qt.Horizontal)
        self.sizeSlider = QtWidgets.QSlider(Qt.Horizontal)
        self.sizeSlider.setValue(40)
        self.mySlider.setValue(10)
        self.LabelK = QtWidgets.QLabel('Коэффициент:')
        self.LabelSize = QtWidgets.QLabel('Толщина линии:')

        layout3.addWidget(QtWidgets.QLabel('Ширина (мм)'), 50)
        layout3.addWidget(self.widthInput, 50)
        layout3.addWidget(QtWidgets.QLabel('Высота (мм)'), 50)
        layout3.addWidget(self.heightInput, 50)
        layout4.addWidget(self.combobox2, 50)
        layout4.addWidget(self.combobox3, 50)
        layout5.addWidget(self.LabelK, 50)
        layout5.addWidget(self.mySlider, 50)
        layout6.addWidget(self.LabelSize, 50)
        layout6.addWidget(self.sizeSlider, 50)
        layout4.addLayout(layout5)
        layout4.addLayout(layout6)
        
        layout2.addLayout(layout3)
        layout2.addLayout(layout4)
        layout.addLayout(layout2)
        layout4.addWidget(self.button_2)
        layout.addWidget(self.button_1)

        #подписка на слайдер
        self.mySlider.valueChanged[int].connect(self.changeValue)
        self.sizeSlider.valueChanged[int].connect(self.changeSize)
        #подписка на комбобоксы
        self.combobox2.currentTextChanged.connect(self.changecolor)
        self.combobox3.currentTextChanged.connect(self.changestyle)

        #кнопка сохранения параметров
        self.button_2.clicked.connect(self.save_data_to_file)

        self.k = 0.1 #коэффициент вычисления

    def save_data_to_file(self):
        save_data()

    def changecolor(self, value):
        if value.lower() == 'красный':
            self.widget_one.color = Qt.red
            dict_settings['color'] = 'red'
        if value.lower() == 'синий':
            self.widget_one.color = Qt.blue
            dict_settings['color'] = 'blue'
        if value.lower() == 'зелёный':
            self.widget_one.color = Qt.green
            dict_settings['color'] = 'green'
        if value.lower() == 'чёрный':
            self.widget_one.color = Qt.black
            dict_settings['color'] = 'black'
        self.draw()
    
    def changestyle(self, value):
        if value.lower() == 'прерывистая':
            self.widget_one.line_style = Qt.DashLine
            dict_settings['style'] = 'dash'
        if value.lower() == 'сплошная':
            self.widget_one.line_style = Qt.SolidLine
            dict_settings['style'] = 'solid'
        if value.lower() == 'точками':
            self.widget_one.line_style = Qt.DotLine
            dict_settings['style'] = 'dot'
        self.draw()

    def changeSize(self, value):
        self.widget_one.size = int(value/20)
        dict_settings['size'] = int(value/20)
        self.widget_one.pen = QtGui.QPen(self.widget_one.color, self.widget_one.size, self.widget_one.line_style)
        print(self.widget_one.size)
        self.draw()
        self.LabelSize.setText("Толщина линии:" + str(int(value/20)))

    def changeValue(self, value):
        self.k = value/100
        dict_settings['k'] = value/100
        self.draw()
        self.LabelK.setText("Коэффициент:" + str(self.k))

    def draw(self):
        self.calculate()
        self.widget_one.repaint()

    def read_data_from_file(self):
        self.k = dict_settings['k']
        self.widget_one.size = dict_settings['size']
        #загружаем color
        if dict_settings['color'] == 'red':
            self.widget_one.color = Qt.red
        if dict_settings['color'] == 'blue':
            self.widget_one.color = Qt.blue
        if dict_settings['color'] == 'green':
            self.widget_one.color = Qt.green
        if dict_settings['color'] == 'black':
            self.widget_one.color = Qt.black
        #загружаем стили
        if dict_settings['style'] == 'dot':
            self.widget_one.line_style = Qt.DotLine
        if dict_settings['style'] == 'dash':
            self.widget_one.line_style = Qt.DashLine
        if dict_settings['style'] == 'solid':
            self.widget_one.line_style = Qt.SolidLine

        self.sizeSlider.setValue(int(self.widget_one.size * 20))
        self.mySlider.setValue(int(self.k * 100))
        self.LabelSize.setText("Толщина линии:" + str(int(int(self.sizeSlider.value())/20)))



    def calculate(self):
        try:
            # if len(self.widthInput.text()) == 0 or len(self.heightInput.text()) == 0:
            #     self.widget_one.state = 2 
            width = int(int(self.widthInput.text()) * self.k)
            height = int(int(self.heightInput.text()) * self.k)
            data.calculate_rect(width, height, int(45 * self.k))
            self.widget_one.rect_coords = data.rect
            self.widget_one.state = 2
        except:
            dlg = QtWidgets.QMessageBox(self)
            dlg.setWindowTitle("Ошибка!")
            dlg.setText('Введите корректные данные ширины и высоты')
            dlg.exec()

class Line:
    def init(self, x1, y1, x2, y2, w=0, h=0, corner_type=35):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.corner_type = corner_type
        self.w = w
        self.h = h
class Data():
    def __init__(self):
        self.rect = []
        self.vlines = []
        self.hlines = []

    def calculate_rect(self, x2:str, y2:str, corner_type:int):
        x1 = 10
        y1 = 10
        x2 = int(x2)
        y2 = int(y2)
        self.rect.clear()
        self.rect.append([x1,y1,x2,y2])
        self.rect.append([x1 + corner_type, y1+corner_type, x2-corner_type*2, y2 - corner_type*2])

    def calculate(self, w, h):
        if h < 2300: #состоит из двух частей
            pass        
data = Data()

dict_settings = {}
default_dict_settings = {
    "color":"red",
    "style":"dot",
    "size":2,
    "k":0.1
}

def create_default():
    #пересоздаем файл с дефолтными настройками
    with open("settings.json", "w", encoding="utf-8") as file:
        json.dump(default_dict_settings, file)

def read_file():
    global dict_settings
    #считываем данные
    with open("settings.json", "r", encoding="utf-8") as file:
        dict_settings = json.load(file)

def save_data():
    with open("settings.json", "w", encoding="utf-8") as file:
        json.dump(dict_settings, file)


try:
    #есть ли файл
    if os.path.exists(os.getcwd() + '\\' + 'settings.json'):
        try:
            read_file()
            #проверяем на корректность (чтобы файл никто не менял, если менял)
            if not("color" in dict_settings and "style" in dict_settings and "size" in dict_settings and "k" in dict_settings):
                create_default()
                read_file()
        except:
            create_default()
            read_file()
    else:
        create_default()
        read_file()
except:
    create_default()
    read_file()


def main():
    app = QtWidgets.QApplication.instance()
    if app is None:
        app = QtWidgets.QApplication([])

    w = MainWindow()
    w.read_data_from_file()
    w.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()