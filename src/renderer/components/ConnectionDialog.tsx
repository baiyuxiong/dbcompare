import React, { useState, useEffect } from 'react';
import { Modal, Form, Input, Select, Button, Table, Space, message, Popconfirm } from 'antd';
import { PlusOutlined, EditOutlined, DeleteOutlined } from '@ant-design/icons';
import { Connection } from '../types';

interface ConnectionDialogProps {
  visible: boolean;
  onCancel: () => void;
  onSelect: (connection: Connection) => void;
  getConnections: () => Promise<Connection[]>;
  addConnection: (connection: Connection) => Promise<number>;
  updateConnection: (connection: Connection) => Promise<void>;
  deleteConnection: (id: number) => Promise<void>;
}

const ConnectionDialog: React.FC<ConnectionDialogProps> = ({
  visible,
  onCancel,
  onSelect,
  getConnections,
  addConnection,
  updateConnection,
  deleteConnection
}) => {
  const [connections, setConnections] = useState<Connection[]>([]);
  const [form] = Form.useForm();
  const [editingId, setEditingId] = useState<number | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (visible) {
      loadConnections();
    }
  }, [visible]);

  const loadConnections = async () => {
    try {
      setLoading(true);
      const data = await getConnections();
      setConnections(data);
    } catch (error) {
      message.error('加载连接失败');
    } finally {
      setLoading(false);
    }
  };

  const handleAdd = () => {
    setEditingId(null);
    form.resetFields();
  };

  const handleEdit = (record: Connection) => {
    setEditingId(record.id || null);
    form.setFieldsValue({
      name: record.name,
      type: record.type,
      host: record.config.host,
      port: record.config.port,
      username: record.config.username,
      password: record.config.password,
      database: record.config.database
    });
  };

  const handleDelete = async (id: number) => {
    try {
      await deleteConnection(id);
      message.success('删除成功');
      loadConnections();
    } catch (error) {
      message.error('删除失败');
    }
  };

  const handleSubmit = async (values: any) => {
    try {
      const connection: Connection = {
        id: editingId || undefined,
        name: values.name,
        type: values.type,
        config: {
          host: values.host,
          port: values.port,
          username: values.username,
          password: values.password,
          database: values.database
        },
        lastUsed: new Date().toISOString(),
        createdAt: editingId ? connections.find(c => c.id === editingId)?.createdAt || new Date().toISOString() : new Date().toISOString()
      };

      if (editingId) {
        await updateConnection(connection);
        message.success('更新成功');
      } else {
        await addConnection(connection);
        message.success('添加成功');
      }

      form.resetFields();
      setEditingId(null);
      loadConnections();
    } catch (error) {
      message.error('操作失败');
    }
  };

  const columns = [
    {
      title: '名称',
      dataIndex: 'name',
      key: 'name',
    },
    {
      title: '类型',
      dataIndex: 'type',
      key: 'type',
      render: (type: string) => type === 'mysql' ? 'MySQL' : 'Agent'
    },
    {
      title: '主机',
      dataIndex: ['config', 'host'],
      key: 'host',
    },
    {
      title: '端口',
      dataIndex: ['config', 'port'],
      key: 'port',
    },
    {
      title: '数据库',
      dataIndex: ['config', 'database'],
      key: 'database',
    },
    {
      title: '操作',
      key: 'action',
      render: (_, record: Connection) => (
        <Space>
          <Button 
            type="link" 
            icon={<EditOutlined />}
            onClick={() => handleEdit(record)}
          >
            编辑
          </Button>
          <Popconfirm
            title="确定要删除这个连接吗？"
            onConfirm={() => handleDelete(record.id!)}
          >
            <Button 
              type="link" 
              danger 
              icon={<DeleteOutlined />}
            >
              删除
            </Button>
          </Popconfirm>
        </Space>
      ),
    },
  ];

  return (
    <Modal
      title="连接管理"
      open={visible}
      onCancel={onCancel}
      footer={null}
      width={800}
    >
      <div style={{ marginBottom: 16 }}>
        <Button 
          type="primary" 
          icon={<PlusOutlined />}
          onClick={handleAdd}
        >
          添加连接
        </Button>
      </div>

      <Form
        form={form}
        layout="vertical"
        onFinish={handleSubmit}
        style={{ marginBottom: 16, padding: 16, background: '#f5f5f5', borderRadius: 6 }}
      >
        <Form.Item label="连接名称" name="name" rules={[{ required: true }]}>
          <Input placeholder="请输入连接名称" />
        </Form.Item>

        <Form.Item label="连接类型" name="type" rules={[{ required: true }]}>
          <Select>
            <Select.Option value="mysql">MySQL</Select.Option>
            <Select.Option value="agent">Agent</Select.Option>
          </Select>
        </Form.Item>

        <Form.Item label="主机" name="host" rules={[{ required: true }]}>
          <Input placeholder="localhost" />
        </Form.Item>

        <Form.Item label="端口" name="port" rules={[{ required: true }]}>
          <Input placeholder="3306" />
        </Form.Item>

        <Form.Item label="用户名" name="username" rules={[{ required: true }]}>
          <Input placeholder="请输入用户名" />
        </Form.Item>

        <Form.Item label="密码" name="password" rules={[{ required: true }]}>
          <Input.Password placeholder="请输入密码" />
        </Form.Item>

        <Form.Item label="数据库" name="database" rules={[{ required: true }]}>
          <Input placeholder="请输入数据库名" />
        </Form.Item>

        <Form.Item>
          <Space>
            <Button type="primary" htmlType="submit">
              {editingId ? '更新' : '添加'}
            </Button>
            <Button onClick={() => { form.resetFields(); setEditingId(null); }}>
              取消
            </Button>
          </Space>
        </Form.Item>
      </Form>

      <Table
        columns={columns}
        dataSource={connections}
        loading={loading}
        rowKey="id"
        pagination={false}
        size="small"
      />
    </Modal>
  );
};

export default ConnectionDialog; 