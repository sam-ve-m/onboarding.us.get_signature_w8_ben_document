# STANDARD IMPORTS
import os
import platform
from decouple import Config, RepositoryEnv

config = None
SYSTEM = platform.system()


def get_config(base_path: str) -> Config:
    path = os.path.join(base_path, "opt", "envs", "update_w8_form_confirmation", ".env")
    path = str(path)
    return Config(RepositoryEnv(path))


if SYSTEM == "Linux":
    config = get_config("/")
elif SYSTEM == "Windows":
    config = get_config("C:/")
else:
    raise Exception("Unsupported system")

__all__ = ["config"]
