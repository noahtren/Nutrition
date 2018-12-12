from tkinter import *
from ctypes import windll
class Nutrition_Gui:
    def __init__(self, day):
        windll.shcore.SetProcessDpiAwareness(1)
        self.master = Tk()
        self.day = day
        # Daily nutrient display
        self.nutrient_labels = []
        self.label_names = []
        # Specific nutrient breakdown
        self.info_labels = []
        self.info_labels_text = []
        # Daily nutrient data
        self.groups = day.Get_Groups()
        self.grouped_nutrients = day.Get_Grouped_Nutrients()
        # DISPLAY GUI
        self.setup()
        self.master.mainloop()
    def rgb_convert(self, r, g, b):
        return "#%02x%02x%02x" % (r, g, b)
    def hover_box(self, event):
        for i in range(0, len(self.info_labels_text)):
            self.info_labels_text[i].set("")
        index = self.nutrient_labels.index(event.widget)
        nutrient_name = self.label_names[index]
        (nutrients, value) = self.day.Nutrient_Analysis(nutrient_name)
        for nutrient in nutrients:
            if (len(self.info_labels) <= nutrients.index(nutrient)):
                self.info_labels.append([])
            if (len(self.info_labels_text) <= nutrients.index(nutrient)):
                self.info_labels_text.append(StringVar(""))
            self.info_labels_text[nutrients.index(nutrient)].set("{}{} in \n{}".format(nutrient.value, nutrient.unit, nutrient.my_food))
            self.info_labels[nutrients.index(nutrient)] = Label(self.master,bg=self.rgb_convert(255-int(255*(nutrient.value/nutrients[0].value)),255,255-int(255*(nutrient.value/nutrients[0].value))),textvariable=self.info_labels_text[nutrients.index(nutrient)])
            self.info_labels[nutrients.index(nutrient)].grid(row=nutrients.index(nutrient),column=len(self.grouped_nutrients))
    def setup(self):
        i = 0
        for group in self.grouped_nutrients:
            self.nutrient_labels.append(Label(self.master,text=self.groups[self.grouped_nutrients.index(group)]).grid(row=0,column=self.grouped_nutrients.index(group)))
            self.label_names.append("Group")
            i = i + 1
            for nutrient in group:
                text = nutrient.Info(True)
                if ("healthy" in text):
                    self.nutrient_labels.append(Label(self.master, text=text, bg="#7aff7a", justify=LEFT))
                elif ("Deficient" in text):
                    self.nutrient_labels.append(Label(self.master, text=text, bg="#ffff7a", justify=LEFT))
                elif ("Too much" in text):
                    self.nutrient_labels.append(Label(self.master, text=text, bg ="#ff7a7a", justify=LEFT))
                else:
                    self.nutrient_labels.append(Label(self.master, text=text))
                self.nutrient_labels[i].grid(row=group.index(nutrient)+1,column=self.grouped_nutrients.index(group))
                self.nutrient_labels[i].bind("<Enter>",self.hover_box)
                self.label_names.append(nutrient.name)
                i = i + 1