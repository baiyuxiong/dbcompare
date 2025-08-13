const { contextBridge, ipcRenderer } = require('electron');

// 暴露API到渲染进程
contextBridge.exposeInMainWorld('databaseAPI', {
  selectFile: () => ipcRenderer.invoke('select-file'),
  getConnections: () => ipcRenderer.invoke('get-connections'),
  addConnection: (connection) => ipcRenderer.invoke('add-connection', connection),
  updateConnection: (connection) => ipcRenderer.invoke('update-connection', connection),
  deleteConnection: (id) => ipcRenderer.invoke('delete-connection', id),
  getHistory: (side) => ipcRenderer.invoke('get-history', side),
  addHistory: (history) => ipcRenderer.invoke('add-history', history),
  updateHistoryLastUsed: (id) => ipcRenderer.invoke('update-history-last-used', id),
  parseSqlFile: (filePath) => ipcRenderer.invoke('parse-sql-file', filePath),
  getTableStructure: (connection) => ipcRenderer.invoke('get-table-structure', connection),
  compareTables: (leftTables, rightTables) => ipcRenderer.invoke('compare-tables', leftTables, rightTables),
  generateSyncSQL: (leftTables, rightTables) => ipcRenderer.invoke('generate-sync-sql', leftTables, rightTables),
}); 