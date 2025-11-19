import re
from typing import List
import logging


class LogReader:
    """
    Reads log files and extracts lines containing the keyword 'ERROR'.

    Methods
    -------
    read_errors(file_path: str) -> list[str]
        Reads a log file and returns all lines classified as errors.
    """

    ERROR_PATTERN = re.compile(
        r"(ERROR|CRITICAL|EXCEPTION|FAIL|FATAL)", re.IGNORECASE
    )

    def read_errors(self, file_path: str) -> List[str]:
        """
        Reads a log file and returns all lines that contain known error markers.

        Parameters
        ----------
        file_path : str
            Path to the log file.

        Returns
        -------
        List[str]
            A list of log lines containing error keywords.

        Raises
        ------
        FileNotFoundError
            If the file does not exist.
        """

        errors: List[str] = []

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                for line in f:
                    if self.ERROR_PATTERN.search(line):
                        errors.append(line.strip())
        except FileNotFoundError as e:
            raise FileNotFoundError(f"Log file not found: {file_path}") from e
        logging.info(f"Extracted {len(errors)} errors from file: {file_path}")
        return errors
