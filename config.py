import json
from utils import read_file, read_file_as_list


CONFIG = json.loads(read_file("config.json"))
ERC20ABI = json.loads(read_file("ERC20ABI.json"))
private_keys = read_file_as_list("data/private-keys.txt")
token_addresses = read_file_as_list("data/token-addresses.txt")
recipient_addresses = read_file_as_list("data/recipient-addresses.txt")