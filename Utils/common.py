import logging.config
import logging

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
def create_ams_response(response, service_id, agent_id, external_id, client_id):
    msgNew = {}
    msgNew['id'] = service_id
    msgNew['agent_id'] = agent_id
    msgNew['status_code'] = response['status']
    if external_id>0:
        msgNew['external_id'] = external_id

    if len(client_id)>0:
        msgNew['client_id'] = client_id

    if response['status'] != 200:
        msgNew['error_description'] = response['error']
        msgNew['state'] = 'error'
    else:
        msgNew['state'] = 'deployed'

    return  msgNew