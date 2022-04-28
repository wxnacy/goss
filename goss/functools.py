
from .constants import Constants

def wush_run_in_shell(command: str):
    """wush run"""

    cmd = f"wush run --config {Constants.CONFIG_PATH} {command}"
    os.system(cmd)

