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
            "current": 'Not Available',
            "safe": 'Not Available',
            "average": 'Not Available',
            "fast": 'Not Available',
            "fastest": 'Not Available',
        }
        gweiPrices = gasPrices
        dollarPrices = gasPrices     
        etherPrices = gasPrices  
        dollarPrices = gasPrices
        allGasPrices = getGasPrices();  
        
        if allGasPrices: 
            gasPrices, gweiPrices, etherPrices, dollarPrices = allGasPrices
        

    return render_template('index.html', gasPrices = gasPrices, gweiPrices= gweiPrices, etherPrices= etherPrices, dollarPrices=dollarPrices)
    
if __name__ == '__main__':
    app.run(debug = True, port=4000)