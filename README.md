# Open Lyrics Dataset
(WIP)
A python library to scrape song lyrics from Genius, and collect additional metadata from Youtube, Spotify and Soundcloud, where available.

## Data
There is no data currently available, as the library is not yet functional. Once the data is available it will be hosted in both Kaggle and a Google drive, both of which will be linked here.

## Running
To run the code in this repo, simply clone the repo as follows
```shell
git clone https://github.com/GenerallyIntelligent/open-lyrics-dataset
```
Then create a new python environment with the method of your choice (I recommend [miniconda](https://docs.conda.io/en/latest/miniconda.html)). Once your new enviroment is created and activated, run the following command to install all dependancies.
```shell
pip install --upgrade -r requirements.txt
```
Then, build and install the `open-lyrics-dataset` package.
```shell
python setup.py build
python setup.py install
```
Finally, run the `collect_data.py` script, as it is the entrypoint to the program. (This will be changed in the future, to make running it easier)

## Developing
The module will be tested using pytest. To perform all tests, simply run:
```shell
pytest
```
To perform a specific test, do something like this:
```shell
pytest path/to/test
```
Where the path is either a directory or `.py` file containing tests you would like to run.
If you are interested in contributing, please let me know, create issues or submit pull requests. I don't update this package very frequently, but I am on github daily.