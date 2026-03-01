ACCEPTED_DOMAINS = [
    'gmail.com', 'yahoo.com', 'yandex.com', 'outlook.com', 'email.com'
]

def check_email_domain(email):
    temp = email.split('@')
    domain = temp[1]

    if domain not in ACCEPTED_DOMAINS:
        return True
    else:
        False
