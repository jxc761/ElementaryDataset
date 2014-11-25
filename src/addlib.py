import sys
import os.path
import inspect

script_dir = os.path.abspath(os.path.dirname(__file__))
root_dir = os.path.dirname(script_dir)

sys.path.append(os.path.join(root_dir, "lib"))


