from flask import Flask, render_template, request
import os
from time import time
from blockchain import BlockChain, Block
from conversion import getGasPrices

STATIC_DIR = os.path.abspath('static')

app = Flask(__name__, static_folder=STATIC_DIR)
app.use_static_for_root = True

chain = BlockChain()
currentBlock = None

@app.route("/", methods= ["GET", "POST"])
def home():
    global blockData, currentBlock, chain
     
    # get all gas prices 
    allPrices = getGasPrices()
    
    if request.method == "GET":
        # return allPrices as second parameter
        return render_template('index.html', allPrices = allPrices)
    else:
        sender = request.form.get("sender")
        receiver = request.form.get("receiver")
        artId = request.form.get("artId")
        amount = request.form.get("amount")
        mode = request.form.get("mode")

        # Calculate the gas/transaction fee prices/ get the mode from front end
        gasPrices, gweiPrices, etherPrices, dollarPrices = allPrices
        
        # Calculate gasPriceGwei, gasPriceEther, transactionFeeEther, transactionFeeDollar
        gasPriceGwei = gweiPrices[mode]
        gasPriceEther = etherPrices[mode]
        transactionFeeEther = etherPrices[mode] * 21000
        transactionFeeDollar = dollarPrices[mode] * 21000
        
        # Replace the values of gasPriceGwei, gasPriceEther, transactionFeeEther, transactionFeeDollar with newly calculated values
        transaction = { 
                "sender": sender, 
                "receiver": receiver, 
                "amount": amount,
                "artId": artId,            
                "gasPriceGwei" : gasPriceGwei,
                "gasPriceEther" : gasPriceEther, 
                "transactionFeeEther" : transactionFeeEther,
                "transactionFeeDollar" : transactionFeeDollar
            }  

        index = chain.length()
        if index==0:
            index = 1
        blockData = {
                'index': index,
                'timestamp': time(),
                'previousHash': "No Previous Hash.",
        }   
        
        if currentBlock == None:
            currentBlock = Block(
                            blockData["index"], 
                            blockData["timestamp"], 
                            blockData["previousHash"])
        
        status = currentBlock.addTransaction(transaction)
        
        if status == "Ready":
            chain.addBlock(currentBlock)   
            isValid = chain.validateBlock(currentBlock)
            currentBlock.isValid = isValid
            currentBlock = None
        
        chain.printChain()

    
    # return allPrices as third parameter  
    return render_template('index.html', blockChain = chain, allPrices = allPrices)


@app.route("/blockchain", methods= ["GET", "POST"])
def show():
    global chain, currentBlock

    currentBlockLength  = 0
    if currentBlock:
        currentBlockLength = len(currentBlock.transactions)
    
    return render_template('blockchain.html', blockChain = chain.chain, currentBlockLength = currentBlockLength)
    
if __name__ == '__main__':
    app.run(debug = True, port=4001)