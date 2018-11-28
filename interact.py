from web3 import Web3
import contract_abi

contract_address = "0x67cAa55428e815156Fc5DcAcfCfCcCC9FE25Bc6d"
wallet_private_key = ""
wallet_address = ""

w3 = Web3(Web3.HTTPProvider("https://rinkeby.infura.io/v3/d5d170b1230544e298b51d49ea8180d5"))

w3.eth.enable_unaudited_features()

contract = w3.eth.contract(address=contract_address, abi=contract_abi.abi)
nonce = w3.eth.getTransactionCount(wallet_address)

def deploy_contract():
    pass

def enter_lottery():
    nonce = w3.eth.getTransactionCount(wallet_address)
    txn_dict = contract.functions.enter().buildTransaction({
        'chainId': 4,
        'value' : w3.toWei('0.1','ether'),
        'gas': 100000,
        'gasPrice': w3.toWei('2','gwei'),
        'nonce': nonce,
    })
    
    signed_txn = w3.eth.account.signTransaction(txn_dict, private_key=wallet_private_key)

    result = w3.eth.sendRawTransaction(signed_txn.rawTransaction)

    tx_receipt = w3.eth.waitForTransactionReceipt(result)

    if tx_receipt is None:
        return {'status': 'failed', 'error': 'timeout'}

    return {'status': 'entered'}

def pick_winner():
    nonce = w3.eth.getTransactionCount(wallet_address)
    txn_dict = contract.functions.pickWinner().buildTransaction({
        'chainId': 4,
        'gas': 100000,
        'gasPrice': w3.toWei('2','gwei'),
        'nonce': nonce,
    })
    
    signed_txn = w3.eth.account.signTransaction(txn_dict, private_key=wallet_private_key)

    result = w3.eth.sendRawTransaction(signed_txn.rawTransaction)

    tx_receipt = w3.eth.waitForTransactionReceipt(result)

    if tx_receipt is None:
        return {'status': 'failed', 'error': 'timeout'}

    return {'status': 'winner picked'}

def get_state():
    players = contract.functions.getPlayers().call()
    manager = contract.functions.manager().call()
    balance = w3.fromWei(w3.eth.getBalance(contract_address),'ether')
    return "This contract is managed by {0}. There are currently {1} people entered, competing to win {2} ether".format(manager,len(players),balance)


if __name__ == "__main__":
    print("Entering a player into the lottery...")
    enter_lottery()
    print(get_state())
    print("Going to pick a winner now...")
    pick_winner()
    print(get_state())
    print(contract.functions.getPlayers().call())