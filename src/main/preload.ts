import { contextBridge, ipcRenderer } from 'electron';

// 定义API接口
export interface DatabaseAPI {
  selectFile: () => Promise<string | null>;
  getConnections: () => Promise<any[]>;
  addConnection: (connection: any) => Promise<number>;
  updateConnection: (connection: any) => Promise<void>;
  deleteConnection: (id: number) => Promise<void>;
  getHistory: (side: string) => Promise<any[]>;
  addHistory: (history: any) => Promise<number>;
  updateHistoryLastUsed: (id: number) => Promise<void>;
  parseSqlFile: (filePath: string) => Promise<any>;
  getTableStructure: (connection: any) => Promise<any>;
  compareTables: (leftTables: any, rightTables: any) => Promise<any>;
  generateSyncSQL: (leftTables: any, rightTables: any) => Promise<string>;
}

// 暴露API到渲染进程
contextBridge.exposeInMainWorld('databaseAPI', {
  selectFile: () => ipcRenderer.invoke('select-file'),
  getConnections: () => ipcRenderer.invoke('get-connections'),
  addConnection: (connection: any) => ipcRenderer.invoke('add-connection', connection),
  updateConnection: (connection: any) => ipcRenderer.invoke('update-connection', connection),
  deleteConnection: (id: number) => ipcRenderer.invoke('delete-connection', id),
  getHistory: (side: string) => ipcRenderer.invoke('get-history', side),
  addHistory: (history: any) => ipcRenderer.invoke('add-history', history),
  updateHistoryLastUsed: (id: number) => ipcRenderer.invoke('update-history-last-used', id),
  parseSqlFile: (filePath: string) => ipcRenderer.invoke('parse-sql-file', filePath),
  getTableStructure: (connection: any) => ipcRenderer.invoke('get-table-structure', connection),
  compareTables: (leftTables: any, rightTables: any) => ipcRenderer.invoke('compare-tables', leftTables, rightTables),
  generateSyncSQL: (leftTables: any, rightTables: any) => ipcRenderer.invoke('generate-sync-sql', leftTables, rightTables),
} as DatabaseAPI);

// 声明全局类型
declare global {
  interface Window {
    databaseAPI: DatabaseAPI;
  }
} 