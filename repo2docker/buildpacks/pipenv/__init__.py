"""Generates Dockerfiles based on Pipfiles"""

import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))

class PipenvBuildPack()