
from PyPDF2 import PdfReader
import json

reader = PdfReader("Dooper AI Bot JSON File.pdf")
text = ""
for p in reader.pages:
    text += p.extract_text() or ""

# Find the JSON substring manually or (if the PDF contains only JSON) parse:
start = text.find("{")
end = text.rfind("}")
json_text = text[start:end+1]
bot_flow = json.loads(json_text)

with open("dooper_bot.json", "w", encoding="utf-8") as f:
    json.dump(bot_flow, f, indent=2, ensure_ascii=False)
print("Saved dooper_bot.json")
