import React, { useState, useEffect } from 'react';
import { Card, Button, Select, Space, Divider, message } from 'antd';
import { DatabaseOutlined, FileTextOutlined, SettingOutlined } from '@ant-design/icons';
import { History, Connection } from '../types';
import { useDatabaseAPI } from '../hooks/useDatabaseAPI';

interface DataSourcePanelProps {
  leftHistory: History | null;
  rightHistory: History | null;
  onSelectFile: (side: 'left' | 'right') => void;
  onSelectConnection: (side: 'left' | 'right', connection: Connection) => void;
  onManageConnections: () => void;
}

const DataSourcePanel: React.FC<DataSourcePanelProps> = ({
  leftHistory,
  rightHistory,
  onSelectFile,
  onSelectConnection,
  onManageConnections
}) => {
  const [leftHistoryList, setLeftHistoryList] = useState<History[]>([]);
  const [rightHistoryList, setRightHistoryList] = useState<History[]>([]);
  const [connections, setConnections] = useState<Connection[]>([]);
  const [loading, setLoading] = useState(false);

  const { getHistory, getConnections } = useDatabaseAPI();

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);
      const [leftHist, rightHist, conns] = await Promise.all([
        getHistory('left'),
        getHistory('right'),
        getConnections()
      ]);
      setLeftHistoryList(leftHist);
      setRightHistoryList(rightHist);
      setConnections(conns);
    } catch (error) {
      message.error('加载数据失败');
    } finally {
      setLoading(false);
    }
  };

  const handleHistorySelect = (side: 'left' | 'right', value: string) => {
    const historyList = side === 'left' ? leftHistoryList : rightHistoryList;
    const history = historyList.find(h => h.display === value);
    
    if (history) {
      if (history.type === 'connection') {
        const connection = connections.find(c => c.id?.toString() === history.value);
        if (connection) {
          onSelectConnection(side, connection);
        }
      } else {
        // 文件类型的历史记录，重新加载文件
        onSelectFile(side);
      }
    }
  };

  const renderDataSourceSelector = (side: 'left' | 'right') => {
    const history = side === 'left' ? leftHistory : rightHistory;
    const historyList = side === 'left' ? leftHistoryList : rightHistoryList;
    const sideText = side === 'left' ? '左侧' : '右侧';

    return (
      <Card 
        title={`${sideText}数据源`} 
        size="small"
        extra={
          <Space>
            <Button 
              size="small" 
              icon={<FileTextOutlined />}
              onClick={() => onSelectFile(side)}
            >
              选择文件
            </Button>
            <Button 
              size="small" 
              icon={<DatabaseOutlined />}
              onClick={() => onSelectConnection(side, connections[0])}
              disabled={connections.length === 0}
            >
              选择连接
            </Button>
          </Space>
        }
      >
        <Space direction="vertical" style={{ width: '100%' }}>
          <Select
            placeholder={`选择${sideText}数据源`}
            value={history?.display || undefined}
            onChange={(value) => handleHistorySelect(side, value)}
            style={{ width: '100%' }}
            loading={loading}
          >
            {historyList.map((h) => (
              <Select.Option key={h.id} value={h.display}>
                <Space>
                  {h.type === 'file' ? <FileTextOutlined /> : <DatabaseOutlined />}
                  {h.display}
                </Space>
              </Select.Option>
            ))}
          </Select>
          
          {history && (
            <div style={{ fontSize: '12px', color: '#666' }}>
              类型: {history.type === 'file' ? 'SQL文件' : '数据库连接'}
              <br />
              最后使用: {new Date(history.lastUsed).toLocaleString()}
            </div>
          )}
        </Space>
      </Card>
    );
  };

  return (
    <div className="data-source-panel">
      <div className="data-source-header">
        <h3>数据源配置</h3>
        <Button 
          type="primary" 
          icon={<SettingOutlined />}
          onClick={onManageConnections}
        >
          连接管理
        </Button>
      </div>
      
      <div className="data-source-content">
        <div style={{ display: 'flex', gap: '16px' }}>
          {renderDataSourceSelector('left')}
          {renderDataSourceSelector('right')}
        </div>
      </div>
    </div>
  );
};

export default DataSourcePanel; 