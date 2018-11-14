from nutrition import *
import tkinter

egg = Food(get_food_data("01132"),50)
banana = Food(get_food_data("09040"),110)
breakfast = Meal((egg, banana))

olive_oil = Food(get_food_data("04053"),10)
spinach = Food(get_food_data("11457"),50)
carrots = Food(get_food_data("11124"),30)
pumpkinseeds = Food(get_food_data("12163"),20)
mushrooms = Food(get_food_data("11238"),30)
chicken = Food(get_food_data("05747"),40)
broccoli1 = Food(get_food_data("11740"),30)
salad = Meal((olive_oil, spinach, carrots, pumpkinseeds, mushrooms, chicken, broccoli1))

noodles = Food(get_food_data("20113"),150)
red_pepper = Food(get_food_data("11823"),20)
onion = Food(get_food_data("11282"),10)
general_tso = Food(get_food_data("36618"),80)
stir_fry = Meal((noodles, red_pepper, onion, general_tso))

green_tea = Food(get_food_data("14278"),900) # 4 cups
water = Food(get_food_data("14555"),900) # 4 cups
beverages = Meal((green_tea, water))

someday = Day((breakfast, salad, stir_fry, beverages)).Get_Meal()

master = tkinter.Tk()

nutrient_labels = []
analysis_labels = []
label_names = []
groups = someday.Get_Groups()
grouped_nutrients = someday.Get_Grouped_Nutrients()
i = 0

def hover_box(event):
    index = nutrient_labels.index(event.widget)
    nutrient_name = label_names[index]
    nutrients = someday.Nutrient_Analysis(nutrient_name)
    print("{}:".format(nutrient_name))
    for nutrient in nutrients:
        print("{}{} in {}".format(nutrient.get_value(), nutrient.get_unit(), nutrient.get_my_food()))

for group in grouped_nutrients:
    nutrient_labels.append(tkinter.Label(master,text=groups[grouped_nutrients.index(group)]).grid(row=0,column=grouped_nutrients.index(group)))
    label_names.append("Group")
    i = i + 1
    for nutrient in group:
        text = nutrient.Nutrient_Info()
        if ("healthy" in text):
            nutrient_labels.append(tkinter.Label(master, text=text, bg="green"))
        elif ("Deficient" in text):
            nutrient_labels.append(tkinter.Label(master, text=text, bg="yellow"))
        elif ("Too much" in text):
            nutrient_labels.append(tkinter.Label(master, text=text, bg ="red"))
        else:
            nutrient_labels.append(tkinter.Label(master, text=text))
        nutrient_labels[i].grid(row=group.index(nutrient)+1,column=grouped_nutrients.index(group))
        nutrient_labels[i].bind("<Enter>",hover_box)
        label_names.append(nutrient.get_name())
        i = i + 1

master.mainloop()
