import requests
import json
import operator
import os
import settings
from profile import recommended_amounts, units, name_filter, name_replace, encapsulators

local_usda_foods = []
url = "https://api.nal.usda.gov/usda/ndb"
try:
    api_key = open("key.txt").read()
except FileNotFoundError:
    print("key.txt not found in working directory! Please obtain a key from https://ndb.nal.usda.gov")
    exit()

'''
Day to Nutrient Hierarchy:
>> Days contain meals
    >> Meals contain foods
        >> Foods contain nutrients
A food object can be used for full analysis of nutrition. A meal is a bunch of foods combined
in context of the recommended daily amounts of a given profile
'''
class Day:
    def __init__(self, meals):
        self.foods = []
        for meal in meals:
            for food in meal.foods:
                self.foods.append(food)
        self.meal = Meal(self.foods)
    def Display_Day(self):
        return self.meal.Meal_Info(True)
class Meal:
    def __init__(self, foods):
        # be able to return a list of grouped nutrients
        # a meal's nutrients are the sum of its food's nutrients
        groups = []
        grouped_names = []
        grouped_values = []
        i = -1
        keys = recommended_amounts.keys()
        for key in keys:
            if type(recommended_amounts[key]) == str:
                groups.append(key)
                grouped_values.append([])
                grouped_names.append([])
                i += 1
            else:
                grouped_names[i].append(key)
                grouped_values[i].append(0)
        for f in foods:
            g_num = 0
            for g in f.nutrients:
                while g[0].group != groups[g_num]:
                    g_num += 1
                n_num = 0
                for n in g:
                    found_one = True
                    while n.name != grouped_names[g_num][n_num]:
                        if n_num == len(grouped_names[g_num])-1:
                            found_one = False
                            break
                        else:
                            n_num += 1
                    if found_one:
                        grouped_values[g_num][n_num] += n.value
                        n_num += 1
                g_num += 1
        grouped_nutrients = []
        for g_num in range(0, len(grouped_names)):
            grouped_nutrients.append([])
            for n_num in range(0, len(grouped_names[g_num])):
                grouped_nutrients[g_num].append(Nutrient(grouped_names[g_num][n_num],
                                                    groups[g_num], round(grouped_values[g_num][n_num],3),
                                                    units[g_num][n_num]))

        # all finished! The list of foods has been turned into a master list of each nutrient
        self.foods = foods
        self.nutrients = grouped_nutrients
        self.groups = groups
    def Export(self, filepath):
        export_file = open("{}.json".format(filepath), "w")
        day_nutrients = []
        for nutrient_group in self.nutrients:
            day_nutrients.append([])
            for nutrient in nutrient_group:
                day_nutrients[self.nutrients.index(nutrient_group)].append(nutrient.Dict(True))
        day_data = dict(groups=self.groups, nutrients=day_nutrients)
        foods = []
        for food in self.foods:
            foods.append(food.Dict())
        data = dict(day=day_data, foods=foods)
        json.dump(data, export_file)
    def Nutrient_Analysis(self, nutrient_name):
        # This is used to tell the top foods that contribute to certain nutrients
        # This is returned in a sorted list of nutrient objects, which contain their
        # component foods
        nutrients = []
        total_val = 0
        for food in self.foods:
            for nutrient_group in food.nutrients:
                for nutrient in nutrient_group:
                    if (nutrient.name == nutrient_name):
                        nutrients.append(nutrient)
                        total_val = total_val + nutrient.value
        nutrients.sort(key=operator.attrgetter('value'), reverse=True)
        return (nutrients, total_val)

    def Meal_Info(self, display_rda=False):
        return_string = ""
        for group_num in range(0, len(self.nutrients)):
            return_string = return_string + "\n\n" + self.groups[group_num]
            for nutrient in self.nutrients[group_num]:
                return_string = return_string + "\n" + nutrient.Info(display_rda)
        return return_string

class Food:
    def __init__(self, first, second): 
        '''
        Python does not support polymorphic constructors like C++ does
        The workaround here is to take two arbitrary parameters
        A Food object can be constructed with data from the database, or from hardcoded nutrients
        >> For data from the database:
            first is data, second is grams
        >> For hardcoded nutrients (see ideal_day.yaml)
            first is name, second is list of nutrients
        '''
        if type(second) is int or type(second) is float:
            nutrient_json = first["nutrients"]
            # parse the json nutrient file to only tracked nutrients
            # in this case, the tracked nutrients are from the recommended amount dict
            to_del = []
            for n in nutrient_json:
                if n["name"] not in recommended_amounts.keys():
                    print("I actually did sometihng")
                    to_del.append(nutrient_json.index(n))
            # this algorithm will never take too much time because a list of nutrients
            # will never be greater than ~150
            for i in to_del:
                del nutrient_json[i]
                for j in to_del:
                    if i < j:
                        to_del[to_del.index(j)] -= 1
            groups = [] # proximates, lipids, etc
            grouped_nutrients = []
            self.name = first["desc"]["name"]
            for nutrient in nutrient_json:
                if (nutrient["group"] not in groups):
                    groups.append(nutrient["group"])
                    grouped_nutrients.append([])
                    count = 0
                grouped_nutrients[len(groups)-1].append(Nutrient(nutrient["name"], nutrient["group"], float(nutrient["value"]), nutrient["unit"], second, self.name))
                count += 1
            self.nutrients = grouped_nutrients
            self.id = first["desc"]["ndbno"]
            self.grams = second
            self.groups = groups
        else:
            self.name = first
            self.id = "User-assigned"
            groups = []
            self.nutrients = []
            for nutrient in second:
                if nutrient.group not in groups:
                    groups.append(nutrient.group)
                    self.nutrients.append([])
                nutrient.food = self.name
                self.nutrients[groups.index(nutrient.group)].append(nutrient)
            # these may need to be sorted here, or sorted when procedurally generated in the ideal day json file
            self.groups = groups
            self.grams = "N/A"
    def Food_Info(self, rda=False):
        if self.grams == "N/A":
            return_string = "{}".format(self.name)
        else:
            return_string = "{} grams of {} ({})".format(self.grams, self.name, self.id)
        for group_num in range(0, len(self.nutrients)):
            return_string = return_string + "\n\n" + self.groups[group_num]
            for nutrient in self.nutrients[group_num]:
                return_string = return_string + "\n" + nutrient.Info(rda)
        return return_string
    def Dict(self):
        n = []
        for ng in self.nutrients:
            for nutrient in ng:
                n.append(nutrient.Dict(False))
        return_dict = dict(
            name=self.name,
            nutrients=n)
        return return_dict

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
            self.rda = list(recommended_amounts[name])
            try:
                self.rda[0] = round(self.rda[0],2)
            except TypeError:
                pass
            try:
                self.rda[1] = round(self.rda[1],2)
            except TypeError:
                pass
            tmp = True
            if (self.rda[1] != "none"):
                if (self.value > self.rda[1]):
                    tmp = False
                    self.rda_message = "Too much\nGoal < {}{}".format(self.rda[1],self.unit)
            if (self.rda[0]!="none"):
                if (self.value < self.rda[0]):
                    tmp = False
                    self.rda_message = "Deficient\nGoal > {}{}".format(self.rda[0],self.unit)
            if tmp:
                self.rda_message = "Healthy amount"
        except KeyError:
            self.rda = None
    def Dict(self, display_rda):
        if display_rda:
            return_dict = dict(
                name=self.name,
                value=self.value,
                unit=self.unit,
                message=self.rda_message
            )
        else:
            return_dict = dict(
                name=self.name,
                value=self.value,
                unit=self.unit,
            )
        return return_dict
    def Info(self, display_rda):
        if (self.rda != None) and display_rda:
            return "{}\n{}{}\n{}".format(self.name,str(self.value),self.unit,self.rda_message)
        else:
            return "{}\n{}{}".format(self.name,str(self.value),self.unit)
'''
Working with the USDA database API
'''
# Returning results as received from an API call 
class Results:
    def __init__(self, data, flav=False):
        if not flav:
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

def access_database(food_id):
    # check local storage
    if len(local_usda_foods) == 0:
        scan_files()
    if food_id in local_usda_foods:
        # file stored locally, get it quickly
        response = open("usda_foods/{}.json".format(food_id), "r").read()
        food_json = json.loads(response)
    else:
        # file not stored locally, get it from API and clean it up
        params = dict(
            ndbno=str(food_id),
            type='f', 
            format='json', 
            api_key=api_key
        )
        response = requests.get(url=url + "/V2/reports", params=params).text
        data_json = json.loads(response)
        data_json = data_json["foods"][0]["food"]
        # remove extra information that isn't needed
        del data_json["sr"]; del data_json["type"]; del data_json["footnotes"]
        del data_json["sources"]; del data_json["langual"]
        desc = data_json["desc"]
        # remove lengthy parentheses around food names
        if "(" in desc["name"]:
            desc["name"] = desc["name"][:desc["name"].find("(")-1]
        extraneous_describers = ["sd", "sn", "cn", "manu", "nf", "cf", "ff", "pf", "r", "rd", "ds",
                                 "ru"]
        for describer in extraneous_describers:
            if describer in desc:
                del desc[describer]
        to_del = []
        encap_names = []; encap_targets = []; encap_values = []
        for encap in encapsulators.keys():
            encap_targets.append(encap)
            encap_values.append(0)
            for name in encapsulators[encap]["includes"]:
                encap_names.append(name)
        # continue making changes to the data to fit with the system
        for n in data_json["nutrients"]:
            if n["unit"] == "µg":
                n["unit"] = "ug"
            if n["name"] in name_filter:
                try:
                    n["name"] = name_replace[name_filter.index(n["name"])]
                except IndexError:
                    print("There was an error filtering {}".format(n["name"]))
                    exit()
            if n["name"] == "Calories" and n["unit"] == "kJ":
                to_del.append(data_json["nutrients"].index(n))
            if n["group"] == "Lipids":
                n["group"] = "Fats"
            del n["measures"]; del n["derivation"]; del n["nutrient_id"]
            del n["sourcecode"]; del n["dp"]; del n["se"]
            if n["name"] in encap_names:
                for target in encap_targets:
                    if n["name"] in encapsulators[target]["includes"]:
                        encap_values[encap_targets.index(target)] += n["value"]
                        print("Added {} to {} for a total of {}".format(n["value"], target, encap_values[encap_targets.index(target)]))
                        # we found the target of this nutrient, so add it
        for encap_idx in range(0, len(encap_targets)):
            name = encap_targets[encap_idx]
            data_json["nutrients"].append(dict(
                name=name,
                group=encapsulators[name]["group"],
                unit=encapsulators[name]["unit"],
                value=encap_values[encap_idx]
            ))
        for i in to_del:
            del data_json["nutrients"][i]
            for j in to_del:
                if i < j:
                    to_del[to_del.index(j)] -= 1
        # now, sort the nutrients according to how they should appear in a standard food
        ordered_names = []
        keys = recommended_amounts.keys()
        for key in keys:
            if type(recommended_amounts[key]) != str:
                ordered_names.append(key)
        nutrients = []
        for i in range(0, len(ordered_names)):
            contains = False
            for n in data_json["nutrients"]:
                if n["name"] == ordered_names[i]:
                    nutrients.append(n)
                    contains = True
        food_json = dict(
                         desc=desc,
                         nutrients=nutrients
        )
        open("usda_foods/{}.json".format(food_id), "w").write(json.dumps(food_json))
    return food_json

def search(name):
    params = dict(
        q=name,
        ds='Standard Reference',
        sort='r',
        max=20,
        format='json',
        api_key=api_key
    )
    response = requests.get(url=url + "/search", params=params).text
    usda_data = json.loads(response)
    return usda_data

def scan_files():
# Update list of files that are in local storage
    cwd = os.getcwd()
    for f in os.scandir(cwd+"/"+settings.usda_food_path):
        local_usda_foods.append(str(f.name).split(".")[0])