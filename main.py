from flask import Flask, request, jsonify
import requests
import os
import traceback

app = Flask(__name__)

OLLAMA_URL = "https://packed-vampire-customize-outline.trycloudflare.com"

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

    prompt = f'''
    Du är en expert på exklusiv webbdesign och SEO för fastighetsmäklare. 
    En potentiell kund har en hemsida på följande URL: {url}
    Här är HTML-innehållet (trimmat): 
    {html[:6000]}

    Uppgiften:
    - Analysera hur lyxig och professionell sidan upplevs visuellt
    - Kommentera struktur, färgsättning, typsnitt, bildkvalitet och intryck
    - Bedöm innehållets styrka (copywriting, rubriker, språk)
    - Gör en SEO-granskning (struktur, laddtid, taggar, meta, mobilvänlighet)
    - Ge konkreta förbättringsförslag i punktform
    Skriv professionellt och vänligt.
    '''

    try:
        response = requests.post(
            f"{OLLAMA_URL}/api/chat",
            json={
                "model": "mistral",
                "messages": [{"role": "user", "content": prompt}],
                "stream": False
            },
            timeout=60
        )

        # Kontrollera statuskod och innehåll
        if not response.ok:
            return jsonify({"error": f"API-svar misslyckades: {response.status_code}"}), 500

        try:
            data = response.json()
        except Exception:
            return jsonify({"error": "Oväntat svar från AI:n, kunde inte tolkas."}), 500

        return jsonify({"analys": data.get("message", {}).get("content", "Inget innehåll i AI-svar.")})

    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": f"Kunde inte använda AI: {str(e)}"}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

@app.route('/')
def home():
    return "Welcome to the Flask app!"
