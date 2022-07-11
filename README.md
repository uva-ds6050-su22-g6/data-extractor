# data-extractor
General purpose data extraction from Wikipedia, used to generate domain-specific corpora. 

Note the execution of this code is syncronous and only after processing the entire file are the records recorded, so it is best to run this code on a system with an internet connection that is stable for multiple hours.

## How to run

1. Create a virtual environment using `python -m venv venv`
2. Source the virtual environment (either `source ./venv/bin/activate` or `source ./venv/Scripts/activate`
3. Install the required dependencies using `python -m pip install -rrequirements.txt`
4. Run the python scripts in the following order.
   1. `python fetch.py`
   2. `python merge.py`

You will be presented with multiple feather and csv datasets.
Each `input_source` file will have a pair of feather and csv files that represent the raw downloaded data, and may contain duplicates.

When running `merge.py`, duplicates are dropped within a source file and is merged into a single `dataset.feather` and `dataset.csv` file.

You can use pandas to read the feather format if pyarrow is installed.
