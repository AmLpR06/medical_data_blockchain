from web3 import Web3
from solcx import compile_standard, install_solc

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
solidity_file_path = "doctor/contracts/use.sol"

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

# Deploy the contract
web3.eth.default_account = web3.eth.accounts[0]
add = web3.eth.accounts[0]
Greeter = web3.eth.contract(abi=contract_abi, bytecode=bytecode)

tx_hash = Greeter.constructor().transact()

tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

greeter = web3.eth.contract(
    address=tx_receipt.contractAddress,
    abi=contract_abi
)
tx_hash = greeter.functions.addUser("JohnDoe", "password123", "john@example.com",add).transact()
tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
# print(tx_receipt)
# Now you can interact with the deployed contract using contract_instance

# ... (rest of the code remains the same)

# Transact addUser function
# def add_user_to_blockchain(username, password, email):
#     if username and password and email:
#         try:
#             tx_hash = contract.functions.addUser(username, email, password).transact({'from': deployer_account})
#             tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

#             if tx_receipt.status == 1:
#                 print("User data stored on the blockchain successfully!")
#                 return True
#             else:
#                 print("Transaction failed. Error code:", tx_receipt.status)
#                 return False
#         except Exception as e:
#             print("Error while adding user:", e)
#             return False
#     else:
#         print('username or email or password is null')

# # Call getUser function
def get_user(userEmail,addr):
    user_contract = web3.eth.contract(abi=contract_abi, bytecode=bytecode)
    tx_hash = user_contract.constructor().transact({'from': web3.eth.accounts[0]})
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    # print(tx_receipt)
    
    # Create a contract instance using the deployed contract address
    greeter = web3.eth.contract(
        address=tx_receipt.contractAddress,
        abi=contract_abi
    )

    try:
        userEmail = userEmail.strip().lower()
        print(userEmail)
        user_details = greeter.functions.getUser(userEmail,addr).call()
        print("User Details:", user_details)
        return user_details
    except ValueError as e:
        print(f"Error while getting user details: {e}")
        return None

