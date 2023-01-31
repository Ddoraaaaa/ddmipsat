#!/usr/bin/env python3

from tests.maxCoverTest import checkTest

checkTest(10, 10, 0, 50, 'result.csv', False, 0)
checkTest(20, 20, 0, 50, 'result.csv', True, 0)
checkTest(30, 30, 0, 50, 'result.csv', True, 0)
checkTest(100, 100, 0, 50, 'result.csv', True, 0)