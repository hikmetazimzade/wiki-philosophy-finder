# Wikipedia Philosophy Page Finder

This Python project is a web scraper that explores the famous "Wikipedia Philosophy Game," where you click the first non-italicized, non-parenthesized link on a Wikipedia page and continue doing so until you reach the **Philosophy** article.

## How It Works

1. Start with a Wikipedia page URL.
2. Fetch the content of the page.
3. Extract relevant links.
4. If the **Philosophy** page is linked, stop.
5. Otherwise, click the next eligible link and repeat.
6. Track the number of steps taken to reach **Philosophy** or stop after a set number of attempts.

## Features

- **Link Filtering**: Ignores invalid or disallowed Wikipedia links.
- **Random Delays**: Introduces random sleep times between requests.
- **Logging**: Logs each visited link with color-coded output for easy tracking.

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/<your-username>/wiki-philosophy-finder.git
    ```

2. Navigate to the project folder:

    ```bash
    cd wiki-philosophy-finder
    ```

3. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

Run the script with an initial Wikipedia page URL:

```bash
python main.py
