# csi-imdb-scraper

This is a scraper project for IMDB data for CSI shows.

## Available Objects

After running `from csi import *`, the following objects will be available:

### Variables

- `headers`: A dictionary containing the HTTP headers used to mimic a browser request.
- `shows`: A list of dictionaries, each containing the title and IMDB code for different CSI shows.
- `alldata`: A list that will store the collected data for all episodes.
- `show`: A list that stores the same data as alldata but by show.

### Functions

- `printout()`: A function that prints the collected data in a tabular format. The table includes the date, show name, episode title, and a warning if the broadcast dates are out of sequence.

### Example Usage

```python
from csi import *

# Collect data for all shows
# (This will be done automatically when the script is run)

# Print the collected data
printout()