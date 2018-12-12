import json
import codecs
data = open("ideal_day.json", "r").read()
data = json.loads(data)
print(data["groups"])
for group in data["nutrients"]:
    print(group)

report = '''<!DOCTYPE html>
<html>

<head>
  <title>Nutrition Report</title>
  <script src="code.js"></script>
  <link rel="stylesheet" href="styles.css" type="text/css">
</head>

<body>'''

groupnames = data["groups"]
i = 0
for group in data["nutrients"]:
    k = 0
    if i % 2 == 0:
        if i > 0:
            report = report + "</div>"
        report = report + "<div class=\"page\">"
    report = report + "\n<div class=\"container\">"
    report = report + "\n   <div class=\"title\">{}</div>".format(groupnames[i])
    for nutrient in group:
        if k % 3 == 0:
            if k > 0:
                report = report + "</div>"
            report = report + "<div class=\"grid\">"
        status = ""
        if "healthy" in nutrient["message"].lower():
            status = "green"
        elif "deficient" in nutrient["message"].lower():
            status = "yellow"
        else:
            status = "red"
        report = report + '''\n       <div class=\"nutrient_{}\" id="parent"><b>{}</b><br />{} {}<br />{}</div>'''.format(status, 
        nutrient["name"].split("(")[0].strip(" ").replace("Fatty acids", "Fat"), nutrient["value"], 
        nutrient["unit"], nutrient["message"].replace("\n", "<br />"))
        k = k + 1 
    report = report + "</div></div>"
    i = i + 1

report = report + "</div></body></html>"
f = codecs.open("reports/report.html", "w", "utf-8")
f.write(report)