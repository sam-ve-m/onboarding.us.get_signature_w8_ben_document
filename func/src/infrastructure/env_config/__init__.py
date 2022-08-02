import os
import platform
from decouple import Config, RepositoryEnv, config
from heimdall_client.src.domain.responses_builder.builder import ResponsesBuilder
from heimdall_client.src.domain.exceptions.exceptions import InternalServerError


SYSTEM = platform.system()


def get_config(base_path: str) -> Config:
    path = os.path.join(base_path, "opt", "envs", "update_w8_form_confirmation", ".env")
    path = str(path)
    return Config(RepositoryEnv(path))


if SYSTEM == "Linux":
    config = get_config("/")
elif SYSTEM == "Darwin":
    config = get_config("/")
elif SYSTEM == "Windows":
    config = get_config("C:\\")
else:
    string_message = ResponsesBuilder.build_error_response(msg="Invalid OS")
    raise InternalServerError(string_message)
__all__ = ["config"]
