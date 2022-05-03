
import os
from .constants import Constants
from wush.cli import run as wush_run


def run_in_shell(module: str, request: str, params: dict = None, **kwargs):
    """wush run"""
    wush_run.run_in_shell( module, request, params = params, **kwargs)

