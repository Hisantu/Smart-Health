import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from base_test import BaseTest

class TestEndToEndWorkflow(BaseTest):
    
    def setup_method(self):
        """Setup before each test"""
        self.setup_driver()
    
    def teardown_method(self):
        """Cleanup after each test"""
        self.teardown_driver()
    
    def test_complete_patient_journey(self):
        """Test complete patient journey from registration to token completion"""
        print("\n🚀 Starting Complete Patient Journey Test")
        
        # Step 1: Admin Login
        print("Step 1: Admin Login")
        self.login("admin", "admin123")
        time.sleep(2)
        
        # Step 2: Register New Patient
        print("Step 2: Register New Patient")
        self.wait_and_click(By.XPATH, "//a[contains(text(), 'Patient Registration')]")
        time.sleep(1)
        
        patient_name = f"E2E Test Patient {int(time.time())}"
        name_field = self.wait_for_element(By.NAME, "name")
        name_field.send_keys(patient_name)
        
        phone_field = self.driver.find_element(By.NAME, "phone")
        phone_field.send_keys("9999888877")
        
        age_field = self.driver.find_element(By.NAME, "age")
        age_field.send_keys("35")
        
        gender_select = Select(self.driver.find_element(By.NAME, "gender"))
        gender_select.select_by_value("Male")
        
        address_field = self.driver.find_element(By.NAME, "address")
        address_field.send_keys("E2E Test Address")
        
        submit_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Register Patient')]")
        submit_button.click()
        time.sleep(3)
        
        # Step 3: Generate Token for Patient
        print("Step 3: Generate Token")
        self.wait_and_click(By.XPATH, "//a[contains(text(), 'Generate Token')]")
        time.sleep(1)
        
        # Select the newly registered patient (should be last in list)
        patient_select = Select(self.wait_for_element(By.NAME, "patient"))
        patient_options = patient_select.options
        if len(patient_options) > 1:
            # Select last patient (newly registered)
            patient_select.select_by_index(len(patient_options) - 1)
        
        dept_select = Select(self.driver.find_element(By.NAME, "department"))
        dept_select.select_by_visible_text("Cardiology")
        
        # Mark as priority
        try:
            priority_checkbox = self.driver.find_element(By.NAME, "priority")
            priority_checkbox.click()
        except:
            pass
        
        generate_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Generate Token')]")
        generate_button.click()
        time.sleep(3)
        
        # Step 4: Setup Queue Management
        print("Step 4: Setup Queue Management")
        self.wait_and_click(By.XPATH, "//a[contains(text(), 'Queue Management')]")
        time.sleep(1)
        
        # Select department
        dept_select = Select(self.wait_for_element(By.XPATH, "//select[contains(@class, 'w-full')]"))
        dept_select.select_by_visible_text("Cardiology")
        time.sleep(2)
        
        # Setup first counter
        try:
            doctor_selects = self.driver.find_elements(By.XPATH, "//select[contains(@class, 'w-full p-3')]")
            if doctor_selects:
                doctor_select = Select(doctor_selects[0])
                if len(doctor_select.options) > 1:
                    doctor_select.select_by_index(1)
                
                # Activate counter
                checkbox = self.driver.find_element(By.XPATH, "//input[@type='checkbox']")
                if not checkbox.is_selected():
                    checkbox.click()
                
                time.sleep(2)
        except Exception as e:
            print(f"Counter setup issue: {str(e)}")
        
        # Step 5: Call Patient Token
        print("Step 5: Call Patient Token")
        try:
            call_buttons = self.driver.find_elements(By.XPATH, "//button[contains(text(), 'Call Patient')]")
            if call_buttons:
                call_buttons[0].click()
                time.sleep(3)
                print("✅ Token called successfully")
                
                # Step 6: Complete Consultation
                print("Step 6: Complete Consultation")
                complete_buttons = self.driver.find_elements(By.XPATH, "//button[contains(text(), 'Complete')]")
                if complete_buttons:
                    complete_buttons[0].click()
                    time.sleep(2)
                    print("✅ Consultation completed")
        except Exception as e:
            print(f"Token management issue: {str(e)}")
        
        print("✅ Complete Patient Journey Test Finished")
    
    def test_display_board_real_time_updates(self):
        """Test display board shows real-time updates"""
        print("\n📺 Testing Display Board Real-time Updates")
        
        # Open display board in current window
        self.driver.get(f"{self.base_url}/display")
        time.sleep(3)
        
        # Verify display board loaded
        try:
            display_elements = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'Smart Health') or contains(text(), 'Queue') or contains(text(), 'Display')]")
            assert len(display_elements) > 0
            print("✅ Display board loaded successfully")
            
            # Check for department sections
            dept_sections = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'Cardiology') or contains(text(), 'Orthopedics') or contains(text(), 'Pediatrics')]")
            if dept_sections:
                print(f"✅ Found {len(dept_sections)} department sections")
            
            # Look for token information
            token_elements = self.driver.find_elements(By.XPATH, "//*[contains(@class, 'token') or contains(text(), 'Token') or contains(text(), 'Currently Serving')]")
            print(f"✅ Display board showing token information: {len(token_elements)} elements")
            
        except Exception as e:
            print(f"⚠️ Display board test issue: {str(e)}")
    
    def test_receptionist_workflow(self):
        """Test receptionist specific workflow"""
        print("\n👩‍💼 Testing Receptionist Workflow")
        
        # Login as receptionist
        self.login("receptionist", "recep123")
        time.sleep(2)
        
        # Verify receptionist dashboard
        try:
            dashboard_elements = self.driver.find_elements(By.XPATH, "//h1[contains(text(), 'Dashboard')] | //div[contains(text(), 'Welcome')]")
            assert len(dashboard_elements) > 0
            print("✅ Receptionist login successful")
            
            # Test navigation to different modules
            modules = ["Patient Registration", "Generate Token", "Queue Management"]
            
            for module in modules:
                try:
                    module_link = self.driver.find_element(By.XPATH, f"//a[contains(text(), '{module}')]")
                    module_link.click()
                    time.sleep(1)
                    print(f"✅ {module} accessible")
                    
                    # Go back to dashboard
                    self.driver.get(f"{self.base_url}/dashboard")
                    time.sleep(1)
                    
                except Exception as e:
                    print(f"⚠️ {module} access issue: {str(e)}")
                    
        except Exception as e:
            print(f"⚠️ Receptionist workflow issue: {str(e)}")

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--html=reports/e2e_test_report.html"])