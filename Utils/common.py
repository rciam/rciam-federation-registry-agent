import logging
import logging.config


def get_log_conf(log_config_file=None):
    """
    Method that searches and gets the default location of configuration and logging configuration
    """
    if log_config_file is not None:
        logging.config.fileConfig(log_config_file, disable_existing_loggers=False)
    else:
        logging.basicConfig(level=logging.INFO, format=logging.BASIC_FORMAT)


# create_ams_response creates a json object with the result of the mitreId api call
# that is readable from the rciam-federation-registry
def create_ams_response(response, service_id, deployer_name, external_id, client_id):
    new_msg = {}
    new_msg["id"] = service_id
    new_msg["status_code"] = response["status"]
    if len(deployer_name) > 0:
        new_msg["deployer_name"] = deployer_name

    if len(external_id) > 0:
        new_msg["external_id"] = external_id

    if len(client_id) > 0:
        new_msg["client_id"] = client_id

    if response["status"] != 200 and response["status"] != 201 and response["status"] != 204:
        new_msg["error_description"] = response["error"]
        new_msg["state"] = "error"
    else:
        new_msg["state"] = "deployed"

    return new_msg


"""
Method that creates the Keycloak issuer based on `auth_server` + `realm`

Parameters:
    config (dict): Keycloak's config options

Returns:
    return (string): Keycloak's issuer URL
"""


def get_keycloak_issuer(config):
    return config["auth_server"] + "/realms/" + config["realm"]
