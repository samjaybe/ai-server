from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route("/analysera", methods=["GET"])
def analysera():
    url = request.args.get("url")
    if not url:
        return jsonify({"error": "Ingen URL angiven"}), 400

    try:
        res = requests.get(url, timeout=10)
        html = res.text
    except Exception as e:
        return jsonify({"error": f"Kunde inte hämta sidan: {str(e)}"}), 500

    # Här sker "analysen" – just nu bara placeholder
    analys = f"Denna sida ({url}) innehåller {len(html)} tecken HTML."

    return jsonify({"analys": analys})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
