import logging
import os


class AppLogger:

    @staticmethod
    def get_logger():
        os.makedirs("logs", exist_ok=True)

        logger = logging.getLogger("ecommerce")
        logger.setLevel(logging.INFO)

        if not logger.handlers:
            handler = logging.FileHandler(
                "logs/ecommerce.log",
                encoding="utf-8"
            )

            formatter = logging.Formatter(
                "%(asctime)s - %(levelname)s - %(message)s"
            )

            handler.setFormatter(formatter)
            logger.addHandler(handler)

        return logger
