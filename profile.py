import yaml
import settings 

profile_dict = yaml.load(open(format(settings.profile_path)))
# This portion is entirely customizable, based on profile path
weight_c = profile_dict["pounds"]
height_c = profile_dict["feet"] * 12 + profile_dict["inches"]
sex = profile_dict["sex"].upper()
hours_of_exercise = profile_dict["hours_of_exercise"]
age = profile_dict["age"]
fat_percent = profile_dict["fat_percent"] * 0.01
protein_percent = profile_dict["protein_percent"] * 0.01
carb_percent = profile_dict["carb_percent"] * 0.01
admittance_percent = profile_dict["leniency"] # how accurate do you want your rda values to be? Within +- this percent
# Conversion and calculation of bmr and tdee (basal metabolic rate, total daily energy expenditure)
weight_m = .4536 * weight_c
height_m = 2.54 * height_c
if (sex == "M"):
    bmr = 66 + (13.7*weight_m) + (5*height_m) - (6.8*age)
else:
    bmr = 655 + (9.6*weight_m) + (1.8*height_m) - (4.7*age)
tdee = bmr * (1 + hours_of_exercise * .55)
top = tdee * (1 + admittance_percent * 0.01)
bot = tdee * (1 - admittance_percent * 0.01)

recommended_amounts = {
    # PROXIMATES
    'Proximates':'Overview of macronutrients',
    'Water': (2500, 3500), #g
    'Calories': (bot, top), #kcal
    'Protein':((bot/4)*protein_percent,(top/4)*protein_percent), #4 calories per g 35%
    'Fat': ((bot/9)*fat_percent,(top/9)*fat_percent),#9 calories per g 55%
    'Carbs':((bot/4)*carb_percent,(top/4)*carb_percent), #4 calories per g 10%
    'Fiber': (0.95*0.014*tdee,1.05*0.014*tdee),#g
    'Sugar': ((bot/4)*0.05,(top/4)*0.1),#g - a bunch of monosaccharides
    # MINERALS
    'Minerals':'Elements that support good health',
    'Calcium':(1000,2500), #mg
    'Iron':(8,45), #mg
    'Magnesium':(300,750), #mg
    'Phosphorus':(700,4000), #mg
    'Potassium':(1400,6000), #mg
    'Sodium':(1000,2300), #mg
    'Zinc':(12,100), #mg
    'Copper':(0.9,10), #mg
    'Manganese':(1.8, "none"), #mg
    'Selenium':(70,400), #ug
    'Fluoride':(400,10000), #ug
    # VITAMINS
    'Vitamins':'Essential organic molecules',
    'Vitamin C':(90,2000), #mg
    'Vitamin B-1 (Thiamine)':(1.2,"none"), # mg
    'Vitamin B-2 (Riboflavin)':(1.3,"none"), #mg
    'Vitamin B-3 (Niacin)':(16,"none"), #mg
    'Vitamin B-5 (Pantothenic acid)':(4,"none"), #mg
    'Vitamin B-6 (Pyridoxine)':(1.3,100), #mg
    'Vitamin B-9 (Folate)':(400,1000), #ug
    'Vitamin B-12 (Cobalamin)':(2.4,"none"), # ug
    'Vitamin A, RAE':(900,3000), #ug
    'Vitamin A, IU':(900,20000), # iu
    'Vitamin E':(15,1000), # mg - many kinds of tocopherols
    'Vitamin D (D2 + D3)':("none","none"), # ug
    'Vitamin D':(1000,8000), # iu
    'Choline':(550,3500), # mg
    'Vitamin K':(120,"none"), #ug
    # FATS/LIPIDS
    'Fats':'Key macronutrient that comes in various forms',
    'Saturated':(0, (tdee/9)*(fat_percent/0.3)*.1), #g
    'Monounsaturated':((tdee/9)*(fat_percent/0.3)*.15,(tdee/9)*(fat_percent/0.3)*.2), #g
    'Polyunsaturated':((tdee/9)*(fat_percent/0.3)*.05,(tdee/9)*(fat_percent/0.3)*.1), #g
    'Omega-3':("none","none"), #g
    'ALA':(0.6,"none"), #g
    'EPA':(0.5,"none"), #g
    'DHA':(0.5,"none"),
    'Trans':(0,(tdee/9)*(fat_percent/0.3)*.01), #g
    'Cholesterol':(0, 300), #mg
    # OTHER
    'Other':'Non-required nutrients, often stimulants',
    'Caffeine':("none", 400), #mg
    'Theobromine':("none", 300), # mg

}
units = [["g", "kcal", "g", "g", "g", "g", "g"],
         ["mg", "mg", "mg", "mg", "mg", "mg", "mg", "mg", "mg", "µg", "µg"],
         ["mg", "mg", "mg", "mg", "mg", "mg", "µg", "µg", "µg", "IU", "mg", "µg", "IU", "mg", "µg"],
         ["g", "g", "g", "g", "g", "g", "g", "g", "mg"],
         ["mg", "mg"]]

# if you change this, remember that it doesn't fix local data
name_filter = ["Energy", "Total lipid (fat)", "Carbohydrate, by difference",
               "Fiber, total dietary", "Sugars, total", "Calcium, Ca", "Iron, Fe",
               "Potassium, K", "Sodium, Na", "Magnesium, Mg", "Phosphorus, P",
               "Zinc, Zn", "Copper, Cu", "Manganese, Mn",
               "Selenium, Se", "Fluoride, F", "Thiamin", "Riboflavin",
               "Niacin", "Vitamin B-6", "Pantothenic acid",
               "Vitamin E (alpha-tocopherol)", "Vitamin K (phylloquinone)",
               "Vitamin C, total ascorbic acid", "Folate, total", 
               "Choline, total", "Vitamin B-12",
               "Fatty acids, total saturated",
               "Fatty acids, total monounsaturated", "Fatty acids, total polyunsaturated",
               "Fatty acids, total trans",
               "18:3 n-3 c,c,c (ALA)", "20:5 n-3 (EPA)", "22:6 n-3 (DHA)"]
name_replace = ["Calories", "Fat", "Carbs", 
                "Fiber", "Sugar", "Calcium", "Iron",
                "Potassium", "Sodium", "Magnesium", "Phosphorus",
                "Zinc", "Copper", "Manganese",
                "Selenium", "Fluoride", "Vitamin B-1 (Thiamine)", "Vitamin B-2 (Riboflavin)",
                "Vitamin B-3 (Niacin)", "Vitamin B-6 (Pyridoxine)", "Vitamin B-5 (Pantothenic acid)",
                "Vitamin E", "Vitamin K",
                "Vitamin C", "Vitamin B-9 (Folate)", 
                "Choline", "Vitamin B-12 (Cobalamin)",
                "Saturated",
                "Monounsaturated", "Polyunsaturated",
                "Trans",
                "ALA", "EPA", "DHA"]

encapsulators = {
    "Omega-3": {
        "includes":["ALA", "EPA", "DHA"],
        "group":"Fats",
        "unit":"g"
    }
}