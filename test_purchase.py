import unittest

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import support.ui as ui
import support.pages as pages


class TestPurchase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.browser = webdriver.Chrome()
        cls.browser.implicitly_wait(1)

    def test_purchase(self):
        pages.LoginPage(self.browser).open()
        pages.LoginPage(self.browser).login('s1iderorama@gmail.com', 'codespace')

        ui.Link(self.browser, 'Men').hover()
        ui.Link(self.browser, 'Blazers').click()

        ui.Product(self.browser, 'Stretch Cotton Blazer').select()

        ui.Select(self.browser, 'Color').select_by_text('Blue')
        ui.Select(self.browser, 'Size').select_by_text('M')
        ui.Button(self.browser, 'Add to Cart').click()

        ui.Button(self.browser, 'Proceed to Checkout').click()

        self.assertTrue(ui.Header(self.browser, 'Checkout').is_visible)

        checkout = pages.CheckoutPage(self.browser)
        # 1 billing information
        checkout.continue_checkout()

        # 2 shipping method
        ui.Checkbox(self.browser, 'Add gift options').wait_for_element_visible().click()
        checkout.continue_checkout()

        # 3 payment information
        WebDriverWait(self.browser, 5).until(
            EC.presence_of_element_located(
                (By.XPATH, '//label[contains(text(), "Cash On Delivery ")]')
            )
        )
        checkout.continue_checkout()

        # 4 place order
        ui.Button(self.browser, 'Place Order').click()

        # 5 verify confirmation page
        self.assertTrue(
            ui.Header(self.browser, 'Your order has been received.').is_visible
        )