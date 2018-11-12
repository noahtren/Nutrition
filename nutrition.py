import requests
import json

url = "https://api.nal.usda.gov/usda/ndb"
key = open("key.txt").read()

recommended_amounts = {
    'Energy': (2600, 3400), #kcal
    'Total lipid (fat)': (70,120),#g
    'Water': (2500, 3500), #g
    'Protein':(120,200), #g
    'Carbohydrate, by difference':(350,450), #g
    'Fiber, total dietary': (30,45),#g
    'Sugars, total': (20,40),#g
    'Calcium, Ca':(1000,2500),
    'Iron, Fe':(8,45),
    'Potassium, K':(400,2000),
    'Sodium, Na':(1000,2300),
    'Magnesium, Mg':(300,750),
    'Phosphorus, P':(700,4000),
    'Zinc, Zn':(12,50),
    'Vitamin E (alpha-tocopherol)':(15,1000),
    'Vitamin K (phylloquinone)':(120,"none"),
    'Vitamin C, total ascorbic acid':(90,2000),
    'Thiamin':(1.2,"none"),
    'Riboflavin':(1.3,"none"),
    'Niacin':(16,35),
    'Vitamin B-6':(1.3,100),
    'Folate, DFE':(400,1000),
    'Vitamin A, RAE':(900,3000),
    'Vitamin A, IU':(900,10000),
    'Vitamin D (D2 + D3)':("none","none"),
    'Vitamin D':(1000,4000),
    'Vitamin B-12':(2.4,"none"),
    # non-vetted values
    'Selenium':(70,400), #ug
    'Copper':(0.9,10), #mg
    'Caffeine':(0, 400),
    'Fatty acids, total saturated':(0, 25),
    'Fatty acids, total monounsaturated':(25,50),
    'Fatty acids, total polyunsaturated':(12,25),
    'Fatty acids, total trans':(0,1),
    'Cholesterol':(0, 300)
}

class Results:
    def __init__(self, data):
        try:
            self.result = True
            result_json = data["list"]["item"]
            names = []
            ids = []
            for result in range(0, len(result_json)):
                names.append(result_json[result]["name"])
                ids.append(result_json[result]["ndbno"])
            self.names = names
            self.ids = ids
        except KeyError:
            self.result = False
    def Search_Info(self):
        if self.result:
            return_string = ""
            for i in range(0, len(self.names)):
                return_string = return_string + "{}: {}\n".format(self.names[i],self.ids[i])
            return return_string
        else:
            return "No results"
class Day:
    def __init__(self, meals):
        self.foods = []
        for meal in meals:
            for food in meal.Get_Foods():
                self.foods.append(food)
        self.meal = Meal(self.foods)
    def Display_Day(self):
        return self.meal.Meal_Info()
    def Get_Meal(self):
        return self.meal
class Meal:
    def __init__(self, foods):
        self.foods = foods
        # be able to return a list of grouped nutrients
        groups = []
        names = []
        grouped_names = []
        units = []
        tmp = False
        for food in self.foods:
            for group in food.Get_Groups():
                if (group not in groups) and (group != None):
                    groups.append(group)
                    grouped_names.append([])
            for nutrient_group in food.Get_Nutrients():
                for nutrient in nutrient_group:
                    if ((nutrient.get_name() not in names) and (nutrient.get_name() != None)):
                        names.append(nutrient.get_name())
                        units.append(nutrient.get_unit())
                    if (nutrient.get_name() != None):
                        if (units[names.index(nutrient.get_name())] != nutrient.get_unit()):
                            print("This is a problem")
                for group in groups:
                    for nutrient in nutrient_group:
                        if nutrient.get_group() == group:
                            if nutrient.get_name() not in grouped_names[groups.index(group)]:
                                grouped_names[groups.index(group)].append(nutrient.get_name())
        # we have a full list of all of the groups
        # now get a full list of all the nutrient names
        namevalues = [0] * len(names)
        for name in names: # calories, calcium, potassium, etc.
            for food in self.foods:
                for nutrient_group in food.Get_Nutrients():
                    for nutrient in nutrient_group:
                        if (nutrient.get_name() == name):
                            namevalues[names.index(name)] += nutrient.get_value()
        grouped_nutrients = []
        for group in grouped_names:
            grouped_nutrients.append([])
            for name in group:
                if (name != None):
                    grouped_nutrients[grouped_names.index(group)].append(Nutrient(name, group, namevalues[names.index(name)], units[names.index(name)], 100, "MEAL"))
        self.nutrients = grouped_nutrients
        self.groups = groups
    def Get_Grouped_Nutrients(self):
        return self.nutrients
    def Get_Groups(self):
        return self.groups
    def Get_Foods(self):
        return self.foods
    def Nutrient_Analysis(self, nutrient):
        # return top contributors to nutrient
        nutrients = []
        total_val = 0
        recommended_value = recommended_amounts[nutrient]
        for food in self.foods:
            for nutrient_group in food.Get_Nutrients():
                for nutrient in nutrient_group:
                    if (nutrient.get_name() == nutrient):
                        nutrients.append(nutrient)
                        total_val = total_val + nutrient.get_value()
        nutrients.sort(key=nutrient.get_value())
        return nutrients

    def Meal_Info(self):
        return_string = ""
        for group_num in range(0, len(self.nutrients)):
            return_string = return_string + "\n\n" + self.groups[group_num]
            for nutrient in self.nutrients[group_num]:
                return_string = return_string + "\n" + nutrient.Nutrient_Info()
        return return_string

class Food:
    def __init__(self, first, second=None, third=None): #first is data, second is grams
                                    # first is name, second is nutrient
        if second == None:
            self.nutrients = None
            self.name = None
            self.id = None
            self.grams = None
            self.groups = None
        elif third == None:
            nutrient_json = first["foods"][0]["food"]["nutrients"]
            groups = [] # proximates, lipids, etc
            grouped_nutrients = []
            self.name = first["foods"][0]["food"]["desc"]["name"]
            for nutrient in nutrient_json:
                if (float(nutrient["value"]) != 0):
                    if (nutrient["group"] not in groups):
                        groups.append(nutrient["group"])
                        grouped_nutrients.append([])
                        count = 0
                    grouped_nutrients[len(groups)-1].append(Nutrient(nutrient["name"], nutrient["group"], float(nutrient["value"]), nutrient["unit"], second, self.name))
                    count += 1
            self.nutrients = grouped_nutrients
            self.id = first["foods"][0]["food"]["desc"]["ndbno"]
            self.grams = second
            self.groups = groups
        else:
            self.name = first
            self.id = "User-assigned"
            groups = []
            self.nutrients = []
            self.nutrients.append([])
            for nutrient in second:
                groups.append(nutrient.get_group())
                self.nutrients[0].append(nutrient)
            self.groups = groups
            self.grams = "N/A"
    def Get_Groups(self):
        return self.groups
    def Get_Nutrients(self):
        return self.nutrients
    def Get_Name(self):
        return self.name
    def Food_Info(self):
        if self.grams == "N/A":
            return_string = "{}".format(self.name)
        else:
            return_string = "{} grams of {} ({})".format(self.grams, self.name, self.id)
        for group_num in range(0, len(self.nutrients)):
            return_string = return_string + "\n\n" + self.groups[group_num]
            for nutrient in self.nutrients[group_num]:
                return_string = return_string + "\n" + nutrient.Nutrient_Info()
        return return_string

class Nutrient:
    def __init__(self, name, group, value, unit, grams=None, my_food=None):
        self.name = name
        self.group = group
        self.unit = unit
        self.my_food = my_food
        self.rda_message = None
        if grams != None:
            self.value = round((value / 100) * grams, 3)
        else:
            self.value = value
        try:
            self.rda = recommended_amounts[name]
            tmp = True
            if (self.rda[1] != "none"):
                if (self.value > self.rda[1]):
                    tmp = False
                    self.rda_message = "Too much, recommended is less than {}{}".format(self.rda[1],self.unit)
            if (self.rda[0]!="none"):
                if (self.value < self.rda[0]):
                    tmp = False
                    self.rda_message = "Deficient, recommended is more than {}{}".format(self.rda[0],self.unit)
            if tmp:
                self.rda_message = "This is a healthy amount"
        except KeyError:
            self.rda = None
    def get_value(self):
        return self.value
    def get_name(self):
        return self.name
    def get_group(self):
        return self.group
    def get_unit(self):
        return self.unit
    def get_my_food(self):
        return self.my_food
    def Nutrient_Info(self):
        if self.rda != None:
            return "{}{} {}\n{}".format(str(self.value),str(self.unit),self.name,self.rda_message)
        else:
            return "{}{} {}".format(str(self.value),str(self.unit),self.name)

def get_food_data(food_id):
    params = dict(
        ndbno=str(food_id),
        type='b', 
        format='json', 
        api_key=key
    )
    response = requests.get(url=url + "/V2/reports", params=params).text
    return json.loads(response)

def search(name):
    params = dict(
        q=name,
        ds='Standard Reference',
        sort='r',
        max=10,
        format='json',
        api_key=key
    )
    response = requests.get(url=url + "/search", params=params).text
    return json.loads(response)

emptynutrient = Nutrient(None, None, None, None, None, None)
emptyfood = Food((emptynutrient, emptynutrient))