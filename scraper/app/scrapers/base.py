from abc import ABC, abstractmethod
from datetime import datetime

class BaseScraper(ABC):
    store_name: str = ""

    def __init__(self, browser):
        self.browser = browser

    @abstractmethod
    def extract(self, url: str) -> dict | None:
        """Cada loja implementa sua própria lógica de extração."""
        pass

    def scrape(self, url: str) -> dict | None:
        try:
            raw = self.extract(url)
            if raw is None:
                return None
            return {
                "store":       self.store_name,
                "price":       self._parse_price(raw["price"]),
                "name":        raw["name"].strip(),
                "url":         url,
                "scraped_at":  datetime.now().isoformat(),
            }
        except Exception as e:
            print(f"[{self.store_name}] Erro em {url}: {e}")
            return None

    @staticmethod
    def _parse_price(raw: str) -> float:
        """'R$ 1.299,90' ou '1299.90' → 1299.90"""
        cleaned = raw.replace("R$", "").strip()
        if "," in cleaned:
            # Formato BR: 1.299,90
            cleaned = cleaned.replace(".", "").replace(",", ".")
        return float(''.join(c for c in cleaned if c.isdigit() or c == '.'))