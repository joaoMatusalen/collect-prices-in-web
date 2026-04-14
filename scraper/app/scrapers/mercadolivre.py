from selenium.webdriver.common.by import By
from .base import BaseScraper


class MercadoLivreScraper(BaseScraper):
    store_name = "Mercado Livre"

    def extract(self, url: str) -> dict | None:
        self.browser.get(url)

        container_price =  self.browser.find_element(By.CSS_SELECTOR, '.ui-pdp-price__second-line')
        
        price = container_price.find_element(By.CSS_SELECTOR, '.andes-money-amount__fraction').text
        price_frac = container_price.find_element(By.CSS_SELECTOR, '.andes-money-amount__cents').text

        return {
            "price": price + "," + price_frac,  # Example: "1299,90"
        }
