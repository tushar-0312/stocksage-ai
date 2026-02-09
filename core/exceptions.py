import sys


class StockSageException(Exception):
    """Custom exception with file and line tracking."""
    
    def __init__(self, error_message, error_details: sys):
        super().__init__(error_message)
        self.error_message = error_message
        _, _, exc_tb = error_details.exc_info()
        
        if exc_tb:
            self.lineno = exc_tb.tb_lineno
            self.file_name = exc_tb.tb_frame.f_code.co_filename
        else:
            self.lineno = "unknown"
            self.file_name = "unknown"
    
    def __str__(self):
        return f"Error in [{self.file_name}] line [{self.lineno}]: {self.error_message}"
