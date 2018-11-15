from nutrition import *
from tkinter import *
# 1 tablespoon is 15g
protein = Food(get_food_data("14058"), 25)
raspberry = Food(get_food_data("09518"),20)
blueberry = Food(get_food_data("09054"),20)
oj = Food(get_food_data("14064"), 40)
chia = Food(get_food_data("12006"), 15)
smoothie = Meal((protein, raspberry, blueberry, oj, chia))

olive_oil = Food(get_food_data("04053"),20)
spinach = Food(get_food_data("11457"),30)
carrots = Food(get_food_data("11124"),30)
pumpkinseeds = Food(get_food_data("12163"),20)
mushrooms = Food(get_food_data("11238"),30)
chicken = Food(get_food_data("05747"),50)
broccoli1 = Food(get_food_data("11740"),30)
salad = Meal((olive_oil, spinach, carrots, pumpkinseeds, mushrooms, chicken, broccoli1))

egg = Food(get_food_data("01132"),80)
banana = Food(get_food_data("09040"),110)
breakfast = Meal((egg, banana))

noodles = Food(get_food_data("20113"),100)
red_pepper = Food(get_food_data("11823"),20)
onion = Food(get_food_data("11282"),10)
general_tso = Food(get_food_data("36618"),60)
almonds = Food(get_food_data("12061"),20)
lunch = Meal((noodles, red_pepper, onion, general_tso, almonds))

rice = Food(get_food_data("20037"),200)
broccoli2 = Food(get_food_data("11740"),20)
pepper = Food(get_food_data("02030"),0.5)
dinner = Meal((rice, broccoli2,pepper))

magnesium_supplemet = Nutrient("Magnesium, Mg", "Minerals", 200, "mg")
vitamin_d_supplement = Nutrient("Vitamin D", "Vitamins", 1000, "IU")
zinc_supplement = Nutrient("Zinc, Zn", "Minerals", 45, "mg")
fish_oil_supplement = Nutrient("Fatty acids, total polyunsaturated", "Lipids", 2, "g")
garlic_supplement = Food(get_food_data("11215"),1)
stack_food = Food("Supplements", (magnesium_supplemet, vitamin_d_supplement, zinc_supplement, fish_oil_supplement), 1)

green_tea = Food(get_food_data("14278"),900) # 4 cups
water = Food(get_food_data("14555"),900) # 4 cups
beverages = Meal((green_tea, water))

supplement_stack = Meal((stack_food, garlic_supplement))

someday = Day((smoothie, salad, breakfast, lunch, beverages, supplement_stack, dinner)).Get_Meal()
master = Tk()

nutrient_labels = [] # for main gui
info_labels = [] # for popup labels
info_label_text = []
label_names = []
groups = someday.Get_Groups()
grouped_nutrients = someday.Get_Grouped_Nutrients()
i = 0

def rgb_convert(r, g, b):
    return "#%02x%02x%02x" % (r, g, b)

def hover_box(event):
    for i in range(0, len(info_label_text)):
        info_label_text[i].set("")
    index = nutrient_labels.index(event.widget)
    nutrient_name = label_names[index]
    (nutrients, value) = someday.Nutrient_Analysis(nutrient_name)
    for nutrient in nutrients:
        if (len(info_labels) <= nutrients.index(nutrient)):
            info_labels.append([])
        if (len(info_label_text) <= nutrients.index(nutrient)):
            info_label_text.append(StringVar(""))
        info_label_text[nutrients.index(nutrient)].set("{}{} in \n{}".format(nutrient.get_value(), nutrient.get_unit(), nutrient.get_my_food()))
        info_labels[nutrients.index(nutrient)] = Label(master,bg=rgb_convert(255-int(255*(nutrient.get_value()/nutrients[0].get_value())),255,255-int(255*(nutrient.get_value()/nutrients[0].get_value()))),textvariable=info_label_text[nutrients.index(nutrient)])
        info_labels[nutrients.index(nutrient)].grid(row=nutrients.index(nutrient),column=len(grouped_nutrients))

for group in grouped_nutrients:
    nutrient_labels.append(Label(master,text=groups[grouped_nutrients.index(group)]).grid(row=0,column=grouped_nutrients.index(group)))
    label_names.append("Group")
    i = i + 1
    for nutrient in group:
        text = nutrient.Nutrient_Info()
        if ("healthy" in text):
            nutrient_labels.append(Label(master, text=text, bg="green"))
        elif ("Deficient" in text):
            nutrient_labels.append(Label(master, text=text, bg="yellow"))
        elif ("Too much" in text):
            nutrient_labels.append(Label(master, text=text, bg ="red"))
        else:
            nutrient_labels.append(Label(master, text=text))
        nutrient_labels[i].grid(row=group.index(nutrient)+1,column=grouped_nutrients.index(group))
        nutrient_labels[i].bind("<Enter>",hover_box)
        label_names.append(nutrient.get_name())
        i = i + 1

master.mainloop()


# needs more b12
# needs less A
# needs more E
# needs more calcium