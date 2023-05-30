#!/usr/bin/env python3

import importlib.machinery
import os
import types
import unittest
from unittest.mock import MagicMock


def get_resource_path(relative_path):
    return os.path.join(os.path.dirname(__file__), relative_path)


# load standalone script as module
loader = importlib.machinery.SourceFileLoader("deployer_keycloak", get_resource_path("../bin/deployer_keycloak"))
deployer_keycloak_oidc = types.ModuleType(loader.name)
loader.exec_module(deployer_keycloak_oidc)

deployer_keycloak_saml = types.ModuleType(loader.name)
loader.exec_module(deployer_keycloak_saml)


class TestDeployerKeycloak(unittest.TestCase):
    # Test the format is compatible with Keycloak
    def test_oidc_format_keycloak_msg(self):
        new_service = {
            "client_id": "testOidcId",
            "service_name": "testName",
            "service_description": "testDescription",
            "protocol": "oidc",
            "contacts": [
                {"name": "name1", "email": "email1", "type": "technical"},
                {"name": "name2", "email": "email2", "type": "security"},
            ],
        }
        out_service = {
            "attributes": {
                "client_credentials.use_refresh_token": "false",
                "contacts": "email1",
                "oauth2.device.authorization.grant.enabled": "false",
                "oauth2.token.exchange.grant.enabled": False,
                "oidc.ciba.grant.enabled": "false",
                "refresh.token.max.reuse": "0",
                "revoke.refresh.token": "false",
                "use.jwks.string": "false",
                "use.jwks.url": "false",
                "use.refresh.tokens": "false",
            },
            "clientId": "testOidcId",
            "consentRequired": False,
            "defaultClientScopes": ["example"],
            "description": "testDescription",
            "directAccessGrantsEnabled": False,
            "implicitFlowEnabled": False,
            "name": "testName",
            "protocol": "openid-connect",
            "publicClient": False,
            "serviceAccountsEnabled": False,
            "standardFlowEnabled": False,
            "webOrigins": ["+"],
        }

        func_result = deployer_keycloak_oidc.format_keycloak_msg(new_service, ["example"], {})
        self.assertEqual(func_result, out_service)

    # Test calling Keycloak to create a new entry
    def test_oidc_deploy_to_keycloak_create(self):
        new_service = {
            "client_id": "testOidcId",
            "service_name": "testName",
            "service_description": "testDescription",
            "protocol": "oidc",
            "contacts": [
                {"name": "name1", "email": "email1", "type": "technical"},
                {"name": "name2", "email": "email2", "type": "security"},
            ],
            "scope": [
                "openid",
                "email",
                "profile",
            ],
            "deployment_type": "create",
        }
        out_service = {
            "response": {
                "attributes": {
                    "client_credentials.use_refresh_token": "false",
                    "contacts": "email1",
                    "oauth2.device.authorization.grant.enabled": "false",
                    "oauth2.token.exchange.grant.enabled": False,
                    "oidc.ciba.grant.enabled": "false",
                    "refresh.token.max.reuse": "0",
                    "revoke.refresh.token": "false",
                    "use.jwks.string": "false",
                    "use.jwks.url": "false",
                    "use.refresh.tokens": "false",
                },
                "consentRequired": False,
                "optionalClientScopes": ["profile", "email"],
                "clientId": "testOidcId",
                "defaultClientScopes": ["example"],
                "description": "testDescription",
                "id": "a1a2a3a4-b5b6-c7c8-d9d0-testOidcId",
                "protocol": "openid-connect",
                "implicitFlowEnabled": False,
                "name": "testName",
                "publicClient": False,
                "serviceAccountsEnabled": False,
                "standardFlowEnabled": False,
            },
            "status": 201,
        }
        realm_default_client_scopes = [
            {"id": "a1a2a3a4-b5b6-c7c8-d9d0-testScope3", "name": "example", "protocol": "openid-connect"}
        ]

        mock = MagicMock()
        mock.create_client = MagicMock(return_value=out_service)
        mock.get_client_by_id = MagicMock(return_value=out_service)
        mock.get_realm_default_client_scopes = MagicMock(return_value=realm_default_client_scopes)

        service_account_config = {
            "service_account": {"attribute_name": "voPersonID", "candidate": "id", "scope": "example.org"}
        }

        func_result = deployer_keycloak_oidc.deploy_to_keycloak(new_service, mock, service_account_config)
        self.assertEqual(func_result, (out_service, "a1a2a3a4-b5b6-c7c8-d9d0-testOidcId", "testOidcId"))

    # Test calling Keycloak to delete an entry
    def test_oidc_deploy_to_keycloak_delete(self):
        new_service = {
            "external_id": "a1a2a3a4-b5b6-c7c8-d9d0-testOidcId",
            "client_id": "testOidcId",
            "service_name": "testName",
            "service_description": "testDescription",
            "protocol": "oidc",
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

        mock = MagicMock()
        mock.delete_client = MagicMock(return_value=out_service)

        func_result = deployer_keycloak_oidc.deploy_to_keycloak(new_service, mock, "config")
        self.assertEqual(func_result, (out_service, "a1a2a3a4-b5b6-c7c8-d9d0-testOidcId", "testOidcId"))

    # Test calling Keycloak to update an entry
    def test_oidc_deploy_to_keycloak_update(self):
        new_service = {
            "external_id": "a1a2a3a4-b5b6-c7c8-d9d0-testOidcId",
            "client_id": "testOidcId",
            "service_name": "testName",
            "service_description": "testDescription",
            "protocol": "oidc",
            "contacts": [
                {"name": "name1", "email": "email1", "type": "technical"},
                {"name": "name2", "email": "email2", "type": "security"},
            ],
            "deployment_type": "edit",
            "scope": ["email", "eduperson_entitlement"],
        }
        out_service = {
            "response": {
                "attributes": {
                    "client_credentials.use_refresh_token": "false",
                    "contacts": "email1",
                    "oauth2.device.authorization.grant.enabled": "false",
                    "oauth2.token.exchange.grant.enabled": False,
                    "oidc.ciba.grant.enabled": "false",
                    "use.jwks.string": "false",
                    "use.jwks.url": "false",
                    "use.refresh.tokens": "false",
                },
                "consentRequired": False,
                "clientId": "testOidcId",
                "description": "testDescription",
                "id": "a1a2a3a4-b5b6-c7c8-d9d0-testOidcId",
                "protocol": "openid-connect",
                "implicitFlowEnabled": False,
                "name": "testName",
                "defaultClientScopes": ["example"],
                "publicClient": False,
                "serviceAccountsEnabled": False,
                "standardFlowEnabled": False,
                "optionalClientScopes": ["email", "profile"],
            },
            "status": 200,
        }
        realm_default_client_scopes = [
            {"id": "a1a2a3a4-b5b6-c7c8-d9d0-testScope7", "name": "example", "protocol": "openid-connect"}
        ]

        client_authz_permissions = {
            "response": {"enabled": False},
            "status": 200,
        }

        mock = MagicMock()
        mock.update_client = MagicMock(return_value=out_service)
        mock.get_realm_default_client_scopes = MagicMock(return_value=realm_default_client_scopes)
        mock.get_client_authz_permissions = MagicMock(return_value=client_authz_permissions)

        func_result = deployer_keycloak_oidc.deploy_to_keycloak(new_service, mock, "config")
        self.assertEqual(func_result, (out_service, "a1a2a3a4-b5b6-c7c8-d9d0-testOidcId", "testOidcId"))

    # Test update data with error when calling Keycloak
    def test_oidc_process_data_fail(self):
        new_msg = [
            {
                "id": 12,
                "client_id": "testOidcId",
                "service_name": "testName",
                "service_description": "testDescription",
                "contacts": [{"name": "name1", "email": "email1"}],
                "deployment_type": "create",
            }
        ]

        keycloak_config = {
            "auth_server": "https://example.com/auth",
            "realm": "example",
        }

        func_result = deployer_keycloak_oidc.process_data(new_msg, "", keycloak_config)
        self.assertEqual(
            func_result,
            [
                {
                    "attributes": {},
                    "data": {
                        "id": 12,
                        "status_code": 0,
                        "state": "error",
                        "error_description": "An error occurred while calling Keycloak",
                    },
                }
            ],
        )

    # Test update data calling Keycloak successfully
    def test_oidc_process_data_success(self):
        new_msg = [
            {
                "id": 12,
                "client_id": "testOidcId",
                "service_name": "testName",
                "service_description": "testDescription",
                "contacts": [{"name": "name1", "email": "email1"}],
                "deployment_type": "create",
            }
        ]
        deployer_keycloak_oidc.deploy_to_keycloak = MagicMock(
            return_value=({"status": 200}, "a1a2a3a4-b5b6-c7c8-d9d0-testOidcId", "testOidcId")
        )

        keycloak_config = {
            "auth_server": "https://example.com/auth",
            "realm": "example",
        }

        func_result = deployer_keycloak_oidc.process_data(new_msg, "token", keycloak_config)
        self.assertEqual(
            func_result,
            [
                {
                    "attributes": {},
                    "data": {
                        "id": 12,
                        "external_id": "a1a2a3a4-b5b6-c7c8-d9d0-testOidcId",
                        "status_code": 200,
                        "state": "deployed",
                        "client_id": "testOidcId",
                    },
                }
            ],
        )

    # Test the format is compatible with Keycloak
    def test_saml_format_keycloak_msg(self):
        new_message = {
            "entity_id": "https://example.org/testSamlId",
            "service_name": "testName",
            "service_description": "testDescription",
            "protocol": "saml",
            "metadata_url": "https://example.org/testSamlId/Shibboleth.sso/Metadata",
            "contacts": [
                {"name": "name1", "email": "email1", "type": "technical"},
                {"name": "name2", "email": "email2", "type": "security"},
            ],
            "requested_attributes": [
                {
                    "friendly_name": "uid",
                    "name": "urn:oid:uid",
                    "type": "custom",
                    "required": True,
                    "name_format": "urn:oasis:names:tc:SAML:2.0:attrname-format:uri",
                },
                {
                    "friendly_name": "voPersonID",
                    "name": "urn:oid:1.3.6.1.4.1.25178.4.1.6",
                    "type": "standard",
                    "required": True,
                    "name_format": "urn:oasis:names:tc:SAML:2.0:attrname-format:uri",
                },
            ],
        }
        out_message = {
            "attributes": {
                "contacts": "email1",
                "saml.auto.updated": "true",
                "saml.metadata.url": "https://example.org/testSamlId/Shibboleth.sso/Metadata",
                "saml.refresh.period": "3600",
                "saml.skip.requested.attributes": "true",
            },
            "clientId": "https://example.org/testSamlId",
            "consentRequired": True,
            "defaultClientScopes": ["example", "uid", "voPersonID"],
            "description": "testDescription",
            "name": "testName",
            "protocol": "saml",
            "protocolMappers": [
                {
                    "config": {
                        "attribute.name": "urn:oid:uid",
                        "attribute.nameformat": "URI Reference",
                        "friendly.name": "uid",
                        "user.attribute": "uid",
                    },
                    "name": "uid",
                    "protocol": "saml",
                    "protocolMapper": "saml-user-attribute-mapper",
                }
            ],
        }

        func_result = deployer_keycloak_saml.format_keycloak_msg(new_message, ["example"], {})
        self.assertEqual(func_result, out_message)

    # Test calling Keycloak to create a new entry
    def test_saml_deploy_to_keycloak_create(self):
        new_service = {
            "entity_id": "https://example.org/testSamlId",
            "service_name": "testName",
            "service_description": "testDescription",
            "protocol": "saml",
            "metadata_url": "https://example.org/testSamlId/Shibboleth.sso/Metadata",
            "contacts": [
                {"name": "name1", "email": "email1", "type": "technical"},
                {"name": "name2", "email": "email2", "type": "security"},
            ],
            "requested_attributes": [
                {
                    "friendly_name": "voPersonID",
                    "name": "urn:oid:1.3.6.1.4.1.25178.4.1.6",
                    "type": "standard",
                    "required": True,
                    "name_format": "urn:oasis:names:tc:SAML:2.0:attrname-format:uri",
                },
                {
                    "friendly_name": "uid",
                    "name": "urn:oid:uid",
                    "type": "custom",
                    "required": True,
                    "name_format": "urn:oasis:names:tc:SAML:2.0:attrname-format:uri",
                },
            ],
            "deployment_type": "create",
        }
        out_service = {
            "response": {
                "attributes": {
                    "contacts": "email1",
                    "saml.auto.updated": "true",
                    "saml.metadata.url": "https://example.org/testSamlId/Shibboleth.sso/Metadata",
                    "saml.refresh.period": "3600",
                    "saml.skip.requested.attributes": "true",
                },
                "clientId": "https://example.org/testSamlId",
                "consentRequired": True,
                "defaultClientScopes": [
                    "uid",
                    "voPersonID",
                ],
                "description": "testDescription",
                "id": "a1a2a3a4-b5b6-c7c8-d9d0-testSamlId",
                "name": "testName",
                "protocol": "saml",
                "protocolMappers": [
                    {
                        "config": {
                            "attribute.nameformat": "URI Reference",
                            "user.attribute": "uid",
                            "friendly.name": "uid",
                            "attribute.name": "urn:oid:uid",
                        },
                        "id": "65322a95-c6af-4097-a92c-96346dc2ba7b",
                        "name": "uid",
                        "protocol": "saml",
                        "protocolMapper": "saml-user-attribute-mapper",
                        "consentRequired": False,
                    },
                ],
            },
            "status": 201,
        }
        realm_default_client_scopes = [
            {"id": "a1a2a3a4-b5b6-c7c8-d9d0-testScope4", "name": "example", "protocol": "saml"}
        ]

        mock = MagicMock()
        mock.create_client = MagicMock(return_value=out_service)
        mock.get_client_by_id = MagicMock(return_value=out_service)
        mock.get_realm_default_client_scopes = MagicMock(return_value=realm_default_client_scopes)

        func_result = deployer_keycloak_saml.deploy_to_keycloak(new_service, mock, "config")
        self.assertEqual(
            func_result, (out_service, "a1a2a3a4-b5b6-c7c8-d9d0-testSamlId", "https://example.org/testSamlId")
        )

    # Test calling Keycloak to delete an entry
    def test_saml_deploy_to_keycloak_delete(self):
        new_service = {
            "external_id": "a1a2a3a4-b5b6-c7c8-d9d0-testSamlId",
            "entity_id": "https://example.org/testSamlId",
            "service_name": "testName",
            "service_description": "testDescription",
            "protocol": "saml",
            "metadata_url": "https://example.org/testSamlId/Shibboleth.sso/Metadata",
            "contacts": [
                {"name": "name1", "email": "email1", "type": "technical"},
                {"name": "name2", "email": "email2", "type": "security"},
            ],
            "requested_attributes": [
                {
                    "friendly_name": "voPersonID",
                    "name": "urn:oid:1.3.6.1.4.1.25178.4.1.6",
                    "type": "standard",
                    "required": True,
                    "name_format": "urn:oasis:names:tc:SAML:2.0:attrname-format:uri",
                },
                {
                    "friendly_name": "uid",
                    "name": "urn:oid:uid",
                    "type": "custom",
                    "required": True,
                    "name_format": "urn:oasis:names:tc:SAML:2.0:attrname-format:uri",
                },
            ],
            "deployment_type": "delete",
        }
        out_service = {
            "response": "OK",
            "status": 204,
        }

        mock = MagicMock()
        mock.delete_client = MagicMock(return_value=out_service)

        func_result = deployer_keycloak_saml.deploy_to_keycloak(new_service, mock, "config")
        self.assertEqual(
            func_result, (out_service, "a1a2a3a4-b5b6-c7c8-d9d0-testSamlId", "https://example.org/testSamlId")
        )

    # Test calling Keycloak to update an entry
    def test_saml_deploy_to_keycloak_update(self):
        new_service = {
            "external_id": "a1a2a3a4-b5b6-c7c8-d9d0-testSamlId",
            "entity_id": "https://example.org/testSamlId",
            "service_name": "testName",
            "service_description": "testDescription",
            "protocol": "saml",
            "metadata_url": "https://example.org/testSamlId/Shibboleth.sso/Metadata",
            "contacts": [
                {"name": "name1", "email": "email1", "type": "technical"},
                {"name": "name2", "email": "email2", "type": "security"},
            ],
            "requested_attributes": [
                {
                    "friendly_name": "voPersonID",
                    "name": "urn:oid:1.3.6.1.4.1.25178.4.1.6",
                    "type": "standard",
                    "required": True,
                    "name_format": "urn:oasis:names:tc:SAML:2.0:attrname-format:uri",
                },
                {
                    "friendly_name": "uid",
                    "name": "urn:oid:uid",
                    "type": "custom",
                    "required": True,
                    "name_format": "urn:oasis:names:tc:SAML:2.0:attrname-format:uri",
                },
            ],
            "deployment_type": "edit",
        }
        out_service = {
            "response": {
                "attributes": {
                    "contacts": "email1",
                    "saml.auto.updated": "true",
                    "saml.metadata.url": "https://example.org/testSamlId/Shibboleth.sso/Metadata",
                    "saml.refresh.period": "3600",
                    "saml.skip.requested.attributes": "true",
                },
                "clientId": "https://example.org/testSamlId",
                "consentRequired": True,
                "defaultClientScopes": [
                    "uid",
                    "voPersonID",
                ],
                "description": "testDescription",
                "id": "a1a2a3a4-b5b6-c7c8-d9d0-testSamlId",
                "name": "testName",
                "protocol": "saml",
                "protocolMappers": [
                    {
                        "config": {
                            "attribute.nameformat": "URI Reference",
                            "user.attribute": "uid",
                            "friendly.name": "uid",
                            "attribute.name": "urn:oid:uid",
                        },
                        "id": "65322a95-c6af-4097-a92c-96346dc2ba7b",
                        "name": "uid",
                        "protocol": "saml",
                        "protocolMapper": "saml-user-attribute-mapper",
                        "consentRequired": False,
                    },
                ],
            },
            "status": 201,
        }
        realm_default_client_scopes = [
            {"id": "a1a2a3a4-b5b6-c7c8-d9d0-testScope8", "name": "example", "protocol": "saml"}
        ]

        mock = MagicMock()
        mock.update_client = MagicMock(return_value=out_service)
        mock.get_realm_default_client_scopes = MagicMock(return_value=realm_default_client_scopes)

        func_result = deployer_keycloak_saml.deploy_to_keycloak(new_service, mock, "config")
        self.assertEqual(
            func_result, (out_service, "a1a2a3a4-b5b6-c7c8-d9d0-testSamlId", "https://example.org/testSamlId")
        )

    # Test update data with error when calling Keycloak
    def test_saml_process_data_fail(self):
        new_msg = [
            {
                "id": 12,
                "entity_id": "https://example.org/testSamlId",
                "metadata_url": "https://example.org/testSamlId/Shibboleth.sso/Metadata",
                "service_name": "testName",
                "service_description": "testDescription",
                "contacts": [{"name": "name1", "email": "email1"}],
                "protocol": "saml",
                "deployment_type": "create",
            }
        ]

        keycloak_config = {
            "auth_server": "https://example.com/auth",
            "realm": "example",
        }

        deployer_keycloak_saml.deploy_to_keycloak = MagicMock(return_value=())

        func_result = deployer_keycloak_saml.process_data(new_msg, "", keycloak_config)
        self.assertEqual(
            func_result,
            [
                {
                    "attributes": {},
                    "data": {
                        "id": 12,
                        "status_code": 0,
                        "state": "error",
                        "error_description": "An error occurred while calling Keycloak",
                    },
                }
            ],
        )

    # Test update data calling Keycloak successfully
    def test_saml_process_data_success(self):
        new_msg = [
            {
                "id": 12,
                "entity_id": "https://example.org/testSamlId",
                "metadata_url": "https://example.org/testSamlId/Shibboleth.sso/Metadata",
                "service_name": "testName",
                "service_description": "testDescription",
                "contacts": [{"name": "name1", "email": "email1"}],
                "protocol": "saml",
                "deployment_type": "create",
            }
        ]
        deployer_keycloak_saml.deploy_to_keycloak = MagicMock(
            return_value=({"status": 200}, "a1a2a3a4-b5b6-c7c8-d9d0-testSamlId", "https://example.org/testSamlId")
        )

        keycloak_config = {
            "auth_server": "https://example.com/auth",
            "realm": "example",
        }

        func_result = deployer_keycloak_saml.process_data(new_msg, "token", keycloak_config)
        self.assertEqual(
            func_result,
            [
                {
                    "attributes": {},
                    "data": {
                        "id": 12,
                        "external_id": "a1a2a3a4-b5b6-c7c8-d9d0-testSamlId",
                        "status_code": 200,
                        "state": "deployed",
                        "client_id": "https://example.org/testSamlId",
                    },
                }
            ],
        )
