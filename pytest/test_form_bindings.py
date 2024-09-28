import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome()  

def init():
    driver.get("https://vuejs.org/examples/#form-bindings") 
    iframe = WebDriverWait(driver, 10).until(lambda x: x.find_element(By.TAG_NAME, "iframe")) 
    driver.switch_to.frame(iframe)

def test_input():
    init()
    input = WebDriverWait(driver, 10).until(lambda x: x.find_element(By.XPATH, '//input[1]')) 
    input_paragraph = driver.find_element(By.XPATH, '//p[1]')
    assert input.get_attribute('value') == 'Edit me'
    assert input_paragraph.text == 'Edit me'
    input.clear()
    input.send_keys('Edited')
    assert input.get_attribute('value') == 'Edited'
    assert input_paragraph.text == 'Edited'

def test_checkbox():
    checkbox = WebDriverWait(driver, 10).until(lambda x: x.find_element(By.CSS_SELECTOR, '#checkbox')) 
    assert checkbox.is_displayed() == True
    checkbox_label = driver.find_element(By.XPATH, '//label[@for="checkbox"]')
    assert checkbox.is_selected() == True
    assert checkbox_label.text == 'Checked: true'
    checkbox.click()
    assert checkbox.is_selected() == False
    assert checkbox_label.text == 'Checked: false'
    

def test_multiple_checboxes():
    jack_checkbox = WebDriverWait(driver, 10).until(lambda x: x.find_element(By.CSS_SELECTOR, '#jack')) 
    john_checkbox = driver.find_element(By.CSS_SELECTOR, '#john')
    mike_checkbox = driver.find_element(By.CSS_SELECTOR, '#mike')
    names_paragraph = driver.find_element(By.XPATH, '//p[2]')
    assert 'Jack' in names_paragraph.text
    jack_checkbox.click()
    john_checkbox.click()
    assert 'Jack' not in names_paragraph.text
    assert 'John' in names_paragraph.text
    mike_checkbox.click()
    assert 'Mike' in names_paragraph.text

def test_radio():
    radio_one = WebDriverWait(driver, 10).until(lambda x: x.find_element(By.CSS_SELECTOR, '#one')) 
    radio_two = driver.find_element(By.CSS_SELECTOR, '#two')
    radio_paragraph = driver.find_element(By.XPATH, '//p[3]')
    assert radio_one.is_selected() == True
    assert radio_paragraph.text == 'Picked: One'
    radio_two.click()
    assert radio_one.is_selected() == False
    assert radio_paragraph.text == 'Picked: Two'

def test_select():
    select = Select(WebDriverWait(driver, 10).until(lambda x: x.find_element(By.XPATH, '//select[1]')))
    select_paragraph = driver.find_element(By.XPATH, '//p[4]')
    assert select.first_selected_option.text == 'A'
    assert select_paragraph.text == 'Selected: A'
    select.select_by_index(2)
    assert select.first_selected_option.text == 'B'
    assert select_paragraph.text == 'Selected: B'
    select.select_by_visible_text('C')
    assert select.first_selected_option.text == 'C'
    assert select_paragraph.text == 'Selected: C'
    
def test_multi_select():
    select = Select(WebDriverWait(driver, 10).until(lambda x: x.find_element(By.XPATH, '//select[2]')))
    select_paragraph = driver.find_element(By.XPATH, '//p[5]')
    assert len(select.all_selected_options) == 1
    assert select.all_selected_options[0].text == 'A'
    assert select_paragraph.text == 'Selected: [ "A" ]'
    ActionChains(driver).key_down(Keys.CONTROL).click(select.select_by_index(1)).key_up(Keys.CONTROL).perform()
    assert len(select.all_selected_options) == 2
    assert select.all_selected_options[0].text == 'A'
    assert select.all_selected_options[1].text == 'B'
    assert select_paragraph.text == 'Selected: [ "A", "B" ]'
    ActionChains(driver).key_down(Keys.CONTROL).click(select.deselect_by_index(0)).key_up(Keys.CONTROL).perform()
    assert len(select.all_selected_options) == 1
    assert select_paragraph.text == 'Selected: [ "B" ]'
    driver.quit()