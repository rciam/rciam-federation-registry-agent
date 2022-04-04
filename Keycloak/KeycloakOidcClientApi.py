import requests, json

"""
Manages all clients on Keycloak

"""


class KeycloakOidcClientApi:

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
    Get a registered client by ID

    Parameters:
        id (str): The id of the client
    
    Returns:
        response (JSON Object): A registered client in JSON format
    """

    def getClientById(self, id):
        url = self.issuer + "/clients-registrations/default/" + str(id)
        header = {"Authorization": "Bearer " + self.token}

        return self.httpRequest("GET", url, header)

    """
    Register new client

    Parameters:
        clientObject (str): A string with the client data in JSON format
    
    Returns:
        response (JSON Object): The registered client in JSON format
    """

    def createClient(self, clientObject):
        url = self.issuer + "/clients-registrations/default"
        header = {
            "Authorization": "Bearer " + self.token,
            "Content-Type": "application/json",
        }

        return self.httpRequest("POST", url, header, clientObject)

    """
    Update an existing client by ID

    Parameters:
        id (str): The id of the client
        clientObject (str): A string with the client data in JSON format
    
    Returns:
        response (JSON Object): The registered client in JSON format
    """

    def updateClientById(self, id, clientObject):
        url = self.issuer + "/clients-registrations/default/" + str(id)
        header = {
            "Authorization": "Bearer " + self.token,
            "Content-Type": "application/json",
        }

        return self.httpRequest("PUT", url, header, clientObject)

    """
    Delete a registered client by ID

    Parameters:
        id (str): The id of the client
    
    Returns:
        response (JSON Object): The registered client in JSON format
    """

    def deleteClientById(self, id):
        url = self.issuer + "/clients-registrations/default/" + str(id)
        header = {"Authorization": "Bearer " + self.token}

        return self.httpRequest("DELETE", url, header)

    """
    Get OIDC client's "Permissions"

    Parameters:
        keycloak_id (str): The keycloak_id of the client
    
    Returns:
        response (JSON Object): The response from the Client AuthZ Permissions API
    """

    def getClientAuthzPermissions(self, keycloak_id):
        url = self.issuer + "/admin/realms/" + self.realm + "/clients/" + str(keycloak_id) +"/management/permissions"
        header = {"Authorization": "Bearer " + self.token}

        return self.httpRequest("GET", url, header)

    """
    Enable OIDC client's "Permissions"

    Parameters:
        keycloak_id (str): The keycloak_id of the client
        action (str): "enable" or "disable" Client Authorization Permissions
    
    Returns:
        response (JSON Object): The registered client in JSON format
    """

    def updateClientAuthzPermissions(self, keycloak_id, action):
        url = self.issuer + "/admin/realms/" + self.realm + "/clients/" + str(keycloak_id) +"/management/permissions"
        header = {"Authorization": "Bearer " + self.token}
        if action == "enable":
            enabled = "true"
        elif action == "disable":
            enabled = "false"
        client_object = '{"enabled": ' + enabled + '}'

        return self.httpRequest("PUT", url, header, client_object)

    """
    Wrapper function for Python requests

    Parameters:
        method (str): The request method
        url (str): The URL of the Client Registration API
        header (str): The Headers of the HTTP Request
        data (str): The data of the HTTP Request, else `None`
    
    Returns:
        response (JSON Object): The status of the HTTP Response
    """

    def httpRequest(self, method, url, header, data=None):
        try:
            response = requests.request(method, url, headers=header, json=data)
            response.raise_for_status()
        except requests.exceptions.HTTPError as errh:
            print("Http Error: %s with error: %s" % (url, repr(errh)))
            return {"status": response.status_code, "error": repr(errh)}
        except requests.exceptions.ConnectionError as errc:
            print("Error Connecting: %s with error: %s" % (url, repr(errc)))
            return {"status": response.status_code, "error": repr(errc)}
        except requests.exceptions.Timeout as errt:
            print("Timeout Error: %s with error: %s" % (url, repr(errt)))
            return {"status": response.status_code, "error": repr(errt)}
        except requests.exceptions.RequestException as err:
            print("Failed to make request to %s with error: %s" % (url, err))
            return {"status": response.status_code, "error": repr(err)}

        if method == "DELETE":
            return {"status": response.status_code, "response": "OK"}
        else:
            return {"status": response.status_code, "response": response.json()}
