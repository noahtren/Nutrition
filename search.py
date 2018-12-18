from nutrition import *

# Create a result object based on a text search
chocolate = Results(search("chocolate"))
print(chocolate.Search_Info())
# Get the food object representing the first result
chocolate = Food(access_database("19081"),100)
# That's a lot of chocolate!

# Show the info of the first result from a search
print(chocolate.Food_Info())
# you can also print chocolate.Food_Info(True) for an assessment of rda values