import json
import undetected_chromedriver as uc

from .scrapers.amazon import AmazonScraper
from .scrapers.kabum import KabumScraper


# Mapeia domínio → classe do scraper
SCRAPERS = {
    "www.amazon.com.br": AmazonScraper,
    "www.kabum.com.br":  KabumScraper,
}


def get_scraper(url: str, browser):
    for domain, cls in SCRAPERS.items():
        if domain in url:
            return cls(browser)
    return None


def run(products: dict):
    options = uc.ChromeOptions()
    options.add_argument("--headless=new")
    browser = uc.Chrome(options=options, version_main=146)

    results = []

    try:
        for group_name, urls in products.items():
            print(f"\nProduto: {group_name}")

            for url in urls:
                scraper = get_scraper(url, browser)

                if scraper is None:
                    print(f"  [!] Loja não suportada: {url}")
                    continue

                result = scraper.scrape(url)

                if result is not None:
                    result["product_group"] = group_name
                    results.append(result)
                    print(f"  ✓ {result['store']} | R$ {result['price']:.2f} | {result['name'][:50]}")

    finally:
        browser.quit()  # fecha o browser mesmo se der erro no meio

    return results