# 🚀 Backend Services Setup Guide (No Docker)

This guide explains how to set up and run all backend services without Docker using the `setup_and_run.sh` script.

## 📋 Prerequisites

- **Python 3.8+** installed on your system
- **pip3** package manager
- **Virtual environment** support (python3-venv)
- Minimum **4GB RAM** recommended
- **Linux/macOS** (for Windows, use WSL2)

## 🛠️ Quick Start

### 1. Setup All Services

This command will create virtual environments and install all dependencies for each service:

```bash
cd backend
./setup_and_run.sh setup
```

This will:
- ✅ Check Python and pip installation
- ✅ Create virtual environments for each service
- ✅ Install all dependencies from requirements.txt

### 2. Start All Services

```bash
./setup_and_run.sh start
```

This will start all services in the background on their respective ports:
- **Authentication**: `http://localhost:8010`
- **Document Ingestion**: `http://localhost:8001`
- **Document Parsing**: `http://localhost:8002`
- **Information Structuring**: `http://localhost:8003`

### 3. Check Status

```bash
./setup_and_run.sh status
```

This displays the current status of all services with their PIDs and ports.

## 📖 Available Commands

| Command | Description |
|---------|-------------|
| `./setup_and_run.sh setup` | Install dependencies for all services |
| `./setup_and_run.sh start` | Start all services in background |
| `./setup_and_run.sh stop` | Stop all running services |
| `./setup_and_run.sh restart` | Restart all services |
| `./setup_and_run.sh status` | Show status of all services |
| `./setup_and_run.sh logs` | Show recent logs from all services |
| `./setup_and_run.sh logs <service>` | Tail logs for a specific service |
| `./setup_and_run.sh clean` | Stop services and remove virtual environments |
| `./setup_and_run.sh help` | Display help information |

## 📝 Examples

### View logs for a specific service

```bash
./setup_and_run.sh logs authentication
```

### Restart all services

```bash
./setup_and_run.sh restart
```

### Clean up everything

```bash
./setup_and_run.sh clean
```

This will stop all services, remove virtual environments, and clear logs.

## 🗂️ Project Structure

```
backend/
├── setup_and_run.sh           # Main setup and run script
├── logs/                       # Service logs (created automatically)
│   ├── authentication.log
│   ├── document-ingestion.log
│   ├── document-parsing.log
│   └── information-structuring.log
├── authentication/
│   ├── venv/                  # Virtual environment
│   ├── requirements.txt
│   └── run.py
├── document-ingestion/
│   ├── venv/
│   ├── requirements.txt
│   └── run.py
├── document-parsing/
│   ├── venv/
│   ├── requirements.txt
│   └── run.py
└── information-structuring/
    ├── venv/
    ├── requirements.txt
    └── run.py
```

## 🔧 Service Ports

Each service runs on a different port:

| Service | Port | Endpoint |
|---------|------|----------|
| Authentication | 8010 | http://localhost:8010 |
| Document Ingestion | 8001 | http://localhost:8001 |
| Document Parsing | 8002 | http://localhost:8002 |
| Information Structuring | 8003 | http://localhost:8003 |

## 📋 Logs

Logs are stored in the `backend/logs/` directory:

- Each service has its own log file
- View logs with: `./setup_and_run.sh logs <service-name>`
- View all logs: `./setup_and_run.sh logs`

## 🐛 Troubleshooting

### Port Already in Use

If you get a "port already in use" error:

```bash
# Check what's using the port
lsof -i :8010

# Kill the process
kill -9 <PID>

# Or let the script handle it
./setup_and_run.sh start
# The script will prompt you to kill existing processes
```

### Service Won't Start

1. Check the logs:
   ```bash
   ./setup_and_run.sh logs <service-name>
   ```

2. Verify dependencies are installed:
   ```bash
   ./setup_and_run.sh setup
   ```

3. Try restarting:
   ```bash
   ./setup_and_run.sh restart
   ```

### Missing Dependencies

If a service fails due to missing dependencies:

```bash
cd <service-directory>
source venv/bin/activate
pip install -r requirements.txt
deactivate
```

### Clean Start

For a completely fresh start:

```bash
./setup_and_run.sh clean
./setup_and_run.sh setup
./setup_and_run.sh start
```

## 🔐 Environment Variables

Some services require environment variables. Create a `.env` file in each service directory:

### Information Structuring Service

Create `backend/information-structuring/.env`:

```env
GEMINI_API_KEY=your_api_key_here
DOCUMENT_PARSING_URL=http://localhost:8002
FEATURE_ENGINEERING_URL=http://localhost:8004
```

### Authentication Service

Create `backend/authentication/.env`:

```env
DATABASE_URL=sqlite:///./auth.db
SECRET_KEY=your_secret_key_here
```

## 🧪 Running Tests

To run tests for a specific service:

```bash
cd <service-directory>
source venv/bin/activate
pytest tests/ -v
deactivate
```

## 🌐 API Documentation

Once services are running, access the interactive API documentation:

- Authentication: http://localhost:8010/docs
- Document Ingestion: http://localhost:8001/docs
- Document Parsing: http://localhost:8002/docs
- Information Structuring: http://localhost:8003/docs

## 💡 Tips

1. **First Time Setup**: Run `setup` before `start`
   ```bash
   ./setup_and_run.sh setup
   ./setup_and_run.sh start
   ```

2. **Monitor Services**: Keep status dashboard open in another terminal
   ```bash
   watch -n 2 './setup_and_run.sh status'
   ```

3. **Development Mode**: Services run with auto-reload enabled by default

4. **Resource Usage**: Monitor with `htop` or `top` to see resource consumption

5. **Quick Restart**: Use restart to pick up code changes
   ```bash
   ./setup_and_run.sh restart
   ```

## 🆚 Docker vs No-Docker

| Feature | Docker | No-Docker (This Script) |
|---------|--------|-------------------------|
| Setup Time | Slower (image builds) | Faster (pip install) |
| Isolation | Full container isolation | Virtual environments |
| Resource Usage | Higher (containers) | Lower (native processes) |
| Development | Requires rebuild | Auto-reload enabled |
| Debugging | More complex | Direct access |

## 📞 Support

If you encounter issues:

1. Check the troubleshooting section above
2. Review service logs: `./setup_and_run.sh logs`
3. Ensure all prerequisites are installed
4. Try a clean setup: `./setup_and_run.sh clean && ./setup_and_run.sh setup`

## 🎯 Next Steps

After starting the services:

1. ✅ Verify all services are running: `./setup_and_run.sh status`
2. ✅ Check the API docs: http://localhost:8010/docs
3. ✅ Test the authentication endpoint
4. ✅ Upload a test document through document-ingestion
5. ✅ Monitor logs for any errors

---

**Happy Coding! 🚀**
