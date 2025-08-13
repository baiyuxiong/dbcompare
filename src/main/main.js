const { app, BrowserWindow, ipcMain, dialog } = require('electron');
const path = require('path');
const { DatabaseManager } = require('./database-manager');
const { SQLParser } = require('./sql-parser');
const { SQLGenerator } = require('./sql-generator');
const { DBConnector } = require('./db-connector');

let mainWindow = null;
const databaseManager = new DatabaseManager();
const sqlParser = new SQLParser();
const sqlGenerator = new SQLGenerator();
const dbConnector = new DBConnector();

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1400,
    height: 900,
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      preload: path.join(__dirname, 'preload.js')
    },
    titleBarStyle: 'default',
    show: false
  });

  // 开发环境加载本地服务器
  if (process.env.NODE_ENV === 'development') {
    mainWindow.loadURL('http://localhost:5173');
    mainWindow.webContents.openDevTools();
  } else {
    mainWindow.loadFile(path.join(__dirname, '../renderer/index.html'));
  }

  mainWindow.once('ready-to-show', () => {
    mainWindow?.show();
  });

  mainWindow.on('closed', () => {
    mainWindow = null;
  });
}

app.whenReady().then(createWindow);

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

// IPC 处理程序
ipcMain.handle('select-file', async () => {
  const result = await dialog.showOpenDialog(mainWindow, {
    properties: ['openFile'],
    filters: [
      { name: 'SQL Files', extensions: ['sql'] },
      { name: 'All Files', extensions: ['*'] }
    ]
  });
  return result.filePaths[0] || null;
});

ipcMain.handle('get-connections', async () => {
  return await databaseManager.getConnections();
});

ipcMain.handle('add-connection', async (event, connection) => {
  return await databaseManager.addConnection(connection);
});

ipcMain.handle('update-connection', async (event, connection) => {
  return await databaseManager.updateConnection(connection);
});

ipcMain.handle('delete-connection', async (event, id) => {
  return await databaseManager.deleteConnection(id);
});

ipcMain.handle('get-history', async (event, side) => {
  return await databaseManager.getHistory(side);
});

ipcMain.handle('add-history', async (event, history) => {
  return await databaseManager.addHistory(history);
});

ipcMain.handle('update-history-last-used', async (event, id) => {
  return await databaseManager.updateHistoryLastUsed(id);
});

ipcMain.handle('parse-sql-file', async (event, filePath) => {
  return await sqlParser.parseFile(filePath);
});

ipcMain.handle('get-table-structure', async (event, connection) => {
  try {
    await dbConnector.connect(connection);
    const structure = await dbConnector.getTableStructure();
    await dbConnector.close();
    return structure;
  } catch (error) {
    await dbConnector.close();
    throw error;
  }
});

ipcMain.handle('compare-tables', async (event, leftTables, rightTables) => {
  return sqlParser.compareTables(leftTables, rightTables);
});

ipcMain.handle('generate-sync-sql', async (event, leftTables, rightTables) => {
  return sqlGenerator.generateSyncSQL(leftTables, rightTables);
}); 