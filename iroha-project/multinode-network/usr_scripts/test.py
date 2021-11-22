import os
import binascii
from iroha import IrohaCrypto, Iroha, IrohaGrpc
import sys

# Iroha peer 1
IROHA_HOST_ADDR_1 = os.getenv('IROHA_HOST_ADDR_1', '172.29.101.121')
IROHA_PORT_1 = os.getenv('IROHA_PORT_1', '50051')
# Iroha peer 2
IROHA_HOST_ADDR_2 = os.getenv('IROHA_HOST_ADDR_2', '172.29.101.122')
IROHA_PORT_2 = os.getenv('IROHA_PORT_2', '50052')
# Iroha peer 3
IROHA_HOST_ADDR_3 = os.getenv('IROHA_HOST_ADDR_2', '172.29.101.123')
IROHA_PORT_3 = os.getenv('IROHA_PORT_3', '50053')

ADMIN_ACCOUNT_ID = os.getenv('ADMIN_ACCOUNT_ID', 'admin@test')
ADMIN_PRIVATE_KEY = os.getenv(
    'ADMIN_PRIVATE_KEY', 'f101537e319568c765b2cc89698325604991dca57b9716b58016b253506cab70')

iroha = Iroha(ADMIN_ACCOUNT_ID)
net_1 = IrohaGrpc('{}:{}'.format(IROHA_HOST_ADDR_1, IROHA_PORT_1))
net_2 = IrohaGrpc('{}:{}'.format(IROHA_HOST_ADDR_2, IROHA_PORT_2))
net_3 = IrohaGrpc('{}:{}'.format(IROHA_HOST_ADDR_3, IROHA_PORT_3))


def trace(func):
    """
    A decorator for tracing methods' begin/end execution points
    """

    def tracer(*args, **kwargs):
        name = func.__name__
        print('\tEntering "{}"'.format(name))
        result = func(*args, **kwargs)
        print('\tLeaving "{}"'.format(name))
        return result

    return tracer


@trace
def send_transaction_and_print_status(transaction):
    hex_hash = binascii.hexlify(IrohaCrypto.hash(transaction))
    print('Transaction hash = {}, creator = {}'.format(
        hex_hash, transaction.payload.reduced_payload.creator_account_id))
    net_1.send_tx(transaction)
    for status in net_1.tx_status_stream(transaction):
        print(status)


# Create a new domain with a new asset
commands = [
    iroha.command('CreateDomain', domain_id='domain', default_role='user'),
    iroha.command('CreateAsset', asset_name='coin',
                  domain_id='domain', precision=2)
]
tx = IrohaCrypto.sign_transaction(
    iroha.transaction(commands), ADMIN_PRIVATE_KEY)
send_transaction_and_print_status(tx)

# Add some coins to admin
tx = iroha.transaction([
    iroha.command('AddAssetQuantity',
                  asset_id='coin#domain', amount='1000.00')
])
IrohaCrypto.sign_transaction(tx, ADMIN_PRIVATE_KEY)
send_transaction_and_print_status(tx)

# Make a user account
user_private_key = IrohaCrypto.private_key()
user_public_key = IrohaCrypto.derive_public_key(user_private_key)
tx = iroha.transaction([
    iroha.command('CreateAccount', account_name='userone', domain_id='domain',
                  public_key=user_public_key)
])
IrohaCrypto.sign_transaction(tx, ADMIN_PRIVATE_KEY)
send_transaction_and_print_status(tx)

# Transfer coin
tx = iroha.transaction([
    iroha.command('TransferAsset', src_account_id='admin@test', dest_account_id='userone@domain',
                  asset_id='coin#domain', description='init top up', amount='2.00')
])
IrohaCrypto.sign_transaction(tx, ADMIN_PRIVATE_KEY)
send_transaction_and_print_status(tx)

# Query coin info
query = iroha.query('GetAssetInfo', asset_id='coin#domain')
IrohaCrypto.sign_query(query, ADMIN_PRIVATE_KEY)

response = net_1.send_query(query)
data = response.asset_response.asset
print('Asset id = {}, precision = {}'.format(data.asset_id, data.precision))

# Query blocks
def get_block(net, height):
    query = iroha.query("GetBlock", height=height)
    IrohaCrypto.sign_query(query, ADMIN_PRIVATE_KEY)

    response = net.send_query(query)
    return response
h=1
b = get_block(net_1, h)
while b.error_response.error_code==0:
    print(b)
    b = get_block(net_1, h)
    h+=1