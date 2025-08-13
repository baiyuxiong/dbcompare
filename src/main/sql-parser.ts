import * as fs from 'fs';
import { Tables, TableDifferences } from './types';

export class SQLParser {
  parseFile(filePath: string): Tables {
    const content = fs.readFileSync(filePath, 'utf-8');
    return this.parseSQL(content);
  }

  parseSQL(sql: string): Tables {
    const tables: Tables = {};
    
    // 简单的SQL解析逻辑
    const createTableRegex = /CREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?`?(\w+)`?\s*\(([\s\S]*?)\)\s*;/gi;
    let match;
    
    while ((match = createTableRegex.exec(sql)) !== null) {
      const tableName = match[1];
      const tableBody = match[2];
      
      tables[tableName] = this.parseTableBody(tableBody);
    }
    
    return tables;
  }

  private parseTableBody(body: string): any {
    const columns: { [key: string]: any } = {};
    const indexes: { [key: string]: any } = {};
    
    const lines = body.split('\n').map(line => line.trim()).filter(line => line);
    
    for (const line of lines) {
      if (line.startsWith('`') || /^\w+\s+/.test(line)) {
        // 解析列定义
        const columnMatch = line.match(/`?(\w+)`?\s+([^,\s]+)(?:\(([^)]+)\))?\s*(NOT\s+NULL|NULL)?\s*(DEFAULT\s+[^,\s]+)?\s*(COMMENT\s+'[^']*')?/i);
        if (columnMatch) {
          const columnName = columnMatch[1];
          const columnType = columnMatch[2];
          const length = columnMatch[3];
          const nullable = !columnMatch[4] || columnMatch[4].toUpperCase() !== 'NOT NULL';
          const defaultValue = columnMatch[5];
          const comment = columnMatch[6];
          
          columns[columnName] = {
            raw: line,
            type: columnType,
            length: length,
            nullable: nullable,
            default: defaultValue,
            comment: comment
          };
        }
      } else if (line.toUpperCase().includes('KEY') || line.toUpperCase().includes('INDEX')) {
        // 解析索引定义
        const indexMatch = line.match(/(?:UNIQUE\s+)?(?:KEY|INDEX)\s+`?(\w+)`?\s*\(([^)]+)\)/i);
        if (indexMatch) {
          const indexName = indexMatch[1];
          const indexColumns = indexMatch[2];
          const isUnique = line.toUpperCase().includes('UNIQUE');
          
          indexes[indexName] = {
            type: isUnique ? 'UNIQUE' : 'INDEX',
            columns: indexColumns,
            unique: isUnique
          };
        }
      }
    }
    
    return { columns, indexes };
  }

  compareTables(leftTables: Tables, rightTables: Tables): TableDifferences {
    const differences: TableDifferences = {
      modifiedTables: {},
      addedTables: [],
      removedTables: []
    };
    
    const allTableNames = new Set([
      ...Object.keys(leftTables),
      ...Object.keys(rightTables)
    ]);
    
    for (const tableName of allTableNames) {
      const leftTable = leftTables[tableName];
      const rightTable = rightTables[tableName];
      
      if (!leftTable) {
        differences.addedTables.push(tableName);
      } else if (!rightTable) {
        differences.removedTables.push(tableName);
      } else {
        const tableDiff = this.compareTableStructure(leftTable, rightTable);
        if (tableDiff) {
          differences.modifiedTables[tableName] = tableDiff;
        }
      }
    }
    
    return differences;
  }

  private compareTableStructure(leftTable: any, rightTable: any): any {
    const differences: any = {};
    
    // 比较列
    const columnDiff = this.compareColumns(leftTable.columns, rightTable.columns);
    if (columnDiff) {
      differences.columns = columnDiff;
    }
    
    // 比较索引
    const indexDiff = this.compareIndexes(leftTable.indexes, rightTable.indexes);
    if (indexDiff) {
      differences.indexes = indexDiff;
    }
    
    return Object.keys(differences).length > 0 ? differences : null;
  }

  private compareColumns(leftColumns: any, rightColumns: any): any {
    const differences: any = {
      addedColumns: {},
      removedColumns: {},
      modifiedColumns: {}
    };
    
    const allColumnNames = new Set([
      ...Object.keys(leftColumns),
      ...Object.keys(rightColumns)
    ]);
    
    for (const columnName of allColumnNames) {
      const leftColumn = leftColumns[columnName];
      const rightColumn = rightColumns[columnName];
      
      if (!leftColumn) {
        differences.addedColumns[columnName] = rightColumn;
      } else if (!rightColumn) {
        differences.removedColumns[columnName] = leftColumn;
      } else if (JSON.stringify(leftColumn) !== JSON.stringify(rightColumn)) {
        differences.modifiedColumns[columnName] = {
          left: leftColumn,
          right: rightColumn
        };
      }
    }
    
    return Object.keys(differences.addedColumns).length > 0 ||
           Object.keys(differences.removedColumns).length > 0 ||
           Object.keys(differences.modifiedColumns).length > 0 ? differences : null;
  }

  private compareIndexes(leftIndexes: any, rightIndexes: any): any {
    const differences: any = {
      addedIndexes: [],
      removedIndexes: [],
      modifiedIndexes: []
    };
    
    const allIndexNames = new Set([
      ...Object.keys(leftIndexes),
      ...Object.keys(rightIndexes)
    ]);
    
    for (const indexName of allIndexNames) {
      const leftIndex = leftIndexes[indexName];
      const rightIndex = rightIndexes[indexName];
      
      if (!leftIndex) {
        differences.addedIndexes.push(indexName);
      } else if (!rightIndex) {
        differences.removedIndexes.push(indexName);
      } else if (JSON.stringify(leftIndex) !== JSON.stringify(rightIndex)) {
        differences.modifiedIndexes.push(indexName);
      }
    }
    
    return differences.addedIndexes.length > 0 ||
           differences.removedIndexes.length > 0 ||
           differences.modifiedIndexes.length > 0 ? differences : null;
  }
} 