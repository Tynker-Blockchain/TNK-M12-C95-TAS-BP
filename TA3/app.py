from flask import Flask, render_template, request
import os
from time import time
from blockchain import BlockChain, Miner, Node
from conversion import getGasPrices

STATIC_DIR = os.path.abspath('static')

app = Flask(__name__, static_folder=STATIC_DIR)
app.use_static_for_root = True

allNodes = {}

@app.route("/", methods= ["GET", "POST"])
def home():
    global blockData, currentBlock, chain, failedBlocks

    global allNodes
    nodeId =request.args.get("node")

    if(nodeId == None or nodeId == ""):
        return render_template('badRequest.html')
    
    if(nodeId not in allNodes):
        node = Node(nodeId)
        miner1 = Miner('Miner 1')
        miner2 = Miner('Miner 2')
        miner3 = Miner('Miner 3')

        node.blockchain.addMiner(miner1)
        node.blockchain.addMiner(miner2)
        node.blockchain.addMiner(miner3)
        
        allNodes[nodeId] = node
    
    currentNode = allNodes[nodeId]
     
    allPrices = getGasPrices()
    
    # Get chain, currentBlock, failedBlocks from currentNode
    

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
    global chain, currentBlock, failedBlocks, allNodes

    # get nodeId from the request data
    
    # Check if nodeId is valid
    
            
    # set currentNode and chain variables        
    
    #####

    currentBlockLength  = 0
    if currentBlock:
        currentBlockLength = len(currentBlock.transactions)
            
    return render_template('blockchain.html', blockChain = chain.chain, currentBlockLength = currentBlockLength, failedBlocks= failedBlocks, nodeId = nodeId)
    

@app.route("/miningPool", methods= ["GET", "POST"])
def miningPool():
    global chain, allNodes
    # get nodeId from the request data
    
    # Check if nodeId is valid
            
    # Set currentNode and chain variables
    
    #####
    
    if request.method == "POST":
        minerAddress = request.form.get("miner")
        chain.minePendingTransactions(minerAddress)
        
    return render_template('miningPool.html', pendingTransactions = chain.pendingTransactions, miners = chain.miners, nodeId = nodeId)
    
if __name__ == '__main__':
    app.run(debug = True, port=4001)