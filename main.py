import asyncio
import pandas as pd
import re
import time

from concurrent.futures import ThreadPoolExecutor
from imdb import IMDb

# File paths
FILE_IN = 'test_movies.csv'
FILE_OUT = 'test_high_rated_movies.csv'

# Read the input CSV file into a DataFrame
df = pd.read_csv(FILE_IN)

# Select only the 'title' column for processing
df_selected = df[['title']]
total_movies_count = len(df_selected)


ia = IMDb()
# Define the lowest rating to consider a movie as high-rated
lowest_rating = 7.0
# Initialize a counter to track processing progress
processing_counter = 1


# Function to get IMDb rating for a movie and check if it is above the lowest rating
def get_rating_if_high(title):
    global processing_counter
    try:
        search_results = ia.search_movie(title)
        if search_results:
            # Get the first result (most relevant)
            movie = search_results[0]
            ia.update(movie)
            rating = movie.get('rating')

            # Print the progress
            print(
                f'Processing movie #{processing_counter} of {total_movies_count}:')
            print(f'Title: {title}, Rating: {rating}\n')
            processing_counter += 1

            # Check if the rating is above the threshold
            if rating and rating >= lowest_rating:
                # Extract the year from the title
                match = re.search(r'\((\d{4})\)', title)
                if match:
                    year = match.group(1)
                    # Remove the year from the title
                    title_without_year = re.sub(
                        r'\(\d{4}\)', '', title).strip()
                    return title_without_year, year, rating

    except Exception as e:
        print(f"Error fetching rating for {title}: {e}")

    return None


# Function to fetch ratings for a list of titles
async def fetch_ratings(titles):
    loop = asyncio.get_event_loop()
    with ThreadPoolExecutor() as executor:
        # Create tasks to fetch ratings concurrently
        tasks = [loop.run_in_executor(
            executor, get_rating_if_high, title) for title in titles]
        return await asyncio.gather(*tasks)


async def main():
    titles = df_selected['title'].tolist()
    results = await fetch_ratings(titles)

    # Filter out None results and create a DataFrame
    filtered_movies = [result for result in results if result]
    df_high_rated = pd.DataFrame(filtered_movies, columns=[
                                 'title', 'year', 'rating'])

    # Sort the DataFrame by year and then by title
    df_high_rated = df_high_rated.sort_values(by=['year', 'title'])

    # Print the sorted and filtered DataFrame
    print(df_high_rated)
    print(f'\nTotal movies with high rating: {len(df_high_rated)}')

    # Save the sorted and filtered DataFrame to a new CSV file
    df_high_rated.to_csv(FILE_OUT, index=False)


if __name__ == '__main__':
    start_time = time.time()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    end_time = time.time()

    runtime = end_time - start_time
    print(f"Runtime: {runtime:.2f} seconds")
