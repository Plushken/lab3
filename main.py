from tkinter import *
from tkinter import ttk, messagebox
import sys
import PIL
import cv2 as cv
import mahotas
import mahotas.demos
from PIL import ImageTk


def median_filter_info():
    messagebox.showinfo("Медианный фильтр", "Заменяет значение яркости пикселя на значение медианы распределения яркостей всех пикселей в окрестности")


def filter_min_info():
    messagebox.showinfo("Фильтр минимума", "Заменяет значение яркости пикселя на значение минимальной яркости в окрестности")


def filter_max_info():
    messagebox.showinfo("Фильтр максимума", "Заменяет значение яркости пикселя на значение максимальной яркости в окрестности")


def bernsen_threshholding_info():
    messagebox.showinfo("Метод Бернсена", "1. Обычная квадратная апертура с нечетным числом пикселей пробегает в цикле по всем пикселям исходного изображения. На каждом шаге находится Min и Max.\n"
                                          "2. Находится среднее значение Avg= (Min + Max) /2.\n"
                                          "3. Если текущий пиксель больше Avg<E — он становится белым, иначе — чёрным. E — некая константа заданная пользователем.\n"
                                          "4. Если среднее меньше порога контраста — то текущий пиксель становится того цвета, который задавался параметром «цвет сомнительного пикселя».\n"
                                          "Имеет ряд недостатков: после обработки монотонных областей яркости формируются сильные паразитные помехи, в некоторых случаях приводит к появлению ложных черных пятен")


def niblack_threshholding_info():
    messagebox.showinfo("Метод Ниблэка", "Идея данного метода состоит в варьировании порога яркости B бинаризации от точки к точке на основании локального значения стандартного отклонения. Порог яркости в точке (x, y) рассчитывается так:"
                                         "\nB(x,y) = μ(x, y) + k*s(x, y)\n"
                                         "где μ(x, y) – среднее и s(x, y) — среднеквадратичное отклонение выборки для некоторой окрестности точки. Размер окрестности должен быть минимальным, но таким, чтобы сохранить локальные детали изображения. "
                                         "В то же время размер должен быть достаточно большим, чтобы понизить влияние шума на результат. Значение k определяет, какую часть границы объекта взять в качестве самого объекта. Значение k=-0.2 задает достаточно хорошее разделение объектов, если они представлены черным цветом, а значение k=+0.2, – если объекты представлены белым цветом.")


def adaptive_thresholding_info():
    messagebox.showinfo("Адаптивная пороговая обработка", "Исходное изображение следует разделить на подобласти, в каждой из которых для сегментации ищется и используется свой порог. \n"
                                                          "адаптивный алгоритм пороговой обработки базируется на идее сопоставления уровней яркости преобразуемого пикселя со значениями локальных средних, "
                                                          "вычисленных непосредственно в его окружении, то есть у соседей. Пиксели обрабатываются поочередно. Интенсивность каждого пикселя сравнивается со "
                                                          "средними значениями яркости в окнах размерности с центром в точке.\n"
                                                          "Основной проблемой здесь является задача разбиения изображения на подобласти и выбор для каждой из них своего порога. ")


def app_info():
    messagebox.showinfo("Информация об приложении", "Методы,которые показаны в данном приложение:\n"
                                                    "-Медианный фильтр\n"
                                                    "-Фильтр минимума\n"
                                                    "-Фильтр максимума\n"
                                                    "-Метод Бернсена\n"
                                                    "-Метод Ниблэка\n"
                                                    "-Адаптивная пороговая обработка\n"
                                                    "Для медианного фильтра, фильтра минимума и максимума необходимо назвать файл 'fil.jpg'\n"
                                                    "А для метода Бернсена, метода Ниблэка и адаптивной пороговой обработки - 'qwe.bmp'")

def bye():
    raise SystemExit()
class MainSolution:
    def __init__(self):
        self.fil = cv.imread('fil.jpg', cv.IMREAD_GRAYSCALE)
        self.qwe = cv.imread('qwe.bmp', cv.IMREAD_GRAYSCALE)

    def filtr(self):
        median_image = cv.medianBlur(self.fil, 7)
        median_image = PIL.Image.fromarray(median_image)
        median_image = median_image.resize((300, 300))
        size = (3, 3)
        shape = cv.MORPH_RECT
        kernel = cv.getStructuringElement(shape, size)
        min_image = cv.erode(self.fil, kernel)
        max_image = cv.dilate(self.fil, kernel)
        min_image = PIL.Image.fromarray(min_image)
        min_image = min_image.resize((300, 300))
        max_image = PIL.Image.fromarray(max_image)
        max_image = max_image.resize((300, 300))
        return ImageTk.PhotoImage(median_image), ImageTk.PhotoImage(min_image), ImageTk.PhotoImage(max_image)

    def getorig(self):
        img = PIL.Image.fromarray(self.fil)
        img = img.resize((300, 300))
        img2 = PIL.Image.fromarray(self.qwe)
        img2 = img2.resize((300, 300))
        return ImageTk.PhotoImage(img), ImageTk.PhotoImage(img2)

    def adaptivethresholding(self):
        th3 = cv.adaptiveThreshold(self.qwe, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 11, 2)
        img = PIL.Image.fromarray(th3)
        img = img.resize((300, 300))
        return ImageTk.PhotoImage(img)

    def bernsenthresholding(self):
        img = self.qwe
        img = mahotas.thresholding.bernsen(img, 5, 15)
        img = PIL.Image.fromarray(img)
        img = img.resize((300, 300))
        return ImageTk.PhotoImage(img)

    def niblackthreshholding(self):
        img = self.qwe
        img = cv.ximgproc.niBlackThreshold(img, maxValue=255, type=cv.THRESH_BINARY, blockSize=15, k=-0.2)
        img = PIL.Image.fromarray(img)
        img = img.resize((300, 300))
        return ImageTk.PhotoImage(img)

if __name__ == "__main__":
    root = Tk()
    root["bg"] = "light green"
    root.title("Алгоритмы и методы обработки изображений")
    ms = MainSolution()
    w, h = root.winfo_screenwidth(), root.winfo_screenheight()
    root.resizable(width=False, height=False)
    root.option_add("*tearOff", FALSE)
    main_menu = Menu()
    info_menu = Menu()
    file_menu = Menu()
    info_menu.add_command(label="Медианный фильтр", command=median_filter_info)
    info_menu.add_command(label="Фильтр минимума", command=filter_min_info)
    info_menu.add_command(label="Фильтр максимума", command=filter_max_info)
    info_menu.add_separator()
    info_menu.add_command(label="Метод Бернсена", command=bernsen_threshholding_info)
    info_menu.add_command(label="Метод Ниблэка", command=niblack_threshholding_info)
    info_menu.add_separator()
    info_menu.add_command(label="Адаптивная пороговая обработка", command=adaptive_thresholding_info)
    file_menu.add_cascade(label="Информация", menu=info_menu)
    main_menu.add_cascade(label="File", menu=file_menu)
    file_menu.add_separator()
    file_menu.add_cascade(label="О приложении", command=app_info)
    file_menu.add_separator()
    file_menu.add_cascade(label="Выход", command= bye)
    root.config(menu=main_menu)

    root.geometry(f"1300x700")
    lbl_text2 = ttk.Label(text="Оригинал", font='Courier 14', background='beige')
    lbl_text2.place(x=130, y=10)
    lbl_text3 = ttk.Label(text="Медианный фильтр", font='Courier 14', background='beige')
    lbl_text3.place(x=390, y=10)
    lbl_text4 = ttk.Label(text="Фильтр минимума", font='Courier 14', background='beige')
    lbl_text4.place(x=710, y=10)
    lbl_text5 = ttk.Label(text="Фильтр максимума", font='Courier 14', background='beige')
    lbl_text5.place(x=1020, y=10)
    lbl_text6 = ttk.Label(text="Оригинал", font='Courier 14', background='beige')
    lbl_text6.place(x=130, y=350)
    lbl_text7 = ttk.Label(text="Метод Бернсена", font='Courier 14', background='beige')
    lbl_text7.place(x=410, y=350)
    lbl_text8 = ttk.Label(text="Метод Ниблэка", font='Courier 14', background='beige')
    lbl_text8.place(x=720, y=350)
    lbl_text9 = ttk.Label(text="Адаптивная пороговая обработка", font='Courier 14', background='beige')
    lbl_text9.place(x=940, y=350)
    img1, img3, img4 = ms.filtr()
    lbl1 = ttk.Label(image=img1)
    lbl1.image = img1
    lbl1.place(x=320, y=40, width=300, height=300)
    img2, img6 = ms.getorig()
    lbl2 = ttk.Label(image=img2)
    lbl2.image = img2
    lbl2.place(x=10, y=40, width=300, height=300)
    lbl3 = ttk.Label(image=img3)
    lbl3.image = img3
    lbl3.place(x=630, y=40, width=300, height=300)
    lbl4 = ttk.Label(image=img4)
    lbl4.image = img4
    lbl4.place(x=940, y=40, width=300, height=300)
    img5 = ms.bernsenthresholding()
    lbl5 = ttk.Label(image=img5)
    lbl5.image = img5
    lbl5.place(x=320, y=380, width=300, height=300)
    lbl6 = ttk.Label(image=img6)
    lbl6.image = img6
    lbl6.place(x=10, y=380, width=300, height=300)
    img7 = ms.niblackthreshholding()
    lbl7 = ttk.Label(image=img7)
    lbl7.image = img7
    lbl7.place(x=630, y=380, width=300, height=300)
    img8 = ms.adaptivethresholding()
    lbl8 = ttk.Label(image=img8)
    lbl8.image = img8
    lbl8.place(x=940, y=380, width=300, height=300)
    root.mainloop()