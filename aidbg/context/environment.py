import platform
import sys

def get_environment_info() -> str:
    return (
        f"Python: {sys.version.split()[0]}\n"
        f"OS: {platform.system()} {platform.release()}"
    )
