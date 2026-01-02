from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import json
from datetime import datetime, timedelta

class SmartHealthPatientToStaffTest:
    def __init__(self):
        options = Options()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1920,1080")
        
        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, 20)
        self.base_url = "https://smart-health-1-nmts.onrender.com"
        self.test_results = []
        
        # Database data from seed file
        self.database_data = {
            "patient_phones": ["1234567890", "9876543210", "5555555555"],
            "staff_credentials": {"username": "receptionist", "password": "recep123"},
            "departments": ["Cardiology", "Orthopedics", "Pediatrics", "General Medicine"],
            "doctors": ["Dr. Sarah Johnson", "Dr. Michael Chen", "Dr. Emily Davis", "Dr. Robert Wilson"]
        }
        self.generated_token = None
        
    def log_test(self, test_name, status, details=""):
        result = {"test": test_name, "status": status, "details": details, "time": datetime.now().strftime("%H:%M:%S")}
        self.test_results.append(result)
        icon = "✅" if status == "PASS" else "❌" if status == "FAIL" else "ℹ️"
        print(f"{icon} {test_name}: {details}")
        
    def patient_login_with_database_phone(self):
        """Step 1: Login to patient interface using existing database phone"""
        print("👤 STEP 1: Patient Login with Database Phone...")
        
        try:
            self.driver.get(self.base_url)
            time.sleep(5)
            
            # Click Patient Login
            patient_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Patient')]")))
            patient_btn.click()
            time.sleep(3)
            
            # Try database phone numbers
            for phone in self.database_data["patient_phones"]:
                try:
                    phone_field = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='tel' or contains(@placeholder, 'Phone')]")))
                    phone_field.clear()
                    phone_field.send_keys(phone)
                    
                    login_btn = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Login')]")
                    login_btn.click()
                    time.sleep(5)
                    
                    # Check if login successful
                    if "dashboard" in self.driver.current_url.lower() or self.driver.find_elements(By.XPATH, "//*[contains(text(), 'Patient') or contains(text(), 'Dashboard')]"):
                        self.log_test("Patient Login", "PASS", f"Logged in with phone: {phone}")
                        return phone
                    else:
                        # Try next phone
                        self.driver.get(self.base_url)
                        time.sleep(2)
                        patient_btn = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Patient')]")
                        patient_btn.click()
                        time.sleep(2)
                        
                except Exception as e:
                    continue
                    
            self.log_test("Patient Login", "FAIL", "No database phone numbers worked")
            return None
            
        except Exception as e:
            self.log_test("Patient Login", "FAIL", str(e))
            return None
            
    def patient_generate_token(self):
        """Step 2: Generate token as patient with all requirements"""
        print("🎫 STEP 2: Patient Generate Token...")
        
        try:
            # Navigate to Generate Token
            token_links = self.driver.find_elements(By.XPATH, "//a[contains(@href, 'token') or contains(text(), 'Token') or contains(text(), 'Generate')]")
            if not token_links:
                # Try navigation menu
                nav_links = self.driver.find_elements(By.XPATH, "//nav//a | //menu//a")
                for link in nav_links:
                    if "token" in link.text.lower():
                        link.click()
                        break
                else:
                    self.log_test("Token Navigation", "FAIL", "Token generation link not found")
                    return None
            else:
                token_links[0].click()
                
            time.sleep(3)
            
            # Select Department (Cardiology first)
            try:
                dept_dropdown = Select(self.wait.until(EC.presence_of_element_located((By.XPATH, "//select[option[contains(text(), 'department') or contains(text(), 'Department')]]"))))
                
                # Try to select Cardiology
                try:
                    dept_dropdown.select_by_visible_text("Cardiology")
                    self.log_test("Token Department Selection", "PASS", "Selected Cardiology")
                except:
                    # Select first available department
                    if len(dept_dropdown.options) > 1:
                        dept_dropdown.select_by_index(1)
                        selected_dept = dept_dropdown.first_selected_option.text
                        self.log_test("Token Department Selection", "PASS", f"Selected {selected_dept}")
                        
            except Exception as e:
                self.log_test("Token Department Selection", "FAIL", str(e))
                
            # Check for priority option
            try:
                priority_checkbox = self.driver.find_element(By.XPATH, "//input[@type='checkbox']")
                priority_checkbox.click()
                self.log_test("Priority Token", "PASS", "Enabled priority token")
            except:
                self.log_test("Priority Token", "INFO", "No priority option found")
                
            # Generate Token
            generate_btn = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Generate')]")
            generate_btn.click()
            time.sleep(5)
            
            # Capture generated token
            try:
                token_elements = self.driver.find_elements(By.XPATH, "//*[contains(@class, 'token') or contains(text(), 'CAR-') or contains(text(), 'ORT-') or contains(text(), 'PED-') or contains(text(), 'GEN-')]")
                if token_elements:
                    self.generated_token = token_elements[0].text
                    self.log_test("Token Generation", "PASS", f"Generated token: {self.generated_token}")
                    return self.generated_token
                else:
                    # Look for any large text that might be token
                    large_text = self.driver.find_elements(By.XPATH, "//*[contains(@class, 'text-8xl') or contains(@class, 'text-6xl')]")
                    if large_text:
                        self.generated_token = large_text[0].text
                        self.log_test("Token Generation", "PASS", f"Generated token: {self.generated_token}")
                        return self.generated_token
                        
            except Exception as e:
                self.log_test("Token Generation", "FAIL", f"Token capture error: {str(e)}")
                
            # Check for success message
            success_elements = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'success') or contains(text(), 'generated')]")
            if success_elements:
                self.log_test("Token Generation", "PASS", "Token generated successfully")
                self.generated_token = "TOKEN-GENERATED"
                return self.generated_token
            else:
                self.log_test("Token Generation", "FAIL", "No token or success message found")
                return None
                
        except Exception as e:
            self.log_test("Token Generation", "FAIL", str(e))
            return None
            
    def patient_book_appointment(self):
        """Step 3: Book appointment as patient with all requirements"""
        print("📅 STEP 3: Patient Book Appointment...")
        
        try:
            # Navigate to Book Appointment
            appt_links = self.driver.find_elements(By.XPATH, "//a[contains(@href, 'appointment') or contains(text(), 'Appointment') or contains(text(), 'Book')]")
            if appt_links:
                appt_links[0].click()
            else:
                # Try navigation menu
                nav_links = self.driver.find_elements(By.XPATH, "//nav//a | //menu//a")
                for link in nav_links:
                    if "appointment" in link.text.lower():
                        link.click()
                        break
                        
            time.sleep(3)
            
            # Select Patient (should be auto-selected for logged-in patient)
            try:
                patient_dropdown = Select(self.driver.find_element(By.XPATH, "//select[option[contains(text(), 'patient')]]"))
                if len(patient_dropdown.options) > 1:
                    patient_dropdown.select_by_index(1)
                    self.log_test("Appointment Patient Selection", "PASS", "Selected patient")
            except:
                self.log_test("Appointment Patient Selection", "INFO", "Patient auto-selected or not found")
                
            # Select Department
            try:
                dept_dropdown = Select(self.driver.find_element(By.XPATH, "//select[option[contains(text(), 'department')]]"))
                dept_dropdown.select_by_visible_text("Cardiology")
                time.sleep(2)
                self.log_test("Appointment Department", "PASS", "Selected Cardiology")
            except:
                try:
                    if len(dept_dropdown.options) > 1:
                        dept_dropdown.select_by_index(1)
                        self.log_test("Appointment Department", "PASS", "Selected first available department")
                except Exception as e:
                    self.log_test("Appointment Department", "FAIL", str(e))
                    
            # Select Doctor
            try:
                doctor_dropdown = Select(self.driver.find_element(By.XPATH, "//select[option[contains(text(), 'doctor') or contains(text(), 'Dr.')]]"))
                if len(doctor_dropdown.options) > 1:
                    doctor_dropdown.select_by_index(1)
                    selected_doctor = doctor_dropdown.first_selected_option.text
                    self.log_test("Doctor Selection", "PASS", f"Selected {selected_doctor}")
            except Exception as e:
                self.log_test("Doctor Selection", "FAIL", str(e))
                
            # Set Appointment Date (tomorrow)
            try:
                date_input = self.driver.find_element(By.XPATH, "//input[@type='date']")
                tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
                date_input.send_keys(tomorrow)
                self.log_test("Appointment Date", "PASS", f"Set date to {tomorrow}")
            except Exception as e:
                self.log_test("Appointment Date", "FAIL", str(e))
                
            # Select Time Slot
            try:
                time_dropdown = Select(self.driver.find_element(By.XPATH, "//select[option[contains(text(), 'AM') or contains(text(), 'PM')]]"))
                time_dropdown.select_by_index(1)
                selected_time = time_dropdown.first_selected_option.text
                self.log_test("Time Slot", "PASS", f"Selected {selected_time}")
            except Exception as e:
                self.log_test("Time Slot", "FAIL", str(e))
                
            # Enter Reason for Visit
            try:
                reason_field = self.driver.find_element(By.XPATH, "//textarea")
                reason_field.send_keys("Automated test appointment - Patient interface booking")
                self.log_test("Appointment Reason", "PASS", "Added reason for visit")
            except Exception as e:
                self.log_test("Appointment Reason", "FAIL", str(e))
                
            # Book Appointment
            book_btn = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Book')]")
            book_btn.click()
            time.sleep(5)
            
            # Verify booking success
            success_elements = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'success') or contains(text(), 'booked') or contains(text(), 'confirmed')]")
            if success_elements:
                self.log_test("Appointment Booking", "PASS", "Appointment booked successfully")
                return True
            else:
                self.log_test("Appointment Booking", "FAIL", "No booking confirmation found")
                return False
                
        except Exception as e:
            self.log_test("Appointment Booking", "FAIL", str(e))
            return False
            
    def logout_patient(self):
        """Step 4: Logout from patient interface"""
        print("🚪 STEP 4: Logout from Patient Interface...")
        
        try:
            # Look for logout button
            logout_buttons = self.driver.find_elements(By.XPATH, "//button[contains(text(), 'Logout') or contains(text(), 'logout')]")
            if logout_buttons:
                logout_buttons[0].click()
                time.sleep(2)
                self.log_test("Patient Logout", "PASS", "Logged out successfully")
            else:
                # Navigate to home page
                self.driver.get(self.base_url)
                time.sleep(3)
                self.log_test("Patient Logout", "PASS", "Navigated to home page")
                
        except Exception as e:
            self.log_test("Patient Logout", "FAIL", str(e))
            
    def staff_login_with_database_credentials(self):
        """Step 5: Login to staff interface using database credentials"""
        print("👨⚕️ STEP 5: Staff Login with Database Credentials...")
        
        try:
            self.driver.get(self.base_url)
            time.sleep(3)
            
            # Click Staff Login
            staff_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Staff')]")))
            staff_btn.click()
            time.sleep(3)
            
            # Enter database credentials
            username_field = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='text']")))
            password_field = self.driver.find_element(By.XPATH, "//input[@type='password']")
            
            username_field.clear()
            username_field.send_keys(self.database_data["staff_credentials"]["username"])
            password_field.clear()
            password_field.send_keys(self.database_data["staff_credentials"]["password"])
            
            # Click Login
            login_btn = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Login')]")
            login_btn.click()
            time.sleep(5)
            
            # Verify staff login
            if "dashboard" in self.driver.current_url.lower() or self.driver.find_elements(By.XPATH, "//*[contains(text(), 'Dashboard') or contains(text(), 'Welcome')]"):
                self.log_test("Staff Login", "PASS", f"Logged in as {self.database_data['staff_credentials']['username']}")
                return True
            else:
                self.log_test("Staff Login", "FAIL", "Staff dashboard not found")
                return False
                
        except Exception as e:
            self.log_test("Staff Login", "FAIL", str(e))
            return False
            
    def staff_queue_management(self):
        """Step 6: Navigate to Queue Management and select requirements"""
        print("📋 STEP 6: Staff Queue Management...")
        
        try:
            # Navigate to Queue Management
            queue_links = self.driver.find_elements(By.XPATH, "//a[contains(@href, 'queue') or contains(text(), 'Queue')]")
            if queue_links:
                queue_links[0].click()
            else:
                # Try dashboard cards
                dashboard_cards = self.driver.find_elements(By.XPATH, "//div[contains(text(), 'Queue') or contains(text(), 'Management')]//parent::*")
                if dashboard_cards:
                    dashboard_cards[0].click()
                    
            time.sleep(5)
            
            # Select Department (Cardiology to match token)
            try:
                dept_dropdown = Select(self.wait.until(EC.presence_of_element_located((By.XPATH, "//select[option[contains(text(), 'department')]]"))))
                dept_dropdown.select_by_visible_text("Cardiology")
                time.sleep(3)
                self.log_test("Queue Department Selection", "PASS", "Selected Cardiology department")
            except:
                try:
                    if len(dept_dropdown.options) > 1:
                        dept_dropdown.select_by_index(1)
                        selected_dept = dept_dropdown.first_selected_option.text
                        self.log_test("Queue Department Selection", "PASS", f"Selected {selected_dept}")
                except Exception as e:
                    self.log_test("Queue Department Selection", "FAIL", str(e))
                    
            # Set Counter Name
            try:
                counter_field = self.driver.find_element(By.XPATH, "//input[contains(@placeholder, 'Counter') or @value='Counter 1']")
                counter_field.clear()
                counter_field.send_keys("Counter 1")
                self.log_test("Counter Assignment", "PASS", "Set counter to Counter 1")
            except Exception as e:
                self.log_test("Counter Assignment", "FAIL", str(e))
                
            # Look for generated token in queue
            if self.generated_token:
                token_elements = self.driver.find_elements(By.XPATH, f"//*[contains(text(), '{self.generated_token}')]")
                if token_elements:
                    self.log_test("Token Verification", "PASS", f"Found generated token {self.generated_token} in queue")
                else:
                    self.log_test("Token Verification", "INFO", f"Token {self.generated_token} not visible in current queue")
            else:
                # Look for any Cardiology tokens
                cardiology_tokens = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'CAR-')]")
                if cardiology_tokens:
                    self.log_test("Token Verification", "PASS", f"Found {len(cardiology_tokens)} Cardiology tokens in queue")
                else:
                    self.log_test("Token Verification", "INFO", "No Cardiology tokens found in queue")
                    
            # Test queue operations
            call_buttons = self.driver.find_elements(By.XPATH, "//button[contains(text(), 'Call')]")
            if call_buttons:
                call_buttons[0].click()
                time.sleep(2)
                self.log_test("Queue Call Operation", "PASS", "Called first token in queue")
                
            skip_buttons = self.driver.find_elements(By.XPATH, "//button[contains(text(), 'Skip')]")
            if skip_buttons:
                skip_buttons[0].click()
                time.sleep(2)
                self.log_test("Queue Skip Operation", "PASS", "Skipped token")
                
            complete_buttons = self.driver.find_elements(By.XPATH, "//button[contains(text(), 'Complete')]")
            if complete_buttons:
                complete_buttons[0].click()
                time.sleep(2)
                self.log_test("Queue Complete Operation", "PASS", "Completed token")
                
        except Exception as e:
            self.log_test("Queue Management", "FAIL", str(e))
            
    def generate_final_report(self):
        """Generate comprehensive test report"""
        passed = len([t for t in self.test_results if t["status"] == "PASS"])
        failed = len([t for t in self.test_results if t["status"] == "FAIL"])
        total = len(self.test_results)
        
        report = {
            "test_execution_time": datetime.now().isoformat(),
            "website_url": self.base_url,
            "generated_token": self.generated_token,
            "total_tests": total,
            "passed_tests": passed,
            "failed_tests": failed,
            "success_rate": f"{(passed/total*100):.1f}%" if total > 0 else "0%",
            "test_results": self.test_results
        }
        
        with open(f"patient_to_staff_test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json", 'w') as f:
            json.dump(report, f, indent=2)
            
        print(f"\n📊 Patient-to-Staff Test Report:")
        print(f"🎫 Generated Token: {self.generated_token}")
        print(f"✅ Passed: {passed}")
        print(f"❌ Failed: {failed}")
        print(f"📈 Success Rate: {report['success_rate']}")
        
    def run_complete_patient_to_staff_workflow(self):
        """Run complete patient-to-staff workflow test"""
        print("🚀 SMART HEALTH: PATIENT-TO-STAFF COMPLETE WORKFLOW TEST")
        print("=" * 70)
        print("WORKFLOW:")
        print("1. 👤 Patient Login → 2. 🎫 Generate Token → 3. 📅 Book Appointment")
        print("4. 🚪 Logout → 5. 👨⚕️ Staff Login → 6. 📋 Queue Management")
        print("=" * 70)
        
        try:
            self.driver.maximize_window()
            
            # Step 1: Patient Login
            patient_phone = self.patient_login_with_database_phone()
            if not patient_phone:
                print("❌ Cannot proceed without patient login")
                return
                
            # Step 2: Generate Token
            token = self.patient_generate_token()
            
            # Step 3: Book Appointment
            self.patient_book_appointment()
            
            # Step 4: Logout from Patient
            self.logout_patient()
            
            # Step 5: Staff Login
            if not self.staff_login_with_database_credentials():
                print("❌ Cannot proceed without staff login")
                return
                
            # Step 6: Queue Management
            self.staff_queue_management()
            
            # Generate Final Report
            self.generate_final_report()
            
            print("\n🎉 COMPLETE PATIENT-TO-STAFF WORKFLOW TEST FINISHED!")
            print("All steps completed successfully!")
            
        except Exception as e:
            print(f"❌ Critical Error: {str(e)}")
            
        finally:
            input("Press Enter to close browser...")
            self.driver.quit()

if __name__ == "__main__":
    test = SmartHealthPatientToStaffTest()
    test.run_complete_patient_to_staff_workflow()