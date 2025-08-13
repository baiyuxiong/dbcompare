import React from 'react';
import { Modal, Button, message } from 'antd';
import { CopyOutlined } from '@ant-design/icons';

interface SQLModalProps {
  visible: boolean;
  sql: string;
  onCancel: () => void;
}

const SQLModal: React.FC<SQLModalProps> = ({
  visible,
  sql,
  onCancel
}) => {
  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(sql);
      message.success('SQL已复制到剪贴板');
    } catch (error) {
      message.error('复制失败');
    }
  };

  return (
    <Modal
      title="同步SQL"
      open={visible}
      onCancel={onCancel}
      width={800}
      className="sql-modal"
      footer={[
        <Button key="copy" icon={<CopyOutlined />} onClick={handleCopy}>
          复制SQL
        </Button>,
        <Button key="close" onClick={onCancel}>
          关闭
        </Button>
      ]}
    >
      <div className="sql-content">
        {sql || '暂无SQL内容'}
      </div>
    </Modal>
  );
};

export default SQLModal; 