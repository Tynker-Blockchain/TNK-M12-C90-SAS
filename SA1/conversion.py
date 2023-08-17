# import Web3 library
from web3 import Web3

# Reference Link : https://web3py.readthedocs.io/en/stable/web3.eth.html

# Set above link as API_URL variable
API_URL = 'https://mainnet.infura.io/v3/cded6e6690d04259b05137dd10b170c3'
# Use Web3 and pass it Web3.HTTPProvide() with API_URL and get response back in web3 variable
web3 =  Web3( Web3.HTTPProvider(API_URL))

def getGasPrices():
    try:
        # Create an empty dict gasPrices
        gasPrices={}

        # Retrieve the gas prices from the network and store in key "current"
        gasPrices["current"] = web3.eth.gas_price

        # Calculate gas prices at different levels
        gasPrices["slow"] = int(gasPrices["current"] * 0.9)  # 90% of the current gas price
        gasPrices["standard"] = int(gasPrices["current"] * 1.0)   # Same as the current gas price
        gasPrices["fast"] = int(gasPrices["current"] * 1.1)      # 110% of the current gas price
        gasPrices["rapid"] = int(gasPrices["current"] * 1.2)   # 120% of the current gas price
        
        # Return the gas prices
        return gasPrices

    except Exception as e:
        print(f"Error: {e}")
        return None
