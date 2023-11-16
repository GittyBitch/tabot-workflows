import json

filename = ".github/classroom/autograding.json"
readme = "Readme.md"


def write_intro(file, title, content):
    if content is not None:
        file.write(f"# {title}\n")
        file.write(f"{content}\n")
    
def write_horizontal_line(file):
    file.write(f"\n---\n")


if __name__ == "__main__":
    with open(filename, 'r', encoding="utf-8") as autograding_file:
        data = json.load(autograding_file)
    
    with open(readme, 'w', encoding="utf-8") as readme_file:
        repo = data.get("repo")
        introduction = ""
        maxTestIndex = data.get("maxTestIndex", 0)
        if repo != None or repo != False:
            statusURL = f"https://github.com/{repo}/actions/workflows/classroom.yml"
            introduction = f"[![GitHub Classroom Workflow]({statusURL}/badge.svg)]({statusURL}) [![Points badge](../../blob/badges/.github/badges/points.svg)](../../actions) \n\n" # FIXME: Der Link stimmt nicht mehr so ganz ...
            
        textIntro = data.get("introduction")
        introduction += textIntro
        total_points = 0
        for p in data.get("tests"):
            total_points += int(p.get("points",0))
        logo_url = data.get("logo_url")
        timeframe = data.get("timeframe", "30 Minuten")
        
        if logo_url is not None:
            readme_file.write(f"<img src=\"{logo_url}\" alt=\"Assignment Logo\" width=\"300\"/>\n")
            write_horizontal_line(readme_file)
        
        if introduction is not None:
            write_intro(readme_file, "Aufgabe", introduction)
            readme_file.write(f"* {total_points} Punkte\n* {timeframe}\n")
            write_horizontal_line(readme_file)
            hint =  "<span style='color:red;'>"

            assignmentType=data.get("type","individual")
            if (assignmentType == "group"):
                hint += ("<b>INFO</b>: Bei dieser Aufgabe handelt es sich um eine Gruppenaufgabe, Ihr solltet "
                        "also miteinander zusammen arbeiten und Euch die Arbeit dabei sinnvoll aufteilen."
                        " Denkt daran, git fetch/pull bzw. pull --rebase zu benutzen falls Ihr gleichzeitig"
                        " Veränderungen an denselben Dateien vornehmt, um merge-Konflikte zu reduzieren!<br/>")
            hint += "<b>WICHTIG</b>: Committet/Pusht eure Lösung bitte nicht in den .github-Ordner.<br/> "
            hint += "<b>ACHTUNG</b>: Die Badges unten werden nicht genauso schnell aktualisiert wie die Pipeline (Actions)<br/>" 
            hint += "<b>Tipp</b>: Der TA-Bot kann Euch am Besten helfen, wenn Ihr regelmäßige kleine Commits pusht-um einen Blick auf Euren Stand zu pushen (es ist völlig normal, alle 5 Minuten zu pushen).<br/>"
            hint += "Für Übersetzungen der Aufgabe in eine andere Sprache: https://translate.google.de <br/>"
            hint += "</span>"
            readme_file.write(f"<p>{hint} </p>\n")
            write_horizontal_line(readme_file)
        readme_file.write(f"<ol>\n")
        tests = data.get("tests")
        if int(maxTestIndex) > 0:
            tests = tests[:int(maxTestIndex)]
            print("Slicing tests", tests)
        counter = 1
        for test in tests:
            have_specs = test.get("specs")
            points = test.get("points")
            title = have_specs.get("title")
            statusURL=f"[![Test Status](../../blob/badges/.github/badges/testStatus_{counter}.svg)](../../actions)"
            readme_file.write(f"\n{statusURL}  \n")
            readme_file.write(f"<li> {title} ({points} Punkte)</li>\n")
            counter += 1
            
                
            if "list" in have_specs:
                for l in have_specs["list"]:
                    readme_file.write(f"<ul><li> {l}</li></ul>\n") 
                    
            if "code-example" in have_specs:
                readme_file.write(f"Code-Beispiel: \n")
                readme_file.write(f"<ul><li><code>{have_specs.get('code-example')}</code></li></ul>\n")
            
            if "urls" in test:
                readme_file.write(f"Hilfe: \n")
                for spickzettel in test["urls"]:
                    #readme_file.write(f"<ul><li>[Spickzettel]({spickzettel})</li></ul> \n")
                    readme_file.write(f"<ul><li><a href=\"{spickzettel}\">Spickzettel</a></li></ul> \n")

            write_horizontal_line(readme_file)
        readme_file.write(f"</ol>\n")
                
                
    readme_file.close()
    autograding_file.close()
