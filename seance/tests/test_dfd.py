import unittest, os
from unittest.mock import patch, MagicMock
from seance.dfd import update_dfd, create_dfd, param


class TestDFD(unittest.TestCase):

    def tearDown(self):
        # Remove the file after the test
        if os.path.exists("media/test_dfd.png"):
            os.remove("media/test_dfd.png")

    def test_create_dfd(self):
        """ Tests if a dfd is created """

        param.multi_admin = True
        param.employee = True
        param.multi_employee = False
        param.remote_employee = True
        param.multi_computer = True
        param.onprem_setup = True
        param.cloud_setup = False
        param.saas = False
        param.iot = True
        param.hosted_webapp = False
        param.remote_webapp = True
        param.waf = False
        param.wifi_share = True
        param.firewall = True
        param.website = True

        # Call the function under test
        create_dfd("test_dfd")

        # Check if the file exists in the media folder
        self.assertTrue(os.path.exists("media/test_dfd.png"))

    @patch("seance.dfd.param")
    def test_update_dfd(self, param_mock):
        """ Tests if DFD parameters are updated correctly """

        # Set up mock parameters
        param_mock.multi_admin = False
        param_mock.employee = False
        param_mock.multi_employee = False
        param_mock.remote_employee = False
        param_mock.multi_computer = False
        param_mock.onprem_setup = False
        param_mock.cloud_setup = False
        param_mock.saas = False
        param_mock.iot = False
        param_mock.hosted_webapp = False
        param_mock.remote_webapp = False
        param_mock.waf = False
        param_mock.wifi_share = False
        param_mock.firewall = False
        param_mock.website = False


        # Call the function under test
        update_dfd(10400, "No")
        update_dfd(20100, 4)
        update_dfd(20200, "Yes")
        update_dfd(30100, 2)
        update_dfd(30300, "Yes")
        update_dfd(30400, "No")
        update_dfd(30500, "No")
        update_dfd(30600, "Yes")
        update_dfd(31900, "Yes")
        update_dfd(31901, "Yes")
        update_dfd(31903, "Yes")
        update_dfd(50300, "Yes")
        update_dfd(60100, "Yes")

        # Assert parameter values
        self.assertTrue(param_mock.multi_admin)
        self.assertFalse(param_mock.employee)
        self.assertTrue(param_mock.multi_employee)
        self.assertTrue(param_mock.remote_employee)
        self.assertTrue(param_mock.multi_computer)
        self.assertTrue(param_mock.onprem_setup)
        self.assertFalse(param_mock.cloud_setup)
        self.assertFalse(param_mock.saas)
        self.assertTrue(param_mock.iot)
        self.assertFalse(param_mock.hosted_webapp)
        self.assertTrue(param_mock.remote_webapp)
        self.assertTrue(param_mock.waf)
        self.assertTrue(param_mock.wifi_share)
        self.assertTrue(param_mock.firewall)
        self.assertTrue(param_mock.website)