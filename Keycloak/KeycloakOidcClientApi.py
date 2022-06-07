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

    def get_client_by_id(self, client_id):
        url = self.auth_url + "/realms/" + self.realm + "/clients-registrations/default/" + str(client_id)
        header = {"Authorization": "Bearer " + self.token}

        return self.http_request("GET", url, header)

    """
    Register new client

    Parameters:
        client_object (str): A string with the client data in JSON format
    
    Returns:
        response (JSON Object): The registered client in JSON format
    """

    def create_client(self, client_object):
        url = self.auth_url + "/realms/" + self.realm + "/clients-registrations/default"
        header = {
            "Authorization": "Bearer " + self.token,
            "Content-Type": "application/json",
        }

        return self.http_request("POST", url, header, client_object)

    """
    Update an existing client by ID

    Parameters:
        client_id (str): The client_id of the client
        client_object (str): A string with the client data in JSON format
    
    Returns:
        response (JSON Object): The registered client in JSON format
    """

    def update_client(self, client_id, client_object):
        url = self.auth_url + "/realms/" + self.realm + "/clients-registrations/default/" + str(client_id)
        header = {
            "Authorization": "Bearer " + self.token,
            "Content-Type": "application/json",
        }

        return self.http_request("PUT", url, header, client_object)

    """
    Delete a registered client by ID

    Parameters:
        client_id (str): The client_id of the client
    
    Returns:
        response (JSON Object): The registered client in JSON format
    """

    def delete_client(self, client_id):
        url = self.auth_url + "/realms/" + self.realm + "/clients-registrations/default/" + str(client_id)
        header = {"Authorization": "Bearer " + self.token}

        return self.http_request("DELETE", url, header)

    """
    Get OIDC client's "Permissions"

    Parameters:
        keycloak_id (str): The keycloak_id of the client
    
    Returns:
        response (JSON Object): The response from the Client AuthZ Permissions API
    """

    def get_client_authz_permissions(self, keycloak_id):
        url = self.auth_url + "/admin/realms/" + self.realm + "/clients/" + str(keycloak_id) + "/management/permissions"
        header = {"Authorization": "Bearer " + self.token}

        return self.http_request("GET", url, header)

    """
    Enable OIDC client's "Permissions"

    Parameters:
        keycloak_id (str): The keycloak_id of the client
        action (str): "enable" or "disable" Client Authorization Permissions
    
    Returns:
        response (JSON Object): The registered client in JSON format
    """

    def update_client_authz_permissions(self, keycloak_id, action):
        url = self.auth_url + "/admin/realms/" + self.realm + "/clients/" + str(keycloak_id) + "/management/permissions"
        header = {"Authorization": "Bearer " + self.token}
        if action == "enable":
            enabled = True
        elif action == "disable":
            enabled = False
        client_object = {"enabled": enabled}

        return self.http_request("PUT", url, header, client_object)

    """
    Get realm default client scopes
    
    Returns:
        response (JSON Object): A registered client in JSON format
    """

    def get_realm_default_client_scopes(self):
        url = self.auth_url + "/admin/realms/" + self.realm + "/default-default-client-scopes"
        header = {"Authorization": "Bearer " + self.token}

        return self.http_request("GET", url, header)

    """
    Sync realm client scopes
    
    Returns:
        response (JSON Object): A registered client in JSON format
    """

    def sync_realm_client_scopes(self):
        url = self.auth_url + "/admin/realms/" + self.realm + "/client-scopes"
        header = {"Authorization": "Bearer " + self.token}
        response = self.http_request("GET", url, header)

        scope_list = {}
        for scope in response["response"]:
            scope_list[scope["name"]] = scope["id"]

        return scope_list

    """
    Create realm client scope
    
    Returns:
        response (JSON Object): A registered client in JSON format
    """

    def create_realm_client_scopes(self, scope_name):
        url = self.auth_url + "/admin/realms/" + self.realm + "/client-scopes"
        header = {"Authorization": "Bearer " + self.token}
        client_scope_object = {
            "name": scope_name,
            "protocol": "openid-connect",
            "attributes": {
                "include.in.token.scope": "true",
                "hide.from.openID.provider.metadata": "true",
                "display.on.consent.screen": "true",
            },
        }

        self.http_request("POST", url, header, client_scope_object)

    """
    Add client scope to the optional client scopes list of the client
    
    Returns:
        response (JSON Object): A registered client in JSON format
    """

    def add_client_scope_by_id(self, keycloak_id, client_scope_id):
        url = (
            self.auth_url
            + "/admin/realms/"
            + self.realm
            + "/clients/"
            + keycloak_id
            + "/optional-client-scopes/"
            + client_scope_id
        )
        header = {"Authorization": "Bearer " + self.token}
        self.http_request("PUT", url, header)

    """
    Remove client scope to the optional client scopes list of the client
    """

    def remove_client_scope_by_id(self, keycloak_id, client_scope_id):
        url = (
            self.auth_url
            + "/admin/realms/"
            + self.realm
            + "/clients/"
            + keycloak_id
            + "/optional-client-scopes/"
            + client_scope_id
        )
        header = {"Authorization": "Bearer " + self.token}
        self.http_request("DELETE", url, header)

    """
    Get the user of the service account
    
    Returns:
        response (JSON Object): A user representation in JSON format
    """

    def get_service_account_user(self, keycloak_id):
        url = self.auth_url + "/admin/realms/" + self.realm + "/clients/" + keycloak_id + "/service-account-user"
        header = {"Authorization": "Bearer " + self.token}
        return self.http_request("GET", url, header)

    """
    Update user profile information
    """

    def update_user(self, service_account_profile, keycloak_response, keycloak_config):
        url = self.auth_url + "/admin/realms/" + self.realm + "/users/" + service_account_profile["id"]
        header = {"Authorization": "Bearer " + self.token}

        update_flag = False
        email_list = keycloak_response["attributes"]["contacts"].split(",")
        first_name = keycloak_response["name"]
        candidate_attr = keycloak_config["attribute_name"]
        candidate_id = [service_account_profile[keycloak_config["candidate"]] + "@" + keycloak_config["scope"]]

        if "email" not in service_account_profile or service_account_profile["email"] != email_list[0]:
            service_account_profile["email"] = email_list[0]
            update_flag = True
        if "firstName" not in service_account_profile or service_account_profile["firstName"] != first_name:
            service_account_profile["firstName"] = first_name
            update_flag = True
        if "attributes" not in service_account_profile:
            service_account_profile["attributes"] = {}
        if (
            candidate_attr not in service_account_profile["attributes"]
            or service_account_profile["attributes"][candidate_attr] != candidate_id
        ):
            service_account_profile["attributes"][candidate_attr] = candidate_id
            update_flag = True

        if update_flag:
            self.http_request("PUT", url, header, service_account_profile)

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

    def http_request(self, method, url, header, data=None):
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

        if method == "DELETE" or response.status_code == 204 or not response.text:
            return {"status": response.status_code, "response": "OK"}
        else:
            return {"status": response.status_code, "response": response.json()}
