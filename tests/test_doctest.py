import unittest
import doctest

import dimstack.eval
import dimstack.stats
import dimstack.tolerance
import dimstack.utils


def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(dimstack.eval))
    tests.addTests(doctest.DocTestSuite(dimstack.stats))
    tests.addTests(doctest.DocTestSuite(dimstack.tolerance))
    tests.addTests(doctest.DocTestSuite(dimstack.utils))

    return tests


if __name__ == "__main__":
    unittest.main()
