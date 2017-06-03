""" Init file for tests sub module. """
import unittest

from . import models_tests


def suite():
    """ Function required to load tests in sub directory. """
    tests_loader = unittest.TestLoader().loadTestsFromModule
    test_suites = []
    test_suites.append(tests_loader(models_tests))
    return unittest.TestSuite(test_suites)
