import os
import matplotlib.font_manager as fm

fonts = [f.name for f in fm.fontManager.ttflist if 'Segoe' in f.name]
print("Segoe fonts found:", sorted(set(fonts)))
