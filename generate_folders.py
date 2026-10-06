import json
import os
import re

with open("/Users/carloseduardomanceravelasquez/Documents/00 IAPLICACIONES/Redes/raw.txt", "r", encoding="utf-8") as f:
    text = f.read()

# Dividimos el texto por red social
sections = re.split(r'RED SOCIAL: (.*?)\n', text)

networks_data = {"WhatsApp": "", "Instagram": "", "TikTok": "", "Facebook": ""}

# Assign raw text to each network
current_net = None
for i in range(1, len(sections), 2):
    net_name = sections[i].split("(")[0].strip()
    if "WHATSAPP" in net_name:
        networks_data["WhatsApp"] = sections[i+1]
    elif "INSTAGRAM" in net_name:
        networks_data["Instagram"] = sections[i+1]
    elif "TIKTOK" in net_name:
        networks_data["TikTok"] = sections[i+1]
    elif "FACEBOOK" in net_name:
        networks_data["Facebook"] = sections[i+1]

# Parsing function for each network
def parse_network(raw_text, network_name):
    # Split by "Semana X"
    semanas = re.split(r'(Semana \d+ - [^\n]+)', raw_text)
    
    parsed = {}
    current_month = "Enero"
    
    # Extract the month before the first week
    if semanas:
        pre_text = semanas[0]
        month_match = re.findall(r'([A-Z]+):', pre_text)
        if month_match:
            current_month = month_match[-1].capitalize()
    
    for i in range(1, len(semanas), 2):
        header = semanas[i]
        content = semanas[i+1]
        
        sem_match = re.search(r'Semana (\d+)', header)
        if not sem_match:
            continue
        sem_num = int(sem_match.group(1))
        
        # Check if the content has a new month declaration for the NEXT weeks
        # We will assign the current month to this week, then check for month changes in its content
        parsed[sem_num] = {
            "mes": current_month,
            "contenido": header + "<br><br>" + content.strip().replace('\n', '<br><br>')
        }
        
        month_match = re.findall(r'([A-Z]+):', content)
        if month_match:
            # Filter out known non-month caps or just check against month list
            meses = ["ENERO", "FEBRERO", "MARZO", "ABRIL", "MAYO", "JUNIO", "JULIO", "AGOSTO", "SEPTIEMBRE", "OCTUBRE", "NOVIEMBRE", "DICIEMBRE"]
            for m in month_match:
                if m in meses:
                    current_month = m.capitalize()

    return parsed

data_wa = parse_network(networks_data["WhatsApp"], "WhatsApp")
data_ig = parse_network(networks_data["Instagram"], "Instagram")
data_tt = parse_network(networks_data["TikTok"], "TikTok")
data_fb = parse_network(networks_data["Facebook"], "Facebook")

# Combine all 52 weeks
plan_data = []

base_dir = "/Users/carloseduardomanceravelasquez/Documents/00 IAPLICACIONES/Redes/Material"
meses_es = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]

for w in range(1, 53):
    # Try to find the month from any network that has it
    mes = "Enero"
    if w in data_wa: mes = data_wa[w]["mes"]
    elif w in data_ig: mes = data_ig[w]["mes"]
    
    # Create folders
    for red in ["WhatsApp", "Instagram", "TikTok", "Facebook"]:
        os.makedirs(os.path.join(base_dir, mes, f"Semana_{w}", red), exist_ok=True)
    
    # Build JSON structure
    week_obj = {
        "semana": w,
        "mes": mes,
        "tema": "Contenido de la semana " + str(w),
        "fecha": "Semana " + str(w),
        "redes": []
    }
    
    # Add WhatsApp
    content_wa = data_wa[w]["contenido"] if w in data_wa else "Contenido pendiente"
    week_obj["redes"].append({
        "nombre": "WhatsApp",
        "dia": "Lunes",
        "color": "bg-green-100 border-green-500 text-green-900",
        "badge": "bg-green-500",
        "contenido": content_wa
    })
    
    # Add Instagram
    content_ig = data_ig[w]["contenido"] if w in data_ig else "Contenido pendiente"
    week_obj["redes"].append({
        "nombre": "Instagram",
        "dia": "Martes",
        "color": "bg-pink-100 border-pink-500 text-pink-900",
        "badge": "bg-gradient-to-r from-purple-500 to-pink-500",
        "contenido": content_ig
    })
    
    # Add TikTok
    content_tt = data_tt[w]["contenido"] if w in data_tt else "Contenido pendiente"
    week_obj["redes"].append({
        "nombre": "TikTok",
        "dia": "Miércoles",
        "color": "bg-gray-100 border-black text-gray-900",
        "badge": "bg-black",
        "contenido": content_tt
    })
    
    # Add Facebook
    content_fb = data_fb[w]["contenido"] if w in data_fb else "Contenido pendiente"
    week_obj["redes"].append({
        "nombre": "Facebook",
        "dia": "Jueves",
        "color": "bg-blue-100 border-blue-600 text-blue-900",
        "badge": "bg-blue-600",
        "contenido": content_fb
    })
    
    plan_data.append(week_obj)

# Write to data.js
js_content = "const planData = " + json.dumps(plan_data, indent=4, ensure_ascii=False) + ";"
with open("/Users/carloseduardomanceravelasquez/Documents/00 IAPLICACIONES/Redes/data.js", "w", encoding="utf-8") as f:
    f.write(js_content)

print("Todo procesado y guardado.")
