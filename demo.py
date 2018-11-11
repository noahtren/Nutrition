from nutrition import *

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

someday = Day((breakfast, salad, stir_fry, beverages))
print(someday.Display_Day())
