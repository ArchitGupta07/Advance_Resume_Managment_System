import logging
import sys

class StreamToLogger(object):
   """
   Fake file-like stream object that redirects writes to a logger instance.
   """
   def __init__(self, logger, stream=sys.stdout, log_level=logging.INFO):
      self.logger = logger
      self.stream = stream
      self.log_level = log_level
      self.linebuf = ''

   def write(self, buf):
      self.stream.write(buf)
      #self.logger.log(self.log_level, repr(buf))
      self.linebuf += buf
      if buf=='\n':
          self.flush()

   def flush(self):
      #Flush all handlers
      for line in self.linebuf.rstrip().splitlines():
         self.logger.log(self.log_level, line.rstrip())
      self.linebuf = ''
      self.stream.flush()
      for handler in self.logger.handlers:
          handler.flush()

def dual_log(*args, **kwargs):
    """
    Converts all print, raise statements to log to a file
    This function accepts all arguments to logging.basicConfig()
    """
    logging.basicConfig( *args, **kwargs)

    stdout_logger = logging.getLogger('STDOUT')
    sl = StreamToLogger(stdout_logger, sys.stdout, logging.INFO)
    sys.stdout = sl

    stderr_logger = logging.getLogger('STDERR')
    sl = StreamToLogger(stderr_logger, sys.stderr, logging.ERROR)
    sys.stderr = sl



def logger():
   dual_log(
        level=logging.DEBUG,
        format="%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s",
        filename="out.log",
        filemode='a'
    )

from time import sleep
print("Test to standard out")
sleep(1)
print("Test to standard out")
sleep(1)
print("Test to standard out")
sleep(1)
print("Test to standard out")
sleep(1)
print("Test to standard out")
sleep(1)
raise Exception('Test to standard error')
