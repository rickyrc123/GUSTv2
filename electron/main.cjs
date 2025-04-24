const { app, BrowserWindow, dialog } = require('electron');
const path = require('path');
const { exec, spawn } = require('child_process');
const fs = require('fs');

let mainWindow;
let backendReady = false;

// Error types for better error handling
const ErrorTypes = {
  DOCKER_NOT_INSTALLED: 'DOCKER_NOT_INSTALLED',
  DOCKER_NOT_RUNNING: 'DOCKER_NOT_RUNNING',
  IMAGES_FILE_NOT_FOUND: 'IMAGES_FILE_NOT_FOUND',
  IMAGE_LOAD_FAILED: 'IMAGE_LOAD_FAILED',
  COMPOSE_FILE_NOT_FOUND: 'COMPOSE_FILE_NOT_FOUND',
  SERVICES_START_FAILED: 'SERVICES_START_FAILED',
  BACKEND_HEALTH_CHECK_FAILED: 'BACKEND_HEALTH_CHECK_FAILED'
};

// Helper function to get paths to resources
function getResourcePath(filename) {
  return app.isPackaged 
    ? path.join(process.resourcesPath, filename)
    : path.join(__dirname, '..', filename);
}

// Check if Docker is installed and running
async function checkDocker() {
  return new Promise((resolve) => {
    exec('docker --version', (error) => {
      if (error) {
        console.error('Docker not installed:', error);
        resolve({
          success: false,
          error: ErrorTypes.DOCKER_NOT_INSTALLED,
          message: 'Docker is not installed or not in PATH'
        });
        return;
      }
      
      exec('docker info', (error) => {
        if (error) {
          console.error('Docker not running:', error);
          resolve({
            success: false,
            error: ErrorTypes.DOCKER_NOT_RUNNING,
            message: 'Docker is installed but not running'
          });
          return;
        }
        
        resolve({ success: true });
      });
    });
  });
}

// Load Docker images from the saved file
async function loadDockerImages() {
  const imagesPath = getResourcePath('docker-images.tar');
  
  if (!fs.existsSync(imagesPath)) {
    console.error('Docker images file not found:', imagesPath);
    return {
      success: false,
      error: ErrorTypes.IMAGES_FILE_NOT_FOUND,
      message: `Docker images file not found: ${imagesPath}`
    };
  }
  
  return new Promise((resolve) => {
    console.log('Loading Docker images from file, this may take a moment...');
    
    const loadProcess = spawn('docker', ['load', '-i', imagesPath]);
    
    loadProcess.stdout.on('data', (data) => {
      console.log(`Docker load: ${data}`);
    });
    
    loadProcess.stderr.on('data', (data) => {
      console.error(`Docker load error: ${data}`);
    });
    
    loadProcess.on('close', (code) => {
      if (code === 0) {
        console.log('Docker images loaded successfully');
        resolve({ success: true });
      } else {
        console.error(`Failed to load Docker images (exit code: ${code})`);
        resolve({
          success: false,
          error: ErrorTypes.IMAGE_LOAD_FAILED,
          message: `Failed to load Docker images (exit code: ${code})`
        });
      }
    });
  });
}

// Check if the backend API is responding
async function checkBackendHealth() {
  return new Promise((resolve) => {
    // Give the backend a moment to start up
    setTimeout(() => {
      const http = require('http');
      const options = {
        hostname: 'localhost',
        port: 8000,
        path: '/health',  // Assuming your FastAPI has a health endpoint
        method: 'GET',
        timeout: 2000
      };
      
      const req = http.request(options, (res) => {
        if (res.statusCode === 200) {
          console.log('Backend API is healthy');
          resolve({ success: true });
        } else {
          console.log(`Backend health check failed with status: ${res.statusCode}`);
          resolve({
            success: false,
            error: ErrorTypes.BACKEND_HEALTH_CHECK_FAILED,
            message: `Backend health check failed with status: ${res.statusCode}`
          });
        }
      });
      
      req.on('error', (error) => {
        console.error('Backend health check error:', error);
        resolve({
          success: false,
          error: ErrorTypes.BACKEND_HEALTH_CHECK_FAILED,
          message: `Backend health check error: ${error.message}`
        });
      });
      
      req.on('timeout', () => {
        console.error('Backend health check timeout');
        req.abort();
        resolve({
          success: false,
          error: ErrorTypes.BACKEND_HEALTH_CHECK_FAILED,
          message: 'Backend health check timeout'
        });
      });
      
      req.end();
    }, 3000);  // Wait 3 seconds before checking
  });
}

// Stop Docker services using docker-compose
async function stopDockerServices() {
  const composePath = getResourcePath('docker-compose.yml');
  
  return new Promise((resolve) => {
    const downProcess = spawn('docker', ['compose', '-f', composePath, 'down']);
    
    downProcess.on('close', (code) => {
      console.log('Docker services stopped');
      resolve();
    });
  });
}

async function initializeBackend() {
  // Check if Docker is available
  const dockerCheck = await checkDocker();
  if (!dockerCheck.success) {
    return dockerCheck;
  }
  
  // Load Docker images
  const imagesLoaded = await loadDockerImages();
  if (!imagesLoaded.success) {
    return imagesLoaded;
  }
  
  // Create required directories
  const dbDir = path.join(app.getPath('userData'), 'db');
  if (!fs.existsSync(dbDir)) {
    fs.mkdirSync(dbDir, { recursive: true });
  }
  
  // Create a temporary docker-compose.yml with correct paths
  const composeTemplate = fs.readFileSync(getResourcePath('docker-compose.yml'), 'utf8');
  const composePath = path.join(app.getPath('userData'), 'docker-compose.yml');
  
  // Replace relative paths with absolute paths
  const modifiedCompose = composeTemplate.replace('./db:/db', `${dbDir}:/db`);
  fs.writeFileSync(composePath, modifiedCompose);
  
  // Start services
  const servicesStarted = await startDockerServices(composePath);
  if (!servicesStarted.success) {
    return servicesStarted;
  }
  
  // Check if backend is healthy
  const healthCheck = await checkBackendHealth();
  return healthCheck;
}

// Modified startDockerServices to accept a custom compose path
async function startDockerServices(composePath) {
  if (!fs.existsSync(composePath)) {
    console.error('Docker Compose file not found:', composePath);
    return {
      success: false,
      error: ErrorTypes.COMPOSE_FILE_NOT_FOUND,
      message: `Docker Compose file not found: ${composePath}`
    };
  }
  
  return new Promise((resolve) => {
    const upProcess = spawn('docker', ['compose', '-f', composePath, 'up', '-d', '--force-recreate']);
    
    upProcess.stdout.on('data', (data) => {
      console.log(`Docker Compose up: ${data}`);
    });
    
    upProcess.stderr.on('data', (data) => {
      console.error(`Docker Compose error: ${data}`);
    });
    
    upProcess.on('close', (code) => {
      if (code === 0) {
        console.log('Docker services started successfully');
        resolve({ success: true });
      } else {
        console.error(`Failed to start Docker services (exit code: ${code})`);
        resolve({
          success: false,
          error: ErrorTypes.SERVICES_START_FAILED,
          message: `Failed to start Docker services (exit code: ${code})`
        });
      }
    });
  });
}

function showErrorDialog(errorResult) {
  let title, message, detail;
  
  switch(errorResult.error) {
    case ErrorTypes.DOCKER_NOT_INSTALLED:
      title = 'Docker Not Installed';
      message = 'This application requires Docker to be installed.';
      detail = 'Please install Docker Desktop and try again.';
      break;
    
    case ErrorTypes.DOCKER_NOT_RUNNING:
      title = 'Docker Not Running';
      message = 'Docker is installed but not running.';
      detail = 'Please start Docker Desktop and try again.';
      break;
      
    case ErrorTypes.IMAGES_FILE_NOT_FOUND:
      title = 'Docker Images Not Found';
      message = 'Could not find the required Docker images.';
      detail = errorResult.message;
      break;
      
    case ErrorTypes.IMAGE_LOAD_FAILED:
      title = 'Docker Images Failed to Load';
      message = 'Failed to load the required Docker images.';
      detail = errorResult.message;
      break;
      
    case ErrorTypes.COMPOSE_FILE_NOT_FOUND:
      title = 'Docker Compose File Not Found';
      message = 'Could not find the Docker Compose configuration file.';
      detail = errorResult.message;
      break;
      
    case ErrorTypes.SERVICES_START_FAILED:
      title = 'Services Failed to Start';
      message = 'Failed to start the required Docker services.';
      detail = errorResult.message;
      break;
      
    case ErrorTypes.BACKEND_HEALTH_CHECK_FAILED:
      title = 'Backend Not Responding';
      message = 'The backend service is not responding.';
      detail = errorResult.message;
      break;
      
    default:
      title = 'Backend Error';
      message = 'An unknown error occurred.';
      detail = errorResult.message || 'No details available.';
  }
  
  dialog.showMessageBox({
    type: 'error',
    title: title,
    message: message,
    detail: detail,
    buttons: ['OK']
  });
}

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    webPreferences: {
      preload: path.join(__dirname, 'preload.cjs'),
      contextIsolation: true,
      nodeIntegration: false
    }
  });

  // Load the app
  if (app.isPackaged) {
    mainWindow.loadFile(path.join(__dirname, '../gust-react/dist/index.html'));
  } else {
    mainWindow.loadURL('http://localhost:5173');
  }

  // Handle window close event
  mainWindow.on('closed', () => {
    mainWindow = null;
  });
}

// Start the application
app.whenReady().then(async () => {
  const result = await initializeBackend();
  
  if (result.success) {
    backendReady = true;
    createWindow();
  } else {
    showErrorDialog(result);
    app.quit();
  }
});

// Quit when all windows are closed
app.on('window-all-closed', async () => {
  if (backendReady) {
    await stopDockerServices();
  }
  
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

// Clean up before quitting
app.on('will-quit', async (event) => {
  if (backendReady) {
    event.preventDefault(); // Prevent quitting until cleanup is done
    await stopDockerServices();
    app.exit(0); // Now we can quit
  }
});

// On macOS, recreate window when the dock icon is clicked
app.on('activate', () => {
  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow();
  }
});