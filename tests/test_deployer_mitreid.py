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

class TestDeployerSsp(unittest.TestCase):

    def test_format_mitreid_msg(self):
        new_service = {"client_id": "testId1", "service_name": "testName1", "service_description": "testDescription1", "contacts":[{"name": "name1", "email":"email1"}]}
        out_service = {"clientId": "testId1", "clientName": "testName1", "clientDescription": "testDescription1", "contacts":["email1"]}
        func_result = deployer_mitreid.format_mitreid_msg(new_service)
        self.assertEqual(func_result, out_service)

    def test_call_mitreid(self):
        new_service = {"client_id": "testId1", "service_name": "testName1", "service_description": "testDescription1", "contacts":[{"name": "name1", "email":"email1"}]}
        out_service = {"clientId": "testId1", "clientName": "testName1", "clientDescription": "testDescription1", "contacts":["email1"]}
        func_result = deployer_mitreid.format_mitreid_msg(new_service)
        self.assertEqual(func_result, out_service)



        
