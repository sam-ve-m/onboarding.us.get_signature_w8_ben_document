#!/bin/bash

# Need pytest installed (pip install pytest)
echo "Starting tests."
export current_folder=$PWD
export PYTHONPATH="$current_folder/func"
pytest -vv || { echo "ERROR: Error while running Pytest. Make sure it is installed or check if the tests ran correctly. [CONTINUING SCRIPT]";  }
echo "Tests completed successfully."