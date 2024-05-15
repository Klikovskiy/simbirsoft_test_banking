import os

import allure
import pytest

from pages.banking_page import BankingPage
from pages.login_page import LoginPage


@pytest.mark.order(1)
@pytest.mark.usefixtures("setup", "login")
class TestBanking:

    def test_customer_login(self):
        login_page = LoginPage(self.driver)
        login_page.load()
        # Проверяем наличие кнопки "Customer Login"
        assert login_page.is_customer_login_button_visible()
        login_page.go_to_customer_login()
        # Проверяем наличие выпадающего списка
        assert login_page.is_customer_select_visible()
        login_page.select_customer("Harry Potter")
        login_page.click_login()

    def test_deposit_and_withdraw(self):
        banking_page = BankingPage(self.driver)

        # Проверяем стартовый баланс на нулевое значение
        balance = banking_page.get_balance()
        assert balance == '0', f"Expected balance to be 0, but got {balance}"

        # Вычисляем число Фибоначчи для текущего дня
        fibonacci_number = banking_page.get_fibonacci_for_today()
        print(f"Fibonacci Number: {fibonacci_number}")

        # Проверяем наличие кнопки Deposit
        print("Checking if Deposit button is visible...")
        assert banking_page.is_deposit_button_visible()

        # Нажимаем на кнопку Deposit
        banking_page.click_deposit_button()

        # Проверяем, что форма ввода суммы депозита появилась
        print("Checking if Deposit form is visible...")
        assert banking_page.is_deposit_form_visible()

        # Вводим полученное число Фибоначчи в форму
        banking_page.enter_deposit_amount(fibonacci_number)

        # Нажимаем кнопку Deposit для подтверждения
        banking_page.click_submit_deposit()

        # Проверяем, что появилось сообщение "Deposit Successful"
        print("Checking if 'Deposit Successful' message is visible...")
        assert banking_page.is_deposit_successful()

        # Проверяем, что баланс обновился
        print("Checking updated balance...")
        updated_balance = banking_page.get_balance()
        assert updated_balance == str(
            fibonacci_number), f"Expected balance to be {fibonacci_number}, but got {updated_balance}"

        # Проверяем наличие кнопки Withdraw
        print("Checking if Withdraw button is visible...")
        assert banking_page.is_withdraw_button_visible()

        # Нажимаем на кнопку Withdraw
        banking_page.click_withdraw_button()

        # Проверяем, что форма ввода суммы вывода появилась
        print("Checking if Withdraw form is visible...")
        assert banking_page.is_withdraw_form_visible()

        # Вводим полученное число Фибоначчи в форму
        banking_page.enter_withdraw_amount(fibonacci_number)

        # Нажимаем кнопку Withdraw для подтверждения
        banking_page.click_submit_withdraw()

        # Проверяем, что появилось сообщение "Transaction successful"
        print("Checking if 'Transaction successful' message is visible...")
        assert banking_page.is_withdraw_successful()

        # Проверяем, что баланс изменился на 0
        print("Checking final balance...")
        final_balance = banking_page.get_balance()
        assert final_balance == '0', f"Expected final balance to be 0, but got {final_balance}"

        # Проверяем наличие кнопки Transactions
        print("Checking if Transactions button is visible...")
        assert banking_page.is_transactions_button_visible()

        # Нажимаем на кнопку Transactions
        banking_page.click_transactions_button()

        # Получаем данные о транзакциях
        print("Fetching transactions data...")
        transactions = banking_page.get_transactions()

        # Проверяем, что транзакции содержат обе операции
        print(
            "Checking if transactions contain both deposit and withdraw operations...")
        assert any(
            tx[1] == str(fibonacci_number) and tx[2] == "Credit" for tx in
            transactions), "Deposit transaction not found"
        assert any(
            tx[1] == str(fibonacci_number) and tx[2] == "Debit" for tx in
            transactions), "Withdraw transaction not found"

        # Экспорт данных о транзакциях в CSV-файл
        csv_file_path = os.path.join(os.getcwd(), 'transactions.csv', )
        banking_page.export_transactions_to_csv(transactions, csv_file_path)

        # Прикрепляем CSV-файл к отчету Allure
        with open(csv_file_path, 'r') as file:
            allure.attach(file.read(), name='Transactions Report',
                          attachment_type=allure.attachment_type.CSV)
