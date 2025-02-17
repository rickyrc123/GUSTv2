import {app, BrowserWindow} from 'electron';

let mainWindow;

app.whenReady().then(() => {
  mainWindow = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      nodeIntegration: false,
    },
  });

  mainWindow.loadURL("http://localhost:5173")
});

app.on("window-all-closed", () => {
  if (process.platform !== "darwin") {
    app.quit()
  }
})