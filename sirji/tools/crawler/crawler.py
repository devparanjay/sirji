from .factory import ContentHandlerFactory
from tools.logger import researcher as logger

def crawl_urls(urls, output_dir):
    """
    Processes a list of URLs using the appropriate handlers based on the URL type.
    - urls: A list of URLs to process.
    - output_dir: The directory where output from the handlers should be stored.
    """
    for url in urls:
        logger.info(f"Researcher: Started crawling URL: {url}")
        
        handler = ContentHandlerFactory.get_handler(url)
        handler.handle(url, output_dir)
        
        logger.info(f"Researcher: Completed crawling URL: {url}")
