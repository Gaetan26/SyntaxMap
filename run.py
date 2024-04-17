from syntaxmap import SyntaxMap


codes = """
let a = "Hello, World!"
const b = "Today"
if (a === b){
    console.log("Matching!")
}
"""


syntax_map = SyntaxMap(codes=codes)
languages = syntax_map.find()

win_name, win_score = str(), int()
for lg in list(languages.keys()):
    if languages[lg] > win_score:
        win_name = lg
        win_score = languages[lg]

print(f"This is {win_name.capitalize()} on {win_score*100}%")