from flask import Flask, jsonify
import requests
import time
import threading

app = Flask(__name__)

# Shared data
last10_results = []
last_api_url = ""

# Background thread: hit API every 60 seconds
def fetch_api_loop():
    global last10_results, last_api_url
    while True:
        ts = int(time.time() * 1000)
        url = f'https://draw.ar-lottery01.com/WinGo/WinGo_1M/GetHistoryIssuePage.json?ts={ts}'
        headers = {
            'User-Agent': 'Mozilla/5.0',
            'Referer': 'https://draw.ar-lottery01.com/'
        }
        try:
            response = requests.get(url, headers=headers)
            data = response.json()
            last10_results[:] = data['data']['list'][:10]
            last_api_url = url
            print(f"✅ API hit: {url}")
            print(last10_results)
        except Exception as e:
            print(f"❌ Error hitting API {url}: {e}")
        time.sleep(60)

# Start background thread
threading.Thread(target=fetch_api_loop, daemon=True).start()

# API endpoint to get last 10 results
@app.route('/api/latest', methods=['GET'])
def latest_results():
    return jsonify({
        "api_url": last_api_url,
        "results": last10_results
    })

if __name__ == '__main__':
    print("🚀 Render webservice running on http://0.0.0.0:5000")
    app.run(host='0.0.0.0', port=5000)