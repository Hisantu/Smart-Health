from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import random

class SmartHealthTest:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 10)
        self.base_url = "http://localhost:5173"
        
    def setup(self):
        self.driver.maximize_window()
        self.driver.get(self.base_url)
        
    def test_staff_login(self):
        """Test staff login flow"""
        print("Testing Staff Login...")
        
        # Select Staff role
        staff_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Staff Login')]")))
        staff_btn.click()
        
        # Enter credentials
        username = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Staff ID']")))
        password = self.driver.find_element(By.XPATH, "//input[@placeholder='Password']")
        
        username.send_keys("receptionist")
        password.send_keys("recep123")
        
        # Click login
        login_btn = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Login')]")
        login_btn.click()
        
        # Verify dashboard
        self.wait.until(EC.presence_of_element_located((By.XPATH, "//h2[contains(text(), 'Welcome Back')]")))
        print("✅ Staff login successful")
        
    def test_patient_registration(self):
        """Test patient registration"""
        print("Testing Patient Registration...")
        
        # Navigate to patient registration
        reg_card = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@href='/register-patient']")))
        reg_card.click()
        
        # Fill patient form
        name = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='John Doe']")))
        phone = self.driver.find_element(By.XPATH, "//input[@placeholder='+1234567890']")
        email = self.driver.find_element(By.XPATH, "//input[@placeholder='john@example.com']")
        age = self.driver.find_element(By.XPATH, "//input[@placeholder='25']")
        
        # Generate random data
        patient_name = f"Test Patient {random.randint(1000, 9999)}"
        patient_phone = f"+1{random.randint(1000000000, 9999999999)}"
        patient_email = f"test{random.randint(100, 999)}@example.com"
        
        name.send_keys(patient_name)
        phone.send_keys(patient_phone)
        email.send_keys(patient_email)
        age.send_keys("30")
        
        # Submit form
        register_btn = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Register Patient')]")
        register_btn.click()
        
        # Wait for success message
        self.wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'successfully')]")))
        print(f"✅ Patient registered: {patient_name}")
        return {"name": patient_name, "phone": patient_phone}
        
    def test_token_generation(self, patient_data):
        """Test token generation"""
        print("Testing Token Generation...")
        
        # Navigate to dashboard first
        self.driver.get(f"{self.base_url}/dashboard")
        time.sleep(2)
        
        # Navigate to token generation
        token_card = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@href='/generate-token']")))
        token_card.click()
        
        # Select patient
        patient_select = Select(self.wait.until(EC.presence_of_element_located((By.XPATH, "//select[option[contains(text(), 'Choose a patient')]]"))))
        patient_select.select_by_visible_text(f"{patient_data['name']} - {patient_data['phone']}")
        
        # Select department
        dept_select = Select(self.driver.find_element(By.XPATH, "//select[option[contains(text(), 'Choose a department')]]"))
        dept_select.select_by_index(1)  # Select first available department
        
        # Generate token
        generate_btn = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Generate Token')]")
        generate_btn.click()
        
        # Wait for token display
        token_number = self.wait.until(EC.presence_of_element_located((By.XPATH, "//h2[contains(@class, 'text-8xl')]")))
        print(f"✅ Token generated: {token_number.text}")
        return token_number.text
        
    def test_appointment_booking(self, patient_data):
        """Test appointment booking"""
        print("Testing Appointment Booking...")
        
        # Navigate to appointments
        self.driver.get(f"{self.base_url}/appointments")
        
        # Select patient
        patient_select = Select(self.wait.until(EC.presence_of_element_located((By.XPATH, "//select[option[contains(text(), 'Choose a patient')]]"))))
        patient_select.select_by_visible_text(f"{patient_data['name']} - {patient_data['phone']}")
        
        # Select department
        dept_select = Select(self.driver.find_element(By.XPATH, "//select[option[contains(text(), 'Choose a department')]]"))
        dept_select.select_by_index(1)
        
        time.sleep(1)  # Wait for doctors to load
        
        # Select doctor
        doctor_select = Select(self.driver.find_element(By.XPATH, "//select[option[contains(text(), 'Choose a doctor')]]"))
        doctor_select.select_by_index(1)
        
        # Set appointment date (tomorrow)
        from datetime import datetime, timedelta
        tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        date_input = self.driver.find_element(By.XPATH, "//input[@type='date']")
        date_input.send_keys(tomorrow)
        
        # Select time slot
        time_select = Select(self.driver.find_element(By.XPATH, "//select[option[contains(text(), '09:00 AM')]]"))
        time_select.select_by_value("10:00")
        
        # Add reason
        reason_textarea = self.driver.find_element(By.XPATH, "//textarea[@placeholder='Describe your symptoms or reason for consultation']")
        reason_textarea.send_keys("Regular checkup and consultation")
        
        # Book appointment
        book_btn = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Book Appointment')]")
        book_btn.click()
        
        # Wait for success
        self.wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'successfully')]")))
        print("✅ Appointment booked successfully")
        
    def test_queue_management(self):
        """Test queue management"""
        print("Testing Queue Management...")
        
        # Navigate to queue management
        self.driver.get(f"{self.base_url}/queue")
        
        # Wait for queue to load
        time.sleep(3)
        
        # Check if tokens are present
        tokens = self.driver.find_elements(By.XPATH, "//div[contains(@class, 'bg-white') and contains(@class, 'rounded-2xl')]//h3")
        
        if tokens:
            # Call first token
            call_btn = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Call')]")
            call_btn.click()
            print("✅ Token called successfully")
        else:
            print("ℹ️ No tokens in queue")
            
    def test_display_board(self):
        """Test display board"""
        print("Testing Display Board...")
        
        # Open display board in new tab
        self.driver.execute_script("window.open('');")
        self.driver.switch_to.window(self.driver.window_handles[1])
        self.driver.get(f"{self.base_url}/display")
        
        # Verify display board loads
        self.wait.until(EC.presence_of_element_located((By.XPATH, "//h1[contains(text(), 'Smart Health Queue System')]")))
        print("✅ Display board loaded successfully")
        
        # Switch back to main window
        self.driver.switch_to.window(self.driver.window_handles[0])
        
    def test_patient_login_flow(self):
        """Test patient login and registration flow"""
        print("Testing Patient Login Flow...")
        
        # Logout first
        self.driver.get(f"{self.base_url}/login")
        
        # Select Patient role
        patient_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Patient Login')]")))
        patient_btn.click()
        
        # Click register for new patient
        register_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'New Patient? Register')]")))
        register_btn.click()
        
        # Fill registration form
        name = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Full Name']")))
        phone = self.driver.find_element(By.XPATH, "//input[@placeholder='Phone Number']")
        
        patient_name = f"Patient User {random.randint(1000, 9999)}"
        patient_phone = f"{random.randint(1000000000, 9999999999)}"
        
        name.send_keys(patient_name)
        phone.send_keys(patient_phone)
        
        # Submit registration
        register_submit = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Register & Login')]")
        register_submit.click()
        
        # Verify patient dashboard
        self.wait.until(EC.presence_of_element_located((By.XPATH, "//h1[contains(text(), 'Patient Portal')]")))
        print("✅ Patient registration and login successful")
        
    def run_all_tests(self):
        """Run all automated tests"""
        try:
            self.setup()
            
            # Test staff login
            self.test_staff_login()
            time.sleep(2)
            
            # Test patient registration
            patient_data = self.test_patient_registration()
            time.sleep(2)
            
            # Test token generation
            token = self.test_token_generation(patient_data)
            time.sleep(2)
            
            # Test appointment booking
            self.test_appointment_booking(patient_data)
            time.sleep(2)
            
            # Test queue management
            self.test_queue_management()
            time.sleep(2)
            
            # Test display board
            self.test_display_board()
            time.sleep(2)
            
            # Test patient login flow
            self.test_patient_login_flow()
            
            print("\n🎉 All tests completed successfully!")
            
        except Exception as e:
            print(f"❌ Test failed: {str(e)}")
            
        finally:
            input("Press Enter to close browser...")
            self.driver.quit()

if __name__ == "__main__":
    test = SmartHealthTest()
    test.run_all_tests()