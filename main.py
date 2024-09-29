from typing import Optional, List
from random import uniform, choice
from time import sleep
import logging

from bs4 import BeautifulSoup
import requests


class ColoredFormatter(logging.Formatter):
    """
    Custom logging formatter to add colors to different log levels.

    Attributes:
        COLORS (dict): A dictionary mapping log levels to their respective terminal color codes.
    """
    COLORS = {
        'INFO': '\033[97m',
        'WARNING': '\033[93m',
        'ERROR': '\033[91m',
        'DEBUG': '\033[94m',
        'RESET': '\033[0m'
    }


    def format(self, record):
        """
        Overrides the format method to apply color formatting based on the log level.

        Args:
            record (logging.LogRecord): The log record object.

        Returns:
            str: The formatted log message with color.
        """
        color = self.COLORS.get(record.levelname, self.COLORS['RESET'])
        reset = self.COLORS['RESET']
        return f"{color}{super().format(record)}{reset}"


def get_logger():
    """
    Configures and returns a logger instance with custom formatting.

    Returns:
        logging.Logger: Configured logger instance with colored log formatting.
    """
    logger = logging.getLogger("ScraperLogger")
    if not logger.hasHandlers():
        logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler()

        # formatter = ColoredFormatter('%(levelname)s - %(message)s')
        formatter = ColoredFormatter('%(levelname)s - %(message)s')
        handler.setFormatter(formatter)

        logger.addHandler(handler)
    return logger


class Content:
    """
    Static class for handling the retrieval of webpage content.
    """

    @staticmethod
    def get_content(url: str) -> Optional[str]:
        """
        Fetches the HTML content of the specified URL.

        Args:
            url (str): The URL of the webpage to retrieve content from.

        Returns:
            Optional[str]: The HTML content of the page if the
            request is successful, otherwise None.
        """
        try:
            response = requests.get(url)

        except Exception:
            logger.error(f"Failed to retrieve content from {url}")
            return None

        if response.status_code != 200:
            return None

        return response.text


class Href:
    """
    Static class for processing and filtering hyperlinks extracted from a webpage.
    """

    @staticmethod
    def get_cleaned_links(hrefs: List[str]) -> List[str]:
        """
        Filters and cleans a list of hrefs based on predefined conditions.

        Args:
            hrefs (List[str]): List of raw href strings.

        Returns:
            List[str]: A cleaned list of hrefs.
        """
        hrefs = [href for href in hrefs if href[:6] == "/wiki/"]
        hrefs = [href for href in hrefs if href[-8:] != "/sandbox"]
        hrefs = [href for href in hrefs if ":" not in href]

        return hrefs


    @staticmethod
    def find_philosophy_href(href_list: List[str]) -> bool:
        """
        Checks if the href list contains a link to the 'Philosophy' Wikipedia page.

        Args:
            href_list (List[str]): List of href strings.

        Returns:
            bool: True if '/wiki/Philosophy' is found in the list, False otherwise.
        """
        return "/wiki/Philosophy" in href_list


    @staticmethod
    def get_click_href(href_list: List[str], visited_hrefs: set) -> Optional[str]:
        """
        Selects an href to click based on the presence of 'philosophy' in the URL.

        Args:
            href_list (List[str]): List of href strings.

        Returns:
            Optional[str]: The selected href, prioritizing
            links containing 'philosophy'. If none, selects a random link.
        """
        if not href_list:
            logger.error("No valid hrefs found on the page.")
            return None

        for i in href_list:
            if "philosophy" in i.lower() and i not in visited_hrefs:
                return i

        return choice(href_list)


class Soup:
    """
    Class for parsing the HTML content using BeautifulSoup and extracting relevant information.
    """

    def __init__(self, content: str):
        """
        Initializes the Soup instance with HTML content.

        Args:
            content (str): The HTML content of a webpage.
        """
        self.soup = BeautifulSoup(content, "html.parser")


    def get_body_soup(self) -> Optional[BeautifulSoup]:
        """
        Extracts the body content section from the soup object.

        Returns:
            Optional[BeautifulSoup]: The body content soup if found, otherwise None.
        """
        body_soup = self.soup.find("div", attrs={"class": "mw-body-content"})
        if body_soup:
            return body_soup
        return None


    def get_hrefs(self) -> List[str]:
        """
        Extracts all hrefs from the body content and applies cleaning rules.

        Returns:
            List[str]: A cleaned list of hrefs.
        """
        body_soup = self.get_body_soup()
        hrefs = [a["href"] for a in body_soup.find_all("a", href=True)]

        hrefs = Href.get_cleaned_links(hrefs)
        return hrefs


def main_finder(url: str) -> Optional[int]:
    """
    Main function to start the process of navigating
    Wikipedia links until the 'Philosophy' page is found.

    Args:
        url (str): The initial Wikipedia page URL to start navigation from.

    Returns:
        Optional[int]: The number of visits it took to reach the
        'Philosophy' page. None if not found.
    """
    visited_hrefs, visit_count = set(), 1
    MAX_ATTEMPTS = 1_000
    SLEEP_MIN, SLEEP_MAX = 1, 2

    for _ in range(MAX_ATTEMPTS):
        content = Content.get_content(url)
        if content:
            hrefs = Soup(content).get_hrefs()
            if Href.find_philosophy_href(hrefs):
                return visit_count

            random_href = Href.get_click_href(hrefs, visited_hrefs)
            if random_href == None:
                return None
            visited_hrefs.add(random_href)

            url = f"https://en.wikipedia.org{random_href}"
            logger.info(random_href[6:])

            visit_count += 1
            sleep(uniform(SLEEP_MIN, SLEEP_MAX))

    return None


if __name__ == "__main__":
    first_url = "https://en.wikipedia.org/wiki/Sport"
    logger = get_logger()
    visit_count = main_finder(first_url)

    if visit_count is None:
        logger.info("Philosophy Link Not Found!")
    else:
        logger.info(f"Attempt Number To Find Philosophy Link -> {visit_count}!")
