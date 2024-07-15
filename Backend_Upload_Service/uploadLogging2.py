import logging
import sys

class StreamToLogger(object):
    """
    Fake file-like stream object that redirects writes to a logger instance.
    """
    def __init__(self, logger, log_level=logging.INFO):
      self.logger = logger
      self.log_level = log_level
      self.linebuf = ''
    
    def flush(self):
        pass
   
    def write(self, buf):
      for line in buf.rstrip().splitlines():
         self.logger.log(self.log_level, line.rstrip())
    
    def isatty(self):
       pass

def upload_logging():
    logging.basicConfig(
        level=logging.WARNING,
        format='%(asctime)s:%(levelname)s:%(name)s:%(message)s',
        filename="out.log",
        filemode='a'
    )

stdout_logger = logging.getLogger('STDOUT')
stdout_logger.setLevel(logging.INFO) 
sl = StreamToLogger(stdout_logger, logging.INFO)
sys.stdout = sl

stderr_logger = logging.getLogger('STDERR')
stderr_logger.setLevel(logging.ERROR) 
sl = StreamToLogger(stderr_logger, logging.ERROR)
sys.stderr = sl

upload_logging()

print("Test to standard out")

print("Test to standard out")
print("Test to standard out")
# raise Exception('Test to standard error')