import pytest
from selenium import webdriver
from selenium.common import TimeoutException, NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
import time

@pytest.fixture()
def driver():
    chrome_options = Options()

    prefs = {
        "profile.default_content_setting_values.notifications": 2
    }
    chrome_options.add_experimental_option("prefs", prefs)

    ch_driver = webdriver.Chrome(service=Service('C:/Windows/chromedriver-win64/chromedriver.exe'))
    ch_driver.maximize_window()
    ch_driver.get('https://ctshop.rs/')
    wait=WebDriverWait(ch_driver, 50)

    yield ch_driver
    ch_driver.quit()

def login(driver):
    wait = WebDriverWait(driver, 30)

    user_icon = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'a.modal-link img[alt="user"]')))
    driver.execute_script("arguments[0].click();", user_icon)

    button_email_and_password_click = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(@class, 'email-and-password') and .//p[text()='Email i šifra']]")
        )
    )
    driver.execute_script("arguments[0].click();", button_email_and_password_click)

    wait.until(EC.visibility_of_element_located((By.ID, "login_email")))

    driver.find_element(By.ID, 'login_email').send_keys('bojanstupar089+test1@gmail.com')
    driver.find_element(By.ID, 'login_password').send_keys('Celarevo44!')
    driver.find_element(By.ID, 'loginBtn').click()



def test_open_google_and_go_to_ctshop(driver):
    wait=WebDriverWait(driver, 30)
    logo = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'img[alt="ComtradeShop"]')))
    assert logo.is_displayed()

def test_register_successful_on_ctshop(driver):
    wait=WebDriverWait(driver, 30)

    user_icon = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'a.modal-link img[alt="user"]')))
    driver.execute_script("arguments[0].click();", user_icon)

    button_email_and_password_click = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(@class, 'email-and-password') and .//p[text()='Email i šifra']]")
        )
    )
    driver.execute_script("arguments[0].click();", button_email_and_password_click)

    make_an_account_click_link=wait.until(EC.visibility_of_element_located((By.XPATH,"//span[@id='create-account-new']")))
    driver.execute_script("arguments[0].click();", make_an_account_click_link)

    driver.find_element(By.ID, 'firstname').send_keys('Bojan')
    driver.find_element(By.ID, 'lastname').send_keys('Stupar')
    driver.find_element(By.ID, 'email').send_keys('bojanstupar089+test7@gmail.com')
    driver.find_element(By.ID, 'password').send_keys('Celarevo44!')
    driver.find_element(By.ID, 'registerBtn').click()


    reg_result=wait.until(EC.visibility_of_element_located((By.ID,"registration-message"))).text
    assert "Hvala na registraciji. Molimo proverite email i aktivirajte Vaš nalog." in reg_result,\
        "Success message after registration was not displayed or is incorrect."

def test_register_required_first_name_required_validation(driver):
    wait=WebDriverWait(driver, 30)

    user_icon = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'a.modal-link img[alt="user"]')))
    driver.execute_script("arguments[0].click();", user_icon)

    button_email_and_password_click = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(@class, 'email-and-password') and .//p[text()='Email i šifra']]")
        )
    )
    driver.execute_script("arguments[0].click();", button_email_and_password_click)

    make_an_account_click_link = wait.until(
        EC.visibility_of_element_located((By.XPATH, "//span[@id='create-account-new']")))
    driver.execute_script("arguments[0].click();", make_an_account_click_link)

    driver.find_element(By.ID, 'firstname').send_keys('')
    driver.find_element(By.ID, 'lastname').send_keys('Stupar')
    driver.find_element(By.ID, 'email').send_keys('bojanstupar089+test4@gmail.com')
    driver.find_element(By.ID, 'password').send_keys('Celarevo44!')
    driver.find_element(By.ID, 'registerBtn').click()

    ime_req=wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'error-container'))).text
    assert"Niste uneli ime!"in ime_req,"First name required error message was not displayed during registration."

def test_register_last_name_required_validation(driver):
    wait = WebDriverWait(driver, 30)

    user_icon = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'a.modal-link img[alt="user"]')))
    driver.execute_script("arguments[0].click();", user_icon)

    button_email_and_password_click = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(@class, 'email-and-password') and .//p[text()='Email i šifra']]")
        )
    )
    driver.execute_script("arguments[0].click();", button_email_and_password_click)

    make_an_account_click_link = wait.until(
        EC.visibility_of_element_located((By.XPATH, "//span[@id='create-account-new']")))
    driver.execute_script("arguments[0].click();", make_an_account_click_link)

    driver.find_element(By.ID, 'firstname').send_keys('Bojan')
    driver.find_element(By.ID, 'lastname').send_keys('')
    driver.find_element(By.ID, 'email').send_keys('bojanstupar089+test4@gmail.com')
    driver.find_element(By.ID, 'password').send_keys('Celarevo44!')
    driver.find_element(By.ID, 'registerBtn').click()

    error_lastname = wait.until(EC.visibility_of_element_located(
        (By.XPATH, "//input[@id='lastname']/following-sibling::div[@class='error-container']/span"))
    ).text
    assert "Niste uneli prezime!" in error_lastname, "Last name required error message was not displayed during registration."

def test_register_email_required_validation(driver):
    wait = WebDriverWait(driver, 30)

    user_icon = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'a.modal-link img[alt="user"]')))
    driver.execute_script("arguments[0].click();", user_icon)

    button_email_and_password_click = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(@class, 'email-and-password') and .//p[text()='Email i šifra']]")
        )
    )
    driver.execute_script("arguments[0].click();", button_email_and_password_click)

    make_an_account_click_link = wait.until(
        EC.visibility_of_element_located((By.XPATH, "//span[@id='create-account-new']")))
    driver.execute_script("arguments[0].click();", make_an_account_click_link)

    driver.find_element(By.ID, 'firstname').send_keys('Bojan')
    driver.find_element(By.ID, 'lastname').send_keys('Stupar')
    driver.find_element(By.ID, 'email').send_keys('')
    driver.find_element(By.ID, 'password').send_keys('Celarevo44!')
    driver.find_element(By.ID, 'registerBtn').click()

    error_email = wait.until(EC.visibility_of_element_located(
        (By.XPATH, "//input[@id='email']/following-sibling::div[@class='error-container']/span"))
    ).text
    assert "Niste uneli email!" in error_email, "Email required error message was not displayed during registration."

def test_register_password_required_validation(driver):
    wait = WebDriverWait(driver, 30)

    user_icon = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'a.modal-link img[alt="user"]')))
    driver.execute_script("arguments[0].click();", user_icon)

    button_email_and_password_click = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(@class, 'email-and-password') and .//p[text()='Email i šifra']]")
        )
    )
    driver.execute_script("arguments[0].click();", button_email_and_password_click)

    make_an_account_click_link = wait.until(
        EC.visibility_of_element_located((By.XPATH, "//span[@id='create-account-new']")))
    driver.execute_script("arguments[0].click();", make_an_account_click_link)

    driver.find_element(By.ID, 'firstname').send_keys('Bojan')
    driver.find_element(By.ID, 'lastname').send_keys('Stupar')
    driver.find_element(By.ID, 'email').send_keys('bojanstupar089"gmail.com')
    driver.find_element(By.ID, 'password').send_keys('')
    driver.find_element(By.ID, 'registerBtn').click()

    error_email = wait.until(EC.visibility_of_element_located(
        (By.XPATH, "//input[@id='password']/following-sibling::div[@class='error-container']/span"))
    ).text
    assert "Niste uneli šifru!" in error_email, "Password required error message was not displayed during registration"

def test_register_email_invalid_format(driver):
    wait = WebDriverWait(driver, 30)
    user_icon = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'a.modal-link img[alt="user"]')))
    driver.execute_script("arguments[0].click();", user_icon)

    button_email_and_password_click = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(@class, 'email-and-password') and .//p[text()='Email i šifra']]")
        )
    )
    driver.execute_script("arguments[0].click();", button_email_and_password_click)

    make_an_account_click_link = wait.until(
        EC.visibility_of_element_located((By.XPATH, "//span[@id='create-account-new']")))
    driver.execute_script("arguments[0].click();", make_an_account_click_link)

    driver.find_element(By.ID, 'firstname').send_keys('Bojan')
    driver.find_element(By.ID, 'lastname').send_keys('Stupar')
    driver.find_element(By.ID, 'email').send_keys('bokica')
    driver.find_element(By.ID, 'password').send_keys('Celarevo44!')
    driver.find_element(By.ID, 'registerBtn').click()

    error_email = wait.until(EC.visibility_of_element_located(
        (By.XPATH, "//input[@id='email']/following-sibling::div[@class='error-container']/span"))
    ).text
    assert "The email must be a valid email address." in error_email, "Invalid email format error message was not shown."

def test_register_unchecked_terms_of_purchase(driver):
    wait = WebDriverWait(driver, 30)
    user_icon = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'a.modal-link img[alt="user"]')))
    driver.execute_script("arguments[0].click();", user_icon)

    button_email_and_password_click = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(@class, 'email-and-password') and .//p[text()='Email i šifra']]")
        )
    )
    driver.execute_script("arguments[0].click();", button_email_and_password_click)

    make_an_account_click_link = wait.until(
        EC.visibility_of_element_located((By.XPATH, "//span[@id='create-account-new']")))
    driver.execute_script("arguments[0].click();", make_an_account_click_link)

    driver.find_element(By.ID, 'firstname').send_keys('Bojan')
    driver.find_element(By.ID, 'lastname').send_keys('Stupar')
    driver.find_element(By.ID, 'email').send_keys('bojanstupar089@gmail.com')
    driver.find_element(By.ID, 'password').send_keys('Celarevo44!')
    driver.find_element(By.ID, 'terms_of_purchase').click()
    driver.find_element(By.ID, 'registerBtn').click()

    error_top = wait.until(EC.visibility_of_element_located(
        (By.XPATH, "//span[contains(text(), 'Molimo vas da prihvatite Uslove kupovine')]")
    )).text

    assert "Molimo vas da prihvatite Uslove kupovine kako biste nastavili sa registracijom." in error_top, "Terms of purchase agreement validation message was not displayed."

def test_register_email_already_exists(driver):
    wait = WebDriverWait(driver, 30)

    user_icon = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'a.modal-link img[alt="user"]')))
    driver.execute_script("arguments[0].click();", user_icon)

    button_email_and_password_click = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(@class, 'email-and-password') and .//p[text()='Email i šifra']]")
        )
    )
    driver.execute_script("arguments[0].click();", button_email_and_password_click)

    make_an_account_click_link = wait.until(
        EC.visibility_of_element_located((By.XPATH, "//span[@id='create-account-new']")))
    driver.execute_script("arguments[0].click();", make_an_account_click_link)

    driver.find_element(By.ID, 'firstname').send_keys('Bojan')
    driver.find_element(By.ID, 'lastname').send_keys('Stupar')
    driver.find_element(By.ID, 'email').send_keys('bojanstupar089+test4@gmail.com')
    driver.find_element(By.ID, 'password').send_keys('Celarevo44!')
    driver.find_element(By.ID, 'registerBtn').click()

    error_email = wait.until(EC.visibility_of_element_located(
        (By.XPATH, "//input[@id='email']/following-sibling::div[@class='error-container']/span"))
    ).text
    assert "Već postoji nalog sa unetom email adresom! Molimo ulogujte se!" in error_email, \
        "Duplicate email error message was not displayed during registration."

def test_login_successful_on_ctshop(driver):

    login(driver)
    wait=WebDriverWait(driver, 30)
    account_heading=wait.until(EC.visibility_of_element_located((By.TAG_NAME,"h1"))).text
    assert "Moj nalog" in account_heading,"Successful login confirmation message was not shown."

def test_login_click_forgot_password_link(driver):
    wait = WebDriverWait(driver, 30)

    user_icon = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'a.modal-link img[alt="user"]')))
    driver.execute_script("arguments[0].click();", user_icon)

    button_email_and_password_click = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(@class, 'email-and-password') and .//p[text()='Email i šifra']]")
        )
    )
    driver.execute_script("arguments[0].click();", button_email_and_password_click)

    wait.until(EC.visibility_of_element_located((By.ID, "login_email")))

    driver.find_element(By.ID, 'login_email').send_keys('bojanstupar089+test1@gmail.com')

    forgot_password_link=wait.until(EC.visibility_of_element_located((By.LINK_TEXT,"Zaboravili ste lozinku?")))
    driver.execute_script("arguments[0].click();", forgot_password_link)

    forgot_password_heading=wait.until(EC.visibility_of_element_located((By.CLASS_NAME,"panel-heading"))).text
    assert "Zaboravljena lozinka" in forgot_password_heading, "Forgot password heading was not found on the page."

def test_login_bad_creadentials(driver):
    wait = WebDriverWait(driver, 30)

    user_icon = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'a.modal-link img[alt="user"]')))
    driver.execute_script("arguments[0].click();", user_icon)

    button_email_and_password_click = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(@class, 'email-and-password') and .//p[text()='Email i šifra']]")
        )
    )
    driver.execute_script("arguments[0].click();", button_email_and_password_click)

    wait.until(EC.visibility_of_element_located((By.ID, "login_email")))

    driver.find_element(By.ID, 'login_email').send_keys('bojanstupar089+test1@gmail.com')
    driver.find_element(By.ID, 'login_password').send_keys('Celar!')
    driver.find_element(By.ID, 'loginBtn').click()

    bc_error=wait.until(EC.visibility_of_element_located((By.ID,"errorLoginMessageTxt"))).text
    assert "Uneta email adresa i lozinka se ne poklapaju." in bc_error, "Expected login error message for invalid credentials was not displayed."

def test_ctshop_click_action(driver):
    wait = WebDriverWait(driver, 30)
    akcija_link = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//a[@href='/akcija' and contains(text(),'AKCIJA')]")))
    driver.execute_script("arguments[0].click();", akcija_link)

def test_ctshop_click_action_select_price_asc(driver):
    wait = WebDriverWait(driver, 30)

    wait = WebDriverWait(driver, 30)
    akcija_link = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//a[@href='/akcija' and contains(text(),'AKCIJA')]")))
    driver.execute_script("arguments[0].click();", akcija_link)

    dropdown = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.category-sort-by > i.fa-angle-down")))
    driver.execute_script("arguments[0].click();", dropdown)
    ceni_rastuce = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a.order-by[data-order-by='asc']")))
    driver.execute_script("arguments[0].click();", ceni_rastuce)

def test_ctshop_click_action_select_price_desc(driver):
    wait = WebDriverWait(driver, 30)
    akcija_link = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//a[@href='/akcija' and contains(text(),'AKCIJA')]")))
    driver.execute_script("arguments[0].click();", akcija_link)

    dropdown = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.category-sort-by > i.fa-angle-down")))
    driver.execute_script("arguments[0].click();", dropdown)
    price_desc = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a.order-by[data-order-by='desc']")))
    driver.execute_script("arguments[0].click();", price_desc)

def test_ctshop_click_cart_link(driver):
    wait = WebDriverWait(driver, 30)
    cart_icon = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.widget-header')))
    driver.execute_script("arguments[0].click();", cart_icon)

    cart_heading=wait.until(EC.element_to_be_clickable((By.TAG_NAME,"h1"))).text
    assert"Vaša korpa" in cart_heading, "Cart heading was not found on the page."

def test_ctshop_navigate_laptops_and_tablets_click_gaming_laptops_link(driver):
    wait = WebDriverWait(driver, 30)

    laptop_hover=wait.until(EC.visibility_of_element_located((By.ID,"laptopovi-tableti")))
    actions=ActionChains(driver)
    actions.move_to_element(laptop_hover).perform()

    gaming_laptop_link=wait.until(EC.presence_of_element_located((By.XPATH,"//a[text()='Gaming laptopovi']")))
    driver.execute_script("arguments[0].click();", gaming_laptop_link)

    gaming_laptop_heading=wait.until(EC.visibility_of_element_located((By.TAG_NAME,"h1"))).text
    assert "Gaming laptopovi" in gaming_laptop_heading,"Expected gaming laptop heading is not good."

def test_ctshop_navigate_tv_audio_click_home_theater(driver):
    wait = WebDriverWait(driver, 30)

    tv_audio_hover = wait.until(EC.visibility_of_element_located((By.ID, "tv-audio")))
    actions = ActionChains(driver)
    actions.move_to_element(tv_audio_hover).perform()

    home_theater_link = wait.until(EC.presence_of_element_located((By.XPATH, "//a[text()='Kućni bioskopi']")))
    driver.execute_script("arguments[0].click();", home_theater_link)

    home_theater_heading = wait.until(EC.visibility_of_element_located((By.TAG_NAME, "h1"))).text
    assert "Kućni bioskopi" in home_theater_heading, "Expected home theater heading is not good."

def test_ctshop_filter_handheld_vacuums_by_bosch_and_black_color(driver):
    wait = WebDriverWait(driver, 30)

    sh_hover = wait.until(EC.visibility_of_element_located((By.ID, "mali-kucni-aparati")))
    actions = ActionChains(driver)
    actions.move_to_element(sh_hover).perform()

    handheld_vacuums_link = wait.until(EC.presence_of_element_located((By.XPATH, "//a[text()='Ručni usisivači']")))
    driver.execute_script("arguments[0].click();", handheld_vacuums_link)

    label_bosch = wait.until(EC.visibility_of_element_located((By.XPATH, "//label[@for='filter_data_brend_55']")))
    actions = ActionChains(driver)
    actions.move_to_element(label_bosch).click().perform()

    color_check=wait.until(EC.visibility_of_element_located((By.XPATH,"//label[@for='filter_data_filter_382']")))
    driver.execute_script("arguments[0].click();", color_check)

    button=wait.until(EC.visibility_of_element_located((By.XPATH,"//button[text()='Primeni']")))
    driver.execute_script("arguments[0].click();", button)

def test_ctshop_add_tesla_36000_white_inverter_to_cart(driver):
    wait = WebDriverWait(driver, 30)

    sh_hover = wait.until(EC.visibility_of_element_located((By.ID, "bela-tehnika")))
    actions = ActionChains(driver)
    actions.move_to_element(sh_hover).perform()

    handheld_vacuums_link = wait.until(EC.presence_of_element_located((By.XPATH, "//a[text()='Inverter klime']")))
    driver.execute_script("arguments[0].click();", handheld_vacuums_link)

    label_tesla = wait.until(EC.visibility_of_element_located((By.XPATH, "//label[@for='filter_data_brend_337']")))
    actions = ActionChains(driver)
    actions.move_to_element(label_tesla).click().perform()

    label_3600 = wait.until(EC.visibility_of_element_located((By.XPATH, "//label[@for='filter_data_filter_223']")))
    actions.move_to_element(label_3600).click().perform()

    label_color = wait.until(EC.visibility_of_element_located((By.XPATH, "//label[@for='filter_data_filter_384']")))
    actions.move_to_element(label_color).click().perform()

    button = wait.until(EC.visibility_of_element_located((By.XPATH, "//button[text()='Primeni']")))
    driver.execute_script("arguments[0].click();", button)

    product_card = wait.until(EC.visibility_of_element_located(
        (By.CSS_SELECTOR, "div#ga4-product-list[data-product-id='65332']")
    ))
    actions.move_to_element(product_card).perform()

    add_inverter_to_cart = wait.until(EC.visibility_of_element_located(
        (By.XPATH, "//a[contains(@class, 'add-to-cart') and contains(text(), 'Dodaj u korpu')]")
    ))
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", add_inverter_to_cart)
    driver.execute_script("arguments[0].click();", add_inverter_to_cart)

    cart_heading=wait.until(EC.visibility_of_element_located((By.CLASS_NAME,"modal-title"))).text
    assert "Proizvod je dodat u korpu" in cart_heading,"Expected cart heading is not good."

def test_ctshop_remove_tesla_36000_white_inverter_from_cart(driver):
    wait = WebDriverWait(driver, 30)

    sh_hover = wait.until(EC.visibility_of_element_located((By.ID, "bela-tehnika")))
    actions = ActionChains(driver)
    actions.move_to_element(sh_hover).perform()

    handheld_vacuums_link = wait.until(EC.presence_of_element_located((By.XPATH, "//a[text()='Inverter klime']")))
    driver.execute_script("arguments[0].click();", handheld_vacuums_link)

    label_tesla = wait.until(EC.visibility_of_element_located((By.XPATH, "//label[@for='filter_data_brend_337']")))
    actions = ActionChains(driver)
    actions.move_to_element(label_tesla).click().perform()

    label_3600 = wait.until(EC.visibility_of_element_located((By.XPATH, "//label[@for='filter_data_filter_223']")))
    actions.move_to_element(label_3600).click().perform()

    label_color = wait.until(EC.visibility_of_element_located((By.XPATH, "//label[@for='filter_data_filter_384']")))
    actions.move_to_element(label_color).click().perform()

    button = wait.until(EC.visibility_of_element_located((By.XPATH, "//button[text()='Primeni']")))
    driver.execute_script("arguments[0].click();", button)

    product_card = wait.until(EC.visibility_of_element_located(
        (By.CSS_SELECTOR, "div#ga4-product-list[data-product-id='65332']")
    ))
    actions.move_to_element(product_card).perform()

    add_inverter_to_cart = wait.until(EC.visibility_of_element_located(
        (By.XPATH, "//a[contains(@class, 'add-to-cart') and contains(text(), 'Dodaj u korpu')]")
    ))
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", add_inverter_to_cart)
    driver.execute_script("arguments[0].click();", add_inverter_to_cart)

    continue_link=wait.until(EC.visibility_of_element_located((By.LINK_TEXT, "Idi u korpu")))
    driver.execute_script("arguments[0].click();", continue_link)

    remove_item_button = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "span.cart-item-desktop-remove.remove-item"))
    )
    driver.execute_script("arguments[0].click();", remove_item_button)

    remove_cart_heading = wait.until(EC.visibility_of_element_located((
        By.XPATH, "//h3[contains(text(), 'Vaša korpa je trenutno prazna.')]"
    ))).text
    assert "Vaša korpa je trenutno prazna." in remove_cart_heading,"Expected cart heading is not good."

def test_ctshop_my_orders(driver):
    login(driver)
    wait=WebDriverWait(driver, 30)

    my_orders_link = wait.until(EC.visibility_of_element_located(
        (By.XPATH, "//a[contains(text(), 'Moje Porudžbine')]")
    ))

    driver.execute_script("arguments[0].click();", my_orders_link)

    my_orders_heading=wait.until(EC.visibility_of_element_located((By.TAG_NAME, "h1"))).text
    assert "Moje Porudžbine" in my_orders_heading,"Expected cart heading is not good."
def test_ctsop_update_my_accounts(driver):
    login(driver)
    wait=WebDriverWait(driver, 30)

    city_input=wait.until(EC.visibility_of_element_located((By.NAME,"city")))
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", city_input)

    city_input=driver.find_element(By.NAME,"city")
    city_input.clear()
    city_input.send_keys("Novi Sad")

    address_input=driver.find_element(By.NAME,"address")
    address_input.clear()
    address_input.send_keys("Rumenacka 5")

    phone_input=driver.find_element(By.NAME,"phone")
    phone_input.clear()
    phone_input.send_keys("12345")

    gender=driver.find_element(By.NAME,"gender")
    select=Select(gender)
    select.select_by_value("1")

    button_submit=driver.find_element(By.XPATH,"//button[@type='submit']")
    driver.execute_script("arguments[0].click();", button_submit)















def test_ctshop_logout(driver):
    login(driver)
    wait=WebDriverWait(driver, 30)
    logout_link = wait.until(EC.visibility_of_element_located(
        (By.XPATH, "//a[contains(text(), 'Odjavi se')]")
    ))

    driver.execute_script("arguments[0].click();", logout_link)

    logo = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'img[alt="ComtradeShop"]')))
    assert logo.is_displayed()























