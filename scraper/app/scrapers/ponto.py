from selenium.webdriver.common.by import By
from .base import BaseScraper


class PontoScraper(BaseScraper):
    store_name = "Ponto"

    def extract(self, url: str) -> dict | None:
        self.browser.get(url)

        price = self.browser.find_element(By.CSS_SELECTOR, "[aria-hidden='true']").text

        return {
            "price": price,  # Example: "R$ 1.299,00"
        }
