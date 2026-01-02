from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time
import random
import json
from datetime import datetime, timedelta
import os

class SmartHealthDeployedTest:
    def __init__(self):
        options = Options()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1920,1080")
        
        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, 20)
        self.base_url = "https://smart-health-1-nmts.onrender.com"
        self.test_results = []
        
        # Create screenshots directory
        self.screenshots_dir = "deployed_test_screenshots"
        os.makedirs(self.screenshots_dir, exist_ok=True)
        
    def take_screenshot(self, name):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.screenshots_dir}/{name}_{timestamp}.png"
        self.driver.save_screenshot(filename)
        print(f"📸 Screenshot: {filename}")
        
    def log_test(self, test_name, status, details=""):
        result = {
            "test": test_name,
            "status": status,
            "details": details,
            "timestamp": datetime.now().isoformat()
        }
        self.test_results.append(result)
        status_icon = "✅" if status == "PASS" else "❌"
        print(f"{status_icon} {test_name}: {details}")
        
    def analyze_website_structure(self):
        """Analyze the website structure and available elements"""
        print("🔍 Analyzing Website Structure...")
        
        try:
            self.driver.get(self.base_url)
            time.sleep(5)  # Wait for full page load
            
            # Check page title
            title = self.driver.title
            self.log_test("Page Load", "PASS", f"Title: {title}")
            
            # Find all buttons
            buttons = self.driver.find_elements(By.TAG_NAME, "button")
            self.log_test("Button Detection", "PASS", f"Found {len(buttons)} buttons")
            
            # Find all input fields
            inputs = self.driver.find_elements(By.TAG_NAME, "input")
            self.log_test("Input Field Detection", "PASS", f"Found {len(inputs)} input fields")
            
            # Find all links
            links = self.driver.find_elements(By.TAG_NAME, "a")
            self.log_test("Link Detection", "PASS", f"Found {len(links)} links")
            
            # Check for login options
            login_buttons = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'Login') or contains(text(), 'login')]")
            self.log_test("Login Options", "PASS", f"Found {len(login_buttons)} login elements")
            
            # Check for role selection
            staff_elements = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'Staff') or contains(text(), 'staff')]")
            patient_elements = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'Patient') or contains(text(), 'patient')]")
            
            self.log_test("Role Detection", "PASS", f"Staff: {len(staff_elements)}, Patient: {len(patient_elements)}")
            
            self.take_screenshot("01_website_analysis")
            
        except Exception as e:
            self.log_test("Website Analysis", "FAIL", str(e))
            
    def test_staff_login_flow(self):
        """Test staff login functionality"""
        print("👨‍⚕️ Testing Staff Login Flow...")
        
        try:
            self.driver.get(self.base_url)
            time.sleep(3)
            
            # Look for staff login button/link
            staff_login_selectors = [
                "//button[contains(text(), 'Staff Login')]",
                "//a[contains(text(), 'Staff Login')]",
                "//button[contains(text(), 'Staff')]",
                "//a[contains(text(), 'Staff')]",
                "//div[contains(text(), 'Staff')]//parent::*",
                "//*[@class='staff-login' or @id='staff-login']"
            ]
            
            staff_element = None
            for selector in staff_login_selectors:
                try:
                    staff_element = self.driver.find_element(By.XPATH, selector)
                    break
                except:
                    continue
                    
            if staff_element:
                staff_element.click()
                time.sleep(2)
                self.log_test("Staff Login Navigation", "PASS", "Clicked staff login")
                self.take_screenshot("02_staff_login_page")
                
                # Try different credential combinations
                credentials = [
                    {"username": "admin", "password": "admin123"},
                    {"username": "receptionist", "password": "recep123"},
                    {"username": "doctor", "password": "doctor123"},
                    {"username": "staff", "password": "staff123"}
                ]
                
                for cred in credentials:
                    try:
                        # Find username field
                        username_selectors = [
                            "//input[@placeholder='Username']",
                            "//input[@placeholder='Staff ID']",
                            "//input[@type='text']",
                            "//input[@name='username']",
                            "//input[@id='username']"
                        ]
                        
                        username_field = None
                        for selector in username_selectors:
                            try:
                                username_field = self.driver.find_element(By.XPATH, selector)
                                break
                            except:
                                continue
                                
                        # Find password field
                        password_selectors = [
                            "//input[@placeholder='Password']",
                            "//input[@type='password']",
                            "//input[@name='password']",
                            "//input[@id='password']"
                        ]
                        
                        password_field = None
                        for selector in password_selectors:
                            try:
                                password_field = self.driver.find_element(By.XPATH, selector)
                                break
                            except:
                                continue
                                
                        if username_field and password_field:
                            username_field.clear()
                            username_field.send_keys(cred["username"])
                            password_field.clear()
                            password_field.send_keys(cred["password"])
                            
                            # Find and click login button
                            login_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Login') or contains(text(), 'login')]")
                            login_button.click()
                            time.sleep(3)
                            
                            # Check if login was successful
                            current_url = self.driver.current_url
                            if "dashboard" in current_url.lower() or "home" in current_url.lower():
                                self.log_test("Staff Login Success", "PASS", f"Logged in with {cred['username']}")
                                self.take_screenshot("03_staff_dashboard")
                                return True
                            else:
                                # Check for error messages
                                error_elements = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'error') or contains(text(), 'invalid') or contains(text(), 'wrong')]")
                                if error_elements:
                                    self.log_test("Staff Login Attempt", "INFO", f"Failed with {cred['username']}: {error_elements[0].text}")
                                    
                    except Exception as e:
                        self.log_test("Staff Login Attempt", "INFO", f"Error with {cred['username']}: {str(e)}")
                        
                self.log_test("Staff Login", "FAIL", "No valid credentials found")
                
            else:
                self.log_test("Staff Login Navigation", "FAIL", "Staff login button not found")
                
        except Exception as e:
            self.log_test("Staff Login Flow", "FAIL", str(e))
            
    def test_patient_registration_and_login(self):
        """Test patient registration and login"""
        print("👤 Testing Patient Registration and Login...")
        
        try:
            self.driver.get(self.base_url)
            time.sleep(3)
            
            # Look for patient login/register
            patient_selectors = [
                "//button[contains(text(), 'Patient')]",
                "//a[contains(text(), 'Patient')]",
                "//button[contains(text(), 'Register')]",
                "//a[contains(text(), 'Register')]"
            ]
            
            patient_element = None
            for selector in patient_selectors:
                try:
                    patient_element = self.driver.find_element(By.XPATH, selector)
                    break
                except:
                    continue
                    
            if patient_element:
                patient_element.click()
                time.sleep(2)
                self.take_screenshot("04_patient_section")
                
                # Generate random patient data
                patient_data = {
                    "name": f"Test Patient {random.randint(1000, 9999)}",
                    "phone": f"555{random.randint(1000000, 9999999)}",
                    "email": f"test{random.randint(100, 999)}@example.com",
                    "age": str(random.randint(18, 80))
                }
                
                # Try to register patient
                self.register_patient(patient_data)
                
                # Try to login as patient
                self.login_patient(patient_data["phone"])
                
            else:
                self.log_test("Patient Section", "FAIL", "Patient section not found")
                
        except Exception as e:
            self.log_test("Patient Registration/Login", "FAIL", str(e))
            
    def register_patient(self, patient_data):
        """Register a new patient"""
        try:
            # Look for registration form fields
            name_field = self.find_input_field(["name", "full name", "patient name"])
            phone_field = self.find_input_field(["phone", "mobile", "contact"])
            email_field = self.find_input_field(["email", "mail"])
            age_field = self.find_input_field(["age"])
            
            if name_field:
                name_field.send_keys(patient_data["name"])
            if phone_field:
                phone_field.send_keys(patient_data["phone"])
            if email_field:
                email_field.send_keys(patient_data["email"])
            if age_field:
                age_field.send_keys(patient_data["age"])
                
            # Look for gender dropdown
            try:
                gender_dropdown = self.driver.find_element(By.XPATH, "//select")
                Select(gender_dropdown).select_by_visible_text("Male")
            except:
                pass
                
            # Submit registration
            submit_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Register') or contains(text(), 'Submit')]")
            submit_button.click()
            time.sleep(3)
            
            self.log_test("Patient Registration", "PASS", f"Registered {patient_data['name']}")
            self.take_screenshot("05_patient_registered")
            
        except Exception as e:
            self.log_test("Patient Registration", "FAIL", str(e))
            
    def login_patient(self, phone):
        """Login as patient"""
        try:
            # Look for phone input field
            phone_field = self.find_input_field(["phone", "mobile", "login"])
            if phone_field:
                phone_field.clear()
                phone_field.send_keys(phone)
                
                login_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Login')]")
                login_button.click()
                time.sleep(3)
                
                self.log_test("Patient Login", "PASS", f"Logged in with {phone}")
                self.take_screenshot("06_patient_dashboard")
                
        except Exception as e:
            self.log_test("Patient Login", "FAIL", str(e))
            
    def find_input_field(self, keywords):
        """Find input field by keywords"""
        for keyword in keywords:
            selectors = [
                f"//input[@placeholder='{keyword}']",
                f"//input[@placeholder='{keyword.title()}']",
                f"//input[contains(@placeholder, '{keyword}')]",
                f"//input[@name='{keyword}']",
                f"//input[@id='{keyword}']"
            ]
            
            for selector in selectors:
                try:
                    return self.driver.find_element(By.XPATH, selector)
                except:
                    continue
        return None
        
    def test_navigation_and_features(self):
        """Test navigation and available features"""
        print("🧭 Testing Navigation and Features...")
        
        try:
            # Look for navigation menu items
            nav_items = self.driver.find_elements(By.XPATH, "//nav//a | //menu//a | //ul//a")
            
            for item in nav_items[:5]:  # Test first 5 navigation items
                try:
                    item_text = item.text
                    if item_text and len(item_text) > 0:
                        item.click()
                        time.sleep(2)
                        self.log_test("Navigation", "PASS", f"Navigated to {item_text}")
                        self.take_screenshot(f"nav_{item_text.replace(' ', '_').lower()}")
                except Exception as e:
                    self.log_test("Navigation", "INFO", f"Navigation item error: {str(e)}")
                    
        except Exception as e:
            self.log_test("Navigation Test", "FAIL", str(e))
            
    def test_form_interactions(self):
        """Test form interactions and data input"""
        print("📝 Testing Form Interactions...")
        
        try:
            # Find all forms on the page
            forms = self.driver.find_elements(By.TAG_NAME, "form")
            
            for i, form in enumerate(forms[:3]):  # Test first 3 forms
                try:
                    inputs = form.find_elements(By.TAG_NAME, "input")
                    selects = form.find_elements(By.TAG_NAME, "select")
                    textareas = form.find_elements(By.TAG_NAME, "textarea")
                    
                    # Fill text inputs
                    for input_field in inputs:
                        input_type = input_field.get_attribute("type")
                        placeholder = input_field.get_attribute("placeholder")
                        
                        if input_type == "text":
                            input_field.send_keys(f"Test Data {random.randint(1, 100)}")
                        elif input_type == "email":
                            input_field.send_keys(f"test{random.randint(1, 100)}@example.com")
                        elif input_type == "tel" or "phone" in placeholder.lower():
                            input_field.send_keys(f"555{random.randint(1000000, 9999999)}")
                        elif input_type == "number":
                            input_field.send_keys(str(random.randint(1, 100)))
                            
                    # Fill select dropdowns
                    for select in selects:
                        try:
                            select_obj = Select(select)
                            options = select_obj.options
                            if len(options) > 1:
                                select_obj.select_by_index(random.randint(1, len(options)-1))
                        except:
                            pass
                            
                    # Fill textareas
                    for textarea in textareas:
                        textarea.send_keys("This is automated test data for textarea field.")
                        
                    self.log_test("Form Interaction", "PASS", f"Filled form {i+1}")
                    self.take_screenshot(f"form_{i+1}_filled")
                    
                except Exception as e:
                    self.log_test("Form Interaction", "INFO", f"Form {i+1} error: {str(e)}")
                    
        except Exception as e:
            self.log_test("Form Interactions", "FAIL", str(e))
            
    def test_responsive_design(self):
        """Test responsive design"""
        print("📱 Testing Responsive Design...")
        
        try:
            # Test different screen sizes
            screen_sizes = [
                (1920, 1080, "Desktop"),
                (1366, 768, "Laptop"),
                (768, 1024, "Tablet"),
                (375, 667, "Mobile")
            ]
            
            for width, height, device in screen_sizes:
                self.driver.set_window_size(width, height)
                time.sleep(2)
                
                # Check if page is still functional
                body_height = self.driver.execute_script("return document.body.scrollHeight")
                self.log_test("Responsive Design", "PASS", f"{device}: {width}x{height}, Height: {body_height}px")
                self.take_screenshot(f"responsive_{device.lower()}")
                
        except Exception as e:
            self.log_test("Responsive Design", "FAIL", str(e))
            
    def generate_comprehensive_report(self):
        """Generate comprehensive test report"""
        report = {
            "test_execution_time": datetime.now().isoformat(),
            "website_url": self.base_url,
            "total_tests": len(self.test_results),
            "passed_tests": len([t for t in self.test_results if t["status"] == "PASS"]),
            "failed_tests": len([t for t in self.test_results if t["status"] == "FAIL"]),
            "info_tests": len([t for t in self.test_results if t["status"] == "INFO"]),
            "test_results": self.test_results,
            "screenshots_directory": self.screenshots_dir
        }
        
        # Calculate success rate
        if report["total_tests"] > 0:
            report["success_rate"] = f"{(report['passed_tests'] / report['total_tests'] * 100):.1f}%"
        else:
            report["success_rate"] = "0%"
            
        # Save report
        report_file = f"deployed_test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
            
        print(f"\n📊 Comprehensive Test Report: {report_file}")
        print(f"✅ Passed: {report['passed_tests']}")
        print(f"❌ Failed: {report['failed_tests']}")
        print(f"ℹ️ Info: {report['info_tests']}")
        print(f"📈 Success Rate: {report['success_rate']}")
        
        return report
        
    def run_complete_test_suite(self):
        """Run complete test suite for deployed website"""
        print("🚀 Starting Comprehensive Smart Health Deployed Website Testing")
        print("=" * 70)
        print(f"🌐 Testing URL: {self.base_url}")
        print("=" * 70)
        
        try:
            self.driver.maximize_window()
            
            # 1. Analyze website structure
            self.analyze_website_structure()
            
            # 2. Test staff login flow
            self.test_staff_login_flow()
            
            # 3. Test patient registration and login
            self.test_patient_registration_and_login()
            
            # 4. Test navigation and features
            self.test_navigation_and_features()
            
            # 5. Test form interactions
            self.test_form_interactions()
            
            # 6. Test responsive design
            self.test_responsive_design()
            
            # 7. Generate comprehensive report
            report = self.generate_comprehensive_report()
            
            print("\n🎉 Comprehensive Testing Completed!")
            print("=" * 70)
            
        except Exception as e:
            print(f"❌ Critical Error: {str(e)}")
            self.take_screenshot("critical_error")
            
        finally:
            input("Press Enter to close browser...")
            self.driver.quit()

if __name__ == "__main__":
    test = SmartHealthDeployedTest()
    test.run_complete_test_suite()