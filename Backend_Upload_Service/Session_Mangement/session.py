import secrets
from datetime import datetime, timedelta

def generateSessionToken():
  return secrets.token_hex(32)

def generateValidationTime():
  return datetime.now() + timedelta(days=10)

def generateSessionName():
  return secrets.token_hex(16)