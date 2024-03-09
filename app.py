from flask import Flask, render_template, request, jsonify
from flask_cors import CORS, cross_origin
import requests
from bs4 import BeautifulSoup as bs
import os

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def homepage():
    return render_template('index.html')

@app.route("/review", methods=['POST'])
def review():
    try:
        if request.method == 'POST':
            query = request.form['content'].replace(" ", "")
            saveDir = "static/images/"
            
            if not os.path.exists(saveDir):
                os.makedirs(saveDir)
                
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"}
            
            response = requests.get(f"https://www.google.com/search?q={query}&tbm=isch", headers=headers)
            soup = bs(response.text, 'html.parser')
            images = soup.find_all('img')
            del images[0] 

            image_filenames = [] 

            for index, image in enumerate(images):
                imageUrl = image['src']
                imageData = requests.get(imageUrl).content
                filename = f"{query}_{index}.jpg"
                
                with open(os.path.join(saveDir, filename), "wb") as f:
                    f.write(imageData)
                
                image_filenames.append(filename)

            return render_template('result.html', image_filenames=image_filenames)
    except Exception as e:
        print(e)
        return "Something went wrong"

    return render_template('index.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000, debug=True)
