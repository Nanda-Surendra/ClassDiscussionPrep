#Imports the os module, which provides functions for interacting with the operating system 
# (like reading environment variables, file paths, etc.).
import os
#Imports the dotenv module, which allows loading environment variables from a .env file.
from dotenv import load_dotenv
#Imports the pathlib module, which provides a way to work with file paths in a platform-independent manner.
from pathlib import Path

# Load .env from root directory (parent of web_apis)
env_path = Path(__file__).parent.parent / '.env'
#Loads the environment variables from the .env file into the environment variables of the current process.
load_dotenv(dotenv_path=env_path)

print(env_path)
print(os.getenv("DB_SERVER"))
print(os.getenv("DB_DATABASE"))
print(os.getenv("DB_USERNAME"))
print(os.getenv("DB_PASSWORD"))