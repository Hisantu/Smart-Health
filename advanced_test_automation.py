from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import json
import random
from datetime import datetime, timedelta
import os

class AdvancedSmartHealthTest:
    def __init__(self):
        options = Options()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1920,1080")
        
        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, 15)
        self.base_url = "http://localhost:5173"
        self.test_results = {"passed": 0, "failed": 0, "errors": []}
        self.screenshots_dir = "test_screenshots"
        os.makedirs(self.screenshots_dir, exist_ok=True)
        
    def take_screenshot(self, name):
        """Screenshot capture for documentation"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.screenshots_dir}/{name}_{timestamp}.png"
        self.driver.save_screenshot(filename)
        print(f"📸 Screenshot: {filename}")
        
    def log_result(self, test_name, passed, error=None):
        """Test reporting"""
        if passed:
            self.test_results["passed"] += 1
            print(f"✅ {test_name}")
        else:
            self.test_results["failed"] += 1
            self.test_results["errors"].append({"test": test_name, "error": str(error)})
            print(f"❌ {test_name}: {error}")
            
    def complete_workflow_testing(self):
        """Complete workflow testing"""
        print("🚀 Starting Complete Workflow Testing...")
        
        try:
            # Staff Login
            self.driver.get(self.base_url)
            self.take_screenshot("01_homepage")
            
            self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Staff Login')]"))).click()
            self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Staff ID']"))).send_keys("receptionist")
            self.driver.find_element(By.XPATH, "//input[@placeholder='Password']").send_keys("recep123")
            self.driver.find_element(By.XPATH, "//button[contains(text(), 'Login')]").click()
            
            self.wait.until(EC.presence_of_element_located((By.XPATH, "//h2[contains(text(), 'Welcome Back')]")))
            self.take_screenshot("02_staff_dashboard")
            self.log_result("Staff Login", True)
            
        except Exception as e:
            self.log_result("Staff Login", False, e)
            
    def multiple_patient_registration(self):
        """Multiple patient registration"""
        print("👥 Multiple Patient Registration...")
        
        patients = [
            {"name": f"Patient A{random.randint(100,999)}", "phone": f"555{random.randint(1000000,9999999)}", "age": "25"},
            {"name": f"Patient B{random.randint(100,999)}", "phone": f"555{random.randint(1000000,9999999)}", "age": "35"},
            {"name": f"Patient C{random.randint(100,999)}", "phone": f"555{random.randint(1000000,9999999)}", "age": "45"}
        ]
        
        registered_patients = []
        
        for i, patient in enumerate(patients):
            try:
                self.wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@href='/register-patient']"))).click()
                
                self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='John Doe']"))).send_keys(patient["name"])
                self.driver.find_element(By.XPATH, "//input[@placeholder='+1234567890']").send_keys(patient["phone"])
                self.driver.find_element(By.XPATH, "//input[@placeholder='john@example.com']").send_keys(f"test{i}@example.com")
                self.driver.find_element(By.XPATH, "//input[@placeholder='25']").send_keys(patient["age"])
                
                self.driver.find_element(By.XPATH, "//button[contains(text(), 'Register Patient')]").click()
                self.wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'successfully')]")))
                
                registered_patients.append(patient)
                self.driver.get(f"{self.base_url}/dashboard")
                time.sleep(1)
                
                self.log_result(f"Patient Registration {i+1}", True)
                
            except Exception as e:
                self.log_result(f"Patient Registration {i+1}", False, e)
                
        self.take_screenshot("03_patients_registered")
        return registered_patients
        
    def bulk_token_generation(self, patients):
        """Bulk token generation"""
        print("🎫 Bulk Token Generation...")
        
        generated_tokens = []
        
        for i, patient in enumerate(patients):
            try:
                self.wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@href='/generate-token']"))).click()
                
                # Select patient
                patient_select = Select(self.wait.until(EC.presence_of_element_located((By.XPATH, "//select[option[contains(text(), 'Choose a patient')]]"))))
                patient_select.select_by_visible_text(f"{patient['name']} - {patient['phone']}")
                
                # Select department
                dept_select = Select(self.driver.find_element(By.XPATH, "//select[option[contains(text(), 'Choose a department')]]"))
                dept_select.select_by_index(random.randint(1, min(4, len(dept_select.options)-1)))
                
                self.driver.find_element(By.XPATH, "//button[contains(text(), 'Generate Token')]").click()
                
                token_element = self.wait.until(EC.presence_of_element_located((By.XPATH, "//h2[contains(@class, 'text-8xl')]")))
                token_number = token_element.text
                generated_tokens.append(token_number)
                
                self.driver.find_element(By.XPATH, "//button[contains(text(), 'Back to Dashboard')]").click()
                time.sleep(1)
                
                self.log_result(f"Token Generation {i+1}", True)
                
            except Exception as e:
                self.log_result(f"Token Generation {i+1}", False, e)
                
        self.take_screenshot("04_tokens_generated")
        return generated_tokens
        
    def priority_token_testing(self, patients):
        """Priority token testing"""
        print("⚡ Priority Token Testing...")
        
        try:
            # Generate priority token for first patient
            self.wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@href='/generate-token']"))).click()
            
            # Select patient
            patient_select = Select(self.wait.until(EC.presence_of_element_located((By.XPATH, "//select[option[contains(text(), 'Choose a patient')]]"))))
            patient_select.select_by_visible_text(f"{patients[0]['name']} - {patients[0]['phone']}")
            
            # Select department
            dept_select = Select(self.driver.find_element(By.XPATH, "//select[option[contains(text(), 'Choose a department')]]"))
            dept_select.select_by_index(1)
            
            # Enable priority
            priority_checkbox = self.driver.find_element(By.XPATH, "//input[@type='checkbox']")
            priority_checkbox.click()
            
            self.driver.find_element(By.XPATH, "//button[contains(text(), 'Generate Token')]").click()
            
            # Verify priority token
            priority_token = self.wait.until(EC.presence_of_element_located((By.XPATH, "//h2[contains(@class, 'text-8xl')]")))
            
            self.take_screenshot("05_priority_token")
            self.log_result("Priority Token Generation", True)
            
            return priority_token.text
            
        except Exception as e:
            self.log_result("Priority Token Generation", False, e)
            return None
            
    def queue_management_testing(self):
        """Queue management testing"""
        print("📋 Queue Management Testing...")
        
        try:
            self.driver.get(f"{self.base_url}/queue")
            time.sleep(3)
            
            # Test calling tokens
            call_buttons = self.driver.find_elements(By.XPATH, "//button[contains(text(), 'Call')]")
            if call_buttons:
                call_buttons[0].click()
                time.sleep(2)
                self.log_result("Call Token", True)
            
            # Test skipping tokens
            skip_buttons = self.driver.find_elements(By.XPATH, "//button[contains(text(), 'Skip')]")
            if skip_buttons:
                skip_buttons[0].click()
                time.sleep(2)
                self.log_result("Skip Token", True)
                
            # Test completing tokens
            complete_buttons = self.driver.find_elements(By.XPATH, "//button[contains(text(), 'Complete')]")
            if complete_buttons:
                complete_buttons[0].click()
                time.sleep(2)
                self.log_result("Complete Token", True)
                
            self.take_screenshot("06_queue_management")
            
        except Exception as e:
            self.log_result("Queue Management", False, e)
            
    def appointment_booking_testing(self, patients):
        """Appointment booking testing"""
        print("📅 Appointment Booking Testing...")
        
        try:
            self.driver.get(f"{self.base_url}/appointments")
            
            # Select patient
            patient_select = Select(self.wait.until(EC.presence_of_element_located((By.XPATH, "//select[option[contains(text(), 'Choose a patient')]]"))))
            patient_select.select_by_visible_text(f"{patients[0]['name']} - {patients[0]['phone']}")
            
            # Select department
            dept_select = Select(self.driver.find_element(By.XPATH, "//select[option[contains(text(), 'Choose a department')]]"))
            dept_select.select_by_index(1)
            
            time.sleep(2)  # Wait for doctors to load
            
            # Select doctor
            doctor_select = Select(self.driver.find_element(By.XPATH, "//select[option[contains(text(), 'Choose a doctor')]]"))
            doctor_select.select_by_index(1)
            
            # Set appointment date
            tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
            date_input = self.driver.find_element(By.XPATH, "//input[@type='date']")
            date_input.send_keys(tomorrow)
            
            # Add reason
            reason_textarea = self.driver.find_element(By.XPATH, "//textarea[@placeholder='Describe your symptoms or reason for consultation']")
            reason_textarea.send_keys("Automated test appointment")
            
            # Book appointment
            self.driver.find_element(By.XPATH, "//button[contains(text(), 'Book Appointment')]").click()
            
            self.wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'successfully')]")))
            self.take_screenshot("07_appointment_booked")
            self.log_result("Appointment Booking", True)
            
        except Exception as e:
            self.log_result("Appointment Booking", False, e)
            
    def display_board_testing(self):
        """Display board testing"""
        print("📺 Display Board Testing...")
        
        try:
            self.driver.execute_script("window.open('');")
            self.driver.switch_to.window(self.driver.window_handles[1])
            self.driver.get(f"{self.base_url}/display")
            
            self.wait.until(EC.presence_of_element_located((By.XPATH, "//h1[contains(text(), 'Smart Health Queue System')]")))
            self.take_screenshot("08_display_board")
            
            self.driver.close()
            self.driver.switch_to.window(self.driver.window_handles[0])
            
            self.log_result("Display Board", True)
            
        except Exception as e:
            self.log_result("Display Board", False, e)
            
    def patient_login_testing(self, patients):
        """Patient login testing"""
        print("👤 Patient Login Testing...")
        
        try:
            self.driver.get(f"{self.base_url}/login")
            
            # Select Patient role
            self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Patient Login')]"))).click()
            
            # Enter phone number
            self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Phone Number']"))).send_keys(patients[0]['phone'])
            
            # Click login
            self.driver.find_element(By.XPATH, "//button[contains(text(), 'Login')]").click()
            
            # Verify patient dashboard
            self.wait.until(EC.presence_of_element_located((By.XPATH, "//h1[contains(text(), 'Patient Portal')]")))
            self.take_screenshot("09_patient_dashboard")
            
            self.log_result("Patient Login", True)
            
        except Exception as e:
            self.log_result("Patient Login", False, e)
            
    def generate_test_report(self):
        """Generate comprehensive test report"""
        report = {
            "test_execution_time": datetime.now().isoformat(),
            "total_tests": self.test_results["passed"] + self.test_results["failed"],
            "passed_tests": self.test_results["passed"],
            "failed_tests": self.test_results["failed"],
            "success_rate": f"{(self.test_results['passed'] / (self.test_results['passed'] + self.test_results['failed']) * 100):.1f}%",
            "errors": self.test_results["errors"],
            "browser": "Chrome",
            "application_url": self.base_url,
            "screenshots_directory": self.screenshots_dir
        }
        
        report_file = f"test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
            
        print(f"\n📊 Test Report Generated: {report_file}")
        print(f"✅ Passed: {report['passed_tests']}")
        print(f"❌ Failed: {report['failed_tests']}")
        print(f"📈 Success Rate: {report['success_rate']}")
        
        return report
        
    def run_advanced_tests(self):
        """Run all advanced tests with error handling"""
        print("🚀 Starting Advanced Smart Health Test Automation")
        print("=" * 60)
        
        try:
            self.driver.maximize_window()
            
            # 1. Complete workflow testing
            self.complete_workflow_testing()
            
            # 2. Multiple patient registration
            patients = self.multiple_patient_registration()
            
            # 3. Bulk token generation
            tokens = self.bulk_token_generation(patients)
            
            # 4. Priority token testing
            priority_token = self.priority_token_testing(patients)
            
            # 5. Queue management testing
            self.queue_management_testing()
            
            # 6. Appointment booking testing
            self.appointment_booking_testing(patients)
            
            # 7. Display board testing
            self.display_board_testing()
            
            # 8. Patient login testing
            self.patient_login_testing(patients)
            
            # 9. Generate test report
            report = self.generate_test_report()
            
            print("\n🎉 Advanced Test Automation Completed!")
            print("=" * 60)
            
        except Exception as e:
            print(f"❌ Critical Error: {str(e)}")
            self.take_screenshot("critical_error")
            
        finally:
            input("Press Enter to close browser...")
            self.driver.quit()

if __name__ == "__main__":
    test = AdvancedSmartHealthTest()
    test.run_advanced_tests()