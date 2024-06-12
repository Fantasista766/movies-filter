# Movies Filter

This project reads a list of movie titles from a CSV file, fetches their IMDb ratings asynchronously, filters out those with ratings below a specified threshold, and saves the high-rated movies to a new CSV file. It also prints the progress of each movie being processed and measures the total runtime of the script.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Runtime](#runtime)

## Features

- Asynchronously fetches IMDb ratings for a list of movie titles.
- Filters out movies with ratings below the specified threshold.
- Saves the filtered and sorted list of high-rated movies to a new CSV file.
- Prints progress and measures the runtime of the script.

## Requirements

- Python 3.7+
- pandas
- IMDbPY
- asyncio

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/Fantasista766/movies-filter.git
    cd movies-filter
    ```

2. Create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Place your input CSV file with movie titles in the same directory as the script. Ensure the CSV file has a column named `title`.

2. Update the `FILE_IN` and `FILE_OUT` constants in `main.py` to match your input and output file names if they are different from `test_movies.csv` and `test_high_rated_movies.csv`.

3. Run the script:
    ```bash
    python main.py
    ```

4. The script will process the movies, fetch their ratings, filter and sort them, and save the high-rated movies to the specified output CSV file. It will also print the progress and the total runtime.

## Runtime

Results for Intell i3-8130u:
- File `test_movies.csv` has been processed in about 20 seconds
- File `movies.csv` has been processed in about 2.5 hours