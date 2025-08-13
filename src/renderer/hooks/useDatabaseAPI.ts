import { useCallback } from 'react';

declare global {
  interface Window {
    databaseAPI: {
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
    };
  }
}

export const useDatabaseAPI = () => {
  const selectFile = useCallback(async (): Promise<string | null> => {
    return await window.databaseAPI.selectFile();
  }, []);

  const getConnections = useCallback(async () => {
    return await window.databaseAPI.getConnections();
  }, []);

  const addConnection = useCallback(async (connection: any) => {
    return await window.databaseAPI.addConnection(connection);
  }, []);

  const updateConnection = useCallback(async (connection: any) => {
    return await window.databaseAPI.updateConnection(connection);
  }, []);

  const deleteConnection = useCallback(async (id: number) => {
    return await window.databaseAPI.deleteConnection(id);
  }, []);

  const getHistory = useCallback(async (side: string) => {
    return await window.databaseAPI.getHistory(side);
  }, []);

  const addHistory = useCallback(async (history: any) => {
    return await window.databaseAPI.addHistory(history);
  }, []);

  const updateHistoryLastUsed = useCallback(async (id: number) => {
    return await window.databaseAPI.updateHistoryLastUsed(id);
  }, []);

  const parseSqlFile = useCallback(async (filePath: string) => {
    return await window.databaseAPI.parseSqlFile(filePath);
  }, []);

  const getTableStructure = useCallback(async (connection: any) => {
    return await window.databaseAPI.getTableStructure(connection);
  }, []);

  const compareTables = useCallback(async (leftTables: any, rightTables: any) => {
    return await window.databaseAPI.compareTables(leftTables, rightTables);
  }, []);

  const generateSyncSQL = useCallback(async (leftTables: any, rightTables: any) => {
    return await window.databaseAPI.generateSyncSQL(leftTables, rightTables);
  }, []);

  return {
    selectFile,
    getConnections,
    addConnection,
    updateConnection,
    deleteConnection,
    getHistory,
    addHistory,
    updateHistoryLastUsed,
    parseSqlFile,
    getTableStructure,
    compareTables,
    generateSyncSQL,
  };
}; 