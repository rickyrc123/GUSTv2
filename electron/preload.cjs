const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electron', {
  sendApiRequest: (data) => ipcRenderer.send('api-request', data),
  onApiResponse: (callback) => ipcRenderer.on('api-response', callback),
});