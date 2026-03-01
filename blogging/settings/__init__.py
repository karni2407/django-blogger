from dotenv import load_dotenv
import os

load_dotenv()

env = os.environ

check_env = os.getenv("ENV")
print(check_env)

if check_env == "prod":
    from .prod import *
else:
    from .dev import *