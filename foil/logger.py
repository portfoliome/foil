import json
import logging
import uuid
import time
from datetime import datetime

from foil.serializers import json_serializer


class JSONFormatter(logging.Formatter):

    converter = time.gmtime

    def format(self, record):

        event_dict = {
            'timestamp': datetime.utcfromtimestamp(record.created),
            'event_id': uuid.uuid4(),
            "name": record.name,
            "level": record.levelname,
            "message": record.msg,
            'pid': record.process,
            'thread': record.thread,
            'sourceFilePath': record.pathname,
            'module': record.module,
            'functionName': record.funcName,
            'lineNumber': record.lineno
        }

        return json.dumps(event_dict, default=json_serializer)
