import logging
import os

# Garante que a pasta de logs exista
os.makedirs("logs", exist_ok=True)

#Configure logging configuration and format
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler('logs/app.log') # Outputs to the file log.txt
                    ])


# Export the logging object
log = logging.getLogger(__name__)
