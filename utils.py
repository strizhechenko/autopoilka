# coding=utf-8
from selenium.webdriver.remote.webelement import WebElement


def fill(element, text):
    element.click()
    element.send_keys(text)
    return element


WebElement.fill = fill


def fill_form(driver, **kwargs):
    for k, v in kwargs.items():
        elem = driver.find_element_by_id(k)
        elem.fill(v)
