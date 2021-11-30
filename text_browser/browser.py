"""
Console browser
"""
import os
import queue
import re
import sys

import requests
from bs4 import BeautifulSoup
from colorama import init, Fore


class TextBrowser:
    """
    Text browser logic
    """
    HTTPS = "https://"
    TEXT_TAGS = ["p", re.compile("h\\d"), "a", "ul", "ol", "li", "span", "title"]

    def __init__(self, cache_directory):
        self._visited_pages = queue.LifoQueue()
        self._current_page = ""
        self._cache_directory = cache_directory
        self.create_dir_if_not_exists(cache_directory)

        # init colorama
        init(autoreset=True)

    def get_previous_page(self):
        """Get cached previous page"""
        if self._visited_pages.empty():
            return ""

        # Convert to file name in case saved item is a URL
        cached_page = self.get_file_name_for_search(self._visited_pages.get())

        self._current_page = cached_page
        return cached_page

    def save_last_page_to_history(self):
        """Save last page to history storage"""
        if self._current_page:
            self._visited_pages.put(self._current_page)
            self._current_page = ""

    def save_page_to_file(self, url, page_content):
        """Save page text to file"""
        path = os.path.join(self._cache_directory, self.filename_from_url(url))
        with open(path, 'w', encoding="utf-8") as file:
            file.write(page_content)

    def cached_page_exists(self, url):
        """Check if cached page exists"""
        filename = self.get_file_name_for_search(url)
        return os.path.exists(os.path.join(self._cache_directory, filename))

    def print_file_content(self, url):
        """Print file content"""
        filename = self.get_file_name_for_search(url)
        path = os.path.join(self._cache_directory, filename)
        with open(path, encoding="utf-8") as file:
            print(file.read())

    def get_file_name_for_search(self, filename):
        """Return file name - convert from URL if needed"""
        if self.is_valid_url(filename):
            return self.filename_from_url(filename)
        return filename

    @classmethod
    def handle_protocol(cls, url):
        """Add protocol to url if not added"""
        if cls.HTTPS not in url:
            url = cls.HTTPS + url
        return url

    @classmethod
    def filename_from_url(cls, url):
        """Ignore protocol if exists, retrieve url part till the last dot,
        replace slashes to be able to save a file with such a name
        replace dots, so that program does not take the file name for a URL"""
        return re.search(f"(?:{cls.HTTPS})?(.*)\\..+", url).group(1) \
            .replace("/", "-").replace(".", "_")

    @staticmethod
    def print_page(page):
        """Print page"""
        print(page)

    @staticmethod
    def create_dir_if_not_exists(name):
        """Create a folder if not exists"""
        if not os.path.exists(name):
            os.mkdir(name)

    @staticmethod
    def is_valid_url(url):
        """Check if a dot and domain name are present in URL"""
        return re.match(".+\\.[a-z]{2,}", url)

    @staticmethod
    def print_invalid_url():
        """Print invalid URL error"""
        print("Error: Incorrect URL")

    @staticmethod
    def get_page_text(url):
        """Send request to get the page HTML and scrape the text"""
        return TextBrowser.scrape_text(requests.get(url=url).text)

    @staticmethod
    def process_text_recursively(element):
        """Recursively process HTML to get the text:
        Check if the tag contains text tag descendants, if yes, check its contents.
        If content is a text, save to the list, if it is another node, check the descendants again.
        Return joined file.
        """
        text_contents = []

        for content_item in element.contents:
            if not content_item:
                continue

            if isinstance(content_item, str):
                text_contents.append(content_item)
            elif content_item.name == "a" and content_item.string:
                text_contents.append(Fore.BLUE + content_item.string + Fore.RESET)
            elif content_item.name in TextBrowser.TEXT_TAGS \
                    or TextBrowser.has_text_tag_descendant(content_item):
                text_contents.append(TextBrowser.process_text_recursively(content_item))

        return " ".join(text for text in text_contents if text)

    @staticmethod
    def has_text_tag_descendant(element):
        """Check if a tag has any text descendants"""
        return any(descendant.name in TextBrowser.TEXT_TAGS for descendant in element.descendants)

    @staticmethod
    def scrape_text(html_doc):
        """Scrape the text using beautiful soup lib, remove extra newlines and spaces"""
        soup = BeautifulSoup(html_doc, 'html.parser')
        return re.sub(r'\n\s+', '\n', TextBrowser.process_text_recursively(soup.html))

    def take_input(self, user_input):
        """Handle user input"""

        # Determine a requested page
        if user_input == "back":
            page = self.get_previous_page()
        else:
            page = user_input
            # Save the last requested page to history
            self.save_last_page_to_history()

        # Stop evaluating if no page is requested
        if not page:
            return

        # Retrieve a page if possible
        self.handle_page(page)

    def handle_page(self, url):
        """Handle a page request, validate, retrieve cached page if exists or a new page"""

        if self.cached_page_exists(url):
            self.print_file_content(url)
            self._current_page = url
        elif not self.is_valid_url(url):
            self.print_invalid_url()
        else:
            url = self.handle_protocol(url)
            page_text = self.get_page_text(url)
            self.print_page(page_text)
            self.save_page_to_file(url, page_text)
            self._current_page = url


def main(argv):
    """Text browser entry point"""
    directory = argv[0]
    browser = TextBrowser(directory)

    while True:
        user_input = input()

        if user_input == "exit":
            break

        browser.take_input(user_input)


if __name__ == "__main__":
    main(sys.argv[1:])
