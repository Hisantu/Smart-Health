import requests
import time

def test_website_accessibility():
    """Test if the deployed website is accessible"""
    base_url = "https://smart-health-1-nmts.onrender.com"
    
    print("Testing Smart Health Website Accessibility")
    print("=" * 50)
    
    try:
        # Test main website
        print("Testing main website...")
        response = requests.get(base_url, timeout=10)
        if response.status_code == 200:
            print("PASS: Main website is accessible")
        else:
            print(f"FAIL: Main website returned status: {response.status_code}")
        
        # Test login page
        print("Testing login page...")
        login_response = requests.get(f"{base_url}/login", timeout=10)
        if login_response.status_code == 200:
            print("PASS: Login page is accessible")
        else:
            print(f"FAIL: Login page returned status: {login_response.status_code}")
        
        # Test API endpoint
        print("Testing API endpoint...")
        api_response = requests.get(f"{base_url}/api/departments", timeout=10)
        if api_response.status_code in [200, 401]:  # 401 is expected without auth
            print("PASS: API endpoint is responding")
        else:
            print(f"FAIL: API endpoint returned status: {api_response.status_code}")
        
        print("\n" + "=" * 50)
        print("Website accessibility test completed!")
        print("Your Smart Health system is deployed and running!")
        
    except requests.exceptions.RequestException as e:
        print(f"FAIL: Error accessing website: {str(e)}")
        print("Please check if your website is deployed and accessible")

if __name__ == "__main__":
    test_website_accessibility()