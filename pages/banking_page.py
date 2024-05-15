import csv
import datetime
import time
from itertools import islice

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class BankingPage:
    def __init__(self, driver):
        self.driver = driver

    def get_balance(self):
        wait = WebDriverWait(self.driver, 10)
        balance_element = wait.until(EC.visibility_of_element_located((
            By.XPATH,
            "//div[@class='center'][1]//strong[@class='ng-binding'][2]")))
        return balance_element.text

    def fibonacci(self):
        a, b = 0, 1
        while True:
            yield a
            a, b = b, a + b

    def get_fibonacci_for_today(self):
        today = datetime.datetime.now()
        day_of_month = today.day
        fib_gen = self.fibonacci()
        fibonacci_number = next(
            islice(fib_gen, day_of_month + 1, day_of_month + 2))
        return fibonacci_number

    def is_deposit_button_visible(self):
        wait = WebDriverWait(self.driver, 10)
        print("Waiting for Deposit button to be visible...")
        return wait.until(EC.visibility_of_element_located(
            (By.XPATH, "//button[@ng-click='deposit()']")))

    def click_deposit_button(self):
        wait = WebDriverWait(self.driver, 10)
        print("Clicking on Deposit button...")
        deposit_button = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[@ng-click='deposit()']")))
        deposit_button.click()

    def is_deposit_form_visible(self):
        wait = WebDriverWait(self.driver, 10)
        print("Waiting for Deposit form to be visible...")
        return wait.until(EC.visibility_of_element_located((By.XPATH,
                                                            "//form[@name='myForm']//input[@placeholder='amount']")))

    def enter_deposit_amount(self, amount):
        wait = WebDriverWait(self.driver, 10)
        print(f"Entering deposit amount: {amount}")
        time.sleep(2)
        amount_input = wait.until(EC.visibility_of_element_located((By.XPATH,
                                                                    "//form[@name='myForm']//input[@placeholder='amount']")))
        amount_input.send_keys(str(amount))
        time.sleep(2)

    def click_submit_deposit(self):
        wait = WebDriverWait(self.driver, 10)
        print("Clicking on Submit Deposit button...")
        submit_button = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//form[@name='myForm']//button[@type='submit']")))
        submit_button.click()

    def is_deposit_successful(self):
        wait = WebDriverWait(self.driver, 10)
        print("Waiting for 'Deposit Successful' message...")
        return wait.until(EC.visibility_of_element_located(
            (By.XPATH, "//span[text()='Deposit Successful']")))

    def is_withdraw_button_visible(self):
        wait = WebDriverWait(self.driver, 10)
        print("Waiting for Withdraw button to be visible...")
        return wait.until(EC.visibility_of_element_located(
            (By.XPATH, "//button[@ng-click='withdrawl()']")))

    def click_withdraw_button(self):
        wait = WebDriverWait(self.driver, 10)
        print("Clicking on Withdraw button...")
        withdraw_button = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[@ng-click='withdrawl()']")))
        withdraw_button.click()

    def is_withdraw_form_visible(self):
        wait = WebDriverWait(self.driver, 10)
        print("Waiting for Withdraw form to be visible...")
        return wait.until(EC.visibility_of_element_located((By.XPATH,
                                                            "//form[@name='myForm']//input[@placeholder='amount']")))

    def enter_withdraw_amount(self, amount):
        wait = WebDriverWait(self.driver, 15)
        print(f"Entering withdraw amount: {amount}")
        time.sleep(2)
        withdraw_input = wait.until(EC.visibility_of_element_located((By.XPATH,
                                                                      "//form[@name='myForm']//input[@placeholder='amount']")))
        withdraw_input.send_keys(str(amount))

    def click_submit_withdraw(self):
        wait = WebDriverWait(self.driver, 10)
        print("Clicking on Submit Withdraw button...")
        submit_button = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//form[@name='myForm']//button[@type='submit']")))
        submit_button.click()
        time.sleep(3)

    def is_withdraw_successful(self):
        wait = WebDriverWait(self.driver, 10)
        print("Waiting for 'Transaction successful' message...")
        return wait.until(EC.visibility_of_element_located(
            (By.XPATH, "//span[text()='Transaction successful']")))

    def is_transactions_button_visible(self):
        wait = WebDriverWait(self.driver, 10)
        print("Waiting for Transactions button to be visible...")
        return wait.until(EC.visibility_of_element_located(
            (By.XPATH, "//button[@ng-click='transactions()']")))

    def click_transactions_button(self):
        wait = WebDriverWait(self.driver, 10)
        print("Clicking on Transactions button...")
        transactions_button = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[@ng-click='transactions()']")))
        transactions_button.click()
        time.sleep(3)

    def get_transactions(self):
        wait = WebDriverWait(self.driver, 10)
        print("Waiting for transactions to be visible...")
        transactions_table = wait.until(EC.visibility_of_element_located((
            By.XPATH,
            "//table[@class='table table-bordered table-striped']")))
        transactions = []
        rows = transactions_table.find_elements(By.XPATH, ".//tbody/tr")
        for row in rows:
            date_time = row.find_element(By.XPATH, ".//td[1]").text
            amount = row.find_element(By.XPATH, ".//td[2]").text
            transaction_type = row.find_element(By.XPATH, ".//td[3]").text
            transactions.append((date_time, amount, transaction_type))
        return transactions

    def export_transactions_to_csv(self, transactions, file_path):
        with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Дата-время Транзакции', 'Сумма', 'Тип Транзакции']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for transaction in transactions:
                date_time_str = datetime.datetime.strptime(transaction[0],
                                                           "%b %d, %Y %I:%M:%S %p").strftime(
                    "%d %B %Y %H:%M:%S")
                writer.writerow({
                    'Дата-время Транзакции': date_time_str,
                    'Сумма': transaction[1],
                    'Тип Транзакции': transaction[2]
                })
