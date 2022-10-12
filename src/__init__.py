# For the module to work
import logging

logging.basicConfig(format="%(name)s - %(levelname)s: %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

f_handler = logging.FileHandler("logs.log")
f_handler.setLevel(logging.ERROR)
f_format = logging.Formatter("%(asctime)s: %(name)s - %(levelname)s: %(message)s")
f_handler.setFormatter(f_format)
logger.addHandler(f_handler)
