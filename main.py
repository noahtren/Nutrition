import profile
import reader
from nutrition import *
from nutrition_gui import *

day_obj = reader.read_day()
my_gui = Nutrition_Gui(day_obj.meal)
day_obj.meal.Export("ideal_day")