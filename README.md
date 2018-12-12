# USDA Nutrition
Working with data from the [USDA Food Composition Database](https://ndb.nal.usda.gov/ndb/).
[End result](reports/report.html)

## The Data
The USDA provides a database and API with nutrient information of foods broken into two categories, Standard Reference (SR) and Branded Foods (BF). This program makes use of the Standard Reference dataset, allowing for relevant nutritional value of unprocessed foods and some generic processed foods. The motive of writing this program was to determine what an ideal day would look like for nutrition. This is done by computing the recommended daily amounts of different nutrients and comparing them with the amounts provided in different food choices throughout a day.

Each food item in the database is recognized by a 5-digit ID. These IDs can be found by searching the database online or by entering a string query into the search() function of nutrition.py. The data returned can be used to initlialize a Results object, which has the method Search_Info(), which returns a list of all relevant foods and their IDs. The code to do this can be found in search.py.

nutrition.py, contains various classes to make sense of the data from USDA at different levels of abstraction. The lowest level is Nutrient, then Food, then Meal, then Day. A Day object is composed of multiple Meal objects, a Meal object is composed of multiple Food objects, and a Food object is composed of multiple Nutrient objects. Food objects are initialized with the data returned when the USDA API is called with the corresponding ID.

## Computing Recommended Daily Amounts
Recommended daily amounts of macronutrients and the subcategories that make them up (carbs, proteins, and different types of fats) are computed by finding the basal metabolic rate (BMR) and total daily energy expenditure (TDEE) of the user. BMR is calculated based on the user's weight, age, height, and gender. TDEE is calculated by multiplying BMR by a coefficient dependent on one's activity levels. For this program, the coefficient is defined as (1 + hours of exercise * 0.55). This would mean that someone with a BMR of 1500 kcal and one hour of exercise each day would have a TDEE of 2325 kcal.

Micronutrients (minerals and vitamins) are based on the recommended intake ranges of an adult, which do not vary too much by gender.

## Building an Ideal Day
The code in main.py describes a nearly ideal day which meets all of the nutritional requirements in terms of macro and micronutrients. It makes use of a tkinter GUI through a class called Nutrition_Gui in nutrition_gui.py. The GUI compiles the net nutritional values of each nutrient in a given day and assigns each one to a square in a grid. The square is colored based on if that nutrient is deficient (yellow), sufficient (green), or in excess (red).
