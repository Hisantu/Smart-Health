import subprocess
import sys
import os
from datetime import datetime

def run_tests():
    """Run all Selenium tests and generate reports"""
    
    print("Smart Health Selenium Test Suite")
    print("=" * 50)
    
    # Create reports directory
    if not os.path.exists("reports"):
        os.makedirs("reports")
    
    # Test files to run
    test_files = [
        ("Admin/Receptionist Tests", "test_admin_receptionist.py"),
        ("Patient Interface Tests", "test_patient_interface.py"),
        ("End-to-End Workflow Tests", "test_e2e_workflow.py")
    ]
    
    results = []
    
    for test_name, test_file in test_files:
        print(f"\nRunning {test_name}")
        print("-" * 30)
        
        try:
            # Run pytest with HTML report
            report_name = f"reports/{test_file.replace('.py', '_report.html')}"
            cmd = [
                sys.executable, "-m", "pytest", 
                test_file, 
                "-v", 
                "--html=" + report_name,
                "--self-contained-html"
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"PASSED: {test_name}")
                results.append((test_name, "PASSED", report_name))
            else:
                print(f"FAILED: {test_name}")
                results.append((test_name, "FAILED", report_name))
                print("Error output:", result.stderr)
                
        except Exception as e:
            print(f"ERROR: {test_name} - {str(e)}")
            results.append((test_name, "ERROR", "N/A"))
    
    # Print summary
    print("\n" + "=" * 50)
    print("TEST SUMMARY")
    print("=" * 50)
    
    for test_name, status, report in results:
        status_icon = "PASS" if status == "PASSED" else "FAIL"
        print(f"{status_icon}: {test_name} - {status}")
        if report != "N/A":
            print(f"   Report: {report}")
    
    print(f"\nTest completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("\nTips:")
    print("- Open HTML reports in browser for detailed results")
    print("- Check screenshots in reports for failed tests")
    print("- Ensure your deployed website is accessible")

if __name__ == "__main__":
    run_tests()