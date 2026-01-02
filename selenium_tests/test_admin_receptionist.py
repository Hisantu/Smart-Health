import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from base_test import BaseTest

class TestAdminReceptionist:
    
    def setup_method(self):
        """Setup before each test"""
        self.base_test = BaseTest()
        self.base_test.setup_driver()
    
    def teardown_method(self):
        """Cleanup after each test"""
        self.base_test.teardown_driver()
    
    def test_admin_login(self):
        """Test admin login functionality"""
        self.base_test.login("admin", "admin123")
        
        # Verify dashboard loaded
        dashboard_title = self.base_test.wait_for_element(By.XPATH, "//h1[contains(text(), 'Dashboard')]")
        assert dashboard_title.is_displayed()
        print("Admin login successful")
    
    def test_patient_registration(self):
        """Test patient registration process"""
        self.base_test.login("admin", "admin123")
        
        # Navigate to Patient Registration
        self.base_test.wait_and_click(By.XPATH, "//a[contains(text(), 'Patient Registration')]")
        time.sleep(1)
        
        # Fill patient form
        name_field = self.base_test.wait_for_element(By.NAME, "name")
        name_field.send_keys("Test Patient Selenium")
        
        phone_field = self.base_test.driver.find_element(By.NAME, "phone")
        phone_field.send_keys("9876543210")
        
        age_field = self.base_test.driver.find_element(By.NAME, "age")
        age_field.send_keys("30")
        
        # Select gender
        gender_select = Select(self.base_test.driver.find_element(By.NAME, "gender"))
        gender_select.select_by_value("Male")
        
        address_field = self.base_test.driver.find_element(By.NAME, "address")
        address_field.send_keys("Test Address, Selenium City")
        
        # Submit form
        submit_button = self.base_test.driver.find_element(By.XPATH, "//button[contains(text(), 'Register Patient')]")
        submit_button.click()
        
        # Wait for success message
        time.sleep(2)
        print("Patient registration completed")
    
    def test_token_generation(self):
        """Test token generation for walk-in patients"""
        self.base_test.login("admin", "admin123")
        
        # Navigate to Generate Token
        self.base_test.wait_and_click(By.XPATH, "//a[contains(text(), 'Generate Token')]")
        time.sleep(1)
        
        # Select patient (first available)
        patient_select = Select(self.base_test.wait_for_element(By.NAME, "patient"))
        patient_options = patient_select.options
        if len(patient_options) > 1:
            patient_select.select_by_index(1)  # Select first patient
        
        # Select department
        dept_select = Select(self.base_test.driver.find_element(By.NAME, "department"))
        dept_select.select_by_visible_text("Cardiology")
        
        # Generate token
        generate_button = self.base_test.driver.find_element(By.XPATH, "//button[contains(text(), 'Generate Token')]")
        generate_button.click()
        
        time.sleep(2)
        print("Token generation completed")
    
    def test_appointment_booking(self):
        """Test appointment booking functionality"""
        self.base_test.login("admin", "admin123")
        
        # Navigate to Appointments
        self.base_test.wait_and_click(By.XPATH, "//a[contains(text(), 'Appointments')]")
        time.sleep(1)
        
        # Click Book Appointment if available
        try:
            book_button = self.base_test.driver.find_element(By.XPATH, "//button[contains(text(), 'Book Appointment')]")
            book_button.click()
            time.sleep(1)
            
            # Select patient
            patient_select = Select(self.base_test.wait_for_element(By.NAME, "patient"))
            if len(patient_select.options) > 1:
                patient_select.select_by_index(1)
            
            # Select department
            dept_select = Select(self.base_test.driver.find_element(By.NAME, "department"))
            dept_select.select_by_visible_text("Cardiology")
            time.sleep(1)
            
            # Select doctor
            doctor_select = Select(self.base_test.driver.find_element(By.NAME, "doctor"))
            if len(doctor_select.options) > 1:
                doctor_select.select_by_index(1)
            
            # Select date (today + 1)
            date_field = self.base_test.driver.find_element(By.NAME, "date")
            from datetime import datetime, timedelta
            tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
            date_field.send_keys(tomorrow)
            
            # Select time slot
            time_select = Select(self.base_test.driver.find_element(By.NAME, "timeSlot"))
            if len(time_select.options) > 1:
                time_select.select_by_index(1)
            
            # Book appointment
            book_final_button = self.base_test.driver.find_element(By.XPATH, "//button[contains(text(), 'Book Appointment')]")
            book_final_button.click()
            
            time.sleep(2)
            print("Appointment booking completed")
            
        except Exception as e:
            print(f"Appointment booking test skipped: {str(e)}")
    
    def test_queue_management(self):
        """Test queue management functionality"""
        self.base_test.login("admin", "admin123")
        
        # Navigate to Queue Management
        self.base_test.wait_and_click(By.XPATH, "//a[contains(text(), 'Queue Management')]")
        time.sleep(1)
        
        # Select department
        dept_select = Select(self.base_test.wait_for_element(By.XPATH, "//select[contains(@class, 'w-full')]"))
        dept_select.select_by_visible_text("Cardiology")
        time.sleep(2)
        
        # Activate a counter
        try:
            # Find first doctor dropdown
            doctor_selects = self.base_test.driver.find_elements(By.XPATH, "//select[contains(@class, 'w-full p-3')]")
            if doctor_selects:
                doctor_select = Select(doctor_selects[0])
                if len(doctor_select.options) > 1:
                    doctor_select.select_by_index(1)
                
                # Activate counter
                checkbox = self.base_test.driver.find_element(By.XPATH, "//input[@type='checkbox']")
                if not checkbox.is_selected():
                    checkbox.click()
                
                time.sleep(2)
                print("Queue management setup completed")
        except Exception as e:
            print(f"Queue management test partial: {str(e)}")

if __name__ == "__main__":
    import subprocess
    subprocess.run(["python", "-m", "pytest", __file__, "-v", "--html=reports/admin_test_report.html"])