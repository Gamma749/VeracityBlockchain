#! /bin/python

"""
Test multinode Iroha network with several scenarios of a malicious client, with logging of outputs
This module assumes a fresh network, so make sure to run manage-network restart
Also note these tests are ordered. Some tests create objects that will be used by later tests
Do NOT employ pytest-random, as tests will fail. This is intended

We start this test by setting up a new domain (pytest) with a basic_role that can only transfer and receive assets
There are users a, b, and c. Each will start with 100 coins
Throughout these tests, user_a will be considered as the malicious one. Other users will remain "honest"
"""
from iroha import primitive_pb2
from IrohaUtils import *
import pytest
import logging
import socket


user_a_id = "user_a@pytest"
user_b_id = "user_b@pytest"
user_c_id = "user_c@pytest"
user_a_private_key = IrohaCrypto.private_key()
user_b_private_key = IrohaCrypto.private_key()
user_c_private_key = IrohaCrypto.private_key()
user_a_public_key = IrohaCrypto.derive_public_key(user_a_private_key)
user_b_public_key = IrohaCrypto.derive_public_key(user_b_private_key)
user_c_public_key = IrohaCrypto.derive_public_key(user_c_private_key)

def node_locations():
    return[
        (IROHA_HOST_ADDR_1, int(IROHA_PORT_1)),
        (IROHA_HOST_ADDR_2, int(IROHA_PORT_2)),
        (IROHA_HOST_ADDR_3, int(IROHA_PORT_3)),
        (IROHA_HOST_ADDR_4, int(IROHA_PORT_4)),
    ]

@pytest.fixture(name="node_locations")
def node_locations_fixture():
    return node_locations()

def node_grpcs():
    return [net_1, net_2, net_3, net_4]

@pytest.fixture(name="node_grpcs")
def node_grpcs_fixture():
    return node_grpcs()


@pytest.fixture(scope="session", autouse=True)
def set_up_test_environment_fixture(node_locations):
    set_up_test_environment(node_locations)

def set_up_test_environment(node_locations):
    """
    Ensure network is up and create all needed domains, assets, accounts etc for testing
    """

    # Check if network is reachable -------------------------------------------
    logging.info("ENSURE NETWORK IS UP")
    for i, location in enumerate(node_locations):
        logging.info(f"ATTEMPTING TO REACH NODE_{i+1}")
        logging.debug(f"Trying to reach location f{location}")
        a_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        a_socket.settimeout(60)
        conn_result = a_socket.connect_ex(location)
        a_socket.close()
        logging.debug(f"CONNECTION RESULT {conn_result}")
        assert conn_result == 0
        logging.info("\tCONNECTION SUCCESS")

    logging.info("NETWORK IS UP")

    # Role Creation -----------------------------------------------------------
    logging.info("CREATING ROLES")
    commands = [
        # A basic user that can send and receive assets, and that's all
        iroha.command("CreateRole", role_name="basic_user", permissions=[
            primitive_pb2.can_receive,
            primitive_pb2.can_transfer
        ])
    ]
    tx = IrohaCrypto.sign_transaction(
        iroha.transaction(commands), ADMIN_PRIVATE_KEY)
    logging.debug(tx)
    status = send_transaction(tx, net_1)
    logging.debug(status)
    assert status[0] == "COMMITTED"
    logging.info("ROLES CREATED")

    # Domain Creation ---------------------------------------------------------
    logging.info("CREATING DOMAIN")
    commands = [
        iroha.command('CreateDomain', domain_id='pytest', default_role='basic_user')
    ]
    tx = IrohaCrypto.sign_transaction(
        iroha.transaction(commands), ADMIN_PRIVATE_KEY)
    logging.debug(tx)
    status = send_transaction(tx, net_1)
    logging.debug(status)
    assert status[0] == "COMMITTED"
    logging.info("DOMAIN CREATED")

    # Asset Creation ----------------------------------------------------------
    logging.info("CREATING ASSETS")
    commands = [
        iroha.command('CreateAsset', asset_name='coin',
                      domain_id='pytest', precision=2)
    ]
    tx = IrohaCrypto.sign_transaction(
        iroha.transaction(commands), ADMIN_PRIVATE_KEY)
    logging.debug(tx)
    status = send_transaction(tx, net_1)
    logging.debug(status)
    assert status[0] == "COMMITTED"
    logging.info("ASSETS CREATED")

    # User Creation -----------------------------------------------------------
    logging.info("CREATING USERS")
    commands = [
        # Create users a,b,c
        iroha.command('CreateAccount', account_name=f'user_a', domain_id='pytest',
                          public_key=user_a_public_key),
        iroha.command('CreateAccount', account_name=f'user_b', domain_id='pytest',
                          public_key=user_b_public_key),
        iroha.command('CreateAccount', account_name=f'user_c', domain_id='pytest',
                          public_key=user_c_public_key)
    ]
    tx = IrohaCrypto.sign_transaction(
        iroha.transaction(commands), ADMIN_PRIVATE_KEY)
    logging.debug(tx)
    status = send_transaction(tx, net_1)
    logging.debug(status)
    assert status[0] == "COMMITTED"
    logging.info("USERS CREATED")

    # Asset Quantity Creation and Transfer ------------------------------------
    logging.info("ADDING ASSETS TO USERS")
    logging.info("ATTEMPTING TO ADD 1000 coin#pytest TO admin@test")
    tx = iroha.transaction([
        iroha.command('AddAssetQuantity',
                      asset_id='coin#pytest', amount='1000.00')
    ])
    tx = IrohaCrypto.sign_transaction(tx, ADMIN_PRIVATE_KEY)
    logging.debug(tx)
    status = send_transaction(tx, net_1)
    logging.debug(status)
    assert status[0] == "COMMITTED"
    logging.info("SUCCESSFULLY ADDED coin#pytest TO admin@test")

    logging.info("TRANSFERING ASSET TO USERS")
    commands = [
        # Create users a,b,c
        iroha.command('TransferAsset', src_account_id='admin@test', dest_account_id=f'user_a@pytest',
                          asset_id='coin#pytest', amount="100"),
        iroha.command('TransferAsset', src_account_id='admin@test', dest_account_id=f'user_b@pytest',
                          asset_id='coin#pytest', amount="100"),
        iroha.command('TransferAsset', src_account_id='admin@test', dest_account_id=f'user_c@pytest',
                          asset_id='coin#pytest', amount="100")
    ]
    tx = IrohaCrypto.sign_transaction(
        iroha.transaction(commands), ADMIN_PRIVATE_KEY)
    logging.debug(tx)
    status = send_transaction(tx, net_1)
    logging.debug(status)
    assert status[0] == "COMMITTED"
    logging.info("TRANSFERAL OF ASSETS COMPLETE")

    logging.info("SET UP COMPLETE")


# Attempt an honest spend to test
def test_honest_transfer():
    """
    Test that two honest accounts can actually transfer funds between them
    User B will send 10 coin to User C
    """

    logging.info("HONEST TRANSFER 10 COIN FROM B to C")
    iroha_user_b = Iroha(user_b_id)
    command = [iroha_user_b.command("TransferAsset", src_account_id=user_b_id, dest_account_id=user_c_id,
                            asset_id="coin#pytest", amount="10")]
    tx = IrohaCrypto.sign_transaction(
        iroha_user_b.transaction(command), user_b_private_key)
    logging.debug(tx)
    status = send_transaction(tx, net_1)
    logging.debug(status)
    assert status[0] == "COMMITTED"

    # Now check that both parties have the correct asset total
    user_b_assets = get_user_assets(user_b_id)
    user_c_assets = get_user_assets(user_c_id)
    assert str(user_b_assets) == '[asset_id: "coin#pytest"\naccount_id: "user_b@pytest"\nbalance: "90"\n]'
    assert str(user_c_assets) == '[asset_id: "coin#pytest"\naccount_id: "user_c@pytest"\nbalance: "110"\n]'
    logging.info("HONEST TRANSFER COMPLETE")

# Attempt to commit Double Spending
def test_double_spending_same_transaction():
    """
    User A will attempt to double spend their 100 coins to both user B and C at the same time
    """

    logging.info("ATTEMPTING DOUBLE SPEND ONE TRANSACTION")
    iroha_user_a = Iroha(user_a_id)
    tx = iroha_user_a.transaction([
        iroha.command('TransferAsset', src_account_id='user_a@pytest', dest_account_id=f'user_b@pytest',
                          asset_id='coin#pytest', amount="100"),
        iroha.command('TransferAsset', src_account_id='user_a@pytest', dest_account_id=f'user_c@pytest',
                          asset_id='coin#pytest', amount="100"),
        
    ])
    tx = IrohaCrypto.sign_transaction(tx, user_a_private_key)
    logging.debug(tx)
    status = send_transaction(tx, net_1)
    logging.debug(status)
    assert status[0] == "REJECTED"
    logging.info("TRANSACTION REJECTED")

    # Now check no coin has left user A's account or entered user B or C
    user_a_assets = get_user_assets(user_a_id)
    user_b_assets = get_user_assets(user_b_id)
    user_c_assets = get_user_assets(user_c_id)
    assert str(user_a_assets) == '[asset_id: "coin#pytest"\naccount_id: "user_a@pytest"\nbalance: "100"\n]'
    assert str(user_b_assets) == '[asset_id: "coin#pytest"\naccount_id: "user_b@pytest"\nbalance: "90"\n]'
    assert str(user_c_assets) == '[asset_id: "coin#pytest"\naccount_id: "user_c@pytest"\nbalance: "110"\n]'

    logging.info("NO COIN HAS BEEN TRANSFERRED")    

def test_double_spending_in_two_transactions():
    """
    User A will attempt to double spend their 100 coins to user B and user C at the same time,
    using two different transactions to two different peers

    It is possible that using asyncio, multiprocessing, or threading could help with this, as 
    we want to ensure the two transactions reach the peers at roughly the same time so the network does not process one over the other
    """

    logging.info("ATTEMPTING DOUBLE SPEND ON TWO TRANSACTIONS")
    

# Attempt to create new role

# Attempt to create new account

# Attempt signing under other user

# Attempt replay attack of own transaction (?)

# Attempt replay attack of others transaction


def get_user_assets(user_id):
    """
    Get all of the assets of a user and return these

    Args:
        user_id (string): The identity of the user to query, already on the blockchain

    Returns:
        List of account asset: The assets of the specified user
    """

    query = iroha.query("GetAccountAssets", account_id=user_id)
    IrohaCrypto.sign_query(query, ADMIN_PRIVATE_KEY)
    response = net_1.send_query(query)
    data = response.account_assets_response.account_assets
    return data

if __name__=="__main__":
    #logging.basicConfig(level=logging.INFO)
    logging.basicConfig(level=logging.DEBUG)

    # input(f"{bcolors.OKGREEN}{bcolors.ENDC}")

    # print(f"{'-'*80}\n\n")

    
    input(f"{bcolors.OKGREEN}Set up test environment with users, domain, and assets{bcolors.ENDC}")
    set_up_test_environment(node_locations())
    print(f"{'-'*80}\n\n")

    input(f"{bcolors.OKGREEN}Test that two honest users can transfer, B sends 10 coins to C{bcolors.ENDC}")
    test_honest_transfer()
    print(f"{'-'*80}\n\n")

    input(f"{bcolors.OKGREEN}Test that a malicious client cannot double spend in the same transaction{bcolors.ENDC}")
    test_double_spending_same_transaction()
    print(f"{'-'*80}\n\n")
