import os
def check_password(input_password):
    correct_password = os.getenv("FIN_SIGHT_PASS","changeme")
    return input_password == correct_password
