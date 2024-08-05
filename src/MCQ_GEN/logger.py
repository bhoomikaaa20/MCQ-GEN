import logging
import os
from datetime import datetime

# Create a log file name with a timestamp
log_file = f"{datetime.now().strftime('%m_%d_%y_%H_%M_%S')}.log"

# Define the path for the logs directory
log_path = os.path.join(os.getcwd(), "logs")

# Create the logs directory if it does not exist
os.makedirs(log_path, exist_ok=True)

# Define the full path for the log file
log_file_path = os.path.join(log_path, log_file)

# Configure logging
logging.basicConfig(
    level=logging.INFO,  # Set the logging level to INFO
    filename=log_file_path,  # Log to the file at the specified path
    format="[%(asctime)s] %(lineno)d -%(name)s - %(levelname)s - %(message)s"  # Define the log message format
)
