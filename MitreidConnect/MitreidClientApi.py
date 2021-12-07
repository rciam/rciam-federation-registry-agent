import requests, json

"""
Manages all clients on MITREid Connect

"""


class mitreidClientApi:

    """
    Class constructor

    Parameters:
        issuer (str): The URI of the Authorization Server
        token  (str): An access token with admin privileges

    """

    def __init__(self, issuer, token):
        self.issuer = issuer
        self.token = token

    """
    Get all registered clients

    Returns:
        response (JSON Object): All registered clients in JSON format
    """

    def getClients(self):
        url = self.issuer + "/api/clients"
        header = {"Authorization": "Bearer " + self.token}

        try:
            response = requests.get(url, headers=header)
            response.raise_for_status()
        except requests.exceptions.HTTPError as errh:
            print("Http Error: %s with error: %s" % (url, repr(errh)))
            return {'status': response.status_code,'error': repr(errh) }
        except requests.exceptions.ConnectionError as errc:
            print("Error Connecting: %s with error: %s" % (url, repr(errc)))
            return {'status': response.status_code,'error': repr(errc) }
        except requests.exceptions.Timeout as errt:
            print("Timeout Error: %s with error: %s" % (url, repr(errt)))
            return {'status': response.status_code,'error': repr(errt) }
        except requests.exceptions.RequestException as err:
            print("Failed to make request to %s with error: %s" % (url, err))
            return {'status': response.status_code,'error': repr(err) }

        return {'status': response.status_code,'response': response.json()}


    """
    Get a registered client by ID

    Parameters:
        id (str): The id of the client
    
    Returns:
        response (JSON Object): A registered client in JSON format
    """

    def getClientById(self, id):
        url = self.issuer + "/api/clients/" + str(id)
        header = {"Authorization": "Bearer " + self.token}

        try:
            response = requests.get(url, headers=header)
            response.raise_for_status()
        except requests.exceptions.HTTPError as errh:
            print("Http Error: %s with error: %s" % (url, repr(errh)))
            return {'status': response.status_code,'error': repr(errh) }
        except requests.exceptions.ConnectionError as errc:
            print("Error Connecting: %s with error: %s" % (url, repr(errc)))
            return {'status': response.status_code,'error': repr(errc) }
        except requests.exceptions.Timeout as errt:
            print("Timeout Error: %s with error: %s" % (url, repr(errt)))
            return {'status': response.status_code,'error': repr(errt) }
        except requests.exceptions.RequestException as err:
            print("Failed to make request to %s with error: %s" % (url, err))
            return {'status': response.status_code,'error': repr(err) }

        return {'status': response.status_code,'response': response.json()}


    """
    Register new client

    Parameters:
        clientObject (str): A string with the client data in JSON format
    
    Returns:
        response (JSON Object): The registered client in JSON format
    """

    def createClient(self, clientObject):
        url = self.issuer + "/api/clients"
        header = {
            "Authorization": "Bearer " + self.token,
            "Content-Type": "application/json",
        }

        try:
            response = requests.post(url, headers=header, json=clientObject)
            response.raise_for_status()
        except requests.exceptions.HTTPError as errh:
            print("Http Error: %s with error: %s" % (url, repr(errh)))
            return {'status': response.status_code,'error': repr(errh) }
        except requests.exceptions.ConnectionError as errc:
            print("Error Connecting: %s with error: %s" % (url, repr(errc)))
            return {'status': response.status_code,'error': repr(errc) }
        except requests.exceptions.Timeout as errt:
            print("Timeout Error: %s with error: %s" % (url, repr(errt)))
            return {'status': response.status_code,'error': repr(errt) }
        except requests.exceptions.RequestException as err:
            print("Failed to make request to %s with error: %s" % (url, err))
            return {'status': response.status_code,'error': repr(err) }

        return {'status': response.status_code,'response': response.json()}


    """
    Update an existing client by ID

    Parameters:
        id (str): The id of the client
        clientObject (str): A string with the client data in JSON format
    
    Returns:
        response (JSON Object): The registered client in JSON format
    """

    def updateClientById(self, id, clientObject):
        url = self.issuer + "/api/clients/" + str(id)
        header = {
            "Authorization": "Bearer " + self.token,
            "Content-Type": "application/json",
        }

        try:
            response = requests.put(url, headers=header, json=clientObject)
            response.raise_for_status()
        except requests.exceptions.HTTPError as errh:
            print("Http Error: %s with error: %s" % (url, repr(errh)))
            return {'status': response.status_code,'error': repr(errh) }
        except requests.exceptions.ConnectionError as errc:
            print("Error Connecting: %s with error: %s" % (url, repr(errc)))
            return {'status': response.status_code,'error': repr(errc) }
        except requests.exceptions.Timeout as errt:
            print("Timeout Error: %s with error: %s" % (url, repr(errt)))
            return {'status': response.status_code,'error': repr(errt) }
        except requests.exceptions.RequestException as err:
            print("Failed to make request to %s with error: %s" % (url, err))
            return {'status': response.status_code,'error': repr(err) }

        return {'status': response.status_code,'response': response.json()}


    """
    Delete a registered client by ID

    Parameters:
        id (str): The id of the client
    
    Returns:
        response (boolean): True if the client was deleted successfully
    """

    def deleteClientById(self, id):
        url = self.issuer + "/api/clients/" + str(id)
        header = {"Authorization": "Bearer " + self.token}

        try:
            response = requests.delete(url, headers=header)       
            response.raise_for_status()
        except requests.exceptions.HTTPError as errh:
            print("Http Error: %s with error: %s" % (url, repr(errh)))
            return {'status': response.status_code,'error': repr(errh) }
        except requests.exceptions.ConnectionError as errc:
            print("Error Connecting: %s with error: %s" % (url, repr(errc)))
            return {'status': response.status_code,'error': repr(errc) }
        except requests.exceptions.Timeout as errt:
            print("Timeout Error: %s with error: %s" % (url, repr(errt)))
            return {'status': response.status_code,'error': repr(errt) }
        except requests.exceptions.RequestException as err:
            print("Failed to make request to %s with error: %s" % (url, err))
            return {'status': response.status_code,'error': repr(err) }

        return {'status': response.status_code,'response': 'OK'}
