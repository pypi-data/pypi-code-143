import TDBRecord.command
import TDBRecord.m3u8
import TDBRecord.config

from prompt_toolkit import PromptSession, print_formatted_text
from streamlink import Streamlink
from pathlib import Path
import logging

streamlink = Streamlink()
psession = PromptSession()
input = psession.prompt
loglevel = logging.INFO

# Logging
class PromptHandler(logging.StreamHandler):
    def emit(self, record):
        msg = self.format(record)
        print_formatted_text(msg)

logger = logging.getLogger("TDBRecord")
logger.handlers = [PromptHandler()]
logger.handlers[0].setFormatter(logging.Formatter('[%(asctime)s] %(levelname)s # %(message)s'))
lm = "[{user}.{platform}] {msg}"
logger.setLevel(logging.INFO)

def create_logger(name: str, platform: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.handlers = [PromptHandler()]
    logger.handlers[0].setFormatter(logging.Formatter('[%(asctime)s] %(levelname)s - [{user}.{platform}] # %(message)s'.format(user=name, platform=platform)))
    logger.setLevel(loglevel)
    logger.propagate = False
    return logger

def create_data(user: str, platform: str, thread) -> dict:
    return {
        "exit": False,
        "logger": create_logger(user, platform),
        "thread": thread,
    }

conf = {}
data = {}
downloadPath = Path(".")

""" data
{
    "user.platform": {
        "exit": false,
        "logger": logger,
    }
}
"""
