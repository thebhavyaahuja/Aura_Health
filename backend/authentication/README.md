# Authentication Service

JWT-based authentication service for the Mammography Report Analysis System.

## Features

- User registration and login
- JWT token generation (access + refresh tokens)
- Token refresh mechanism
- Role-based access control (clinic_admin, gcf_coordinator)
- Password hashing with bcrypt
- Secure logout with token revocation

## Default Users

The system creates two default users on startup:

### Clinic Admin
- **Email:** admin@gmail.com
- **Password:** pw
- **Role:** clinic_admin
- **Organization:** City Imaging Center

### GCF Coordinator
- **Email:** coord@gmail.com
- **Password:** pw
- **Role:** gcf_coordinator
- **Organization:** GCF Program

## API Endpoints

### POST /auth/register
Register a new user

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "password123",
  "full_name": "John Doe",
  "organization": "Hospital Name",
  "role": "clinic_admin"
}
```

### POST /auth/login
Login and receive JWT tokens

**Request Body:**
```json
{
  "email": "admin@gmail.com",
  "password": "pw"
}
```

**Response:**
```json
{
  "user": {
    "id": "uuid",
    "email": "admin@gmail.com",
    "full_name": "Admin User",
    "organization": "City Imaging Center",
    "role": "clinic_admin",
    "is_active": true,
    "created_at": "2024-01-01T00:00:00",
    "last_login": "2024-01-01T00:00:00"
  },
  "token": {
    "access_token": "eyJ...",
    "refresh_token": "eyJ...",
    "token_type": "bearer",
    "expires_in": 86400
  }
}
```

### POST /auth/refresh
Refresh access token

**Request Body:**
```json
{
  "refresh_token": "eyJ..."
}
```

### POST /auth/logout
Logout and revoke refresh tokens

**Headers:**
```
Authorization: Bearer <access_token>
```

### GET /auth/me
Get current user information

**Headers:**
```
Authorization: Bearer <access_token>
```

### POST /auth/change-password
Change user password

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "current_password": "oldpassword",
  "new_password": "newpassword123"
}
```

## Running Locally

```bash
python run.py
```

The service will start on port 8010.

## Environment Variables

- `SECRET_KEY` - JWT secret key (default: auto-generated, set in production!)
- `DATABASE_URL` - SQLite database path (default: ./auth.db)

## Database

The service uses SQLite with two tables:
- `users` - User accounts
- `refresh_tokens` - Active refresh tokens

## Security Notes

⚠️ **Important for Production:**
1. Change the SECRET_KEY in config.py
2. Use a secure database (PostgreSQL recommended)
3. Enable HTTPS
4. Set strong password requirements
5. Add rate limiting on auth endpoints
6. Configure proper CORS origins
