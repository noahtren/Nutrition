import time
start = time.clock()
import profile
print("Time to build profile {}".format(str(time.clock() - start)))
start = time.clock()
import reader
print("Time to read daily values {}".format(str(time.clock() - start)))
start = time.clock()
from nutrition import *
print("Time to read local database {}".format(str(time.clock() - start)))
start = time.clock()
from nutrition_gui import *
print("Time to import gui {}".format(str(time.clock() - start)))
start = time.clock()
import json
berries = (access_database("09040"))
print("Time to access database {}".format(str(time.clock() - start)))
start = time.clock()

day_obj = reader.read_day()
print("Time to build day object {}".format(str(time.clock() - start)))
start = time.clock()

my_gui = Nutrition_Gui(day_obj.meal)
print("Time build GUI {}".format(str(time.clock() - start)))
start = time.clock()

day_obj.meal.Export("reports/ideal_day")
print("Time to export {}".format(str(time.clock() - start)))
