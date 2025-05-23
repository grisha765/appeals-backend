import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from appeals.core.init import run_server
from appeals.config.config import Config
from appeals.config import logging_config
logging = logging_config.setup_logging(__name__)

logging.info(f"Script initialization, logging level: {Config.log_level}")


if __name__ == '__main__':
    run_server()
