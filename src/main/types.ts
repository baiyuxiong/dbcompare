export interface Connection {
  id?: number;
  name: string;
  type: 'mysql' | 'agent';
  config: any;
  lastUsed: string;
  createdAt: string;
}

export interface History {
  id?: number;
  side: 'left' | 'right';
  type: 'file' | 'connection';
  value: string;
  display: string;
  lastUsed: string;
}

export interface TableColumn {
  raw: string;
  type: string;
  length?: string;
  nullable: boolean;
  default?: string;
  comment?: string;
}

export interface TableIndex {
  type: string;
  columns: string;
  unique: boolean;
}

export interface TableStructure {
  columns: { [key: string]: TableColumn };
  indexes: { [key: string]: TableIndex };
}

export interface Tables {
  [tableName: string]: TableStructure;
}

export interface TableDifferences {
  modifiedTables: { [tableName: string]: any };
  addedTables: string[];
  removedTables: string[];
} 