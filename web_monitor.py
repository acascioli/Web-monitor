import requests
import os
from bs4 import BeautifulSoup
import time
import logging
from plyer import notification

# change this to the URL you want to monitor
URL_TO_MONITOR = 'https://www.google.com'
DELAY_TIME = 60  # seconds


def open_notification():
    notification.notify(
        title="Urgent",
        message="Results available",

        # displaying time
                timeout=10
    )


def process_html(string):
    soup = BeautifulSoup(string, features="lxml")

    # make the html look good
    soup.prettify()

    # remove script tags
    for s in soup.select('script'):
        s.extract()

    # remove meta tags
    for s in soup.select('meta'):
        s.extract()

    # convert to a string, remove '\r', and return
    return str(soup).replace('\r', '')


def webpage_was_changed():
    """Returns true if the webpage was changed, otherwise false."""
    headers = {'User-Agent': 'Mozilla/5.0',
               'Pragma': 'no-cache', 'Cache-Control': 'no-cache'}
    response = requests.get(URL_TO_MONITOR, headers=headers)

    # create the previous_content.txt if it doesn't exist
    if not os.path.exists("previous_content.txt"):
        open("previous_content.txt", 'w+').close()
    try:
        filehandle = open("previous_content.txt", 'r')
        previous_response_html = filehandle.read()
    except UnicodeDecodeError:
        filehandle = open("previous_content.txt", 'r', encoding="cp1252")
        previous_response_html = filehandle.read()

    filehandle.close()

    processed_response_html = process_html(response.text)

    if processed_response_html == previous_response_html:
        return False
    else:
        filehandle = open("previous_content.txt", 'w')
        filehandle.write(processed_response_html)
        filehandle.close()
        return True


def main():
    log = logging.getLogger(__name__)
    logging.basicConfig(level=os.environ.get(
        "LOGLEVEL", "INFO"), format='%(asctime)s %(message)s')
    log.info("Running Website Monitor")
    while True:
        if webpage_was_changed():
            log.info("WEBPAGE WAS CHANGED.")
            open_notification()
        else:
            log.info("Webpage was not changed.")
        time.sleep(DELAY_TIME)


if __name__ == "__main__":
    main()
