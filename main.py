from flask import Flask, request, jsonify
import requests
import ollama

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

    # Prompt for AI
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
        # Replace with your local AI model
        ai_response = ollama.run("mistral", prompt=prompt)

        if ai_response:
            return jsonify({"analys": ai_response})
        else:
            return jsonify({"error": "AI-svaret saknar innehåll."}), 500

    except requests.exceptions.RequestException as e:
        print(f"RequestException: {e}")
        return jsonify({"error": f"Kunde inte använda lokal AI: {str(e)}"}), 500

    except Exception as e:
        print(f"General Exception: {e}")
        return jsonify({"error": f"Kunde inte använda lokal AI: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
