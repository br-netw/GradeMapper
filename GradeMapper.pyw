import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import json

class MainMenu():

    def __init__(self):

        fileVals = open("gradeTypes.json", "r", encoding="utf8")
        self.subjects = list(json.load(fileVals).keys())
        fileVals.close()

        self.app = QApplication(sys.argv)

        self.grid = QGridLayout()
        self.window = QDialog()
        self.window.setLayout(self.grid)

        ## Кнопка старта

        self.startButton = QPushButton(self.window)
        self.startButton.setText("Начать")
        #self.startButton.move(25, 25)
        self.startButton.clicked.connect(self.bootstrap)

        ## Меню

        self.menu = QComboBox()
        for i in self.subjects:
            self.menu.addItem(i)
            
        ## Название

        self.nameLabel = QLabel()
        self.nameLabel.setAlignment(Qt.AlignCenter)
        self.nameLabel.setText("GradeMapper")

        self.grid.addWidget(self.startButton, 1, 0, 1, 2)
        self.grid.addWidget(self.menu, 2, 0, 1, 2)
        self.grid.addWidget(self.nameLabel, 0, 0, 1, 2)
        #self.grid.addWidget(self.out, 2, 0, 1, 2)
        
        self.window.setWindowTitle("GradeMapper PyQt")
        self.window.setGeometry(100, 100, 0, 0)
        self.window.show()

    def bootstrap(self):

        self.calc = GradeCalculator(self.menu.currentText())
        self.calc.window.show()
        
class GradeCalculator():

    def __init__(self, subject):

        #self.app = QApplication(sys.argv)

        self.grid = QGridLayout()
        self.window = QDialog()
        self.window.setLayout(self.grid)
        
        fileVals = open("gradeTypes.json", "r", encoding="utf8")
        self.types = json.load(fileVals)[subject]
        fileVals.close()

        keys = list(self.types.keys())
        
        ## Данные об оценках
        
        self.weightedGrades = []
        self.weights = []

        ## Текст ввода-вывода и прогнозов

        self.gradeIn = QLineEdit(self.window)
        self.gradeOut = QLabel(self.window)
        self.gradeOut.setAlignment(Qt.AlignCenter)
        self.gradeOut.setText("Оценка: -")
        
        self.barrier = QLabel(self.window)
        self.barrier.setAlignment(Qt.AlignCenter)
        self.barrier.setText("--------------------")
        
        self.forecastGrade = QLineEdit(self.window)
        self.forecast = QLabel(self.window)
        self.forecast.setAlignment(Qt.AlignCenter)
        self.forecast.setText("Прогноз: -")

        ## Кнопки

        self.loadGradeButton = QPushButton(self.window)
        self.clearButton = QPushButton(self.window)
        self.removeLastButton = QPushButton(self.window)
        self.makeForecastButton = QPushButton(self.window)

        self.loadGradeButton.clicked.connect(self.loadGrade)
        self.clearButton.clicked.connect(self.clearGrade)
        self.removeLastButton.clicked.connect(self.removeLastGrade)
        self.makeForecastButton.clicked.connect(self.makeForecast)

        self.loadGradeButton.setText("Загрузить и вычислить")
        self.clearButton.setText("Очистить")
        self.removeLastButton.setText("Удалить последнюю оценку")
        self.makeForecastButton.setText("Сделать прогноз")

        ## Меню
        
        self.workMenu = QComboBox()
        for i in self.types.keys():
            self.workMenu.addItem(i)

        ## Сетка

        self.grid.addWidget(self.workMenu, 0, 0, 1, 1)
        self.grid.addWidget(self.gradeIn, 1, 0, 1, 1)
        self.grid.addWidget(self.gradeOut, 2, 0, 1, 1)
        
        self.grid.addWidget(self.loadGradeButton, 0, 1, 1, 1)
        self.grid.addWidget(self.clearButton, 1, 1, 1, 1)
        self.grid.addWidget(self.removeLastButton, 2, 1, 1, 1)
        
        self.grid.addWidget(self.barrier, 3, 0, 1, 2)
        
        self.grid.addWidget(self.forecastGrade, 4, 0, 1, 1)
        self.grid.addWidget(self.makeForecastButton, 4, 1, 1, 1)
        self.grid.addWidget(self.forecast, 5, 0, 1, 1)

        self.window.setWindowTitle("GradeMapper " + subject)
        self.window.setGeometry(100, 100, 0, 0)
        #self.window.show()
        
    def removeLastGrade(self):
        
        self.weightedGrades.pop(-1)
        self.weights.pop(-1)
        self.outputAverage()

    def outputAverage(self):

        self.gradeOut.setText("Оценка: " + str(round(sum(self.weightedGrades) / sum(self.weights), 2)))
        self.gradeIn.clear()
		
    def loadGrade(self):
        
        try:
            gr = int(self.gradeIn.text())
        except Exception:
            return -1

        if gr < 1 or gr > 5:
            return -1

        currentWorkWeight = self.types[self.workMenu.currentText()]
                    
        self.weightedGrades.append(gr * currentWorkWeight)
        self.weights.append(currentWorkWeight)

        self.outputAverage()
		
    def clearGrade(self):
        
        self.gradeIn.clear()
        self.gradeOut.clear()
        
        self.weights = []
        self.weightedGrades = []
        
        self.gradeOut.setText("Оценка: -")

        self.forecast.setText("Оценка: -")
        self.forecastGrade.clear()

    def makeForecast(self):
            
        try:
            desiredGrade = int(self.forecastGrade.text())
        except Exception:
            return -1
                
        if desiredGrade > 5 or desiredGrade < 1:
            return -1
            
        workTypes = {1.0:"Д/З", 1.2:"С/Р", 1.3:"Пр/Р", 1.5:"К/Р"}

        #results = []
        resultsText = ""
            
        for i in workTypes.keys():
            forecastGrades = {5:0, 4:0, 3:0, 2:0, 1:0}
            weightedGradesCopy = sum(self.weightedGrades)
            weightsCopy = sum(self.weights)
            currentTargetGrade = 5

            while weightedGradesCopy / weightsCopy < desiredGrade - 0.4:
                weightedGradesCopy += i * currentTargetGrade
                weightsCopy += i
                forecastGrades[currentTargetGrade] += 1

                if (weightedGradesCopy / weightsCopy > desiredGrade - 0.8) and (currentTargetGrade - 1 >= desiredGrade):
                    currentTargetGrade -= 1
                    continue

            resultsText += "{}: ".format(workTypes[i])

            for j in forecastGrades.keys():
                if j < desiredGrade:
                    break
                resultsText += "{} {}; ".format(forecastGrades[j], j)

            resultsText += "\n"

            

        #for i in workTypes.keys():
        
                
        self.forecast.setText(resultsText)

if __name__ == "__main__":
    menu = MainMenu()
    sys.exit(menu.app.exec_())
