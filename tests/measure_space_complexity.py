import inspect
import os
import sys
import unittest

current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

import pm4py

pm4py.util.constants.SHOW_PROGRESS_BAR = True
pm4py.util.constants.SHOW_EVENT_LOG_DEPRECATION = False
pm4py.util.constants.SHOW_INTERNAL_WARNINGS = False
pm4py.util.constants.MEASURE_SPACE_COMPLEXITY = True
# pm4py.util.constants.DEFAULT_TIMESTAMP_PARSE_FORMAT = None


loader = unittest.TestLoader()
suite = unittest.TestSuite()

from tests.space_complexity_test import SpaceComplexityMeasurements

suite.addTests(loader.loadTestsFromTestCase(SpaceComplexityMeasurements))


def main():
    runner = unittest.TextTestRunner()
    runner.run(suite)


if __name__ == "__main__":
    main()
