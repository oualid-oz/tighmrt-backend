import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    handlers=[logging.FileHandler("logs/log.txt"), logging.StreamHandler()]
)

logger = logging.getLogger(__name__)
