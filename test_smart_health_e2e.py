import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import random
from datetime import datetime, timedelta

class TestSmartHealthE2E:
    
    @pytest.fixture(scope="class")
    def driver(self):
        options = Options()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1920,1080")
        
        driver = webdriver.Chrome(options=options)
        driver.maximize_window()
        yield driver
        driver.quit()
    
    @pytest.fixture(scope="class")
    def base_url(self):
        return "https://smart-health-1-nmts.onrender.com"
    
    @pytest.fixture(scope="class")
    def wait(self, driver):
        return WebDriverWait(driver, 15)
    
    @pytest.fixture(scope="class")
    def test_phone(self):
        return f"555{random.randint(1000000, 9999999)}"
    
    @pytest.fixture(scope="class")
    def generated_token(self):
        return {"token": None}

    def test_phase1_patient_login(self, driver, wait, base_url, test_phone):
        """Phase 1: Patient Login"""
        driver.get(base_url)
        time.sleep(3)
        
        # Click Patient Login
        patient_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Patient')]")))
        patient_btn.click()
        
        # Enter phone number
        phone_field = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='tel' or contains(@placeholder, 'Phone')]")))
        phone_field.send_keys(test_phone)
        
        # Click Login
        login_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Login')]")
        login_btn.click()
        time.sleep(2)
        
        # Verify patient dashboard or registration prompt
        assert driver.current_url != base_url
    
    def test_phase1_book_appointment(self, driver, wait, test_phone):
        """Phase 1: Book Appointment"""
        # Navigate to Book Appointment
        appointment_link = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, 'appointment') or contains(text(), 'Appointment')]")))
        appointment_link.click()
        time.sleep(2)
        
        # Select Patient
        patient_select = Select(wait.until(EC.presence_of_element_located((By.XPATH, "//select[option[contains(text(), 'patient')]]"))))
        patient_select.select_by_index(1)
        
        # Select Department
        dept_select = Select(driver.find_element(By.XPATH, "//select[option[contains(text(), 'department')]]"))
        dept_select.select_by_visible_text("Cardiology")
        time.sleep(1)
        
        # Select Doctor
        doctor_select = Select(driver.find_element(By.XPATH, "//select[option[contains(text(), 'doctor')]]"))
        doctor_select.select_by_index(1)
        
        # Choose date (tomorrow)
        date_input = driver.find_element(By.XPATH, "//input[@type='date']")
        tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        date_input.send_keys(tomorrow)
        
        # Choose time
        time_select = Select(driver.find_element(By.XPATH, "//select[option[contains(text(), 'AM') or contains(text(), 'PM')]]"))
        time_select.select_by_index(1)
        
        # Enter reason
        reason_field = driver.find_element(By.XPATH, "//textarea")
        reason_field.send_keys("Automated test appointment")
        
        # Book appointment
        book_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Book')]")
        book_btn.click()
        time.sleep(3)
        
        # Verify booking success
        success_msg = driver.find_elements(By.XPATH, "//*[contains(text(), 'success') or contains(text(), 'booked')]")
        assert len(success_msg) > 0
    
    def test_phase1_generate_token(self, driver, wait, generated_token):
        """Phase 1: Generate Token"""
        # Navigate to Generate Token
        token_link = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, 'token') or contains(text(), 'Token')]")))
        token_link.click()
        time.sleep(2)
        
        # Select Cardiology
        dept_select = Select(wait.until(EC.presence_of_element_located((By.XPATH, "//select[option[contains(text(), 'department')]]"))))
        dept_select.select_by_visible_text("Cardiology")
        
        # Click Generate
        generate_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Generate')]")
        generate_btn.click()
        time.sleep(3)
        
        # Capture token number
        token_element = wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'CAR-') or contains(@class, 'token')]")))
        token_text = token_element.text
        generated_token["token"] = token_text
        
        assert "CAR-" in token_text or len(token_text) > 3
    
    def test_phase2_staff_login(self, driver, wait, base_url):
        """Phase 2: Staff Login"""
        driver.get(base_url)
        time.sleep(3)
        
        # Click Staff Login
        staff_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Staff')]")))
        staff_btn.click()
        
        # Enter credentials
        username_field = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='text' or @placeholder='Username' or @placeholder='Staff ID']")))
        password_field = driver.find_element(By.XPATH, "//input[@type='password']")
        
        username_field.send_keys("receptionist")
        password_field.send_keys("recep123")
        
        # Click Login
        login_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Login')]")
        login_btn.click()
        time.sleep(3)
        
        # Verify staff dashboard
        dashboard_elements = driver.find_elements(By.XPATH, "//*[contains(text(), 'Dashboard') or contains(text(), 'Welcome')]")
        assert len(dashboard_elements) > 0
    
    def test_phase2_patient_registration(self, driver, wait):
        """Phase 2: Patient Registration"""
        # Navigate to Patient Registration
        reg_link = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, 'register') or contains(text(), 'Registration')]")))
        reg_link.click()
        time.sleep(2)
        
        # Generate random data
        name = f"Test Patient {random.randint(1000, 9999)}"
        phone = f"555{random.randint(1000000, 9999999)}"
        email = f"test{random.randint(100, 999)}@example.com"
        age = str(random.randint(18, 80))
        
        # Fill form fields
        name_field = wait.until(EC.presence_of_element_located((By.XPATH, "//input[contains(@placeholder, 'Name')]")))
        phone_field = driver.find_element(By.XPATH, "//input[contains(@placeholder, 'Phone')]")
        email_field = driver.find_element(By.XPATH, "//input[@type='email']")
        age_field = driver.find_element(By.XPATH, "//input[contains(@placeholder, 'Age')]")
        
        name_field.send_keys(name)
        phone_field.send_keys(phone)
        email_field.send_keys(email)
        age_field.send_keys(age)
        
        # Select Gender
        gender_select = Select(driver.find_element(By.XPATH, "//select"))
        gender_select.select_by_visible_text("Male")
        
        # Fill Address
        address_field = driver.find_element(By.XPATH, "//textarea")
        address_field.send_keys("123 Test Street, Test City")
        
        # Submit registration
        register_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Register')]")
        register_btn.click()
        time.sleep(3)
        
        # Verify registration success
        success_msg = driver.find_elements(By.XPATH, "//*[contains(text(), 'success') or contains(text(), 'registered')]")
        assert len(success_msg) > 0
    
    def test_phase2_queue_management_setup(self, driver, wait):
        """Phase 2: Queue Management Setup"""
        # Navigate to Queue Management
        queue_link = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, 'queue') or contains(text(), 'Queue')]")))
        queue_link.click()
        time.sleep(3)
        
        # Select Cardiology department
        dept_select = Select(wait.until(EC.presence_of_element_located((By.XPATH, "//select[option[contains(text(), 'department')]]"))))
        dept_select.select_by_visible_text("Cardiology")
        time.sleep(2)
        
        # Assign Doctor to Counter 1
        counter_field = driver.find_element(By.XPATH, "//input[contains(@placeholder, 'Counter') or @value='Counter 1']")
        counter_field.clear()
        counter_field.send_keys("Counter 1")
        
        # Click Active checkbox if present
        try:
            active_checkbox = driver.find_element(By.XPATH, "//input[@type='checkbox']")
            if not active_checkbox.is_selected():
                active_checkbox.click()
        except:
            pass
        
        time.sleep(2)
    
    def test_phase2_verify_token_in_queue(self, driver, wait, generated_token):
        """Phase 2: Verify Token in Queue"""
        # Look for the generated token in the queue
        token_to_find = generated_token["token"]
        
        if token_to_find:
            # Search for token in queue section
            token_elements = driver.find_elements(By.XPATH, f"//*[contains(text(), '{token_to_find}') or contains(text(), 'CAR-')]")
            
            # If not found, refresh and try again
            if not token_elements:
                driver.refresh()
                time.sleep(3)
                token_elements = driver.find_elements(By.XPATH, f"//*[contains(text(), '{token_to_find}') or contains(text(), 'CAR-')]")
            
            # Assert token is visible in queue
            assert len(token_elements) > 0, f"Token {token_to_find} not found in queue"
        else:
            # Fallback: check for any Cardiology tokens
            cardiology_tokens = driver.find_elements(By.XPATH, "//*[contains(text(), 'CAR-')]")
            assert len(cardiology_tokens) > 0, "No Cardiology tokens found in queue"

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])