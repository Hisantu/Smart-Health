from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import json
from datetime import datetime

class SmartHealthDatabaseTest:
    def __init__(self):
        options = Options()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1920,1080")
        
        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, 20)
        self.base_url = "https://smart-health-1-nmts.onrender.com"
        self.test_results = []
        
        # Use existing database data
        self.existing_data = {
            "staff_credentials": {"username": "receptionist", "password": "recep123"},
            "departments": ["Cardiology", "Orthopedics", "Pediatrics", "General Medicine"],
            "doctors": ["Dr. Sarah Johnson", "Dr. Michael Chen", "Dr. Emily Davis", "Dr. Robert Wilson"]
        }
        
    def log_test(self, test_name, status, details=""):
        result = {"test": test_name, "status": status, "details": details, "time": datetime.now().strftime("%H:%M:%S")}
        self.test_results.append(result)
        icon = "✅" if status == "PASS" else "❌" if status == "FAIL" else "ℹ️"
        print(f"{icon} {test_name}: {details}")
        
    def staff_login_with_existing_credentials(self):
        """Login using existing staff credentials from database"""
        print("🔐 Staff Login with Database Credentials...")
        
        try:
            self.driver.get(self.base_url)
            time.sleep(5)
            
            # Click Staff Login
            staff_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Staff') or contains(text(), 'staff')]")))
            staff_btn.click()
            time.sleep(3)
            
            # Enter existing credentials
            username_field = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='text' or @placeholder='Username' or @placeholder='Staff ID']")))
            password_field = self.driver.find_element(By.XPATH, "//input[@type='password']")
            
            username_field.clear()
            username_field.send_keys(self.existing_data["staff_credentials"]["username"])
            password_field.clear()
            password_field.send_keys(self.existing_data["staff_credentials"]["password"])
            
            # Click Login
            login_btn = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Login')]")
            login_btn.click()
            time.sleep(5)
            
            # Verify login success
            if "dashboard" in self.driver.current_url.lower() or self.driver.find_elements(By.XPATH, "//*[contains(text(), 'Dashboard') or contains(text(), 'Welcome')]"):
                self.log_test("Staff Login", "PASS", f"Logged in as {self.existing_data['staff_credentials']['username']}")
                return True
            else:
                self.log_test("Staff Login", "FAIL", "Login failed - no dashboard found")
                return False
                
        except Exception as e:
            self.log_test("Staff Login", "FAIL", str(e))
            return False
            
    def use_existing_patients_for_tokens(self):
        """Generate tokens using existing patients from database"""
        print("🎫 Using Existing Patients for Token Generation...")
        
        try:
            # Navigate to token generation
            token_links = self.driver.find_elements(By.XPATH, "//a[contains(@href, 'token') or contains(text(), 'Token') or contains(text(), 'Generate')]")
            if token_links:
                token_links[0].click()
                time.sleep(3)
                
                # Select existing patient from dropdown
                try:
                    patient_dropdown = Select(self.wait.until(EC.presence_of_element_located((By.XPATH, "//select[option[contains(text(), 'patient') or contains(text(), 'Patient')]]"))))
                    
                    # Use first available patient (skip "Choose patient" option)
                    if len(patient_dropdown.options) > 1:
                        patient_dropdown.select_by_index(1)
                        selected_patient = patient_dropdown.first_selected_option.text
                        self.log_test("Patient Selection", "PASS", f"Selected: {selected_patient}")
                    else:
                        self.log_test("Patient Selection", "FAIL", "No patients found in database")
                        return False
                        
                except Exception as e:
                    self.log_test("Patient Selection", "FAIL", f"Patient dropdown error: {str(e)}")
                    return False
                    
                # Select existing department
                try:
                    dept_dropdown = Select(self.driver.find_element(By.XPATH, "//select[option[contains(text(), 'department') or contains(text(), 'Department')]]"))
                    
                    # Try to select Cardiology first, then any available department
                    dept_selected = False
                    for dept in self.existing_data["departments"]:
                        try:
                            dept_dropdown.select_by_visible_text(dept)
                            self.log_test("Department Selection", "PASS", f"Selected: {dept}")
                            dept_selected = True
                            break
                        except:
                            continue
                            
                    if not dept_selected and len(dept_dropdown.options) > 1:
                        dept_dropdown.select_by_index(1)
                        selected_dept = dept_dropdown.first_selected_option.text
                        self.log_test("Department Selection", "PASS", f"Selected: {selected_dept}")
                        
                except Exception as e:
                    self.log_test("Department Selection", "FAIL", str(e))
                    
                # Generate token
                generate_btn = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Generate')]")
                generate_btn.click()
                time.sleep(5)
                
                # Verify token generation
                try:
                    token_display = self.driver.find_element(By.XPATH, "//*[contains(@class, 'token') or contains(text(), '-') or contains(@class, 'text-8xl')]")
                    token_number = token_display.text
                    self.log_test("Token Generation", "PASS", f"Generated token: {token_number}")
                    return token_number
                except:
                    # Check for success message
                    success_elements = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'success') or contains(text(), 'generated')]")
                    if success_elements:
                        self.log_test("Token Generation", "PASS", "Token generated successfully")
                        return "TOKEN-GENERATED"
                    else:
                        self.log_test("Token Generation", "FAIL", "No token display found")
                        return None
                        
        except Exception as e:
            self.log_test("Token Generation", "FAIL", str(e))
            return None
            
    def use_existing_data_for_appointments(self):
        """Book appointments using existing patients and doctors"""
        print("📅 Booking Appointments with Existing Data...")
        
        try:
            # Navigate to appointments
            appt_links = self.driver.find_elements(By.XPATH, "//a[contains(@href, 'appointment') or contains(text(), 'Appointment')]")
            if appt_links:
                appt_links[0].click()
                time.sleep(3)
                
                # Select existing patient
                try:
                    patient_dropdown = Select(self.wait.until(EC.presence_of_element_located((By.XPATH, "//select[option[contains(text(), 'patient')]]"))))
                    if len(patient_dropdown.options) > 1:
                        patient_dropdown.select_by_index(1)
                        self.log_test("Appointment Patient Selection", "PASS", "Selected existing patient")
                except Exception as e:
                    self.log_test("Appointment Patient Selection", "FAIL", str(e))
                    
                # Select existing department
                try:
                    dept_dropdown = Select(self.driver.find_element(By.XPATH, "//select[option[contains(text(), 'department')]]"))
                    dept_dropdown.select_by_visible_text("Cardiology")
                    time.sleep(2)
                    self.log_test("Appointment Department Selection", "PASS", "Selected Cardiology")
                except:
                    try:
                        if len(dept_dropdown.options) > 1:
                            dept_dropdown.select_by_index(1)
                            self.log_test("Appointment Department Selection", "PASS", "Selected first available department")
                    except Exception as e:
                        self.log_test("Appointment Department Selection", "FAIL", str(e))
                        
                # Select existing doctor
                try:
                    doctor_dropdown = Select(self.driver.find_element(By.XPATH, "//select[option[contains(text(), 'doctor')]]"))
                    if len(doctor_dropdown.options) > 1:
                        doctor_dropdown.select_by_index(1)
                        self.log_test("Doctor Selection", "PASS", "Selected existing doctor")
                except Exception as e:
                    self.log_test("Doctor Selection", "FAIL", str(e))
                    
                # Set appointment date
                try:
                    date_input = self.driver.find_element(By.XPATH, "//input[@type='date']")
                    from datetime import datetime, timedelta
                    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
                    date_input.send_keys(tomorrow)
                    self.log_test("Appointment Date", "PASS", f"Set date to {tomorrow}")
                except Exception as e:
                    self.log_test("Appointment Date", "FAIL", str(e))
                    
                # Select time slot
                try:
                    time_dropdown = Select(self.driver.find_element(By.XPATH, "//select[option[contains(text(), 'AM') or contains(text(), 'PM')]]"))
                    time_dropdown.select_by_index(1)
                    self.log_test("Time Slot Selection", "PASS", "Selected time slot")
                except Exception as e:
                    self.log_test("Time Slot Selection", "FAIL", str(e))
                    
                # Add reason
                try:
                    reason_field = self.driver.find_element(By.XPATH, "//textarea")
                    reason_field.send_keys("Automated test using existing database data")
                    self.log_test("Appointment Reason", "PASS", "Added reason")
                except Exception as e:
                    self.log_test("Appointment Reason", "FAIL", str(e))
                    
                # Book appointment
                book_btn = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Book')]")
                book_btn.click()
                time.sleep(5)
                
                # Verify booking
                success_elements = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'success') or contains(text(), 'booked')]")
                if success_elements:
                    self.log_test("Appointment Booking", "PASS", "Appointment booked successfully")
                else:
                    self.log_test("Appointment Booking", "FAIL", "No success confirmation found")
                    
        except Exception as e:
            self.log_test("Appointment Booking", "FAIL", str(e))
            
    def test_queue_with_existing_tokens(self):
        """Test queue management with existing tokens"""
        print("📋 Testing Queue Management with Existing Tokens...")
        
        try:
            # Navigate to queue management
            queue_links = self.driver.find_elements(By.XPATH, "//a[contains(@href, 'queue') or contains(text(), 'Queue')]")
            if queue_links:
                queue_links[0].click()
                time.sleep(5)
                
                # Select department to view tokens
                try:
                    dept_dropdown = Select(self.driver.find_element(By.XPATH, "//select[option[contains(text(), 'department')]]"))
                    dept_dropdown.select_by_visible_text("Cardiology")
                    time.sleep(3)
                    self.log_test("Queue Department Selection", "PASS", "Selected Cardiology for queue")
                except:
                    try:
                        if len(dept_dropdown.options) > 1:
                            dept_dropdown.select_by_index(1)
                            time.sleep(3)
                            self.log_test("Queue Department Selection", "PASS", "Selected first available department")
                    except Exception as e:
                        self.log_test("Queue Department Selection", "FAIL", str(e))
                        
                # Check for existing tokens in queue
                token_elements = self.driver.find_elements(By.XPATH, "//*[contains(text(), '-') and (contains(text(), 'CAR') or contains(text(), 'ORT') or contains(text(), 'PED') or contains(text(), 'GEN'))]")
                
                if token_elements:
                    self.log_test("Queue Token Detection", "PASS", f"Found {len(token_elements)} tokens in queue")
                    
                    # Test queue operations on existing tokens
                    call_buttons = self.driver.find_elements(By.XPATH, "//button[contains(text(), 'Call')]")
                    if call_buttons:
                        call_buttons[0].click()
                        time.sleep(2)
                        self.log_test("Queue Call Operation", "PASS", "Called first token")
                        
                    skip_buttons = self.driver.find_elements(By.XPATH, "//button[contains(text(), 'Skip')]")
                    if skip_buttons:
                        skip_buttons[0].click()
                        time.sleep(2)
                        self.log_test("Queue Skip Operation", "PASS", "Skipped token")
                        
                else:
                    self.log_test("Queue Token Detection", "INFO", "No tokens found in current queue")
                    
        except Exception as e:
            self.log_test("Queue Management", "FAIL", str(e))
            
    def test_patient_login_with_existing_data(self):
        """Test patient login using existing patient data"""
        print("👤 Testing Patient Login with Existing Data...")
        
        try:
            # Logout and go to patient login
            self.driver.get(self.base_url)
            time.sleep(3)
            
            # Click Patient Login
            patient_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Patient')]")))
            patient_btn.click()
            time.sleep(2)
            
            # Try common phone numbers that might exist in database
            test_phones = ["1234567890", "9876543210", "5555555555", "1111111111"]
            
            for phone in test_phones:
                try:
                    phone_field = self.driver.find_element(By.XPATH, "//input[@type='tel' or contains(@placeholder, 'Phone')]")
                    phone_field.clear()
                    phone_field.send_keys(phone)
                    
                    login_btn = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Login')]")
                    login_btn.click()
                    time.sleep(3)
                    
                    # Check if login was successful
                    if "dashboard" in self.driver.current_url.lower() or self.driver.find_elements(By.XPATH, "//*[contains(text(), 'Patient') and contains(text(), 'Portal')]"):
                        self.log_test("Patient Login", "PASS", f"Logged in with phone: {phone}")
                        return True
                    else:
                        # Go back to try next phone
                        self.driver.get(self.base_url)
                        time.sleep(2)
                        patient_btn = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Patient')]")
                        patient_btn.click()
                        time.sleep(2)
                        
                except Exception as e:
                    continue
                    
            self.log_test("Patient Login", "FAIL", "No existing patient phone numbers worked")
            return False
            
        except Exception as e:
            self.log_test("Patient Login", "FAIL", str(e))
            return False
            
    def generate_final_report(self):
        """Generate test report"""
        passed = len([t for t in self.test_results if t["status"] == "PASS"])
        failed = len([t for t in self.test_results if t["status"] == "FAIL"])
        total = len(self.test_results)
        
        report = {
            "test_execution_time": datetime.now().isoformat(),
            "website_url": self.base_url,
            "total_tests": total,
            "passed_tests": passed,
            "failed_tests": failed,
            "success_rate": f"{(passed/total*100):.1f}%" if total > 0 else "0%",
            "test_results": self.test_results
        }
        
        with open(f"database_test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json", 'w') as f:
            json.dump(report, f, indent=2)
            
        print(f"\n📊 Database Test Report:")
        print(f"✅ Passed: {passed}")
        print(f"❌ Failed: {failed}")
        print(f"📈 Success Rate: {report['success_rate']}")
        
    def run_database_tests(self):
        """Run tests using existing database data"""
        print("🚀 SMART HEALTH TESTING WITH EXISTING DATABASE DATA")
        print("=" * 60)
        
        try:
            self.driver.maximize_window()
            
            # 1. Staff Login with existing credentials
            if not self.staff_login_with_existing_credentials():
                print("❌ Cannot proceed without staff login")
                return
                
            # 2. Use existing patients for token generation
            self.use_existing_patients_for_tokens()
            
            # 3. Use existing data for appointments
            self.use_existing_data_for_appointments()
            
            # 4. Test queue with existing tokens
            self.test_queue_with_existing_tokens()
            
            # 5. Test patient login with existing data
            self.test_patient_login_with_existing_data()
            
            # 6. Generate final report
            self.generate_final_report()
            
            print("\n🎉 DATABASE TESTING COMPLETED!")
            
        except Exception as e:
            print(f"❌ Critical Error: {str(e)}")
            
        finally:
            input("Press Enter to close browser...")
            self.driver.quit()

if __name__ == "__main__":
    test = SmartHealthDatabaseTest()
    test.run_database_tests()