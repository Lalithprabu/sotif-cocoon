import logging

logging.basicConfig(
    filename="sotif_cocoon.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger("sotif_cocoon")