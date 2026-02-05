import secrets

def generate_otp():
    return f"{secrets.randbelow(10000):04d}"
