# coding: utf-8

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import logging
from utils import fill_form
import config
import time

driver = webdriver.Firefox()
driver.fill_form = fill_form
driver.maximize_window()
logging.basicConfig(level=logging.INFO)

org_name = ''


def login():
    logging.info("Вхожу")
    url = f'{config.url}/login'
    logging.info(url)
    driver.get(url)
    fill_form(driver, **{
        'input-email': config.user,
        'input-password': config.secret
    })
    driver.find_element_by_xpath('//input[@value="Войти"]').click()


def repeat_latest():
    logging.info("Иду в историю заказов!")
    driver.get(f'{config.url}/order-history')
    table = driver.find_element_by_class_name('order-history-table').find_element_by_tag_name('tbody')
    order = table.find_element_by_tag_name('tr')
    repeat = order.find_element_by_class_name('ord-action').find_element_by_class_name('btn-primary')
    repeat.click()


def choose_next_day():
    logging.info("Пытаюсь повторить заказ")
    driver.find_element_by_class_name('fa-calendar').click()
    datepicker = driver.find_element_by_class_name('datepicker-days')
    today = False
    for day in datepicker.find_elements_by_class_name('day'):
        logging.debug('debug: day %s', day.text)
        if 'today' in day.get_attribute('class'):
            today = True
            continue
        elif not today:
            continue
        logging.info("RIGHT day: %s", day.text)
        day.click()
        return


def choose_morning():
    logging.info("Осталось выбрать время")
    time.sleep(1)
    variants = driver.find_element_by_id('customer_order_time_type').find_elements_by_tag_name('option')
    found = False
    for variant in variants:
        if 'утро' in variant.text.lower():
            found = True
            variant.click()
            break
    if not found:
        raise NoSuchElementException("Не нашёл утро")
    time.sleep(1)
    time_range = driver.find_element_by_id('customer_order_time_morning').find_element_by_tag_name('option')
    if '13:00' not in time_range.text:
        raise NoSuchElementException("Не нашёл 9:00 - 13:00")
    time_range.click()


def choose_yandex():
    logging.info("Осталась только оплата!")
    time.sleep(1)
    driver.find_element_by_id('yandex_money').click()
    time.sleep(1)
    driver.find_element_by_id('simplecheckout_button_next').click()


def choose_alfabank():
    time.sleep(1)
    form = driver.find_element_by_id('yandex-money-payment-form')
    found = False
    for method in form.find_elements_by_tag_name('input'):
        if method.get_attribute('value') == 'alfabank':
            found = True
            method.click()
            break
    if not found:
        raise NoSuchElementException("Не нашли альфабанк")
    print(1)


def send_bill():
    driver.find_element_by_id('alfa-login').fill(config.phone)
    driver.find_element_by_class_name('simplecheckout-button-right').click()


def main():
    try:
        login()
        repeat_latest()
        choose_next_day()
        choose_morning()
        choose_yandex()
        choose_alfabank()
        send_bill()
    except Exception as err:
        logging.exception(err)
        driver.close()


if __name__ == '__main__':
    main()
