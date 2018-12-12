import yaml
import settings 

profile_dict = yaml.load(open(format(settings.profile_path)))
# This portion is entirely customizable
weight_c = profile_dict["pounds"]
height_c = profile_dict["feet"] * 12 + profile_dict["inches"]
sex = profile_dict["sex"].upper()
hours_of_exercise = profile_dict["hours_of_exercise"]
age = profile_dict["age"]
fat_percent = profile_dict["fat_percent"] * 0.01
protein_percent = profile_dict["protein_percent"] * 0.01
carb_percent = profile_dict["carb_percent"] * 0.01
admittance_percent = 7 # how accurate do you want your rda values to be? Within +- this percent
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
    'Energy': (bot, top), #kcal
    'Total lipid (fat)': ((bot/9)*fat_percent,(top/9)*fat_percent),#9 calories per g 55%
    'Water': (2500, 3500), #g
    'Protein':((bot/4)*protein_percent,(top/4)*protein_percent), #4 calories per g 35%
    'Carbohydrate, by difference':((bot/4)*carb_percent,(top/4)*carb_percent), #4 calories per g 10%
    'Fiber, total dietary': (0.95*0.014*tdee,1.05*0.014*tdee),#g
    'Sugars, total': ((bot/4)*0.05,(top/4)*0.1),#g
    'Calcium, Ca':(1000,2500),
    'Iron, Fe':(8,45),
    'Potassium, K':(1400,6000),
    'Sodium, Na':(1000,2300),
    'Magnesium, Mg':(300,750),
    'Phosphorus, P':(700,4000),
    'Zinc, Zn':(12,100),
    'Vitamin E (alpha-tocopherol)':(15,1000),
    'Vitamin K (phylloquinone)':(120,"none"),
    'Vitamin C, total ascorbic acid':(90,2000),
    'Thiamin':(1.2,"none"),
    'Riboflavin':(1.3,"none"),
    'Niacin':(16,"none"), # make sure you can't have too much of this
    'Vitamin B-6':(1.3,100),
    'Folate, DFE':(400,1000),
    'Vitamin A, RAE':(900,3000),
    'Vitamin A, IU':(900,20000),
    'Vitamin D (D2 + D3)':("none","none"),
    'Vitamin D':(1000,8000),
    'Vitamin B-12':(2.4,"none"),
    # non-vetted values
    'Selenium':(70,400), #ug
    'Copper':(0.9,10), #mg
    'Caffeine':(0, 400),
    'Fatty acids, total saturated':(0, (tdee/9)*(fat_percent/0.3)*.1),
    'Fatty acids, total monounsaturated':((tdee/9)*(fat_percent/0.3)*.15,(tdee/9)*(fat_percent/0.3)*.2),
    'Fatty acids, total polyunsaturated':((tdee/9)*(fat_percent/0.3)*.05,(tdee/9)*(fat_percent/0.3)*.1),
    'Fatty acids, total trans':(0,(tdee/9)*(fat_percent/0.3)*.01),
    'Cholesterol':(0, 300)
}