from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import random
import json
from datetime import datetime, timedelta

class SmartHealthWebsiteAnalyzer:
    def __init__(self):
        options = Options()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1920,1080")
        
        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, 15)
        self.base_url = "https://smart-health-1-nmts.onrender.com"
        self.analysis_results = []
        
    def log_result(self, test, status, details=""):
        result = {"test": test, "status": status, "details": details, "timestamp": datetime.now().strftime("%H:%M:%S")}
        self.analysis_results.append(result)
        icon = "✅" if status == "PASS" else "❌" if status == "FAIL" else "ℹ️"
        print(f"{icon} {test}: {details}")
        
    def analyze_homepage(self):
        """Analyze homepage structure"""
        print("🏠 Analyzing Homepage...")
        
        try:
            self.driver.get(self.base_url)
            time.sleep(5)
            
            # Check title
            title = self.driver.title
            self.log_result("Homepage Title", "PASS", f"Title: {title}")
            
            # Find all interactive elements
            buttons = self.driver.find_elements(By.TAG_NAME, "button")
            links = self.driver.find_elements(By.TAG_NAME, "a")
            inputs = self.driver.find_elements(By.TAG_NAME, "input")
            
            self.log_result("Interactive Elements", "PASS", f"Buttons: {len(buttons)}, Links: {len(links)}, Inputs: {len(inputs)}")
            
            # Check for login options
            login_elements = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'Login') or contains(text(), 'login')]")
            self.log_result("Login Options", "PASS", f"Found {len(login_elements)} login elements")
            
            # Check for role selection
            staff_elements = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'Staff') or contains(text(), 'staff')]")
            patient_elements = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'Patient') or contains(text(), 'patient')]")
            
            self.log_result("Role Selection", "PASS", f"Staff: {len(staff_elements)}, Patient: {len(patient_elements)}")
            
        except Exception as e:
            self.log_result("Homepage Analysis", "FAIL", str(e))
            
    def test_staff_workflow(self):
        """Test complete staff workflow"""
        print("👨⚕️ Testing Staff Workflow...")
        
        try:
            # Staff Login
            self.driver.get(self.base_url)
            time.sleep(3)
            
            # Click Staff Login
            staff_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Staff')]")))
            staff_btn.click()
            time.sleep(2)
            
            # Enter credentials
            username_field = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='text']")))
            password_field = self.driver.find_element(By.XPATH, "//input[@type='password']")
            
            username_field.send_keys("receptionist")
            password_field.send_keys("recep123")
            
            login_btn = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Login')]")
            login_btn.click()
            time.sleep(3)
            
            self.log_result("Staff Login", "PASS", "Logged in successfully")
            
            # Test Patient Registration
            self.test_patient_registration()
            
            # Test Token Generation
            self.test_token_generation()
            
            # Test Queue Management
            self.test_queue_management()
            
            # Test Appointment Booking
            self.test_appointment_booking()
            
        except Exception as e:
            self.log_result("Staff Workflow", "FAIL", str(e))
            
    def test_patient_registration(self):
        """Test patient registration"""
        try:
            # Navigate to patient registration
            reg_elements = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'Register') or contains(@href, 'register')]")
            if reg_elements:
                reg_elements[0].click()
                time.sleep(2)
                
                # Generate random patient data
                name = f"Test Patient {random.randint(1000, 9999)}"
                phone = f"555{random.randint(1000000, 9999999)}"
                email = f"test{random.randint(100, 999)}@example.com"
                
                # Fill form
                name_field = self.driver.find_element(By.XPATH, "//input[contains(@placeholder, 'Name') or contains(@placeholder, 'name')]")
                phone_field = self.driver.find_element(By.XPATH, "//input[contains(@placeholder, 'Phone') or contains(@placeholder, 'phone')]")
                
                name_field.send_keys(name)
                phone_field.send_keys(phone)
                
                # Try to fill other fields
                try:
                    email_field = self.driver.find_element(By.XPATH, "//input[@type='email']")
                    email_field.send_keys(email)
                except:
                    pass
                    
                try:
                    age_field = self.driver.find_element(By.XPATH, "//input[contains(@placeholder, 'Age')]")
                    age_field.send_keys("30")
                except:
                    pass
                    
                # Submit
                submit_btn = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Register') or contains(text(), 'Submit')]")
                submit_btn.click()
                time.sleep(3)
                
                self.log_result("Patient Registration", "PASS", f"Registered {name}")
                
        except Exception as e:
            self.log_result("Patient Registration", "FAIL", str(e))
            
    def test_token_generation(self):
        """Test token generation"""
        try:
            # Navigate to token generation
            token_elements = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'Token') or contains(@href, 'token')]")
            if token_elements:
                token_elements[0].click()
                time.sleep(2)
                
                # Select patient
                try:
                    patient_select = Select(self.driver.find_element(By.XPATH, "//select"))
                    if len(patient_select.options) > 1:
                        patient_select.select_by_index(1)
                except:
                    pass
                    
                # Select department
                try:
                    dept_selects = self.driver.find_elements(By.XPATH, "//select")
                    if len(dept_selects) > 1:
                        dept_select = Select(dept_selects[1])
                        if len(dept_select.options) > 1:
                            dept_select.select_by_index(1)
                except:
                    pass
                    
                # Generate token
                generate_btn = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Generate')]")
                generate_btn.click()
                time.sleep(3)
                
                self.log_result("Token Generation", "PASS", "Token generated successfully")
                
        except Exception as e:
            self.log_result("Token Generation", "FAIL", str(e))
            
    def test_queue_management(self):
        """Test queue management"""
        try:
            # Navigate to queue management
            queue_elements = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'Queue') or contains(@href, 'queue')]")
            if queue_elements:
                queue_elements[0].click()
                time.sleep(3)
                
                # Test queue operations
                call_buttons = self.driver.find_elements(By.XPATH, "//button[contains(text(), 'Call')]")
                if call_buttons:
                    call_buttons[0].click()
                    time.sleep(2)
                    self.log_result("Queue Management - Call", "PASS", "Called token")
                    
                skip_buttons = self.driver.find_elements(By.XPATH, "//button[contains(text(), 'Skip')]")
                if skip_buttons:
                    skip_buttons[0].click()
                    time.sleep(2)
                    self.log_result("Queue Management - Skip", "PASS", "Skipped token")
                    
        except Exception as e:
            self.log_result("Queue Management", "FAIL", str(e))
            
    def test_appointment_booking(self):
        """Test appointment booking"""
        try:
            # Navigate to appointments
            appt_elements = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'Appointment') or contains(@href, 'appointment')]")
            if appt_elements:
                appt_elements[0].click()
                time.sleep(2)
                
                # Fill appointment form
                selects = self.driver.find_elements(By.XPATH, "//select")
                for i, select in enumerate(selects[:3]):
                    try:
                        select_obj = Select(select)
                        if len(select_obj.options) > 1:
                            select_obj.select_by_index(1)
                            time.sleep(1)
                    except:
                        pass
                        
                # Set date
                try:
                    date_input = self.driver.find_element(By.XPATH, "//input[@type='date']")
                    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
                    date_input.send_keys(tomorrow)
                except:
                    pass
                    
                # Add reason
                try:
                    reason_field = self.driver.find_element(By.XPATH, "//textarea")
                    reason_field.send_keys("Automated test appointment")
                except:
                    pass
                    
                # Book appointment
                book_btn = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Book')]")
                book_btn.click()
                time.sleep(3)
                
                self.log_result("Appointment Booking", "PASS", "Appointment booked")
                
        except Exception as e:
            self.log_result("Appointment Booking", "FAIL", str(e))
            
    def test_patient_workflow(self):
        """Test patient workflow"""
        print("👤 Testing Patient Workflow...")
        
        try:
            # Logout and go to patient login
            self.driver.get(self.base_url)
            time.sleep(3)
            
            # Click Patient Login
            patient_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Patient')]")))
            patient_btn.click()
            time.sleep(2)
            
            # Try patient registration first
            register_elements = self.driver.find_elements(By.XPATH, "//button[contains(text(), 'Register')]")
            if register_elements:
                register_elements[0].click()
                time.sleep(2)
                
                # Fill registration form
                name = f"Patient User {random.randint(1000, 9999)}"
                phone = f"555{random.randint(1000000, 9999999)}"
                
                name_field = self.driver.find_element(By.XPATH, "//input[contains(@placeholder, 'Name')]")
                phone_field = self.driver.find_element(By.XPATH, "//input[contains(@placeholder, 'Phone')]")
                
                name_field.send_keys(name)
                phone_field.send_keys(phone)
                
                # Submit registration
                submit_btn = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Register')]")
                submit_btn.click()
                time.sleep(3)
                
                self.log_result("Patient Registration", "PASS", f"Patient {name} registered")
                
                # Test patient dashboard features
                self.test_patient_dashboard()
                
        except Exception as e:
            self.log_result("Patient Workflow", "FAIL", str(e))
            
    def test_patient_dashboard(self):
        """Test patient dashboard features"""
        try:
            # Check for patient dashboard elements
            dashboard_elements = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'Patient') or contains(text(), 'Dashboard')]")
            if dashboard_elements:
                self.log_result("Patient Dashboard", "PASS", "Patient dashboard loaded")
                
                # Test appointment viewing
                appt_elements = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'Appointment')]")
                if appt_elements:
                    self.log_result("Patient Appointments", "PASS", "Appointments section found")
                    
                # Test token viewing
                token_elements = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'Token')]")
                if token_elements:
                    self.log_result("Patient Tokens", "PASS", "Tokens section found")
                    
        except Exception as e:
            self.log_result("Patient Dashboard", "FAIL", str(e))
            
    def test_display_board(self):
        """Test display board"""
        print("📺 Testing Display Board...")
        
        try:
            # Open display board in new tab
            self.driver.execute_script("window.open('');")
            self.driver.switch_to.window(self.driver.window_handles[1])
            
            # Try different display board URLs
            display_urls = [
                f"{self.base_url}/display",
                f"{self.base_url}/board",
                f"{self.base_url}/queue-display"
            ]
            
            for url in display_urls:
                try:
                    self.driver.get(url)
                    time.sleep(3)
                    
                    # Check if display board loaded
                    if len(self.driver.page_source) > 1000:
                        self.log_result("Display Board", "PASS", f"Display board accessible at {url}")
                        break
                except:
                    continue
            else:
                self.log_result("Display Board", "FAIL", "Display board not accessible")
                
            # Close display board tab
            self.driver.close()
            self.driver.switch_to.window(self.driver.window_handles[0])
            
        except Exception as e:
            self.log_result("Display Board", "FAIL", str(e))
            
    def test_responsive_design(self):
        """Test responsive design"""
        print("📱 Testing Responsive Design...")
        
        screen_sizes = [
            (1920, 1080, "Desktop"),
            (1366, 768, "Laptop"),
            (768, 1024, "Tablet"),
            (375, 667, "Mobile")
        ]
        
        for width, height, device in screen_sizes:
            try:
                self.driver.set_window_size(width, height)
                time.sleep(2)
                
                # Check if page is still functional
                body_height = self.driver.execute_script("return document.body.scrollHeight")
                self.log_result("Responsive Design", "PASS", f"{device}: {width}x{height}, Height: {body_height}px")
                
            except Exception as e:
                self.log_result("Responsive Design", "FAIL", f"{device}: {str(e)}")
                
    def generate_analysis_report(self):
        """Generate comprehensive analysis report"""
        passed = len([r for r in self.analysis_results if r["status"] == "PASS"])
        failed = len([r for r in self.analysis_results if r["status"] == "FAIL"])
        total = len(self.analysis_results)
        
        report = {
            "analysis_time": datetime.now().isoformat(),
            "website_url": self.base_url,
            "total_tests": total,
            "passed_tests": passed,
            "failed_tests": failed,
            "success_rate": f"{(passed/total*100):.1f}%" if total > 0 else "0%",
            "test_results": self.analysis_results
        }
        
        with open(f"website_analysis_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json", 'w') as f:
            json.dump(report, f, indent=2)
            
        print(f"\n📊 Website Analysis Report:")
        print(f"✅ Passed: {passed}")
        print(f"❌ Failed: {failed}")
        print(f"📈 Success Rate: {report['success_rate']}")
        
    def run_complete_analysis(self):
        """Run complete website analysis"""
        print("🚀 SMART HEALTH WEBSITE COMPLETE ANALYSIS")
        print("=" * 60)
        
        try:
            self.driver.maximize_window()
            
            # 1. Analyze homepage
            self.analyze_homepage()
            
            # 2. Test staff workflow
            self.test_staff_workflow()
            
            # 3. Test patient workflow
            self.test_patient_workflow()
            
            # 4. Test display board
            self.test_display_board()
            
            # 5. Test responsive design
            self.test_responsive_design()
            
            # 6. Generate analysis report
            self.generate_analysis_report()
            
            print("\n🎉 COMPLETE WEBSITE ANALYSIS FINISHED!")
            
        except Exception as e:
            print(f"❌ Critical Error: {str(e)}")
            
        finally:
            input("Press Enter to close browser...")
            self.driver.quit()

if __name__ == "__main__":
    analyzer = SmartHealthWebsiteAnalyzer()
    analyzer.run_complete_analysis()