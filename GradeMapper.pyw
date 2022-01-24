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
        
        self.subject = subject
        fileVals = open("gradeTypes.json", "r", encoding="utf8")
        self.types = json.load(fileVals)[self.subject]
        fileVals.close()

        keys = list(self.types.keys())
        
        ## Данные об оценках
        
        self.weightedGrades = []
        self.weights = []

        ## Текст ввода-вывода

        self.gradeIn = QLineEdit(self.window)
        self.gradeOut = QLabel(self.window)
        self.gradeOut.setAlignment(Qt.AlignCenter)
        self.gradeOut.setText("Оценка: -")

        ## Кнопки ввода и очистки

        self.loadGradeButton = QPushButton(self.window)
        self.clearButton = QPushButton(self.window)
        self.removeLastButton = QPushButton(self.window)

        self.loadGradeButton.clicked.connect(self.loadGrade)
        self.clearButton.clicked.connect(self.clearGrade)
        self.removeLastButton.clicked.connect(self.removeLastGrade)

        self.loadGradeButton.setText("Загрузить и вычислить")
        self.clearButton.setText("Очистить")
        self.removeLastButton.setText("Удалить последнюю оценку")

        ## Меню
                
        self.workMenu = QComboBox()
        for i in self.types.keys():
            self.workMenu.addItem(i)

        ## Текст модуля прогнозов

        self.barrier = QLabel(self.window)
        self.barrier.setAlignment(Qt.AlignCenter)
        self.barrier.setText("--------------------")
        
        self.forecastGrade = QLineEdit(self.window)
        self.forecast = QLabel(self.window)
        self.forecast.setAlignment(Qt.AlignCenter)
        self.forecast.setText("Прогноз: -")

        ## Кнопка модуля прогнозов

        self.makeForecastButton = QPushButton(self.window)
        self.makeForecastButton.clicked.connect(self.makeForecast)
        self.makeForecastButton.setText("Сделать прогноз")

        ## Текст модуля сохранения
                
        self.barrier2 = QLabel(self.window)
        self.barrier2.setAlignment(Qt.AlignCenter)
        self.barrier2.setText(self.barrier.text())

        self.gradesFilename = QLineEdit(self.window)

        self.gradeSaveModuleLog = QLabel(self.window)
        self.gradeSaveModuleLog.setAlignment(Qt.AlignCenter)
        self.gradeSaveModuleLog.setText(" ")

        ## Кнопки модуля сохранения

        self.writeToFileButton = QPushButton(self.window)
        self.loadFromFileButton = QPushButton(self.window)

        self.writeToFileButton.clicked.connect(self.writeToFile)
        self.loadFromFileButton.clicked.connect(self.loadFromFile)

        self.writeToFileButton.setText("Сохранить в файл")
        self.loadFromFileButton.setText("Загрузить из файла:")

        ## Сетка

        self.grid.addWidget(self.gradeIn, 1, 0, 1, 1)
        self.grid.addWidget(self.gradeOut, 2, 0, 1, 1)
        self.grid.addWidget(self.workMenu, 0, 0, 1, 1)
        
        self.grid.addWidget(self.loadGradeButton, 0, 1, 1, 1)
        self.grid.addWidget(self.clearButton, 1, 1, 1, 1)
        self.grid.addWidget(self.removeLastButton, 2, 1, 1, 1)
        
        self.grid.addWidget(self.barrier, 3, 0, 1, 2)
        
        self.grid.addWidget(self.forecastGrade, 4, 0, 1, 1)
        self.grid.addWidget(self.makeForecastButton, 4, 1, 1, 1)
        self.grid.addWidget(self.forecast, 5, 0, 1, 1)

        self.grid.addWidget(self.barrier2, 6, 0, 1, 2)

        self.grid.addWidget(self.gradesFilename, 7, 1, 1, 1)

        self.grid.addWidget(self.loadFromFileButton, 7, 0, 1, 1)
        self.grid.addWidget(self.writeToFileButton, 8, 0, 1, 2)

        self.grid.addWidget(self.gradeSaveModuleLog, 9, 0, 1, 2)

        self.window.setWindowTitle("GradeMapper " + subject)
        self.window.setGeometry(100, 100, 0, 0)
        #self.window.show()
        
    def removeLastGrade(self):
        
        self.weightedGrades.pop(-1)
        self.weights.pop(-1)
        self.outputAverage()

    def outputAverage(self):

        self.gradeOut.setText("Оценка: {}".format(str(round(sum(self.weightedGrades) / sum(self.weights), 2))))
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
        resultsText = ""
        suffixes = {1:"-ка" , 2:"-ки", 3:"-ки", 4:"-ки"}
            
        for i in workTypes.keys():
            forecastGrades = {5:0, 4:0, 3:0, 2:0, 1:0}
            weightedGradesCopy = sum(self.weightedGrades)
            weightsCopy = sum(self.weights)
            currentTargetGrade = desiredGrade

            while weightedGradesCopy / weightsCopy < desiredGrade - 0.4:
                weightedGradesCopy += i * currentTargetGrade
                weightsCopy += i
                forecastGrades[currentTargetGrade] += 1

                if (weightedGradesCopy / weightsCopy > desiredGrade - 0.8) and (currentTargetGrade < 5):
                    currentTargetGrade += 1
                    continue

            resultsText += "{}: ".format(workTypes[i])

            for j in forecastGrades.keys():
                if forecastGrades[j] == 0:
                    continue
                if j < desiredGrade:
                    break
                if forecastGrades[j] not in suffixes:
                	suffix = "-ок"
                else:
                	suffix = suffixes[int(forecastGrades[j])]
                resultsText += "{} {}; ".format(forecastGrades[j], str(j) + suffix)

            resultsText += "\n"

            

        #for i in workTypes.keys():
        
                
        self.forecast.setText(resultsText)

    def writeToFile(self):

        fileName = "{}_{}".format("_".join(self.subject.split(" ")), str(int(sum(self.weightedGrades))))
        fOut = open(fileName, "w")
        gradesZipped = dict(zip(self.weightedGrades, self.weights))
        json.dump(gradesZipped, fOut, indent = 4)
        fOut.close()
        self.gradeSaveModuleLog.setText("Сохранено в " + fileName)

    def loadFromFile(self):

        fileName = self.gradesFilename.text()
        try:
        	f = open(fileName, "r")
        except FileNotFoundError:
        	self.gradeSaveModuleLog.setText("Файл {} не найден".format(fileName))
        	return -1
        gradesZipped = json.load(f)
        f.close()
        self.weightedGrades = [float(x) for x in list(gradesZipped.keys())]
        self.weights = list(gradesZipped.values())
        #print(self.weights)
        #print(self.weightedGrade)
        self.gradeSaveModuleLog.setText(" ")
        self.outputAverage()
        
if __name__ == "__main__":
    menu = MainMenu()
    sys.exit(menu.app.exec_())
