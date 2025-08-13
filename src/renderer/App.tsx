import React, { useState, useEffect } from 'react';
import { Layout, Button, message, Spin } from 'antd';
import { DatabaseOutlined, FileTextOutlined, CompareOutlined, CodeOutlined } from '@ant-design/icons';
import DataSourcePanel from './components/DataSourcePanel';
import ComparisonPanel from './components/ComparisonPanel';
import ConnectionDialog from './components/ConnectionDialog';
import SQLModal from './components/SQLModal';
import { useDatabaseAPI } from './hooks/useDatabaseAPI';
import { Tables, Connection, History } from './types';

const { Header, Content } = Layout;

const App: React.FC = () => {
  const [leftTables, setLeftTables] = useState<Tables>({});
  const [rightTables, setRightTables] = useState<Tables>({});
  const [leftHistory, setLeftHistory] = useState<History | null>(null);
  const [rightHistory, setRightHistory] = useState<History | null>(null);
  const [connectionDialogVisible, setConnectionDialogVisible] = useState(false);
  const [sqlModalVisible, setSqlModalVisible] = useState(false);
  const [syncSQL, setSyncSQL] = useState('');
  const [loading, setLoading] = useState(false);

  const { 
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
    selectFile
  } = useDatabaseAPI();

  const handleSelectFile = async (side: 'left' | 'right') => {
    try {
      const filePath = await selectFile();
      if (!filePath) return;

      setLoading(true);
      const tables = await parseSqlFile(filePath);
      
      // 添加到历史记录
      const history: History = {
        side,
        type: 'file',
        value: filePath,
        display: filePath,
        lastUsed: new Date().toISOString()
      };
      await addHistory(history);

      // 更新状态
      if (side === 'left') {
        setLeftTables(tables);
        setLeftHistory(history);
      } else {
        setRightTables(tables);
        setRightHistory(history);
      }

      message.success(`${side === 'left' ? '左侧' : '右侧'}文件加载成功`);
    } catch (error) {
      message.error(`加载文件失败: ${error}`);
    } finally {
      setLoading(false);
    }
  };

  const handleSelectConnection = async (side: 'left' | 'right', connection: Connection) => {
    try {
      setLoading(true);
      const tables = await getTableStructure(connection);
      
      // 添加到历史记录
      const display = connection.type === 'mysql' 
        ? `${connection.name} (${connection.config.host}:${connection.config.port})`
        : `${connection.name} (${connection.config.url})`;
      
      const history: History = {
        side,
        type: 'connection',
        value: connection.id?.toString() || '',
        display,
        lastUsed: new Date().toISOString()
      };
      await addHistory(history);

      // 更新状态
      if (side === 'left') {
        setLeftTables(tables);
        setLeftHistory(history);
      } else {
        setRightTables(tables);
        setRightHistory(history);
      }

      message.success(`${side === 'left' ? '左侧' : '右侧'}数据库连接成功`);
    } catch (error) {
      message.error(`连接数据库失败: ${error}`);
    } finally {
      setLoading(false);
    }
  };

  const handleCompare = async () => {
    if (!leftHistory || !rightHistory) {
      message.warning('请先选择两个数据源');
      return;
    }

    try {
      setLoading(true);
      const differences = await compareTables(leftTables, rightTables);
      
      // 这里可以显示比较结果
      const addedTables = differences.addedTables.length;
      const removedTables = differences.removedTables.length;
      const modifiedTables = Object.keys(differences.modifiedTables).length;
      
      message.success(`比较完成: 新增${addedTables}个表, 删除${removedTables}个表, 修改${modifiedTables}个表`);
    } catch (error) {
      message.error(`比较失败: ${error}`);
    } finally {
      setLoading(false);
    }
  };

  const handleGenerateSQL = async () => {
    if (!leftHistory || !rightHistory) {
      message.warning('请先选择两个数据源');
      return;
    }

    try {
      setLoading(true);
      const sql = await generateSyncSQL(leftTables, rightTables);
      setSyncSQL(sql);
      setSqlModalVisible(true);
    } catch (error) {
      message.error(`生成SQL失败: ${error}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Layout>
      <Header>
        <div className="logo">
          <DatabaseOutlined style={{ marginRight: 8 }} />
          DBCompare - MySQL表结构比较工具
        </div>
        <div className="header-actions">
          <Button 
            type="primary" 
            icon={<CompareOutlined />}
            onClick={handleCompare}
            disabled={!leftHistory || !rightHistory}
          >
            开始比较
          </Button>
          <Button 
            type="primary" 
            icon={<CodeOutlined />}
            onClick={handleGenerateSQL}
            disabled={!leftHistory || !rightHistory}
          >
            生成同步SQL
          </Button>
        </div>
      </Header>
      
      <Content className="content-area">
        <Spin spinning={loading} tip="处理中...">
          <DataSourcePanel
            leftHistory={leftHistory}
            rightHistory={rightHistory}
            onSelectFile={handleSelectFile}
            onSelectConnection={handleSelectConnection}
            onManageConnections={() => setConnectionDialogVisible(true)}
          />
          
          <ComparisonPanel
            leftTables={leftTables}
            rightTables={rightTables}
          />
        </Spin>
      </Content>

      <ConnectionDialog
        visible={connectionDialogVisible}
        onCancel={() => setConnectionDialogVisible(false)}
        onSelect={(connection) => {
          setConnectionDialogVisible(false);
          // 这里可以处理连接选择
        }}
        getConnections={getConnections}
        addConnection={addConnection}
        updateConnection={updateConnection}
        deleteConnection={deleteConnection}
      />

      <SQLModal
        visible={sqlModalVisible}
        sql={syncSQL}
        onCancel={() => setSqlModalVisible(false)}
      />
    </Layout>
  );
};

export default App; 