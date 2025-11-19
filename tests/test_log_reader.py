from src.log_reader import LogReader

def test_read_errors_return_type():
    reader = LogReader()
    errors = reader.read_errors("logs/sample.log")
    assert isinstance(errors, list)
