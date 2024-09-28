import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions

driver = webdriver.Chrome()  

def init():
    driver.get("https://vuejs.org/examples/#modal") 
    iframe = WebDriverWait(driver, 10).until(lambda x: x.find_element(By.TAG_NAME, "iframe")) 
    driver.switch_to.frame(iframe)

def test_modal():
    init()
    show_modal_button = WebDriverWait(driver, 10).until(lambda x: x.find_element(By.CSS_SELECTOR, '#show-modal')) 
    show_modal_button.click()
    modal = WebDriverWait(driver, 10).until(lambda x: x.find_element(By.CSS_SELECTOR, 'div.modal-container')) 
    modal_header = driver.find_element(By.CSS_SELECTOR, 'div.modal-header')
    modal_body = driver.find_element(By.CSS_SELECTOR, 'div.modal-body')
    modal_footer = driver.find_element(By.CSS_SELECTOR, 'div.modal-footer')
    modal_button = driver.find_element(By.CSS_SELECTOR, 'button.modal-default-button')
    assert modal.is_displayed() == True
    assert modal_header.text == 'Custom Header'
    assert modal_body.text == 'default body'
    assert 'default footer' in modal_footer.text
    modal_button.click()
    WebDriverWait(driver, 10).until(expected_conditions.invisibility_of_element(modal))
    driver.quit()