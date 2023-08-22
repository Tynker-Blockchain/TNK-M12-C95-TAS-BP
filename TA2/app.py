# SA2 Create a node for different Url paths

from flask import Flask, render_template, request
import os
from time import time
# Import node from Blockchain
from blockchain import BlockChain
from miner import Miner
from conversion import getGasPrices

STATIC_DIR = os.path.abspath('static')

app = Flask(__name__, static_folder=STATIC_DIR)
app.use_static_for_root = True

chain = BlockChain()
currentBlock = None
failedBlocks = []

miner1 = Miner('Miner 1')
miner2 = Miner('Miner 2')
miner3 = Miner('Miner 3')

chain.addMiner(miner1)
chain.addMiner(miner2)
chain.addMiner(miner3)

# Create dictionary of the nodes named allNodes


@app.route("/", methods= ["GET", "POST"])
def home():
    global currentBlock, chain, failedBlocks

    # Access allNodes as global 
    
    
    nodeId =request.args.get("node")

    if(nodeId == None or nodeId == ""):
        return render_template('badRequest.html')
     
    # Check if nodeId does not exits in allNodes, and then create new node
    




    #print current node
    

    allPrices = getGasPrices()
    
    if request.method == "GET":
        return render_template('index.html', allPrices = allPrices, nodeId = nodeId)
    else:
        sender = request.form.get("sender")
        receiver = request.form.get("receiver")
        artId = request.form.get("artId")
        amount = request.form.get("amount")
        mode = request.form.get("mode")

        gasPrices, gweiPrices, etherPrices, dollarPrices = allPrices
        
        gasPriceGwei = gweiPrices[mode]
        gasPriceEther = etherPrices[mode]
        transactionFeeEther = etherPrices[mode] * 21000
        transactionFeeDollar = dollarPrices[mode] * 21000
        
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

        chain.addToMiningPool(transaction)
   
    return render_template('index.html', blockChain = chain, allPrices = allPrices, nodeId = nodeId)


@app.route("/blockchain", methods= ["GET", "POST"])
def show():
    global chain, currentBlock, failedBlocks
    nodeId =request.args.get("node")

    currentBlockLength  = 0
    if currentBlock:
        currentBlockLength = len(currentBlock.transactions)
    
    return render_template('blockchain.html', blockChain = chain.chain, currentBlockLength = currentBlockLength, failedBlocks= failedBlocks, nodeId = nodeId)
    

@app.route("/miningPool", methods= ["GET", "POST"])
def miningPool():
    global chain
    nodeId =request.args.get("node")
    if request.method == "POST":
        minerAddress = request.form.get("miner")
        chain.minePendingTransactions(minerAddress)

    return render_template('miningPool.html', pendingTransactions = chain.pendingTransactions, miners = chain.miners, nodeId = nodeId)
    
if __name__ == '__main__':
    app.run(debug = True, port=4001)