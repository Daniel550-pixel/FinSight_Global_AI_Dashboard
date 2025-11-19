import logging
logging.basicConfig(filename='features/security/audit.log', level=logging.INFO)
def log_action(user, action):
    logging.info(f"{user} performed {action}")
