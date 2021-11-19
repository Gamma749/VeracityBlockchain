import os
import binascii
from iroha import IrohaCrypto, Iroha, IrohaGrpc
# from iroha.primitive_pb2 import can_set_my_account_detail
import sys

IROHA_HOST_ADDR = os.getenv('IROHA_HOST_ADDR', '127.0.0.1')
IROHA_PORT = os.getenv('IROHA_PORT', '50051')
ADMIN_ACCOUNT_ID = os.getenv('ADMIN_ACCOUNT_ID', 'admin@test')
ADMIN_PRIVATE_KEY = os.getenv(
    'ADMIN_PRIVATE_KEY', 'f101537e319568c765b2cc89698325604991dca57b9716b58016b253506cab70')

iroha = Iroha(ADMIN_ACCOUNT_ID)
net = IrohaGrpc('{}:{}'.format(IROHA_HOST_ADDR, IROHA_PORT))


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
    net.send_tx(transaction)
    for status in net.tx_status_stream(transaction):
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

response = net.send_query(query)
data = response.asset_response.asset
print('Asset id = {}, precision = {}'.format(data.asset_id, data.precision))

# Query blocks
def get_block(height):
    query = iroha.query("GetBlock", height=height)
    IrohaCrypto.sign_query(query, ADMIN_PRIVATE_KEY)

    response = net.send_query(query)
    return response
h=1
b = get_block(h)
while b.error_response.error_code==0:
    print(b)
    b = get_block(h)
    h+=1