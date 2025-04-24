const { app, BrowserWindow } = require('electron');
const path = require('path');

function createWindow() {
    const mainWindow = new BrowserWindow({
        width: 1200,
        height: 800,
        webPreferences: {
            preload: path.join(__dirname, 'preload.cjs'),
            contextIsolation: true, // Important for security
            enableRemoteModule: false, // Disable remote module for security reasons
            nodeIntegration: false // Do not enable nodeIntegration for security reasons
        }
    });

    // Load the local web server URL
    mainWindow.loadURL('http://localhost:5173');

    // Handle window close event
    mainWindow.on('closed', () => {
      cleanupProcesses();
  });
}

function cleanupProcesses() {
  console.log('Cleaning up processes...');
  
  // Stop Docker containers
  exec('docker compose down', (error, stdout, stderr) => {
      if (error) {
          console.error(`Error stopping Docker containers: ${error}`);
          return;
      }
      console.log('Docker containers stopped successfully');
  });
  
  // Find and kill the serve process on port 5173
  if (process.platform === 'win32') {
      exec('for /f "tokens=5" %a in (\'netstat -ano ^| findstr :5173\') do taskkill /F /PID %a', (error) => {
          if (error) console.error(`Error killing serve process: ${error}`);
      });
  } else {
      exec('kill $(lsof -t -i:5173)', (error) => {
          if (error) console.error(`Error killing serve process: ${error}`);
      });
  }
}

app.whenReady().then(createWindow);

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit();
    }
});

app.on('will-quit', (event) => {
  // Ensure cleanup completes before quitting
  cleanupProcesses();
});