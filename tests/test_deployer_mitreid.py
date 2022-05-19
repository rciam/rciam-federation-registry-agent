#!/usr/bin/env python3

import json
import unittest
import types
import os
import importlib.machinery
import filecmp
import requests
from unittest.mock import MagicMock, Mock

def get_resource_path(relative_path):
    return os.path.join(os.path.dirname(__file__), relative_path)

# load standalone script as module
loader = importlib.machinery.SourceFileLoader('deployer_mitreid', get_resource_path('../bin/deployer_mitreid'))
deployer_mitreid = types.ModuleType(loader.name)
loader.exec_module(deployer_mitreid)

class TestDeployerMitreid(unittest.TestCase):

    # Test the format is compatible with mitreid
    def test_format_mitreid_msg(self):
        new_service = {"client_id": "testId1", "service_name": "testName1", "service_description": "testDescription1", "contacts":[{"name": "name1", "email":"email1", "type": "technical"},{"name": "name2", "email":"email2", "type": "security"}]}
        out_service = {"clientId": "testId1", "clientName": "testName1", "clientDescription": "testDescription1", "contacts":["email1"]}

        func_result = deployer_mitreid.format_mitreid_msg(new_service,'create')
        self.assertEqual(func_result, out_service)

    # Test calling mitre id to create a new entry
    def test_call_mitreid_create(self):
        new_service = {"client_id": "testId1", "service_name": "testName1", "service_description": "testDescription1", "contacts":[{"name": "name1", "email":"email1", "type": "technical"},{"name": "name2", "email":"email2", "type": "security"}], "deployment_type": "create"}
        out_service = {"response": {"id": "12","clientId": "testId1", "clientName": "testName1", "clientDescription": "testDescription1", "contacts":["email1"]}, "status": 200}

        mock = Mock()
        mock.createClient = MagicMock(return_value=out_service)

        func_result = deployer_mitreid.call_mitreid(new_service,mock)
        self.assertEqual(func_result, (out_service,"12", 'testId1'))

    # Test calling mitre id to delete an entry
    def test_call_mitreid_delete(self):
        new_service = {"external_id": "12", "client_id": "testId1", "service_name": "testName1", "service_description": "testDescription1", "contacts":[{"name": "name1", "email":"email1", "type": "technical"},{"name": "name2", "email":"email2", "type": "security"}], "deployment_type": "delete"}
        out_service = {"response": {"id": "12","clientId": "testId1", "clientName": "testName1", "clientDescription": "testDescription1", "contacts":["email1"]}, "status": 200}

        mock = Mock()
        mock.deleteClientById = MagicMock(return_value=out_service)

        func_result = deployer_mitreid.call_mitreid(new_service,mock)
        self.assertEqual(func_result, (out_service,"12",''))

    # Test calling mitre id to update an entry
    def test_call_mitreid_update(self):
        new_service = {"external_id": "12", "client_id": "testId1", "service_name": "testName1", "service_description": "testDescription1", "contacts":[{"name": "name1", "email":"email1", "type": "technical"},{"name": "name2", "email":"email2", "type": "security"}], "deployment_type": "edit"}
        out_service = {"response": {"id": "12","clientId": "testId1", "clientName": "testName1", "clientDescription": "testDescription1", "contacts":["email1"]}, "status": 200}

        mock = Mock()
        mock.updateClientById = MagicMock(return_value=out_service)

        func_result = deployer_mitreid.call_mitreid(new_service,mock)
        self.assertEqual(func_result, (out_service,"12", 'testId1'))

    # Test update data with error when calling mitreid
    def test_update_data_fail(self):
        new_msg = [{"id": "12", "client_id": "testId1", "service_name": "testName1", "service_description": "testDescription1", "contacts":[{"name": "name1", "email":"email1"}], "deployment_type": "create"}]

        func_result = deployer_mitreid.update_data(new_msg,'','',1)
        self.assertEqual(func_result, [{'attributes':{},'data': {"id":"12","agent_id":1,"status_code": 0, "state": "error", "error_description": "An error occurred while calling mitreId"}}])

    # Test update data calling mitreid successfully
    def test_update_data_success(self):
        new_msg = [{"id": "12", "client_id": "testId1", "service_name": "testName1", "service_description": "testDescription1", "contacts":[{"name": "name1", "email":"email1"}], "deployment_type": "create"}]
        deployer_mitreid.call_mitreid = MagicMock(return_value=({'status':200},"12", 'testId1'))

        func_result = deployer_mitreid.update_data(new_msg,'url','token',1)
        self.assertEqual(func_result, [{'attributes':{},'data': {"id":"12","external_id": "12","agent_id":1,"status_code": 200, "state": "deployed", "client_id": "testId1"}}])

        
