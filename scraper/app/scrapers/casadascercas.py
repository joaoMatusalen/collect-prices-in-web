from selenium.webdriver.common.by import By
from .base import BaseScraper


class CasaDasCercasScraper(BaseScraper):
    store_name = "Casa das Cercas"

    def extract(self, url: str) -> dict | None:
        self.browser.get(url)

        price = self.browser.find_element(By.CSS_SELECTOR, ".detalhesdataProdRight_precos_vista").text

        return {
            "price": price,  # Example: "R$ 299,99"
        }
