# :flying_saucer: Fanatical Book Bundle Scraper & Cleaner

This Python project scrapes book bundles from [fanatical.com](https://www.fanatical.com/), filters for book bundles,
and exports a clean, structured CSV containing:

* Bundle Name
* Book Title
* Author(s)

## :mag: Features

* :white_check_mark: Detects and filters *book bundles* only (ignores game and software bundles)
* :white_check_mark: Supports both **Pick-and-Mix** and **regular** bundle formats
* :white_check_mark: Extracts all book titles and author names
* :white_check_mark: Cleanse author fields from list format (e.g., `['Author A', 'Author B']`)
* :white_check_mark: Takes slug and cleans it into bundle name (e.g., `books-on-sale` to `Books On Sale`)
* :white_check_mark: Saves results to `./csv_exports` directory with a timestamped filename
* :white_check_mark: Handles multiple tiers per bundle where applicable

## :hammer_and_wrench: Requirements

* Python 3.9+
* `requests`
* `pandas`