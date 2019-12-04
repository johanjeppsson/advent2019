# Advent of code, 2019

To run the code for a specific day:
`python -m day1`

## Environment

Use [conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/linux.html) to set up the environment:

`conda env create -f environment.yml`
Activate the environment:
`conda activate advent`

### Input
The input is specific to each user. There are two options for get_data to load
your specific data:
* Download the data manually and put it in `input.txt` in the folder of the day.
* Get your [session cookie](https://github.com/wimglenn/advent-of-code-wim/issues/1) and save it as `.cookie` in the root directory. This allows get_data
to download the input automatically.
