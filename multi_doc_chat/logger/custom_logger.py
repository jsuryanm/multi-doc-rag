import os 
import logging 
from datetime import datetime 
import structlog 
# structlog writes the log messages in json format

class CustomLogger:
    def __init__(self,log_dir = "logs"):
        self.logs_dir = os.path.join(os.getcwd(),log_dir)
        os.makedirs(self.logs_dir,exist_ok=True)
        log_file = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
        self.log_file_path = os.path.join(self.logs_dir,log_file)\
        
    
    def get_logger(self,name=__file__):
        # basename returns file name 
        logger_name = os.path.basename(name)

        file_handler = logging.FileHandler(self.log_file_path)
        # writes logs to file
        file_handler.setFormatter(logging.Formatter("%(message)s"))
        # only prints the message (doesnt have INFO:logger name: message) just message

        console_handler = logging.StreamHandler()
        # prints logs to terminal 
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(logging.Formatter("%(message)s"))

        logging.basicConfig(level=logging.INFO,
                            format="%(message)s",
                            handlers=[console_handler,file_handler])
        
        structlog.configure(
            processors=[
                structlog.processors.TimeStamper(fmt="iso", utc=True, key="timestamp"),
                structlog.processors.add_log_level,
                structlog.processors.EventRenamer(to="event"),
                structlog.processors.JSONRenderer()
            ],
            logger_factory=structlog.stdlib.LoggerFactory(),
            cache_logger_on_first_use=True,
        )

        return structlog.get_logger(logger_name)