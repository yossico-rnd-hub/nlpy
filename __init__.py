from .api.server import NlpyServer
from .nlp import Nlp
from .logger import logger

name = "nlpy"

__all__ = [
    "logger",
    "NlpyServer",
    "Nlp",
]
