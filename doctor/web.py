import codecs
from web3 import Web3
from solcx import compile_standard, install_solc
from web3 import Web3
from web3.middleware import geth_poa_middleware
install_solc("0.8.17")

# Connect to Ganache
ganache_url = "http://localhost:7545"
web3 = Web3(Web3.HTTPProvider(ganache_url))

if web3.is_connected():
    client_version = web3.client_version
    print("Connected to Ganache!", client_version)
else:
    print("Failed to connect to Ganache.")

# Solidity file path
solidity_file_path = "doctor/contracts/user.sol"

# Read the Solidity code
with open(solidity_file_path, "r") as file:
    solidity_code = file.read()

# Compile Solidity code
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {solidity_file_path: {"content": solidity_code}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "evm.bytecode"]}
            }
        }
    },
    solc_version="0.8.17"
)

# Get contract ABI and bytecode
contract_abi = compiled_sol["contracts"][solidity_file_path]["UserCredentials"]["abi"]
contract_interface = compiled_sol["contracts"][solidity_file_path]["UserCredentials"]
bytecode = contract_interface["evm"]["bytecode"]["object"]

def deploy_contract():
    try:
        # Deploy the contract
        tx_hash = web3.eth.contract(abi=contract_abi, bytecode=bytecode).constructor().transact({'from': web3.eth.accounts[0]})
        
        # Wait for the transaction receipt
        tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

        # Get the contract address from the transaction receipt
        contract_address = tx_receipt.contractAddress

        return contract_address
    except Exception as e:
        print("Error deploying contract:", e)
        return None

def add_user_to_blockchain(username, email, password, contract):
    if username and password and email:
        try:
            tx_hash = contract.functions.addUser(username, email, password).transact({'from': web3.eth.accounts[0]})
            
            tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
            print(tx_receipt)  
            if tx_receipt.status == 1:
                print("User data stored on the blockchain successfully!")
                return True
            else:
                print("Transaction failed. Error code:", tx_receipt.status)
                return False
        except Exception as e:
            print("Error while adding user:", e)
            return False
    else:
        print('username or email or password is null')

def get_user(userEmail, contract):
    try:
        user_details = contract.functions.getUser(userEmail).call()
        print("User Details:", user_details)
        return user_details
    except ValueError as e:
        print(f"Error while getting user details: {e}")
        return None



# Deploy the contract and get the contract address
contract_address = deploy_contract()
print(type(contract_address))
def add_user(username,email,password):
    if contract_address:
        print("Contract deployed at address:", contract_address)
        # Create contract instance using the deployed contract address
        contract = web3.eth.contract(address=contract_address, abi=contract_abi)
        add_user_to_blockchain(username, email, password, contract)
        # # Call getUser function
        # a=get_user(email, contract)
        # print(a,'-------------********----------')
        return contract_address
    else:
        print("Failed to deploy contract.")
        return 'error'
# add_user('t','t@gmail.com','kk')
def getUs(email,addr):
    if addr:
            print("Contract deployed at address:", addr)
            # Create contract instance using the deployed contract address
            contract = web3.eth.contract(address=addr, abi=contract_abi)
     
            user = get_user(email, contract)
            print(user,'------------------------')
            return user
    else:
        print("Failed to deploy contract.")