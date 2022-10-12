from src.main import start_program
import os
import sys

# Update the current working directory to always work with relative imports
# regardless of where the script was called
os.chdir(os.path.dirname(os.path.realpath(__file__)))

# see if command line arguments are present
# and if the args are valid,
# make the pet and display it!
if len(sys.argv) == 2:
    # This will be used to allow user to make a specific pet regardless of the default pet
    start_program(sys.argv[1])
elif len(sys.argv) > 2:
    raise Exception(f"Expected 0 or 1 positional arguments, not {len(sys.argv) - 1}")
else:
    start_program()
