import sys, os
sys.path.insert(0, r"C:\Users\Kenny\.gemini\antigravity-ide\scratch\school_football_prediction")
import app.server as s
print("Server imported cleanly! App name:", s.app.name)
print("Available endpoints:")
for rule in s.app.url_map.iter_rules():
    print(" ", rule.rule, "->", rule.endpoint)

