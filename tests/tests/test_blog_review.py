from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

BASE = "https://ecommerce-playground.lambdatest.io/index.php?route=common/home"

def _click(driver, wait, locators):
    for by in locators:
        try:
            el = wait.until(EC.element_to_be_clickable(by))
            driver.execute_script("arguments[0].scrollIntoView({block:'center'})", el)
            el.click(); return
        except Exception:
            continue
    raise RuntimeError("cannot click any locator")

def test_blog_review():
    opts = Options()
    opts.add_argument("--headless=new")
    opts.add_argument("--window-size=1280,900")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)
    wait = WebDriverWait(driver, 15)
    try:
        driver.get(BASE)

        _click(driver, wait, [
            (By.LINK_TEXT, "Blog"),
            (By.PARTIAL_LINK_TEXT, "Blog"),
            (By.CSS_SELECTOR, "a[title='Blog']"),
            (By.CSS_SELECTOR, "a[href*='blog']"),
        ])

        wait.until(EC.presence_of_element_located((
            By.XPATH, "//*[contains(translate(.,'abcdefghijklmnopqrstuvwxyz','ABCDEFGHIJKLMNOPQRSTUVWXYZ'),'LATEST ARTICLES')]"
        )))
        cards = driver.find_elements(By.CSS_SELECTOR, "a[href*='article_id']")
        assert len(cards) >= 1

        el = cards[0]
        driver.execute_script("arguments[0].scrollIntoView({block:'center'})", el)
        el.click()

        wait.until(EC.url_contains("article_id"))
        assert ("article" in driver.current_url) or ("article_id" in driver.current_url)
        wait.until(EC.visibility_of_element_located((By.XPATH, "//h1 | //h2[contains(@class,'title') or contains(@class,'heading')]")))
    finally:
        driver.quit()
