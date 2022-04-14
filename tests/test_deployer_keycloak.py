#!/usr/bin/env python3

import unittest
import types
import os
import importlib.machinery
from unittest.mock import MagicMock, Mock


def get_resource_path(relative_path):
    return os.path.join(os.path.dirname(__file__), relative_path)


# load standalone script as module
loader = importlib.machinery.SourceFileLoader(
    "deployer_keycloak", get_resource_path("../bin/deployer_keycloak")
)
deployer_keycloak = types.ModuleType(loader.name)
loader.exec_module(deployer_keycloak)


class TestDeployerKeycloak(unittest.TestCase):

    # Test the format is compatible with Keycloak
    def test_format_keycloak_msg(self):
        new_service = {
            "client_id": "testId1",
            "service_name": "testName1",
            "service_description": "testDescription1",
            "contacts": [
                {"name": "name1", "email": "email1", "type": "technical"},
                {"name": "name2", "email": "email2", "type": "security"},
            ],
        }
        out_service = {
            "attributes": {
                "client_credentials.use_refresh_token": "false",
                "oauth2.device.authorization.grant.enabled": "false",
                "oauth2.token.exchange.grant.enabled": "false",
                "oidc.ciba.grant.enabled": "false",
                "use.jwks.string": "false",
                "use.jwks.url": "false",
                "use.refresh.tokens": "false",
                "contacts": "email1"
            },
            "consentRequired": "true",
            "implicitFlowEnabled": "false",
            "publicClient": "false",
            "serviceAccountsEnabled": "false",
            "standardFlowEnabled": "false",
            "defaultClientScopes": [
                "example"
            ],
            "clientId": "testId1",
            "name": "testName1",
            "description": "testDescription1",
        }

        func_result = deployer_keycloak.format_keycloak_msg(new_service, ["example"])
        self.assertEqual(func_result, out_service)

    # Test calling Keycloak to create a new entry
    def test_call_keycloak_create(self):
        new_service = {
            "client_id": "testId1",
            "service_name": "testName1",
            "service_description": "testDescription1",
            "contacts": [
                {"name": "name1", "email": "email1", "type": "technical"},
                {"name": "name2", "email": "email2", "type": "security"},
            ],
            "deployment_type": "create",
        }
        out_service = {
            "response": {
                "attributes": {
                    "client_credentials.use_refresh_token": "false",
                    "oauth2.device.authorization.grant.enabled": "false",
                    "oauth2.token.exchange.grant.enabled": "false",
                    "oidc.ciba.grant.enabled": "false",
                    "use.jwks.string": "false",
                    "use.jwks.url": "false",
                    "use.refresh.tokens": "false",
                    "contacts": "email1"
                },
                "consentRequired": "true",
                "implicitFlowEnabled": "false",
                "publicClient": "false",
                "serviceAccountsEnabled": "false",
                "standardFlowEnabled": "false",
                "clientId": "testId1",
                "name": "testName1",
                "description": "testDescription1",
                "id": "a1a2a3a4-b5b6-c7c8-d9d0-e1e2e3e4e5e6",
            },
            "status": 200,
        }
        realm_default_client_scopes = {
            "response": [
                {
                    "id": "a1a2a3a4-b5b6-c7c8-d9d0-e1e2e3e4e5e6",
                    "name": "example",
                    "protocol": "openid-connect"
                }
            ],
            "status": 200,
        }

        mock = Mock()
        mock.createClient = MagicMock(return_value=out_service)
        mock.getRealmDefaultClientScopes = MagicMock(return_value=realm_default_client_scopes)

        func_result = deployer_keycloak.call_keycloak(new_service, mock)
        self.assertEqual(func_result, (out_service, "a1a2a3a4-b5b6-c7c8-d9d0-e1e2e3e4e5e6", "testId1"))

    # Test calling Keycloak to delete an entry
    def test_call_keycloak_delete(self):
        new_service = {
            "external_id": "a1a2a3a4-b5b6-c7c8-d9d0-e1e2e3e4e5e6",
            "client_id": "testId1",
            "service_name": "testName1",
            "service_description": "testDescription1",
            "contacts": [
                {"name": "name1", "email": "email1", "type": "technical"},
                {"name": "name2", "email": "email2", "type": "security"},
            ],
            "deployment_type": "delete",
        }
        out_service = {
            "response": "OK",
            "status": 200,
        }
        realm_default_client_scopes = {
            "response": [
                {
                    "id": "a1a2a3a4-b5b6-c7c8-d9d0-e1e2e3e4e5e6",
                    "name": "example",
                    "protocol": "openid-connect"
                }
            ],
            "status": 200,
        }

        mock = Mock()
        mock.deleteClientById = MagicMock(return_value=out_service)
        mock.getRealmDefaultClientScopes = MagicMock(return_value=realm_default_client_scopes)

        func_result = deployer_keycloak.call_keycloak(new_service, mock)
        self.assertEqual(func_result, (out_service, "a1a2a3a4-b5b6-c7c8-d9d0-e1e2e3e4e5e6", ""))

    # Test calling Keycloak to update an entry
    def test_call_keycloak_update(self):
        new_service = {
            "external_id": "a1a2a3a4-b5b6-c7c8-d9d0-e1e2e3e4e5e6",
            "client_id": "testId1",
            "service_name": "testName1",
            "service_description": "testDescription1",
            "contacts": [
                {"name": "name1", "email": "email1", "type": "technical"},
                {"name": "name2", "email": "email2", "type": "security"},
            ],
            "deployment_type": "edit",
        }
        out_service = {
            "response": {
                "attributes": {
                    "client_credentials.use_refresh_token": "false",
                    "oauth2.device.authorization.grant.enabled": "false",
                    "oauth2.token.exchange.grant.enabled": "false",
                    "oidc.ciba.grant.enabled": "false",
                    "use.jwks.string": "false",
                    "use.jwks.url": "false",
                    "use.refresh.tokens": "false",
                    "contacts": "email1"
                },
                "consentRequired": "true",
                "implicitFlowEnabled": "false",
                "publicClient": "false",
                "serviceAccountsEnabled": "false",
                "standardFlowEnabled": "false",
                "clientId": "testId1",
                "name": "testName1",
                "description": "testDescription1",
                "id": "a1a2a3a4-b5b6-c7c8-d9d0-e1e2e3e4e5e6",
            },
            "status": 200,
        }
        realm_default_client_scopes = {
            "response": [
                {
                    "id": "a1a2a3a4-b5b6-c7c8-d9d0-e1e2e3e4e5e6",
                    "name": "example",
                    "protocol": "openid-connect"
                }
            ],
            "status": 200,
        }
        client_authz_permissions = {
            "response": {
                "enabled": False
            },
            "status": 200,
        }

        mock = Mock()
        mock.updateClientById = MagicMock(return_value=out_service)
        mock.getRealmDefaultClientScopes = MagicMock(return_value=realm_default_client_scopes)
        mock.getClientAuthzPermissions = MagicMock(return_value=client_authz_permissions)

        func_result = deployer_keycloak.call_keycloak(new_service, mock)
        self.assertEqual(func_result, (out_service, "a1a2a3a4-b5b6-c7c8-d9d0-e1e2e3e4e5e6", "testId1"))

    # Test update data with error when calling Keycloak
    def test_update_data_fail(self):
        new_msg = [
            {
                "id": 12,
                "client_id": "testId1",
                "service_name": "testName1",
                "service_description": "testDescription1",
                "contacts": [{"name": "name1", "email": "email1"}],
                "deployment_type": "create",
            }
        ]

        func_result = deployer_keycloak.update_data(new_msg, "", "", "", 1)
        self.assertEqual(
            func_result,
            [
                {
                    "attributes": {},
                    "data": {
                        "id": 12,
                        "agent_id": 1,
                        "status_code": 0,
                        "state": "error",
                        "error_description": "An error occurred while calling Keycloak",
                    },
                }
            ],
        )

    # Test update data calling Keycloak successfully
    def test_update_data_success(self):
        new_msg = [
            {
                "id": 12,
                "client_id": "testId1",
                "service_name": "testName1",
                "service_description": "testDescription1",
                "contacts": [{"name": "name1", "email": "email1"}],
                "deployment_type": "create",
            }
        ]
        deployer_keycloak.call_keycloak = MagicMock(
            return_value=({"status": 200}, 12, "testId1")
        )

        func_result = deployer_keycloak.update_data(new_msg, "url", "realm", "token", 1)
        self.assertEqual(
            func_result,
            [
                {
                    "attributes": {},
                    "data": {
                        "id": 12,
                        "external_id": 12,
                        "agent_id": 1,
                        "status_code": 200,
                        "state": "deployed",
                        "client_id": "testId1",
                    },
                }
            ],
        )
