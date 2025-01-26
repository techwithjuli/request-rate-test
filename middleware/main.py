from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/categorize', methods=['POST'])
def categorize():
    data = request.get_json()
    input_text = data.get("inputText", "").lower()

    # Einfache Regel: enth. "error" => Kategorie "Error", sonst "General"
    if "error" in input_text:
        category = "Error"
    else:
        category = "General"

    return jsonify({"category": category}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6000, debug=True, use_reloader=False)