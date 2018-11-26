from nutrition import *

# Create a result object based on a text search
broccoli_results = Results(search("broccoli"))
print(broccoli_results.Search_Info())
# Get the food object representing the first result
first = broccoli_results.Get_Result(0)
broccoli = Food(get_food_data(first),100)
# Show the info of the first result from a search
print(broccoli.Food_Info())
# you can also print broccoli.Food_Info(True) for an assessment of rda values