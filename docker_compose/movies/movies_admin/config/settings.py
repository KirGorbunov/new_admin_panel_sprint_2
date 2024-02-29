import os
from pathlib import Path

from split_settings.tools import include


# Include settings:
include(
    "components/common.py",  # standard django settings
    "components/database.py",  # postgres
)
