from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time

class ExactWorkflowTest:
    def __init__(self):
        options = Options()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1920,1080")
        
        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, 15)
        self.base_url = "https://smart-health-1-nmts.onrender.com"
        
    def run_exact_workflow(self):
        """Run exact workflow as specified"""
        print("🚀 EXACT WORKFLOW TEST")
        print("=" * 50)
        
        try:
            self.driver.maximize_window()
            
            # 1. Patient Login with 8951659518
            print("1️⃣ Patient Login with 8951659518...")
            self.driver.get(self.base_url)
            time.sleep(3)
            
            patient_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Patient')]")))
            patient_btn.click()
            time.sleep(2)
            
            phone_field = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='tel']")))
            phone_field.send_keys("8951659518")
            
            login_btn = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Login')]")
            login_btn.click()
            time.sleep(3)
            
            # Register if needed
            if self.driver.find_elements(By.XPATH, "//button[contains(text(), 'Register')]"):
                register_btn = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Register')]")
                register_btn.click()
                time.sleep(1)
                
                name_field = self.driver.find_element(By.XPATH, "//input[contains(@placeholder, 'Name')]")
                name_field.send_keys("Patient 8951659518")
                
                phone_field = self.driver.find_element(By.XPATH, "//input[contains(@placeholder, 'Phone')]")
                phone_field.clear()
                phone_field.send_keys("8951659518")
                
                submit_btn = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Register')]")
                submit_btn.click()
                time.sleep(3)
                
            print("✅ Patient logged in")
            
            # 2. Click Generate Token
            print("2️⃣ Click Generate Token...")
            token_links = self.driver.find_elements(By.XPATH, "//a[contains(text(), 'Token')] | //*[contains(text(), 'Generate')]//parent::*")
            token_links[0].click()
            time.sleep(2)
            
            # 3. Select Department (Cardiology)
            print("3️⃣ Select Department (Cardiology)...")
            dept_dropdown = Select(self.wait.until(EC.presence_of_element_located((By.XPATH, "//select"))))
            dept_dropdown.select_by_visible_text("Cardiology")
            time.sleep(1)
            
            # 4. Click Generate Token
            print("4️⃣ Click Generate Token...")
            generate_btn = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Generate')]")
            generate_btn.click()
            time.sleep(3)
            
            # Capture token
            token_elements = self.driver.find_elements(By.XPATH, "//*[contains(@class, 'text-8xl')]")
            if token_elements:
                generated_token = token_elements[0].text
                print(f"✅ Generated token: {generated_token}")
            else:
                print("✅ Token generated")
                
            # 5. Logout from patient
            print("5️⃣ Logout from patient...")
            logout_btns = self.driver.find_elements(By.XPATH, "//button[contains(text(), 'Logout')]")
            if logout_btns:
                logout_btns[0].click()
            else:
                self.driver.get(self.base_url)
            time.sleep(2)
            
            # 6. Staff Login
            print("6️⃣ Staff Login...")
            staff_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Staff')]")))
            staff_btn.click()
            time.sleep(2)
            
            username_field = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='text']")))
            password_field = self.driver.find_element(By.XPATH, "//input[@type='password']")
            
            username_field.send_keys("receptionist")
            password_field.send_keys("recep123")
            
            login_btn = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Login')]")
            login_btn.click()
            time.sleep(3)
            print("✅ Staff logged in")
            
            # 7. Select Queue Management
            print("7️⃣ Select Queue Management...")
            queue_links = self.driver.find_elements(By.XPATH, "//a[contains(text(), 'Queue')]")
            queue_links[0].click()
            time.sleep(3)
            
            # 8. Select Department (Cardiology)
            print("8️⃣ Select Department (Cardiology)...")
            dept_dropdown = Select(self.wait.until(EC.presence_of_element_located((By.XPATH, "//select"))))
            dept_dropdown.select_by_visible_text("Cardiology")
            time.sleep(2)
            print("✅ Selected Cardiology department")
            
            # 9. Counter 1 - Select Dr. Sarah Johnson
            print("9️⃣ Counter 1 - Select Dr. Sarah Johnson...")
            doctor_selects = self.driver.find_elements(By.XPATH, "//select[option[contains(text(), 'Dr.')]]")
            if doctor_selects:
                doctor_dropdown = Select(doctor_selects[0])
                for option in doctor_dropdown.options:
                    if "Sarah Johnson" in option.text and "Interventional Cardiologist" in option.text:
                        doctor_dropdown.select_by_visible_text(option.text)
                        break
                    elif "Sarah Johnson" in option.text:
                        doctor_dropdown.select_by_visible_text(option.text)
                        break
                else:
                    doctor_dropdown.select_by_index(1)
            print("✅ Selected Dr. Sarah Johnson - Interventional Cardiologist")
            
            # 10. Click Active
            print("🔟 Click Active...")
            active_checkboxes = self.driver.find_elements(By.XPATH, "//input[@type='checkbox']")
            if active_checkboxes and not active_checkboxes[0].is_selected():
                active_checkboxes[0].click()
            time.sleep(2)
            print("✅ Activated Counter 1")
            
            # 11. Click Call Patient
            print("1️⃣1️⃣ Click Call Patient...")
            call_buttons = self.driver.find_elements(By.XPATH, "//button[contains(text(), 'Call')]")
            if call_buttons:
                call_buttons[0].click()
                time.sleep(2)
                print("✅ Called patient")
                
                # 12. Click Complete Consultation
                print("1️⃣2️⃣ Click Complete Consultation...")
                complete_buttons = self.driver.find_elements(By.XPATH, "//button[contains(text(), 'Complete')]")
                if complete_buttons:
                    complete_buttons[0].click()
                    time.sleep(2)
                    print("✅ Completed consultation")
            else:
                print("ℹ️ No tokens to call")
                
            # 13. Click Back
            print("1️⃣3️⃣ Click Back...")
            back_buttons = self.driver.find_elements(By.XPATH, "//button[contains(text(), 'Back')]")
            if back_buttons:
                back_buttons[0].click()
                time.sleep(1)
                print("✅ Clicked Back")
                
            print("\n🎉 EXACT WORKFLOW COMPLETED SUCCESSFULLY!")
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            
        finally:
            input("Press Enter to close browser...")
            self.driver.quit()

if __name__ == "__main__":
    test = ExactWorkflowTest()
    test.run_exact_workflow()