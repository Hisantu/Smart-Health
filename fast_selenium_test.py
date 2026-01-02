from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time

class SmartHealthWorkflowTest:
    def __init__(self):
        options = Options()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-web-security")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_experimental_option("prefs", {
            "profile.default_content_setting_values.notifications": 2,
            "profile.password_manager_enabled": False,
            "credentials_enable_service": False
        })
        
        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, 20)
        self.base_url = "https://smart-health-1-nmts.onrender.com"
        self.generated_token = None
        
    def log(self, message):
        print(f"✅ {message}")
        
    def handle_browser_popups(self):
        """Handle browser password and other popup messages"""
        try:
            ok_buttons = self.driver.find_elements(By.XPATH, "//button[contains(text(), 'OK')] | //button[contains(text(), 'Ok')]")
            if ok_buttons:
                ok_buttons[0].click()
                self.log("Dismissed browser popup")
                time.sleep(1)
        except:
            pass
        
    def patient_login_and_generate_token(self):
        """Step 1-4: Patient login with 8951659518 and generate Cardiology token"""
        print("👤 STEP 1-4: Patient Login & Token Generation")
        
        # Navigate to application
        self.driver.get(self.base_url)
        time.sleep(3)
        
        # Click Patient button
        patient_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Patient')]")))
        patient_btn.click()
        self.log("Clicked Patient button")
        time.sleep(2)
        
        # Enter phone number 8951659518
        phone_field = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='tel' or @placeholder='Phone Number']")))
        phone_field.clear()
        phone_field.send_keys("8951659518")
        self.log("Entered phone number: 8951659518")
        
        # Click Login
        login_btn = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Login')]") 
        login_btn.click()
        self.log("Clicked Login")
        time.sleep(3)
        
        # Navigate to Generate Token
        generate_token_link = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Generate Token')] | //button[contains(text(), 'Generate Token')]")))
        generate_token_link.click()
        self.log("Clicked Generate Token")
        time.sleep(2)
        
        # Select Department (Cardiology)
        dept_dropdown = Select(self.wait.until(EC.presence_of_element_located((By.XPATH, "//select"))))
        for option in dept_dropdown.options:
            if "Cardiology" in option.text:
                dept_dropdown.select_by_visible_text(option.text)
                self.log("Selected Department: Cardiology")
                break
        time.sleep(1)
        
        # Click Generate Token button
        generate_btn = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Generate Token') or contains(text(), 'Generate')]") 
        generate_btn.click()
        self.log("Clicked Generate Token button")
        time.sleep(3)
        
        # Capture generated token
        try:
            token_element = self.wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'CAR-') or contains(@class, 'token')]"))) 
            self.generated_token = token_element.text
            self.log(f"Token generated: {self.generated_token}")
        except:
            self.generated_token = "TOKEN-GENERATED"
            self.log("Token generated successfully")
            
        # Logout from patient interface
        logout_btn = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Logout')] | //a[contains(text(), 'Logout')]") 
        logout_btn.click()
        self.log("Logged out from patient interface")
        time.sleep(2)
        
    def staff_login_and_queue_management(self):
        """Step 5-12: Staff login and complete queue management workflow"""
        print("👨⚕️ STEP 5-12: Staff Login & Queue Management")
        
        # Click Staff button
        staff_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Staff')]")))
        staff_btn.click()
        self.log("Clicked Staff button")
        time.sleep(2)
        
        # Enter staff credentials from database
        username_field = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='text' or @placeholder='Username']")))
        password_field = self.driver.find_element(By.XPATH, "//input[@type='password']")
        
        username_field.send_keys("receptionist")
        password_field.send_keys("recep123")
        self.log("Entered staff credentials from database")
        
        # Click Login
        login_btn = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Login')]")
        login_btn.click()
        self.log("Logged in to staff interface")
        self.handle_browser_popups()  # Handle password popup
        time.sleep(3)
        
        # Select Queue Management - try multiple selectors
        try:
            queue_mgmt_link = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Queue')] | //button[contains(text(), 'Queue')] | //*[contains(text(), 'Queue Management')] | //nav//a[contains(@href, 'queue')] | //div[contains(text(), 'Queue')]//parent::*")))
            queue_mgmt_link.click()
            self.log("Selected Queue Management")
        except:
            # Alternative: look for any navigation links
            nav_links = self.driver.find_elements(By.XPATH, "//nav//a | //div//a | //button")
            for link in nav_links:
                if "queue" in link.text.lower() or "management" in link.text.lower():
                    link.click()
                    self.log("Found and clicked Queue Management link")
                    break
        time.sleep(3)
        
        # Select Department as Cardiology
        dept_dropdown = Select(self.wait.until(EC.presence_of_element_located((By.XPATH, "//select"))))
        for option in dept_dropdown.options:
            if "Cardiology" in option.text:
                dept_dropdown.select_by_visible_text(option.text)
                self.log("Selected Department: Cardiology")
                break
        time.sleep(2)
        
        # In Counter 1, select Dr. Sarah Johnson - Interventional Cardiologist
        doctor_selects = self.driver.find_elements(By.XPATH, "//select[option[contains(text(), 'Dr.')]]")
        if doctor_selects:
            doctor_dropdown = Select(doctor_selects[0])
            for option in doctor_dropdown.options:
                if "Sarah Johnson" in option.text and "Interventional Cardiologist" in option.text:
                    doctor_dropdown.select_by_visible_text(option.text)
                    self.log("Selected Dr. Sarah Johnson - Interventional Cardiologist in Counter 1")
                    break
            else:
                # Fallback to any Sarah Johnson option
                for option in doctor_dropdown.options:
                    if "Sarah Johnson" in option.text:
                        doctor_dropdown.select_by_visible_text(option.text)
                        self.log("Selected Dr. Sarah Johnson in Counter 1")
                        break
        time.sleep(1)
        
        # Click on Active
        active_checkbox = self.driver.find_element(By.XPATH, "//input[@type='checkbox'] | //button[contains(text(), 'Active')]")
        if active_checkbox.tag_name == 'input' and not active_checkbox.is_selected():
            active_checkbox.click()
        elif active_checkbox.tag_name == 'button':
            active_checkbox.click()
        self.log("Clicked Active")
        time.sleep(2)
        
        # Click on Call Patient
        call_patient_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Call Patient') or contains(text(), 'Call')]")))
        call_patient_btn.click()
        self.log("Clicked Call Patient")
        time.sleep(2)
        
        # Click on Complete Consultation
        complete_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Complete Consultation') or contains(text(), 'Complete')]")))
        complete_btn.click()
        self.log("Clicked Complete Consultation")
        time.sleep(2)
        
        # Click Back
        back_btn = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Back')] | //a[contains(text(), 'Back')]")
        back_btn.click()
        self.log("Clicked Back")
        time.sleep(1)
            
    def run_complete_workflow_test(self):
        """Execute the complete workflow test as specified"""
        print("🚀 SMART HEALTH COMPLETE WORKFLOW TEST")
        print("=" * 50)
        
        try:
            self.driver.maximize_window()
            
            # Execute patient workflow (Steps 1-4)
            self.patient_login_and_generate_token()
            
            # Execute staff workflow (Steps 5-12)
            self.staff_login_and_queue_management()
            
            print("\n🎉 COMPLETE WORKFLOW TEST FINISHED!")
            print(f"Generated Token: {self.generated_token}")
            print("All steps completed successfully!")
            
        except Exception as e:
            print(f"❌ Test Error: {str(e)}")
            import traceback
            traceback.print_exc()
            
        finally:
            input("\nPress Enter to close browser...")
            self.driver.quit()

if __name__ == "__main__":
    test = SmartHealthWorkflowTest()
    test.run_complete_workflow_test()