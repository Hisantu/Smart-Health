# Smart Healthcare Appointment & Queue Management System

A complete full-stack healthcare queue management system with real-time updates, built with React, Node.js, Express, MongoDB, and Socket.io.

## Features

### Core Modules
- **Patient Management** - Register and manage patient information
- **Token Queue Management** - Generate walk-in tokens with priority support
- **Appointment Booking** - Schedule appointments with doctors
- **Doctor & Shift Management** - Manage doctor availability and schedules
- **Real-time Display Board** - Live queue status display
- **Staff Dashboard** - Call, skip, and manage tokens
- **Notification System** - Push notifications for patients

### Key Capabilities
- ✅ Real-time queue updates using Socket.io
- ✅ Priority token support for elderly/emergency cases
- ✅ Department-wise queue management
- ✅ Closed department handling
- ✅ Full queue detection
- ✅ Role-based access (Admin, Receptionist, Doctor)
- ✅ Modern animated UI with Framer Motion
- ✅ Responsive design with Tailwind CSS

## Tech Stack

### Backend
- Node.js & Express
- MongoDB (Local)
- Socket.io for real-time updates
- JWT authentication
- Mongoose ODM
- Twilio SMS integration
- Morgan logging
- bcryptjs for password hashing

### Frontend
- React 18
- React Router v6
- Axios for API calls
- Socket.io Client
- Framer Motion for animations
- Tailwind CSS for styling
- Vite build tool
- PostCSS & Autoprefixer

## Installation & Setup

### Prerequisites
- Node.js (v16 or higher)
- MongoDB installed and running locally
- npm or yarn

### Quick Start

1. **Start MongoDB Service** (if not running)
   ```bash
   # Windows (Run as Administrator)
   net start MongoDB
   ```

2. **Run the Application**
   - Double-click `START_APPLICATION.bat`
   - OR manually start:
     ```bash
     # Terminal 1 - Backend
     cd smart_health/smart_health/server
     npm install
     npm run seed    # First time only
     npm run dev

     # Terminal 2 - Frontend
     cd smart_health/smart_health/web
     npm install
     npm run dev
     ```

3. **Access the Application**
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:4000
   - Display Board: http://localhost:5173/display

### Default Login Credentials
- **Admin**: `admin` / `admin123`
- **Receptionist**: `receptionist` / `recep123`

## Project Structure

```
smart_health/
├── smart_health/          # Main application folder
│   ├── server/            # Backend
│   │   ├── src/
│   │   │   ├── models/    # MongoDB models
│   │   │   ├── routes/    # API routes
│   │   │   ├── middleware/# Auth middleware
│   │   │   ├── seed/      # Database seeding
│   │   │   └── index.js   # Server entry
│   │   ├── .env           # Environment variables
│   │   └── package.json
│   │
│   ├── web/               # Frontend
│   │   ├── src/
│   │   │   ├── pages/     # React pages
│   │   │   ├── api/       # Axios config
│   │   │   ├── App.jsx    # Main app
│   │   │   └── main.jsx   # Entry point
│   │   ├── index.html
│   │   ├── package.json
│   │   ├── tailwind.config.js
│   │   └── vite.config.js
│   │
│   └── prisma/            # Database schema (future)
│
├── README.md
├── START_APPLICATION.bat  # Quick start script
└── START_BACKEND.bat      # Backend only script
```

## API Endpoints

### Authentication
- `POST /api/auth/login` - User login
- `POST /api/auth/register` - Register new user

### Patients
- `GET /api/patients` - Get all patients
- `POST /api/patients` - Register new patient
- `GET /api/patients/:id` - Get patient by ID

### Tokens
- `GET /api/tokens` - Get tokens (with filters)
- `POST /api/tokens` - Generate new token
- `PATCH /api/tokens/:id/call` - Call token
- `PATCH /api/tokens/:id/skip` - Skip token
- `PATCH /api/tokens/:id/complete` - Complete token

### Appointments
- `GET /api/appointments` - Get appointments
- `POST /api/appointments` - Book appointment
- `PATCH /api/appointments/:id` - Update appointment

### Departments
- `GET /api/departments` - Get all departments
- `POST /api/departments` - Create department
- `PATCH /api/departments/:id` - Update department

### Doctors
- `GET /api/doctors` - Get doctors
- `POST /api/doctors` - Add doctor
- `GET /api/doctors/:id/shifts` - Get doctor shifts
- `POST /api/doctors/:id/shifts` - Add shift

### Notifications
- `GET /api/notifications` - Get notifications

## Real-time Events (Socket.io)

- `tokenCreated` - New token generated
- `tokenCalled` - Token called to counter
- `tokenUpdated` - Token status updated

## Environment Variables

```env
PORT=4000
MONGO_URL=mongodb://localhost:27017/smarthealth
JWT_SECRET=your_jwt_secret_here_change_me
TWILIO_ACCOUNT_SID=your_twilio_sid
TWILIO_AUTH_TOKEN=your_twilio_token
TWILIO_FROM=your_twilio_phone_number
```

## Usage Guide

### For Receptionists

1. **Register Patient**
   - Navigate to "Patient Registration"
   - Fill in patient details
   - Submit to register

2. **Generate Token**
   - Go to "Generate Token"
   - Select patient and department
   - Check "Priority" if needed
   - Generate token

3. **Manage Queue**
   - Open "Queue Management"
   - Select department
   - Call next token
   - Skip or complete as needed

### For Patients

1. **Book Appointment**
   - Select "Appointments"
   - Choose patient, department, doctor
   - Pick date and time slot
   - Submit booking

2. **View Queue Status**
   - Open Display Board (public view)
   - See current token being served
   - Check waiting queue position

## Features in Detail

### Priority Tokens
- Elderly patients
- Emergency cases
- Special needs
- Automatically moved to front of queue

### Queue Validation
- Department open/closed check
- Maximum queue size enforcement
- Duplicate token prevention
- Real-time capacity monitoring

### Notifications
- Token called alerts
- Appointment confirmations
- Queue position updates
- Push notification support

## Development

### Run in Development Mode
```bash
# Backend with auto-reload
cd smart_health/server
npm run dev

# Frontend with hot reload
cd smart_health/web
npm run dev
```

### Build for Production
```bash
cd smart_health/web
npm run build
```

## Troubleshooting

### MongoDB Connection Issues
- Ensure MongoDB service is running
- Check connection string in `.env`
- Verify port 27017 is not blocked

### Port Already in Use
- Backend: Change PORT in `.env`
- Frontend: Change port in `vite.config.js`

### Socket.io Connection Failed
- Check backend URL in frontend Socket.io client
- Ensure CORS is properly configured
- Verify backend server is running

## Future Enhancements
- SMS notifications via Twilio
- Email notifications
- Patient mobile app
- Analytics dashboard
- Multi-language support
- Payment integration
- Medical records management

## License
MIT

## Support
For issues and questions, please create an issue in the repository.
