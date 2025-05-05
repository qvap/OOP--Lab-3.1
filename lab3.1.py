import customtkinter as ctk
from tkinter import Canvas
from math import sqrt

class CCircle(): # Базовый класс круга

    def __init__(self, canvas, x, y):
        # Private
        self.__radius = 50
        self.__color = "#fc7f03"
        self.__border_color = "#9c4d00"
        self.__selected_border_color = "#FFFFFF"
        self.__x = x
        self.__y = y

        # Public
        self.canvas = canvas

        print(f"New point: {x}, {y}")

    def draw(self, draw_border: bool): # Отрисовывает круг на Canvas
        __chosen_border_color = self.__selected_border_color if draw_border else self.__border_color
        self.canvas.create_oval(self.__x - self.__radius, self.__y - self.__radius,\
            self.__x + self.__radius, self.__y + self.__radius, fill = self.__color, width = 5, outline = __chosen_border_color)
    
    def mousecheck(self, x: int, y: int) -> bool: # Проверяет, наход. ли точка внутри круга
        return ((x - self.__x)**2 + (y - self.__y)**2) <= self.__radius**2

class Container():

    def __init__(self, canvas):
        # Private
        self.__container = list()
        self.__selected_container = list()
        self.__multiple_selection = False

        # Public
        self.canvas = canvas
    
    def container_append(self, object: CCircle): # Добавляет в контейнер новый круг
        print(f"Appending new object: {object}")
        self.__container.insert(0, object)
    
    def create_object(self, point): # Создаёт новый круг и добавляет в список
        self.deselect_objects() # Снять выделение при создании нового объекта

        self.container_append(CCircle(x=point.x, y=point.y, canvas=self.canvas))

        self.redraw()
    
    def select_objects(self, point): # Выделяет круги (в зависимости от __multiple_selection меняется поведение)
        if not self.__multiple_selection:
            self.deselect_objects()
        
        for circle in self.__container:
            if circle.mousecheck(point.x, point.y):
                self.__selected_container.insert(0, circle)
                if not (self.__multiple_selection):
                    break
        
        self.redraw()
    
    def deselect_objects(self, *args): # Снимает выделение со всех кругов
        self.__selected_container.clear()
    
    def delete_objects(self, *args): # Удаляет выделенные объекты
        for obj in self.__selected_container:
            self.__container.remove(obj)
            del obj
        self.__selected_container.clear()

        self.redraw()
    
    def initiate_selection(self, *args): # Включает множественное выделение
        self.__multiple_selection = True

    def stop_selection(self, *args): # Выключает множественное выделение
        self.__multiple_selection = False
    
    def redraw(self):
        self.canvas.delete("all")
        for circle_index in range(len(self.__container)-1, -1, -1):
            draw_border = True if self.__container[circle_index] in self.__selected_container else False
            self.__container[circle_index].draw(draw_border)
    

class App(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Лабораторная работа №3")
        self.geometry("400x600")
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.canvas = Canvas(master=self, bg="#24211e", highlightbackground="#24211e")
        self.canvas.grid(row=0, column=0, sticky="nsew")

        self.container = Container(canvas=self.canvas)

        self.bind("<Button-1>", self.container.create_object)
        self.bind("<Button-3>", self.container.select_objects)
        self.bind_all("<Escape>", self.container.deselect_objects)
        self.bind_all("<Delete>", self.container.delete_objects)
        self.bind("<KeyPress-Control_L>", self.container.initiate_selection)
        self.bind("<KeyRelease-Control_L>", self.container.stop_selection)

if __name__ == "__main__":
    app = App()
    app.mainloop()