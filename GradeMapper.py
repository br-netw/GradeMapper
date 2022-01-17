from tkinter import *
import json

## Около 50% кода в этом файле украдены с моего собственного проекта. Имейте в виду.

class MainMenu():

    def __init__(self):

        self.window = Tk()
        self.window.title("GradeMapper")
        self.window.geometry("340x100")
        
        fileVals = open("gradeTypes.json", "r", encoding="utf8")
        vals = list(json.load(fileVals).keys()) # Загружаем список типов оценок
        fileVals.close()

        self.measures = StringVar()
        self.measures.set(vals[0])

        self.mainMenu = OptionMenu(self.window, self.measures, *vals)
        self.mainMenu.grid(row = 1, column = 0)

        self.startButton = Button(self.window, text = "Запустить", command = self.bootstrap)
        self.startButton.grid(row = 1, column = 1)

        self.nameLabel = Label(self.window, text="GradeMapper", font=("Arial Bold", 20))
        self.nameLabel.grid(row=0, column=1)

    def bootstrap(self):

        #print(self.measures.get())

        newConverter = Converter(self.measures.get(), self) # Открываем окно конвертера для необходимой величины

        ## StackOverflow сказал не запускать больше одного mainloop()
        #newConverter.window.mainloop()

class Converter():

    def __init__(self, valType, menu):

        #print(open("conversionValues-ru.json", "r", encoding="utf8").read())

        self.gradesWeighted = 0
        self.weightsSum = 0
        
        fileVals = open("gradeTypes.json", "r", encoding="utf8")
        self.convVals = json.load(fileVals)[valType]
        fileVals.close()

        self.window = Toplevel(menu.window)
        self.window.title("GradeMapper " + valType.capitalize())
        self.window.geometry("335x120")
        #print(list(self.convVals.keys()))

        keys = list(self.convVals.keys())
        
        ## Эти переменные содержат выбранные пункты меню с ЕИ
        self.gradeType = StringVar()
        self.gradeType.set(keys[0])

        ## Текстбокс
        self.grade = Text(self.window, height = 2, width = 16)
        self.grade.grid(row = 1, column = 0)

        self.avgGrade = Text(self.window, height = 2, width = 16)
        self.avgGrade.grid(row = 2, column = 0)

        ## Кнопки

        self.logButton = Button(self.window, text="Загрузить оценку", command=self.logGrade)
        self.logButton.grid(row=0, column=1)
        self.submitButton = Button(self.window, text="Рассчитать", command=self.submit)
        self.submitButton.grid(row=1, column=1)

        self.createUnitMenus()

    def createUnitMenus(self):

        # Создание меню для выбора величин

        self.typeMenu = OptionMenu(self.window, self.gradeType, *list(self.convVals.keys()))
        self.typeMenu.grid(row = 0, column = 0)

    def logGrade(self):
                    
        currentGrade = self.grade.get(1.0, "end")
        #print(self.gradeType.get())
        currentGradeWeight = self.convVals[self.gradeType.get()]

        self.grade.delete(1.0, "end")
        self.avgGrade.delete(1.0, "end")

        try:
            catch = int(currentGrade)
        except Exception:
            self.avgGrade.insert("end", "Не является числом")
            return -1

        if int(currentGrade) < 1 or int(currentGrade) > 5:
            self.avgGrade.insert("end", "Невалидная оценка")
            return -1

        self.gradesWeighted += int(currentGrade) * currentGradeWeight
        self.weightsSum += currentGradeWeight
        #print(self.gradesWeighted, self.weightsSum)

    def submit(self):

        self.avgGrade.insert("end", round(self.gradesWeighted / self.weightsSum, 2))

menu = MainMenu()
menu.window.mainloop()
