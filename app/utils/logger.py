import logging
from pathlib import Path
def configure_logger(folder):
    Path(folder).mkdir(parents=True,exist_ok=True)
    logging.basicConfig(filename=Path(folder)/"app.log",level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    return logging.getLogger("systemsense")
