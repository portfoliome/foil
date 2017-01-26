import json
import unittest
from logging import INFO, LogRecord

from foil.logger import JSONFormatter


class TestLogFormatter(unittest.TestCase):
    def test_json_formatter(self):
        name = 'name'
        line = 42
        module = 'some_module'
        func = 'some_function'
        msg = {'content': 'sample log'}

        log_record = LogRecord(
            name, INFO, module, line, msg, None, None, func=func
        )
        formatter = JSONFormatter()

        log_result = formatter.format(log_record)
        result = json.loads(log_result)

        # check some of the fields to ensure json formatted correctly
        self.assertEqual(name, result['name'])
        self.assertEqual(line, result['lineNumber'])
        self.assertEqual(func, result['functionName'])
        self.assertEqual(module, result['module'])
        self.assertEqual('INFO', result['level'])
        self.assertEqual(msg, result['message'])
