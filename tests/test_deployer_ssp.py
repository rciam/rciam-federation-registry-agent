#!/usr/bin/env python3

import json
import unittest
import types
import os
import importlib.machinery
import filecmp
import requests
import subprocess
from unittest.mock import MagicMock, Mock

def get_resource_path(relative_path):
    return os.path.join(os.path.dirname(__file__), relative_path)

# load standalone script as module
loader = importlib.machinery.SourceFileLoader('deployer_ssp', get_resource_path('../bin/deployer_ssp'))
deployer_ssp = types.ModuleType(loader.name)
loader.exec_module(deployer_ssp)

class TestDeployerSsp(unittest.TestCase):

    # Test that a creation adds a new enty in the data array
    def test_update_data_create(self):
        services = [{"registry_service_id": "testId1", "whitelist": ["testEntityId1"], "src": "TestMetadataUrl1"}]
        new_service = [{"id": "testId2", "entity_id": "testEntityId2", "deployment_type": "create", "metadata_url": "TestMetadataUrl2"}]
        test_case_result = [{"registry_service_id": "testId1", "whitelist": ["testEntityId1"], "src": "TestMetadataUrl1"}, \
            {"registry_service_id": "testId2", "whitelist": ["testEntityId2"], "src": "TestMetadataUrl2"}]

        func_result = deployer_ssp.update_data(services, new_service)
        self.assertEqual(func_result, test_case_result)

    # Test that a creation of an existing enty do not alter the data array
    def test_update_data_double_create(self):
        services = [{"registry_service_id": "testId1", "whitelist": ["testEntityId1"], "src": "TestMetadataUrl1"}]
        new_service = [{"id": "testId2", "entity_id": "testEntityId2", "deployment_type": "create", "metadata_url": "TestMetadataUrl2"}]
        test_case_result = [{"registry_service_id": "testId1", "whitelist": ["testEntityId1"], "src": "TestMetadataUrl1"}, \
            {"registry_service_id": "testId2", "whitelist": ["testEntityId2"], "src": "TestMetadataUrl2"}]

        func_result = deployer_ssp.update_data(services, new_service)
        func_result = deployer_ssp.update_data(func_result, new_service)
        self.assertEqual(func_result, test_case_result)

    # Test that an edit to an entry alters the data array
    def test_update_data_update(self):
        services = [{"registry_service_id": "testId1", "whitelist": ["testEntityId1"], "src": "TestMetadataUrl1"}, \
            {"registry_service_id": "testId2", "whitelist": ["testEntityId2"], "src": "TestMetadataUrl2"}]
        update_service = [{"id": "testId2", "entity_id": "testEntityId2", "deployment_type": "edit", "metadata_url": "TestMetadataUrlEDIT"}]
        test_case_result = [{"registry_service_id": "testId1", "whitelist": ["testEntityId1"], "src": "TestMetadataUrl1"}, \
            {"registry_service_id": "testId2", "whitelist": ["testEntityId2"], "src": "TestMetadataUrlEDIT"}]

        func_result = deployer_ssp.update_data(services, update_service)
        self.assertEqual(func_result, test_case_result)

    # Test that a deletion removes the entry from the data array
    def test_update_data_delete(self):
        services = [{"registry_service_id": "testId1", "whitelist": ["testEntityId1"], "src": "TestMetadataUrl1"}, \
            {"registry_service_id": "testId2", "whitelist": ["testEntityId2"], "src": "TestMetadataUrl2"}]
        delete_service = [{"id": "testId2", "entity_id": "testEntityId2", "deployment_type": "delete", "metadata_url": "TestMetadataUrl2"}]
        test_case_result = [{"registry_service_id": "testId1", "whitelist": ["testEntityId1"], "src": "TestMetadataUrl1"}]

        func_result = deployer_ssp.update_data(services, delete_service)
        self.assertEqual(func_result, test_case_result)

    # Test that a deletion of a non existing entry does not alters the data array
    def test_update_data_double_delete(self):
        services = [{"registry_service_id": "testId1", "whitelist": ["testEntityId1"], "src": "TestMetadataUrl1"}, \
            {"registry_service_id": "testId2", "whitelist": ["testEntityId2"], "src": "TestMetadataUrl2"}]
        delete_service = [{"id": "testId2", "entity_id": "testEntityId2", "deployment_type": "delete", "metadata_url": "TestMetadataUrl2"}]
        test_case_result = [{"registry_service_id": "testId1", "whitelist": ["testEntityId1"], "src": "TestMetadataUrl1"}]

        func_result = deployer_ssp.update_data(services, delete_service)
        func_result = deployer_ssp.update_data(func_result, delete_service)
        self.assertEqual(func_result, test_case_result)

    # Verify the generated php config
    def test_generate_config(self):
        services = [{"registry_service_id": "testId1", "whitelist": ["testEntityId1"], "src": "TestMetadataUrl1"}, \
            {"registry_service_id": "testId2", "whitelist": ["testEntityId2"], "src": "TestMetadataUrl2"}]
        deployer_ssp.generate_config(services,'./test_file.php') 
        self.assertTrue(filecmp.cmp('./test_file.php',get_resource_path('./files/ssp_config.php')), 'You error message')

    # Call ssp syncer with 200 http response
    def test_call_ssp_syncer_positive(self):
        mock = Mock()
        mock.status_code = 200
        mock.return_value.raise_for_status = None
        mock.json = MagicMock(return_value='')
        mock_req = requests
        mock_req.get = MagicMock(return_value=mock)
        func_result = deployer_ssp.call_ssp_syncer('test_url', 'key', 60, 'hourly')
        self.assertEqual(func_result['status'],200)

    # Call ssp syncer with 400 http response
    def test_call_ssp_syncer_negative(self):
        mock = Mock()
        mock.status_code = 400
        mock.return_value.raise_for_status = Exception('ERROR')
        mock.json = MagicMock(return_value='ERROR')
        mock_req = requests
        mock_req.get = MagicMock(return_value=mock)
        func_result = deployer_ssp.call_ssp_syncer('test_url', 'key', 60, 'hourly')
        self.assertEqual(func_result['status'],400)

    # Test reading from php configuration file
    def test_get_services_from_conf(self):
        mock_sub = subprocess
        ret = subprocess.CompletedProcess
        ret.stdout = '[{"id":11}]'
        mock_sub.run = MagicMock(return_value=ret)
        self.assertEqual(deployer_ssp.get_services_from_conf(''),[{"id":11}])
    
    # Test reading from php configuration file with return value that is not list
    def test_get_services_from_conf_fail(self):
        mock_sub = subprocess
        ret = subprocess.CompletedProcess
        ret.stdout = '{"id":11}'
        mock_sub.run = MagicMock(return_value=ret)
        with self.assertRaises(SystemExit):
            deployer_ssp.get_services_from_conf('')
