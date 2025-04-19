import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from backend.src.image_describer import ImageGridDescriber


class FalabellaScraper:
        
    def _get_selenium(self, url):
        # Selenium 
        options = Options()
        options.add_argument("--headless")
        driver = webdriver.Chrome(options=options)
        driver.get(url)
        time.sleep(1)  # Allow JS to load
        return driver

    def _get_soup(self, url):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        return soup

    def get_product_name(self, soup):
        tag = soup.find("h1", class_="jsx-783883818")
        return tag.text.strip() if tag else "Product name not found"

    def get_product_price(self, soup):
        tag = soup.find(
            "span", class_="copy12 primary senary jsx-2835692965 bold line-height-29"
        )
        return tag.text.strip() if tag else "Price not found"

    def get_product_specifications(self, soup):
        data = []
        table = soup.find("table", class_="jsx-960159652 specification-table")
        if table:
            table_body = table.find("tbody")
            rows = table_body.find_all("tr")
            for row in rows:
                cols = row.find_all("td")
                specs = [col.text.strip() for col in cols]
                data.append(specs)
        return data

    def get_additional_info(self, soup):
        additional_info = []
        informations = soup.find("div", class_="fb-product-information-tab__copy")
        for info in informations:
            text = [t.text.strip() for t in info]
            additional_info.append(text)
        return additional_info

    def get_image_links(self, driver):
        image_links = []
        try:
            slider = WebDriverWait(driver, 1).until(
                EC.presence_of_element_located((By.CLASS_NAME, "image-slider"))
            )
            imgs = slider.find_elements(By.TAG_NAME, "img")
            for img in imgs:
                image_links.append(img.get_attribute("src"))
        except Exception as e:
            print(f"Error fetching image links: {e}")
        return image_links

    def get_available_sizes(self, driver):
        sizes = []
        try:
            size_buttons = WebDriverWait(driver, 1).until(
                EC.presence_of_all_elements_located(
                    (By.XPATH, "//button[starts-with(@id, 'testId-sizeButton')]")
                )
            )
            for btn in size_buttons:
                size = btn.text.strip()
                sizes.append(size)
        except Exception as e:
            print(f"Error fetching available sizes: {e}")
        return sizes

    def get_image_description(self, image_links):
        concatenated_image = ImageGridDescriber().concatenate_images_square(image_links)
        image_description = ImageGridDescriber().get_image_description(concatenated_image)
        return image_description

    def scrape(self, url):
        soup = self._get_soup(url)
        driver = self._get_selenium(url)

        product_data = {
            "name": self.get_product_name(soup),
            "price": self.get_product_price(soup),
            "image_links": self.get_image_links(driver),
            "specifications": self.get_product_specifications(soup),
            "additional_info": self.get_additional_info(soup),
            "available_sizes": self.get_available_sizes(driver),
        }

        image_links = product_data.get("image_links", [])
        if image_links:
            image_description = self.get_image_description(image_links)
            product_data["image_description"] = image_description
        else:
            product_data["image_description"] = None

        # selenium driver quit
        driver.quit()
        return product_data

def __main__():
    url = "https://www.falabella.com.pe/falabella-pe/product/883158187/Polo-University-Club-Liso-Manga-Corta-100-Algodon/883158198"
    scraper = FalabellaScraper()
    product_data = scraper.scrape(url)

    for key, value in product_data.items():
        print(f"{key}: {value}")

if __name__ == "__main__":
    __main__()
