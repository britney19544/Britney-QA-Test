
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class LoginTest(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 20)
        self.driver.maximize_window()
        self.driver.get("https://stagewallet.mobipaid.com/login")

    def login(self, email, password):

        # Step 1: Enter email
        email_field = self.wait.until(
            EC.visibility_of_element_located((By.ID, "email"))
        )
        email_field.send_keys(email)

        # Step 2: Click Next
        next_button = self.wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "button[type='submit']")
            )
        )
        next_button.click()

        # Step 3: Wait for password field
        try:
            password_field = self.wait.until(
                EC.visibility_of_element_located(
                    (By.ID, "password_by_email")
                )
            )
        except Exception:
            self.driver.save_screenshot("debug_failed_email.png")
            print("\nScreenshot saved: debug_failed_email.png")
            print("Current URL:", self.driver.current_url)
            raise

        # Step 4: Enter password
        password_field.send_keys(password)

        # Step 5: Click Login
        login_button = self.wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "button[type='submit']")
            )
        )
        login_button.click()

    # TEST 1: Successful Login
    def test_successful_login(self):

        self.login("britney.jessica@student.umn.ac.id", "calumhood2026")

        # Wait until URL changes
        self.wait.until(
            EC.url_changes("https://stagewallet.mobipaid.com/login")
        )

        # Verify login success
        self.assertNotIn("/login", self.driver.current_url)

        self.driver.save_screenshot("successful_login.png")
        print("\nSuccessful login test completed.")

    # TEST 2: Failed Login - Invalid Email
    def test_failed_login(self):

        # Step 1: Enter invalid email
        email_field = self.wait.until(
            EC.visibility_of_element_located((By.ID, "email"))
        )
        email_field.send_keys("invalid@email.com")

        # Step 2: Click Next
        next_button = self.wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "button[type='submit']")
            )
        )
        next_button.click()

        # Step 3: Verify password field does NOT appear
        password_field = self.driver.find_elements(
            By.ID, "password_by_email"
        )

        self.assertEqual(
            len(password_field), 0,
            "Invalid email should not proceed to password page."
        )

        # Step 4: Screenshot
        self.driver.save_screenshot("failed_login.png")
        print("\nInvalid email rejected. Screenshot saved.")

    def tearDown(self):

        # Save screenshot if the test encounters an error
        if hasattr(self, "_outcome"):
            result = self._outcome.result
            if result and (result.failures or result.errors):
                self.driver.save_screenshot("test_error.png")
                print("\nError screenshot saved: test_error.png")

        self.driver.quit()


if __name__ == "__main__":
    unittest.main(verbosity=2)
