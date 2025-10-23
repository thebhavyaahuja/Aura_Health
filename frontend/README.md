# Aura Health - Mammogram Report Management System

A professional medical web application designed for managing mammogram reports and AI-driven risk assessment.

## Features

### User Types
- **Clinic Administrators**: Upload mammogram reports securely
- **GCF Program Coordinators**: Review and prioritize reports based on AI risk scores

### Key Functionality
- Secure login system with role-based access
- File upload with drag-and-drop support
- AI-powered risk assessment (High/Medium/Low)
- Comprehensive dashboard with KPI metrics
- Advanced filtering and search capabilities
- Detailed report analysis with keyword highlighting
- Status tracking and internal notes system

### Design Theme
**"Hopeful Professionalism & Clarity"**
- Clean, modern interface inspiring confidence
- Professional navy blue primary color (#003366)
- Subtle pink accents for breast cancer awareness (#F7D9E3)
- Clear typography using Inter font family
- Card-based layouts with generous whitespace

## Demo Credentials

### Clinic Administrator
- Username: `admin@clinic.com`
- Password: `password`
- Access: Clinic Portal for uploading reports

### GCF Program Coordinator  
- Username: `coordinator@gcf.org`
- Password: `password`
- Access: GCF Dashboard for reviewing reports

## User Workflows

### Clinic Administrator Flow
1. Login → Clinic Portal Dashboard
2. Upload reports via drag-and-drop or file browser
3. View submission history with status tracking
4. Monitor upload progress and confirmations

### GCF Coordinator Flow
1. Login → GCF Main Dashboard
2. View KPI metrics (new reports, high-risk cases, etc.)
3. Filter and search reports by risk level, clinic, or patient ID
4. Click "View Details" on any report
5. Analyze original document alongside AI analysis
6. Update review status and add internal notes
7. Return to dashboard with updated status reflected

## Technical Implementation
- Built with Next.js 14 and TypeScript
- Tailwind CSS for styling with custom design tokens
- Responsive design for desktop and mobile
- Client-side state management with localStorage sync
- Professional medical-grade UI components

## Getting Started
1. Clone the repository
2. Install dependencies: `npm install`
3. Run development server: `npm run dev`
4. Open http://localhost:3000 and use demo credentials above
