import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions

driver = webdriver.Chrome()  

def init():
    driver.get("https://vuejs.org/examples/#crud") 
    iframe = WebDriverWait(driver, 10).until(lambda x: x.find_element(By.TAG_NAME, "iframe")) 
    driver.switch_to.frame(iframe)

def test_create():
    init()
    name_input = WebDriverWait(driver, 10).until(lambda x: x.find_element(By.XPATH, '//label/input[1]'))
    surname_input = driver.find_element(By.XPATH, '(//label/input)[2]')
    select = Select(driver.find_element(By.TAG_NAME, 'select'))
    create_button = driver.find_element(By.TAG_NAME, 'button')

    assert len(select.options) == 3
    name_input.click()
    name_input.send_keys('Dude')
    surname_input.click()
    surname_input.send_keys('Dudovic')
    create_button.click()
    assert len(select.options) == 4
    assert name_input.get_attribute('value') == ''
    assert surname_input.get_attribute('value') == ''
    select.select_by_visible_text('Dudovic, Dude')
    assert name_input.get_attribute('value') == 'Dude'
    assert surname_input.get_attribute('value') == 'Dudovic'
    
def test_delete():
    filter_input = WebDriverWait(driver, 10).until(lambda x: x.find_element(By.XPATH, '//input[@placeholder="Filter prefix"]')) 
    name_input = driver.find_element(By.XPATH, '//label/input[1]')
    surname_input = driver.find_element(By.XPATH, '(//label/input)[2]')
    select = WebDriverWait(driver, 10).until(lambda x: Select(x.find_element(By.XPATH, '//div//select')))
    delete_button = driver.find_element(By.XPATH, '//button[3]')

    select.select_by_index(1)
    assert name_input.get_attribute('value') == 'Max'
    assert surname_input.get_attribute('value') == 'Mustermann'
    delete_button.click()
    assert len(select.options) == 3
    filter_input.click()
    filter_input.send_keys('Mu')
    assert len(select.options) == 0
    filter_input.send_keys(Keys.BACKSPACE)
    filter_input.send_keys(Keys.BACKSPACE)

def test_update():
    filter_input = WebDriverWait(driver, 10).until(lambda x: x.find_element(By.XPATH, '//input[@placeholder="Filter prefix"]')) 
    name_input = driver.find_element(By.XPATH, '//label/input[1]')
    surname_input = driver.find_element(By.XPATH, '(//label/input)[2]')
    select = WebDriverWait(driver, 10).until(lambda x: Select(x.find_element(By.XPATH, '//div//select')))
    update_button = driver.find_element(By.XPATH, '//button[2]')
    
    select.select_by_visible_text('Tisch, Roman')
    assert name_input.get_attribute('value') == 'Roman'
    assert surname_input.get_attribute('value') == 'Tisch'
    name_input.send_keys('a')
    surname_input.send_keys('a')
    update_button.click()
    assert len(select.options) == 3
    filter_input.click()
    filter_input.send_keys('Tischa')
    assert len(select.options) == 1
    select.select_by_visible_text('Tischa, Romana')
    assert name_input.get_attribute('value') == 'Romana'
    assert surname_input.get_attribute('value') == 'Tischa'
    driver.quit()


# def test_update():
#     driver.quit()