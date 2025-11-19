import re

class LogReader:
    """
    Reads log files and extracts lines that contain errors or critical events.
    """

    ERROR_PATTERN = re.compile(r"(ERROR|CRITICAL|EXCEPTION|FAIL|FATAL)", re.IGNORECASE)

    def read_errors(self, file_path):
        """
        Reads a log file and returns all lines matching the error pattern.
        """
        errors = []

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                for line in f:
                    if self.ERROR_PATTERN.search(line):
                        errors.append(line.strip())
        except FileNotFoundError:
            raise FileNotFoundError(f"Log file not found: {file_path}")

        return errors
