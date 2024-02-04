from dataclasses import dataclass
from dotenv import load_dotenv
import os
from typing import Final

load_dotenv()
@dataclass(slots=True)
class Constants:
    AVG_CPU_CORES : Final[int]     = int(os.getenv('AVG_CPU_CORES'))
    MAX_CPU_CORES : Final[int]     = int(os.getenv('MAX_CPU_CORES'))
    MAX_PANDAS_FETCH : Final[int]  = int(os.getenv('MAX_PANDAS_FETCH'))
    OUTPUT_FILE_PATH : str         = os.getenv('OUTPUT_FILE_PATH')
    MAX_ROWS_PER_FILE : Final[int] = int(os.getenv('MAX_ROWS_PER_FILE'))
    DB_HOST : str                  = os.getenv('DB_HOST')
    DB_USER : str                  = os.getenv('DB_USER')
    DB_PASSWORD : str              = os.getenv('DB_PASSWORD')
    DB_NAME : str                  = os.getenv('DB_NAME')
    DB_TABLE : str                 = os.getenv('DB_TABLE')

# creating object to be used in app.
constants : Constants = Constants()