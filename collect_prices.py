#%%
import datetime
import json

import pandas as pd
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By

def find_product_amazon(link):

    browser.get(link)

    # Name
    product_name = browser.find_element(By.ID, 'productTitle').text

    # Price
    price_element = browser.find_element(By.CLASS_NAME, 'a-price-whole').text
    price_fraction = browser.find_element(By.CLASS_NAME, 'a-price-fraction').text
    
    product_price = price_element + "." + price_fraction

    now = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S.%f")

    return {'date_updated': now, 'store':'Amazon', 'name':product_name, 'price':product_price, 'link':link}

def find_product_kabum(link):

    browser.get(link)

    # Name
    product_name = browser.find_element(By.CSS_SELECTOR, ".col-span-4 h1").text

    # Price
    product_price = browser.find_element(By.CLASS_NAME, 'text-4xl').text

    now = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S.%f")

    return {'date_updated': now, 'store':'Kabum', 'name':product_name, 'price':product_price, 'link':link}

def find_product_elements(link):

    browser.get(link)

    # Name
    product_name = browser.find_element(By.CLASS_NAME, 'product-info__title').text

    # Price
    product_price = browser.find_element(By.CLASS_NAME, 'finalPrice').text

    now = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S.%f")

    return {'date_updated': now, 'store':'Elements', 'name':product_name, 'price':product_price, 'link':link}

def find_product_mercadolivre(link):

    browser.get(link)

    # Name
    product_name = browser.find_element(By.CLASS_NAME, 'ui-pdp-title').text

    # Price
    product_price = ''.join(browser.find_element(By.CLASS_NAME, 'ui-pdp-price__second-line').text.split('\n')[:-1])

    now = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S.%f")

    return {'date_updated': now, 'store':'Mercado Livre', 'name':product_name, 'price':product_price, 'link':link}

def check_store(link):

    match link:
        case link if 'www.amazon.com.br' in link:
                info_product = find_product_amazon(link)
                return info_product
        case link if 'www.kabum.com.br' in link:
                info_product = find_product_kabum(link)
                return info_product
        case link if 'loja.elements.com.br' in link:
                info_product = find_product_elements(link)
                return info_product
        case link if 'www.mercadolivre.com.br' in link:
                info_product = find_product_mercadolivre(link)
                return info_product
        case _:
                return print('store not localizated')

def find_product(products):

    all_products_data = []

    #product = check_store(product_link)

    for product_name, links_list in products.items():
        print(f"Scraping links for product: {product_name}")
        
        if not isinstance(links_list, list):
            print(f"Warning: Links for '{product_name}' is not a list. Skipping.")
            continue
            
        for link in links_list:
            
            print(link)

            product_data = check_store(link)
            
            if product_data:
                # Add the product name from the dictionary key to the scraped data
                product_data['product_group'] = product_name
                all_products_data.append(product_data)

    browser.quit()

    return all_products_data

#%%

with open('data/products.json', 'r') as file:
      products = json.load(file)

browser = Firefox()   

list_products = find_product(products)


#%%

list_products 
