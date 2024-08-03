import sys


def error_message_detail(error, error_detail: sys):
    _, _, exc_tb = error_detail.exc_info()
    file_name = exc_tb.tb_frame.f_code.co_filename
    line_number = exc_tb.tb_lineno
    return f"Error happend in: {file_name} & the line is: {line_number} & the message is: {error}"


class CustomizedException(Exception):
    def __init__(self, message, error_code: sys):
        super().__init__(message)
        self.error_code = error_code
        self.message = error_message_detail(message, error_code)

    def __str__(self) -> str:
        return self.message
