# Smart Health Selenium Testing Guide

## 🧪 Automated Testing for Deployed Smart Health System

This test suite performs **End-to-End (E2E) testing** on your deployed Smart Health system at:
**https://smart-health-1-nmts.onrender.com**

## 📋 What Tests Are Covered

### 1. Admin/Receptionist Tests (`test_admin_receptionist.py`)
- ✅ Admin login functionality
- ✅ Patient registration process
- ✅ Token generation for walk-in patients
- ✅ Appointment booking
- ✅ Queue management setup

### 2. Patient Interface Tests (`test_patient_interface.py`)
- ✅ Patient dashboard access
- ✅ Patient self-registration
- ✅ Patient token generation
- ✅ Patient appointment booking
- ✅ Display board functionality
- ✅ My Tokens view

### 3. End-to-End Workflow Tests (`test_e2e_workflow.py`)
- ✅ Complete patient journey (registration → token → queue → completion)
- ✅ Display board real-time updates
- ✅ Receptionist workflow validation

## 🚀 Quick Setup & Run

### Step 1: Install Dependencies
```bash
cd E:\smart_health\selenium_tests
pip install -r requirements.txt
```

### Step 2: Run All Tests
```bash
python run_tests.py
```

### Step 3: View Results
- HTML reports generated in `reports/` folder
- Open in browser for detailed results with screenshots

## 📁 Project Structure
```
selenium_tests/
├── requirements.txt          # Dependencies
├── base_test.py             # Base test utilities
├── test_admin_receptionist.py   # Admin/Staff tests
├── test_patient_interface.py    # Patient tests
├── test_e2e_workflow.py         # End-to-end tests
├── run_tests.py             # Test runner
├── reports/                 # Generated HTML reports
└── README.md               # This guide
```

## 🔧 Individual Test Execution

### Run Specific Test File
```bash
pytest test_admin_receptionist.py -v --html=reports/admin_report.html
pytest test_patient_interface.py -v --html=reports/patient_report.html
pytest test_e2e_workflow.py -v --html=reports/e2e_report.html
```

### Run Single Test Method
```bash
pytest test_admin_receptionist.py::TestAdminReceptionist::test_admin_login -v
```

## 🎯 Test Scenarios Explained

### Admin Login Test
- Opens login page
- Enters admin credentials
- Verifies dashboard loads
- **Expected**: Successful login and dashboard display

### Patient Registration Test
- Navigates to patient registration
- Fills all required fields
- Submits form
- **Expected**: Patient registered successfully

### Token Generation Test
- Selects patient and department
- Generates walk-in token
- **Expected**: Token created with proper number

### Queue Management Test
- Sets up department and counter
- Assigns doctor to counter
- Activates counter
- **Expected**: Queue ready for patient management

### Complete Patient Journey Test
- Registers new patient
- Generates token
- Sets up queue
- Calls patient
- Completes consultation
- **Expected**: Full workflow completion

## 🛠️ Troubleshooting

### Chrome Driver Issues
```bash
# Update Chrome driver
pip install --upgrade webdriver-manager
```

### Website Not Accessible
- Verify your deployed URL is working
- Check internet connection
- Ensure website is not in maintenance mode

### Test Failures
- Check HTML reports for detailed error messages
- Screenshots are included in reports
- Verify test data (patients, departments) exists

### Timeout Issues
- Increase wait times in `base_test.py`
- Check if website is slow to load
- Verify elements are present on page

## 📊 Understanding Test Reports

### HTML Reports Include:
- ✅ Test execution summary
- 📸 Screenshots of failures
- 🕐 Execution time for each test
- 📝 Detailed error messages
- 📈 Pass/Fail statistics

### Report Locations:
- `reports/test_admin_receptionist_report.html`
- `reports/test_patient_interface_report.html`
- `reports/test_e2e_workflow_report.html`

## 🎓 For Viva/Interview Presentation

### Key Points to Highlight:
1. **Real Deployment Testing**: Tests run on actual deployed website
2. **Complete User Journeys**: Tests simulate real user behavior
3. **Multiple User Roles**: Admin, Receptionist, Patient workflows
4. **Automated Validation**: No manual intervention required
5. **Detailed Reporting**: HTML reports with screenshots

### Demo Flow:
1. Show test execution: `python run_tests.py`
2. Open HTML reports in browser
3. Explain test scenarios and validations
4. Show both passed and failed test examples
5. Discuss real-world testing benefits

## 🔄 Continuous Integration Ready

This test suite can be integrated with:
- GitHub Actions
- Jenkins
- Azure DevOps
- Any CI/CD pipeline

## 📞 Support

For issues with tests:
1. Check HTML reports first
2. Verify website accessibility
3. Update dependencies if needed
4. Check Chrome browser version compatibility

---

**🎉 Your Smart Health system now has professional-grade automated testing!**