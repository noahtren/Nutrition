// stores the status of nutrient_display node
var display_activity = ""
// parses hidden json on page to json object
var food_json = JSON.parse(document.getElementById('json').innerHTML)
var food_json = food_json["foods"]

// returns the top foods for a given nutrient
function top_foods(nutrient, amount) {
  var foods = []
  var value = 0
  for (var i = 0; i < food_json.length; i++) {
    var name = food_json[i]["name"]
    for (var j = 0; j < food_json[i]["nutrients"].length; j++) {
      if (food_json[i]["nutrients"][j]["name"] == nutrient) {
        var value = food_json[i]["nutrients"][j]["value"]
        var unit = food_json[i]["nutrients"][j]["unit"]
      }
    }
    if (value > 0) {
      var to_add = '{"name": "' + name + '", "value": ' + value + ', "unit": "' + unit + '"}'
      to_add = JSON.parse(to_add)
      foods.push(to_add)
    }
    value = 0
  }
  foods.sort(function (a, b) {
    return b.value - a.value;
  });
  if (amount < foods.length) {
    foods = foods.slice(0,amount)
  }
  return foods
}

// reveal nutrient_display at click site and populate it with top foods
function display_detail(nutrient) {
  if (display_activity != "") {
    var to_del = document.getElementById('display')
    to_del.parentNode.removeChild(to_del)
    display_activity = ""
  } 
  display_activity = nutrient.innerHTML
  var grid = nutrient.parentElement

  var nutrient_display = document.createElement('div')
  nutrient_display.className = "nutrient_display"
  nutrient_display.id = "display"

  let reg = "<b>(.*)<\/b>"
  nutrient_search = display_activity.match(reg)[1]
  console.log(nutrient_search)
  var results = top_foods(nutrient_search, 10)
  var display_string = ""
  console.log(results)
  console.log(display_activity)
  for (var food = 0; food < results.length; food++) {
    display_string += results[food].name + ": " + results[food].value + results[food].unit + "<br />"
  }
  nutrient_display.innerHTML = display_string

  grid.parentNode.insertBefore(nutrient_display, grid.nextSibling)
  setTimeout(function() {
    nutrient_display.className += ' in';;  
  }, 0);
}