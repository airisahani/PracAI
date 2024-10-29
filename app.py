import os
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
from analyze import read_image

load_dotenv()

app = Flask(__name__, template_folder='templates')

endpoint = os.getenv("endpoint")
key = os.getenv("key")

@app.route("/")
def home():
    return render_template('index.html')


# API at /api/v1/analysis/ 
@app.route("/api/v1/analysis/", methods=['GET'])
def analysis():
    try:
        get_json = request.get_json()
        image_uri = get_json['uri']
    except:
        return jsonify({'error': 'Missing URI in JSON'}), 400
    
    try:
        res = read_image(image_uri)  # Call the modified read_image function
        
        # Check if the result is a string indicating an error
        if "error:" in res or "An error occurred" in res:
            return jsonify({'error': res}), 500  # Return the detailed error message
        
        response_data = {
            "text": res
        }
    
        return jsonify(response_data), 200
    except Exception as e:
        return jsonify({'error': 'Error in processing: {}'.format(str(e))}), 500



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000, debug=True)