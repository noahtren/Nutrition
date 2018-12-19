var display_activity = ""
var food_json = JSON.parse(document.getElementById('json').innerHTML)
var food_json = food_json["foods"]

console.log(top_foods("Water"))

function top_foods(nutrient) {
  var foods = []
  for (var i = 0; i < food_json.length; i++) {
    var name = food_json[i]["name"]
    for (var j = 0; j < food_json[i]["nutrients"].length; j++) {
      if (food_json[i]["nutrients"][j]["name"] == nutrient) {
        var value = food_json[i]["nutrients"][j]["value"]
        break
      }
    }
    console.log(value)
    var to_add = '{"name": "' + name + '", "value": ' + value + '}'
    to_add = JSON.parse(to_add)
    foods.push(to_add)
  }
  foods.sort(function(a, b) {
    return a.value > b.value;
  });
  foods.sort();
  return foods
}

function display_detail(nutrient) {
  if (display_activity != "") {
    var to_del = document.getElementById('display')
    to_del.parentNode.removeChild(to_del)
    display_activity = ""
  } 
  grid = nutrient.parentElement
  display_activity = nutrient.innerHTML

  var nutrient_display = document.createElement('div')
  nutrient_display.className = "nutrient_display"
  nutrient_display.id = "display"
  nutrient_display.innerHTML = display_activity
  grid.parentNode.insertBefore(nutrient_display, grid.nextSibling)
  setTimeout(function() {
    nutrient_display.className += ' in';;  
  }, 0);
}