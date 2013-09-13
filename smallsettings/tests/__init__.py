import unittest
import logging

from smallsettings.tests import settings
from smallsettings.tests import factory

all_test_cases = [
    settings.SettingsTest,
    settings.PathsTest,
    settings.MergedTest,

    factory.FactoryTest,
]


def get_all_test_suite():
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)-15s:%(message)s", filename='test.log')
    logging.getLogger('smallsettings').info('\n\t*** TESTING STARTED ***')
    suite = unittest.TestLoader()
    prepered_all_test_cases = []
    for test_case in all_test_cases:
        prepered_all_test_cases.append(
            suite.loadTestsFromTestCase(test_case)
        )
    return unittest.TestSuite(prepered_all_test_cases)
