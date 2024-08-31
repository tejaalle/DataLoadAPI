import logging
import uuid
class ContextFilter(logging.Filter):
    def __init__(self, run_id=None):
        super().__init__()
        self.runid = run_id or str(uuid.uuid4())

    def filter(self, record):
        record.runid = self.runid or str(uuid.uuid4())
        return True