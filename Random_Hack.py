from flask import Flask, render_template_string
import requests
import random
import time
import threading
import webbrowser

app = Flask(__name__)

# Game state ab history table bhi store karega
game_state = {
    "next_issue": "Loading...",
    "prediction": "Wait...",
    "sure_numbers": "Wait...",
    "history_table": []  # Pichle results yahan save honge
}

API_URL = "https://draw.ar-lottery01.com/WinGo/WinGo_1M/GetHistoryIssuePage.json"

def generate_prediction(history):
    best_size = random.choice(["BIG", "SMALL"])
    if len(history) >= 2:
        recent = history[:2]
        if recent[0] == recent[1]:
            best_size = recent[0]
        else:
            best_size = "SMALL" if recent[0] == "BIG" else "BIG"

    # MAIN FIX: random.sample() ka use kiya hai 2 numbers nikalne ke liye
    if best_size == "BIG":
        sure_numbers = random.sample([5, 6, 7, 8, 9], 2)
    else:
        sure_numbers = random.sample([0, 1, 2, 3, 4], 2)
        
    # Numbers ko sort kar diya taki sequence me dikhein (e.g., 6 - 8)
    sure_numbers.sort()
        
    return {"prediction": best_size, "sure_numbers": sure_numbers}

def run_bot():
    global game_state
    last_server_issue = None
    current_prediction = None

    while True:
        try:
            response = requests.get(API_URL, timeout=10)
            data = response.json()
            results = data["data"]["list"]

            if not results:
                time.sleep(2)
                continue

            latest = results[0]
            server_issue = latest["issueNumber"]

            if server_issue != last_server_issue:
                # Result Check Karna (Agar koi prediction pehle se thi)
                if current_prediction:
                    actual_num = int(latest["number"])
                    actual_size = "BIG" if actual_num >= 5 else "SMALL"
                    
                    predicted_size = current_prediction["prediction"]
                    sure_nums = current_prediction["sure_numbers"]

                    size_match = actual_size == predicted_size
                    number_match = actual_num in sure_nums

                    if size_match and number_match:
                        status = "🎉 JACKPOT"
                        color = "#ffeb3b" # Yellow
                    elif size_match or number_match:
                        status = "✅ WIN"
                        color = "#4caf50" # Green
                    else:
                        status = "❌ LOSS"
                        color = "#f44336" # Red

                    # History list mein data add karna
                    history_entry = {
                        "issue": current_prediction["issue"],
                        "prediction_text": f"{predicted_size} ({sure_nums[0]}-{sure_nums[1]})",
                        "result_text": f"{status} ({actual_size} {actual_num})",
                        "color": color
                    }
                    
                    # Naye result ko list ke top par add karein
                    game_state["history_table"].insert(0, history_entry)
                    
                    # Memory bachane ke liye sirf last 15 history rakhein
                    game_state["history_table"] = game_state["history_table"][:15]

                # Nayi History Generate Karna
                history = []
                for item in results:
                    history.append("BIG" if int(item["number"]) >= 5 else "SMALL")

                # Next Prediction Generate Karna
                result = generate_prediction(history)
                next_issue = str(int(server_issue) + 1)

                current_prediction = {
                    "issue": next_issue,
                    "prediction": result["prediction"],
                    "sure_numbers": result["sure_numbers"]
                }

                # Browser ke liye Current Prediction Update karna
                game_state["next_issue"] = next_issue
                game_state["prediction"] = result["prediction"]
                game_state["sure_numbers"] = f"{result['sure_numbers'][0]} - {result['sure_numbers'][1]}"

                last_server_issue = server_issue

            time.sleep(2)

        except Exception as e:
            # Agar koi error aayegi toh terminal pe dikhegi, loop rukega nahi
            print(f"ERROR: {e}")
            time.sleep(5)


# Flask HTML Page jisme Jinja2 templating use hui hai table banane ke liye
HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>ADARSH VIP HACK</title>
    <meta http-equiv="refresh" content="2">
    <style>
        body { 
            background-color: #0d0d0d; 
            color: #ffffff; 
            font-family: 'Courier New', Courier, monospace; 
            text-align: center; 
            margin-top: 30px; 
        }
        .container { 
            border: 2px solid #00ffff; 
            padding: 20px; 
            width: 80%; 
            margin: auto; 
            box-shadow: 0 0 20px #00ffff; 
            border-radius: 10px;
            background: #1a1a1a;
        }
        h1 { color: #00ffff; letter-spacing: 2px; text-shadow: 0 0 10px #00ffff;}
        
        /* Current Prediction Section */
        .current-prediction {
            background: rgba(0, 255, 255, 0.1);
            border: 1px dashed #00ffff;
            padding: 20px;
            border-radius: 8px;
            margin: 20px 0;
        }
        .current-prediction h2 { margin: 10px 0; font-size: 28px; }
        .highlight { color: #00ffff; font-weight: bold; font-size: 32px; }

        /* History Table Section */
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 30px;
        }
        th, td {
            border: 1px solid #333;
            padding: 15px;
            text-align: center;
            font-size: 18px;
        }
        th {
            background-color: #00ffff;
            color: #000;
            font-weight: bold;
            font-size: 20px;
        }
        tr:nth-child(even) { background-color: #111; }
        tr:nth-child(odd) { background-color: #222; }
        
        .no-data { padding: 20px; color: #888; font-style: italic; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔥 ADARSH VIP HACK 🔥</h1>
        
        <div class="current-prediction">
            <h2>NEXT ISSUE : <span class="highlight">{{ data.next_issue }}</span></h2>
            <h2>PREDICTION : <span class="highlight">{{ data.prediction }}</span></h2>
            <h2>SURE NUMS  : <span class="highlight">{{ data.sure_numbers }}</span></h2>
        </div>
        
        <table>
            <thead>
                <tr>
                    <th>Period Number</th>
                    <th>Prediction</th>
                    <th>Result</th>
                </tr>
            </thead>
            <tbody>
                {% if data.history_table %}
                    {% for row in data.history_table %}
                    <tr>
                        <td>{{ row.issue }}</td>
                        <td>{{ row.prediction_text }}</td>
                        <td style="color: {{ row.color }}; font-weight: bold;">{{ row.result_text }}</td>
                    </tr>
                    {% endfor %}
                {% else %}
                    <tr>
                        <td colspan="3" class="no-data">Waiting for first result...</td>
                    </tr>
                {% endif %}
            </tbody>
        </table>

    </div>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML_PAGE, data=game_state)

if __name__ == "__main__":
    threading.Thread(target=run_bot, daemon=True).start()
    print("Engine Started. Opening browser...")
    webbrowser.open("http://127.0.0.1:5000")
    
    import logging
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)
    app.run(port=5000, debug=False, use_reloader=False)