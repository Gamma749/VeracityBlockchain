import logging
from time import sleep
from iroha import primitive_pb2
from IrohaUtils import *
import pickle

logging.basicConfig(level=logging.INFO)
iroha_setup = False
DOMAIN_NAME = "document"
user = new_user("swipluser", DOMAIN_NAME)
with open("/notebooks/iroha_connection/user_data.pkl", "wb+") as user_data:
    pickle.dump(user, user_data)
logging.debug(user)

def setup_iroha():

    commands = [
        # Create a new role that can only create assets (i.e. create hashes) and read assets (to see if they exist)
        iroha_admin.command("CreateRole", role_name="document_creator", permissions=[
                primitive_pb2.can_create_asset,
                primitive_pb2.can_read_assets
            ]),
        # Create a new domain that has document_creator as role
        iroha_admin.command("CreateDomain", domain_id=DOMAIN_NAME, default_role="document_creator"),
        iroha_admin.command('CreateAccount', account_name=user["name"], domain_id=DOMAIN_NAME,
                            public_key=user["public_key"])
    ]
    # Sign and send set up block
    tx = IrohaCrypto.sign_transaction(
            iroha_admin.transaction(commands), ADMIN_PRIVATE_KEY)
    logging.debug(tx)
    status = send_transaction(tx, net_1)
    logging.debug(status)
    return status[0] == "COMMITTED"

while not iroha_setup:
    try:
        logging.info("Iroha connection setup attempt")
        iroha_setup = setup_iroha()
        if not iroha_setup:
            logging.info("Setup failed! Reattempting")
    except Exception:
        logging.info("Network unreachable! Reattempting")
        sleep(1)
        continue

logging.info("Iroha Setup Complete")