import os
import binascii
import logging
from iroha import IrohaCrypto, Iroha, IrohaGrpc

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


# Iroha peer 1
IROHA_HOST_ADDR_1 = os.getenv('IROHA_HOST_ADDR_1', '172.29.101.121')
IROHA_PORT_1 = os.getenv('IROHA_PORT_1', '50051')
# Iroha peer 2
IROHA_HOST_ADDR_2 = os.getenv('IROHA_HOST_ADDR_2', '172.29.101.122')
IROHA_PORT_2 = os.getenv('IROHA_PORT_2', '50052')
# Iroha peer 3
IROHA_HOST_ADDR_3 = os.getenv('IROHA_HOST_ADDR_3', '172.29.101.123')
IROHA_PORT_3 = os.getenv('IROHA_PORT_3', '50053')
# Iroha peer 4
IROHA_HOST_ADDR_4 = os.getenv('IROHA_HOST_ADDR_3', '172.29.101.124')
IROHA_PORT_4 = os.getenv('IROHA_PORT_4', '50054')


ADMIN_ACCOUNT_ID = os.getenv('ADMIN_ACCOUNT_ID', 'admin@test')
ADMIN_PRIVATE_KEY = os.getenv(
    'ADMIN_PRIVATE_KEY', 'f101537e319568c765b2cc89698325604991dca57b9716b58016b253506cab70')

iroha = Iroha(ADMIN_ACCOUNT_ID)
net_1 = IrohaGrpc('{}:{}'.format(IROHA_HOST_ADDR_1, IROHA_PORT_1), timeout=10)
net_2 = IrohaGrpc('{}:{}'.format(IROHA_HOST_ADDR_2, IROHA_PORT_2), timeout=10)
net_3 = IrohaGrpc('{}:{}'.format(IROHA_HOST_ADDR_3, IROHA_PORT_3), timeout=10)
net_4 = IrohaGrpc('{}:{}'.format(IROHA_HOST_ADDR_4, IROHA_PORT_4), timeout=10)


def trace(func):
    """
    A decorator for tracing methods' begin/end execution points
    """

    def tracer(*args, **kwargs):
        name = func.__name__
        logging.debug(f'{bcolors.HEADER}==> Entering "{name}"{bcolors.ENDC}')
        result = func(*args, **kwargs)
        logging.debug(f'{bcolors.HEADER}==> Leaving "{name}"{bcolors.ENDC}')
        return result

    return tracer


@trace
def send_transaction(transaction, connection, verbose=False):
    """Send a transaction across a network to a peer and return the final status
    Verbose mode intended mainly for manual transaction sending and testing
    This method is blocking, waiting for a final status for the transaction

    Args:
        transaction (Iroha.transaction): The signed transaction to send to a peer
        connection (IrohaGrpc): The Grpc connection to send the transaction across
        verbose (bool): A boolean to print the status stream to stdout

    Returns:
        Iroha Transaction Status: The final transaction status received
    """

    hex_hash = binascii.hexlify(IrohaCrypto.hash(transaction))
    logging.debug('Transaction hash = {}, creator = {}'.format(
        hex_hash, transaction.payload.reduced_payload.creator_account_id))
    connection.send_tx(transaction)
    last_status = None
    for status in connection.tx_status_stream(transaction):
        if verbose: print(status)
        last_status = status
    return last_status

@trace
def get_block(block_number, connection):
    """Get the block at height block_number from the node specified by connection 

    Args:
        block_number (int): The block number to get. Must be >0 and less than the maximum height
        connection (IrohaGrpc): The connection to a node to get blocks from

    Returns:
        JSON: the JSON description of the block requested
    
    Throws:
        Exception if block height is invalid, or if connection is invalid
    """

    query = iroha.query("GetBlock", height=block_number)
    IrohaCrypto.sign_query(query, ADMIN_PRIVATE_KEY)
    block = connection.send_query(query)

    return block