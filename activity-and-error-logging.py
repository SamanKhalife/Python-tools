import logging
from logging.handlers import RotatingFileHandler

handler = RotatingFileHandler('activity_errors.log', maxBytes=2000, backupCount=5)
console_handler = logging.StreamHandler()

logging.basicConfig(handlers=[handler, console_handler], level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def log_activity(user_id, action):
    """لاگ فعالیت کاربر."""
    logging.info(f'User {user_id} performed action: {action}')

def log_warning(message):
    """ثبت هشدار."""
    logging.warning(f'Warning: {message}')

def log_debug(message):
    """ثبت لاگ در سطح دیباگ."""
    logging.debug(f'Debug: {message}')

def log_error(message):
    """ثبت خطا."""
    logging.error(f'Error: {message}')

def get_user_input():
    """پرسش از کاربر برای اطلاعات."""
    user_id = input("Enter user ID: ")
    action = input("Enter user action (e.g., 'logged in'): ")
    warning_message = input("Enter a warning message (optional): ")
    debug_message = input("Enter a debug message (optional): ")
    error_message = input("Enter an error message (optional): ")
    return user_id, action, warning_message, debug_message, error_message

def main():
    """دریافت ورودی از کاربر و ثبت در لاگ."""
    user_id, action, warning_message, debug_message, error_message = get_user_input()

    log_activity(user_id, action)

    if warning_message:
        log_warning(warning_message)

    if debug_message:
        log_debug(debug_message)

    if error_message:
        log_error(error_message)

if __name__ == "__main__":
    main()
