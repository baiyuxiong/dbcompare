import { Tables } from './types';

export class SQLGenerator {
  generateSyncSQL(leftTables: Tables, rightTables: Tables): string {
    const differences = this.compareTables(leftTables, rightTables);
    let sql = '';
    
    // 生成添加表的SQL
    for (const tableName of differences.addedTables) {
      sql += this.generateCreateTableSQL(tableName, rightTables[tableName]);
    }
    
    // 生成删除表的SQL
    for (const tableName of differences.removedTables) {
      sql += `DROP TABLE IF EXISTS \`${tableName}\`;\n\n`;
    }
    
    // 生成修改表的SQL
    for (const [tableName, tableDiff] of Object.entries(differences.modifiedTables)) {
      sql += this.generateAlterTableSQL(tableName, tableDiff);
    }
    
    return sql;
  }

  private compareTables(leftTables: Tables, rightTables: Tables): any {
    const differences: any = {
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

  private generateCreateTableSQL(tableName: string, tableStructure: any): string {
    let sql = `CREATE TABLE \`${tableName}\` (\n`;
    const columns: string[] = [];
    
    // 添加列定义
    for (const [columnName, column] of Object.entries(tableStructure.columns)) {
      const col = column as any;
      let columnDef = `  \`${columnName}\` ${col.type}`;
      
      if (col.length) {
        columnDef += `(${col.length})`;
      }
      
      if (!col.nullable) {
        columnDef += ' NOT NULL';
      }
      
      if (col.default) {
        columnDef += ` ${col.default}`;
      }
      
      if (col.comment) {
        columnDef += ` ${col.comment}`;
      }
      
      columns.push(columnDef);
    }
    
    // 添加索引定义
    for (const [indexName, index] of Object.entries(tableStructure.indexes)) {
      const idx = index as any;
      let indexDef = '';
      
      if (idx.type === 'UNIQUE') {
        indexDef = `  UNIQUE KEY \`${indexName}\` (${idx.columns})`;
      } else {
        indexDef = `  KEY \`${indexName}\` (${idx.columns})`;
      }
      
      columns.push(indexDef);
    }
    
    sql += columns.join(',\n') + '\n) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;\n\n';
    return sql;
  }

  private generateAlterTableSQL(tableName: string, tableDiff: any): string {
    let sql = `-- 修改表 ${tableName}\n`;
    
    if (tableDiff.columns) {
      // 添加列
      for (const [columnName, column] of Object.entries(tableDiff.columns.addedColumns)) {
        const col = column as any;
        sql += `ALTER TABLE \`${tableName}\` ADD COLUMN \`${columnName}\` ${col.type}`;
        
        if (col.length) {
          sql += `(${col.length})`;
        }
        
        if (!col.nullable) {
          sql += ' NOT NULL';
        }
        
        if (col.default) {
          sql += ` ${col.default}`;
        }
        
        if (col.comment) {
          sql += ` ${col.comment}`;
        }
        
        sql += ';\n';
      }
      
      // 删除列
      for (const columnName of Object.keys(tableDiff.columns.removedColumns)) {
        sql += `ALTER TABLE \`${tableName}\` DROP COLUMN \`${columnName}\`;\n`;
      }
      
      // 修改列
      for (const [columnName, columnDiff] of Object.entries(tableDiff.columns.modifiedColumns)) {
        const diff = columnDiff as any;
        const rightCol = diff.right;
        
        sql += `ALTER TABLE \`${tableName}\` MODIFY COLUMN \`${columnName}\` ${rightCol.type}`;
        
        if (rightCol.length) {
          sql += `(${rightCol.length})`;
        }
        
        if (!rightCol.nullable) {
          sql += ' NOT NULL';
        }
        
        if (rightCol.default) {
          sql += ` ${rightCol.default}`;
        }
        
        if (rightCol.comment) {
          sql += ` ${rightCol.comment}`;
        }
        
        sql += ';\n';
      }
    }
    
    if (tableDiff.indexes) {
      // 删除索引
      for (const indexName of tableDiff.indexes.removedIndexes) {
        sql += `ALTER TABLE \`${tableName}\` DROP INDEX \`${indexName}\`;\n`;
      }
      
      // 添加索引
      for (const indexName of tableDiff.indexes.addedIndexes) {
        const index = tableDiff.indexes.addedIndexes[indexName];
        if (index.type === 'UNIQUE') {
          sql += `ALTER TABLE \`${tableName}\` ADD UNIQUE KEY \`${indexName}\` (${index.columns});\n`;
        } else {
          sql += `ALTER TABLE \`${tableName}\` ADD KEY \`${indexName}\` (${index.columns});\n`;
        }
      }
    }
    
    sql += '\n';
    return sql;
  }
} 