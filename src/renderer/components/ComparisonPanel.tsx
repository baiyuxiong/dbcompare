import React, { useState } from 'react';
import { Card, Table, Checkbox, Space, Tag } from 'antd';
import { Tables } from '../types';

interface ComparisonPanelProps {
  leftTables: Tables;
  rightTables: Tables;
}

const ComparisonPanel: React.FC<ComparisonPanelProps> = ({
  leftTables,
  rightTables
}) => {
  const [hideSame, setHideSame] = useState(false);
  const [showMissingOnly, setShowMissingOnly] = useState(false);
  const [syncScroll, setSyncScroll] = useState(true);

  const renderTableData = (tables: Tables, side: 'left' | 'right') => {
    const data: any[] = [];
    const allTableNames = Object.keys(tables).sort();

    allTableNames.forEach((tableName, tableIndex) => {
      const table = tables[tableName];
      const columnCount = Object.keys(table.columns).length;
      const indexCount = Object.keys(table.indexes).length;

      // 添加表头行
      data.push({
        key: `table-${tableName}`,
        type: 'table',
        name: tableName,
        info: `字段数: ${columnCount} 索引数: ${indexCount}`,
        isHeader: true
      });

      // 添加字段
      if (Object.keys(table.columns).length > 0) {
        data.push({
          key: `header-${tableName}-columns`,
          type: 'header',
          name: '字段',
          info: '',
          isHeader: true
        });

        Object.entries(table.columns).forEach(([columnName, column], colIndex) => {
          data.push({
            key: `${tableName}-${columnName}`,
            type: 'column',
            name: columnName,
            info: column.raw,
            tableName,
            columnName
          });
        });
      }

      // 添加索引
      if (Object.keys(table.indexes).length > 0) {
        data.push({
          key: `header-${tableName}-indexes`,
          type: 'header',
          name: '索引',
          info: '',
          isHeader: true
        });

        Object.entries(table.indexes).forEach(([indexName, index]) => {
          data.push({
            key: `${tableName}-index-${indexName}`,
            type: 'index',
            name: indexName,
            info: `${index.type} (${index.columns})`,
            tableName,
            indexName
          });
        });
      }

      // 添加空行
      data.push({
        key: `empty-${tableName}`,
        type: 'empty',
        name: '',
        info: ''
      });
    });

    return data;
  };

  const columns = [
    {
      title: '序号',
      dataIndex: 'index',
      key: 'index',
      width: 80,
      render: (_: any, record: any, index: number) => {
        if (record.type === 'table' || record.type === 'header') {
          return '';
        }
        return index + 1;
      }
    },
    {
      title: '名称',
      dataIndex: 'name',
      key: 'name',
      width: 200,
      render: (text: string, record: any) => {
        if (record.isHeader) {
          return <strong style={{ color: '#1890ff' }}>{text}</strong>;
        }
        return text;
      }
    },
    {
      title: '定义',
      dataIndex: 'info',
      key: 'info',
      render: (text: string, record: any) => {
        if (record.type === 'table') {
          return <span style={{ color: '#666' }}>{text}</span>;
        }
        if (record.type === 'header') {
          return <span style={{ color: '#999' }}>{text}</span>;
        }
        return <code style={{ fontSize: '12px' }}>{text}</code>;
      }
    }
  ];

  const leftData = renderTableData(leftTables, 'left');
  const rightData = renderTableData(rightTables, 'right');

  return (
    <div className="comparison-area">
      <div className="left-panel">
        <div className="panel-header">
          左侧数据源
          <Space style={{ float: 'right' }}>
            <Checkbox 
              checked={syncScroll} 
              onChange={(e) => setSyncScroll(e.target.checked)}
            >
              同步滚动
            </Checkbox>
            <Checkbox 
              checked={hideSame} 
              onChange={(e) => setHideSame(e.target.checked)}
            >
              隐藏相同
            </Checkbox>
            <Checkbox 
              checked={showMissingOnly} 
              onChange={(e) => setShowMissingOnly(e.target.checked)}
            >
              仅显示缺失
            </Checkbox>
          </Space>
        </div>
        <div className="panel-content">
          <div className="table-container">
            <Table
              columns={columns}
              dataSource={leftData}
              pagination={false}
              size="small"
              scroll={{ y: 400 }}
              rowClassName={(record) => {
                if (record.isHeader) return 'table-header';
                return 'table-row';
              }}
            />
          </div>
        </div>
      </div>

      <div className="right-panel">
        <div className="panel-header">
          右侧数据源
        </div>
        <div className="panel-content">
          <div className="table-container">
            <Table
              columns={columns}
              dataSource={rightData}
              pagination={false}
              size="small"
              scroll={{ y: 400 }}
              rowClassName={(record) => {
                if (record.isHeader) return 'table-header';
                return 'table-row';
              }}
            />
          </div>
        </div>
      </div>
    </div>
  );
};

export default ComparisonPanel; 