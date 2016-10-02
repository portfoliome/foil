import os
from contextlib import closing


def set_env_file(path: str):
    try:
        for env_key, env_value in read_dotenv(path):
            os.environ.setdefault(env_key, env_value)
    except FileNotFoundError:
        pass


def read_dotenv(dotenv_path: str):
    with closing(open(dotenv_path, 'r')) as file:
        for line in file:
            line = line.rstrip(os.linesep)

            if not line or line.startswith('#') or '=' not in line:
                continue

            env_key, env_value = line.split('=', 1)
            env_value = env_value.strip("'").strip('"')
            yield env_key, env_value
