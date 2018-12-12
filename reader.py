import yaml
import settings
from nutrition import *

def read_day():
    day_dict = yaml.load(open(settings.day_path, "r"))["day"]["meals"]
    meal_objs = []
    for meal in day_dict:
        food_objs = []
        for food in day_dict[meal]:
            food_dict = day_dict[meal][food]
            food_dict["meal"] = meal
            if 'nutrients' not in food_dict.keys():
                food_objs.append(Food(access_database(food_dict["id"]), food_dict["grams"]))
            else:
                nutrient_objs = []
                for nutrient in day_dict[meal][food]["nutrients"]:
                    nutrient_objs.append(Nutrient(nutrient["name"],nutrient["group"],nutrient["value"],nutrient["unit"]))
                food_objs.append(Food(food, nutrient_objs))
        if len(food_objs) > 0:
            meal_objs.append(Meal(food_objs))
    day_obj = Day(meal_objs)
    return day_obj
