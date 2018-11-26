from nutrition import *
from nutrition_gui import *

# Listing each specific food and converting it into a set of meals
# Morning smoothie
whey = Food(get_food_data("14066"), 50)
raspberry = Food(get_food_data("09518"),20)
blueberry = Food(get_food_data("09054"),20)
oj = Food(get_food_data("14064"), 100)
chia = Food(get_food_data("12006"), 12)
smoothie = Meal((whey, raspberry, blueberry, oj, chia))

# Breakfast
egg = Food(get_food_data("01132"),60)
banana = Food(get_food_data("09040"),60)
yogurt = Food(get_food_data("01284"),100)
breakfast = Meal((egg, banana, yogurt)) 

# Lunch
noodles = Food(get_food_data("20110"),200)
red_pepper = Food(get_food_data("11823"),20)
onion = Food(get_food_data("11282"),10) 
tofu = Food(get_food_data("16162"),30)
chicken2 = Food(get_food_data("05136"),60)
sauce = Food(get_food_data("27050"),20)
lunch = Meal((noodles, red_pepper, onion, sauce, chicken2, tofu))

# Snacks
peanut_butter = Food(get_food_data("16098"), 40)
pretzels = Food(get_food_data("19047"), 25)
snacks = Meal((peanut_butter, pretzels))

# Afternoon salad
olive_oil = Food(get_food_data("04053"),15)
spinach = Food(get_food_data("11457"),30)
carrots = Food(get_food_data("11124"),20)
sunflowerseeds = Food(get_food_data("12537"),20)
mushrooms = Food(get_food_data("11238"),20)
broccoli1 = Food(get_food_data("11093"),40)
peas = Food(get_food_data("11300"),15)
beans = Food(get_food_data("16015"),15)
salad = Meal((olive_oil, spinach, carrots, sunflowerseeds, mushrooms, broccoli1, peas, beans))

# Dinner
rice = Food(get_food_data("20037"),220)
broccoli2 = Food(get_food_data("11093"),20)
pepper = Food(get_food_data("02030"),0.5)
chicken = Food(get_food_data("05136"),100)
dinner = Meal((rice, broccoli2, pepper, chicken))

# Supplements
vitamin_d_supplement = Nutrient("Vitamin D", "Vitamins", 2000, "IU")
zinc_supplement = Nutrient("Zinc, Zn", "Minerals", 45, "mg")
fish_oil_supplement = Nutrient("Fatty acids, total polyunsaturated", "Lipids", 2, "g")
garlic_supplement = Food(get_food_data("11215"),1)
calcium_supplement = Nutrient("Calcium, Ca", "Minerals", 400, "mg")
supplements = Food("Supplements", (vitamin_d_supplement, zinc_supplement, fish_oil_supplement, calcium_supplement), 1)
supplement_stack = Meal((supplements, garlic_supplement))

# Beverages
green_tea = Food(get_food_data("14278"),450) # 2 cups
coffee = Food(get_food_data("14180"),450) # 2 cups
creamer = Food(get_food_data("16261"),30)
water = Food(get_food_data("14555"),900) # 4 cups
beverages = Meal((green_tea, water, creamer, coffee))

# Combine all of the meals into a day object
ideal_day = Day((smoothie, breakfast, lunch, salad, dinner, supplement_stack, beverages, snacks)).Get_Meal()

# Display the daily health information in a color-coded GUI
# the GUI displays which nutrients are deficient, in healthy
# amounts, or too much. For example, it will show if you have
# too much sodium on a day, or not enough Vitamin D
my_gui = Nutrition_Gui(ideal_day)