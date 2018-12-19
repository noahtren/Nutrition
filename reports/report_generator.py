import json
import codecs
import os

def Gen_Report():
    d = os.path.realpath(__file__)
    d = os.path.dirname(d)

    data = open("{}/ideal_day.json".format(d), "r").read()
    data = json.loads(data)

    report = '''<!DOCTYPE html>
    <html>

    <head>
    <title>Nutrition Report</title>
    <link rel="stylesheet" href="styles.css" type="text/css">
    </head>

    <body>'''

    groupnames = data["day"]["groups"]
    i = 0
    for group in data["day"]["nutrients"]:
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
            report = report + '''\n       <div class=\"nutrient_{}\" onclick=\"display_detail(this)\"><b>{}</b><br />{} {}<br />{}</div>'''.format(status, 
            nutrient["name"], nutrient["value"], 
            nutrient["unit"], nutrient["message"].replace("\n", "<br />"))
            k = k + 1 
        report = report + "</div></div>"
        i = i + 1

    report = report + "\n</div>"
    report = report + "<div class=\"json\" id=\"json\">{}</div>".format(json.dumps(data))
    report = report + "</body>    <script src=\"code.js\"></script></html>"
    f = codecs.open("{}/report.html".format(d), "w", "utf-8")
    f.write(report)