import requests, json

"""
Manages all clients on Keycloak

"""


class KeycloakOidcClientApi:

    """
    Class constructor

    Parameters:
        auth_url (str): The URI of the Authorization Server
        realm (str): The name of the realm
        token  (str): An access token with admin privileges

    """

    def __init__(self, auth_url, realm, token):
        self.auth_url = auth_url
        self.realm = realm
        self.token = token

    """
    Get a registered client by ID

    Parameters:
        client_id (str): The client_id of the client
    
    Returns:
        response (JSON Object): A registered client in JSON format
    """

    def getClientById(self, client_id):
        url = (
            self.auth_url
            + "/realms/"
            + self.realm
            + "/clients-registrations/default/"
            + str(client_id)
        )
        header = {"Authorization": "Bearer " + self.token}

        return self.httpRequest("GET", url, header)

    """
    Register new client

    Parameters:
        client_object (str): A string with the client data in JSON format
    
    Returns:
        response (JSON Object): The registered client in JSON format
    """

    def createClient(self, client_object):
        url = self.auth_url + "/realms/" + self.realm + "/clients-registrations/default"
        header = {
            "Authorization": "Bearer " + self.token,
            "Content-Type": "application/json",
        }

        return self.httpRequest("POST", url, header, client_object)

    """
    Update an existing client by ID

    Parameters:
        client_id (str): The client_id of the client
        client_object (str): A string with the client data in JSON format
    
    Returns:
        response (JSON Object): The registered client in JSON format
    """

    def updateClientById(self, client_id, client_object):
        url = (
            self.auth_url
            + "/realms/"
            + self.realm
            + "/clients-registrations/default/"
            + str(client_id)
        )
        header = {
            "Authorization": "Bearer " + self.token,
            "Content-Type": "application/json",
        }

        return self.httpRequest("PUT", url, header, client_object)

    """
    Delete a registered client by ID

    Parameters:
        client_id (str): The client_id of the client
    
    Returns:
        response (JSON Object): The registered client in JSON format
    """

    def deleteClientById(self, client_id):
        url = (
            self.auth_url
            + "/realms/"
            + self.realm
            + "/clients-registrations/default/"
            + str(client_id)
        )
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
        url = (
            self.auth_url
            + "/admin/realms/"
            + self.realm
            + "/clients/"
            + str(keycloak_id)
            + "/management/permissions"
        )
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
        url = (
            self.auth_url
            + "/admin/realms/"
            + self.realm
            + "/clients/"
            + str(keycloak_id)
            + "/management/permissions"
        )
        header = {"Authorization": "Bearer " + self.token}
        if action == "enable":
            enabled = "true"
        elif action == "disable":
            enabled = "false"
        client_object = '{"enabled": ' + enabled + "}"

        return self.httpRequest("PUT", url, header, client_object)

    """
    Get realm default client scopes
    
    Returns:
        response (JSON Object): A registered client in JSON format
    """

    def getRealmDefaultClientScopes(self):
        url = self.auth_url + "/admin/realms/" + self.realm + "/default-default-client-scopes"
        header = {"Authorization": "Bearer " + self.token}

        return self.httpRequest("GET", url, header)

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