from flask import Flask, render_template, request
import os
from conversion import getGasPrices

STATIC_DIR = os.path.abspath('static')

app = Flask(__name__, static_folder=STATIC_DIR)
app.use_static_for_root = True

@app.route("/", methods= ["GET", "POST"])
def home():
    global blockData, encryptedData
    
    if request.method == "GET":
        gasPrices= {
            "slow": 'Not Available',
            "standard": 'Not Available',
            "fast": 'Not Available',
            "rapid": 'Not Available',
        }
        allGasPrices = getGasPrices();  
        
        if allGasPrices: 
            gasPrices = allGasPrices
        

    return render_template('index.html', gasPrices = gasPrices)
    
if __name__ == '__main__':
    app.run(debug = True, port=4000)