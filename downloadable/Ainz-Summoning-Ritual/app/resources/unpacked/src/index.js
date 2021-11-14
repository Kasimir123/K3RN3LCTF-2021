const { app, BrowserWindow } = require('electron');
const path = require('path');

if (require('electron-squirrel-startup')) {
  app.quit();
}

const createWindow = () => {
  const win = new BrowserWindow({
    minWidth: 1000,
    minHeight: 700,
    autoHideMenuBar: true,
    show: false
  })
  
  win.maximize();
  win.loadFile(path.join(__dirname, 'index.html'))
  win.show();
};

app.on('ready', createWindow);

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('activate', () => {
  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow();
  }
});