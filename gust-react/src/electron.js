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

  // mainWindow.loadURL("http://localhost:3000")
  mainWindow.loadFile("index.html")
});

app.on("window-all-closed", () => {
  if (process.platform !== "darwin") {
    app.quit()
  }
})