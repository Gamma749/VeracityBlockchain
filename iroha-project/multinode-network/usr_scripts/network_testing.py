#! /bin/python

"""
Test multinode Iroha network with several mundane scenarios, with logging of outputs
This module assumes a fresh network, so make sure to run manage-network restart
Also note these tests are ordered. Some tests create objects that will be used by later tests
Do NOT employ pytest-random, as tests will fail. This is intended
"""
from IrohaUtils import *
import pytest
import logging
import socket

logging.basicConfig(level=logging.DEBUG)


@pytest.fixture
def node_locations():
    return[
        (IROHA_HOST_ADDR_1, int(IROHA_PORT_1)),
        (IROHA_HOST_ADDR_2, int(IROHA_PORT_2)),
        (IROHA_HOST_ADDR_3, int(IROHA_PORT_3)),
        (IROHA_HOST_ADDR_4, int(IROHA_PORT_4)),
    ]


@pytest.fixture
def node_grpcs():
    return [net_1, net_2, net_3, net_4]


def test_node_reachable(node_locations):
    """
    Test that a node can be reached on the address:port specified
    """

    for location in node_locations:
        logging.debug(f"ATTEMPTING TO REACH {location}")
        a_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        a_socket.settimeout(1)
        conn_result = a_socket.connect_ex(location)
        a_socket.close()
        logging.debug(f"CONNECTION RESULT {conn_result}")
        assert conn_result == 0


def test_create_domain():
    """
    Test that an admin can create a domain
    """

    commands = [
        iroha.command('CreateDomain', domain_id='pytest', default_role='user')
    ]

    tx = IrohaCrypto.sign_transaction(
        iroha.transaction(commands), ADMIN_PRIVATE_KEY)
    status = send_transaction(tx, net_1)
    assert status[0] == "COMMITTED"


def test_create_asset():
    """
    Test that an admin can create an asset on a domain
    """

    commands = [
        iroha.command('CreateAsset', asset_name='coin',
                      domain_id='pytest', precision=2)
    ]

    tx = IrohaCrypto.sign_transaction(
        iroha.transaction(commands), ADMIN_PRIVATE_KEY)
    status = send_transaction(tx, net_1)
    assert status[0] == "COMMITTED"


def test_add_asset():
    """
    Test if an admin can add an asset to their account in a domain
    """

    tx = iroha.transaction([
        iroha.command('AddAssetQuantity',
                      asset_id='coin#pytest', amount='1000.00')
    ])
    tx = IrohaCrypto.sign_transaction(tx, ADMIN_PRIVATE_KEY)
    status = send_transaction(tx, net_1)
    assert status[0] == "COMMITTED"


def test_create_users(node_grpcs):
    """
    Test that an admin can create users in a domain, and check this for one user per node
    """

    for i, node_grpc in enumerate(node_grpcs):
        user_private_key = IrohaCrypto.private_key()
        user_public_key = IrohaCrypto.derive_public_key(user_private_key)
        tx = iroha.transaction([
            iroha.command('CreateAccount', account_name=f'user{i}', domain_id='pytest',
                          public_key=user_public_key)
        ])
        IrohaCrypto.sign_transaction(tx, ADMIN_PRIVATE_KEY)
        status = send_transaction(tx, node_grpc)
        assert status[0] == "COMMITTED"


def test_transfer_asset_to_users(node_grpcs):
    """
    Test that an admin can transfer assets to other users
    """
    
    for i, node_grpc in enumerate(node_grpcs):
        tx = iroha.transaction([
            iroha.command('TransferAsset', src_account_id='admin@test', dest_account_id=f'user{i}@pytest',
                          asset_id='coin#pytest', description='Top Up', amount=f'{(i+1)*1.11}')
        ])
        IrohaCrypto.sign_transaction(tx, ADMIN_PRIVATE_KEY)
        status = send_transaction(tx, node_grpc)
        assert status[0] == "COMMITTED"


def test_query_on_asset(node_grpcs):
    """
    Test that an admin can query an asset property
    """
    
    for i, node_grpc in enumerate(node_grpcs):
        query = iroha.query('GetAssetInfo', asset_id='coin#pytest')
        IrohaCrypto.sign_query(query, ADMIN_PRIVATE_KEY)
        response = node_grpc.send_query(query)
        data = response.asset_response.asset
        assert str(data) == 'asset_id: "coin#pytest"\ndomain_id: "pytest"\nprecision: 2\n'
