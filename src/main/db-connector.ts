import mysql from 'mysql2/promise';
import { Tables } from './types';

export class DBConnector {
  private connection: mysql.Connection | null = null;

  async connect(config: any): Promise<void> {
    try {
      this.connection = await mysql.createConnection({
        host: config.host,
        port: config.port || 3306,
        user: config.username || config.user,
        password: config.password,
        database: config.database,
        charset: 'utf8mb4'
      });
    } catch (error) {
      throw new Error(`连接数据库失败: ${error}`);
    }
  }

  async close(): Promise<void> {
    if (this.connection) {
      await this.connection.end();
      this.connection = null;
    }
  }

  async getTableStructure(): Promise<Tables> {
    if (!this.connection) {
      throw new Error('数据库未连接');
    }

    const tables: Tables = {};

    try {
      // 获取所有表名
      const [tableRows] = await this.connection.execute(
        "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = ?",
        [this.connection.config.database]
      ) as any[];

      for (const tableRow of tableRows) {
        const tableName = tableRow.TABLE_NAME;
        const tableStructure = await this.getTableStructureByName(tableName);
        tables[tableName] = tableStructure;
      }
    } catch (error) {
      throw new Error(`获取表结构失败: ${error}`);
    }

    return tables;
  }

  private async getTableStructureByName(tableName: string): Promise<any> {
    if (!this.connection) {
      throw new Error('数据库未连接');
    }

    const columns: { [key: string]: any } = {};
    const indexes: { [key: string]: any } = {};

    try {
      // 获取列信息
      const [columnRows] = await this.connection.execute(`
        SELECT 
          COLUMN_NAME,
          DATA_TYPE,
          CHARACTER_MAXIMUM_LENGTH,
          IS_NULLABLE,
          COLUMN_DEFAULT,
          COLUMN_COMMENT
        FROM INFORMATION_SCHEMA.COLUMNS 
        WHERE TABLE_SCHEMA = ? AND TABLE_NAME = ?
        ORDER BY ORDINAL_POSITION
      `, [this.connection.config.database, tableName]) as any[];

      for (const columnRow of columnRows) {
        const columnName = columnRow.COLUMN_NAME;
        const dataType = columnRow.DATA_TYPE;
        const maxLength = columnRow.CHARACTER_MAXIMUM_LENGTH;
        const isNullable = columnRow.IS_NULLABLE === 'YES';
        const defaultValue = columnRow.COLUMN_DEFAULT;
        const comment = columnRow.COLUMN_COMMENT;

        let typeDef = dataType;
        if (maxLength) {
          typeDef += `(${maxLength})`;
        }

        let rawDef = `\`${columnName}\` ${typeDef}`;
        if (!isNullable) {
          rawDef += ' NOT NULL';
        }
        if (defaultValue !== null) {
          rawDef += ` DEFAULT ${defaultValue}`;
        }
        if (comment) {
          rawDef += ` COMMENT '${comment}'`;
        }

        columns[columnName] = {
          raw: rawDef,
          type: dataType,
          length: maxLength ? maxLength.toString() : undefined,
          nullable: isNullable,
          default: defaultValue !== null ? `DEFAULT ${defaultValue}` : undefined,
          comment: comment ? `COMMENT '${comment}'` : undefined
        };
      }

      // 获取索引信息
      const [indexRows] = await this.connection.execute(`
        SELECT 
          INDEX_NAME,
          NON_UNIQUE,
          GROUP_CONCAT(COLUMN_NAME ORDER BY SEQ_IN_INDEX) as COLUMNS
        FROM INFORMATION_SCHEMA.STATISTICS 
        WHERE TABLE_SCHEMA = ? AND TABLE_NAME = ?
        GROUP BY INDEX_NAME, NON_UNIQUE
        ORDER BY INDEX_NAME
      `, [this.connection.config.database, tableName]) as any[];

      for (const indexRow of indexRows) {
        const indexName = indexRow.INDEX_NAME;
        const isUnique = !indexRow.NON_UNIQUE;
        const indexColumns = indexRow.COLUMNS;

        // 跳过主键
        if (indexName === 'PRIMARY') {
          continue;
        }

        indexes[indexName] = {
          type: isUnique ? 'UNIQUE' : 'INDEX',
          columns: indexColumns,
          unique: isUnique
        };
      }
    } catch (error) {
      throw new Error(`获取表 ${tableName} 结构失败: ${error}`);
    }

    return { columns, indexes };
  }
} 