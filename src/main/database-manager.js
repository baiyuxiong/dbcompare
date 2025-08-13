const path = require('path');
const fs = require('fs');

class DatabaseManager {
  constructor() {
    // 确保数据目录存在
    this.dataPath = path.join(process.env.APPDATA || process.env.HOME || '', '.dbcompare');
    if (!fs.existsSync(this.dataPath)) {
      fs.mkdirSync(this.dataPath, { recursive: true });
    }
    
    this.connectionsFile = path.join(this.dataPath, 'connections.json');
    this.historyFile = path.join(this.dataPath, 'history.json');
    this.initFiles();
  }

  initFiles() {
    // 初始化连接文件
    if (!fs.existsSync(this.connectionsFile)) {
      fs.writeFileSync(this.connectionsFile, JSON.stringify([], null, 2));
    }

    // 初始化历史文件
    if (!fs.existsSync(this.historyFile)) {
      fs.writeFileSync(this.historyFile, JSON.stringify([], null, 2));
    }
  }

  readConnections() {
    try {
      const data = fs.readFileSync(this.connectionsFile, 'utf-8');
      return JSON.parse(data);
    } catch (error) {
      return [];
    }
  }

  writeConnections(connections) {
    fs.writeFileSync(this.connectionsFile, JSON.stringify(connections, null, 2));
  }

  readHistory() {
    try {
      const data = fs.readFileSync(this.historyFile, 'utf-8');
      return JSON.parse(data);
    } catch (error) {
      return [];
    }
  }

  writeHistory(history) {
    fs.writeFileSync(this.historyFile, JSON.stringify(history, null, 2));
  }

  async getConnections() {
    const connections = this.readConnections();
    return connections.sort((a, b) => new Date(b.lastUsed).getTime() - new Date(a.lastUsed).getTime());
  }

  async addConnection(connection) {
    const connections = this.readConnections();
    const newId = connections.length > 0 ? Math.max(...connections.map(c => c.id || 0)) + 1 : 1;
    connection.id = newId;
    connections.push(connection);
    this.writeConnections(connections);
    return newId;
  }

  async updateConnection(connection) {
    const connections = this.readConnections();
    const index = connections.findIndex(c => c.id === connection.id);
    if (index !== -1) {
      connections[index] = connection;
      this.writeConnections(connections);
    }
  }

  async deleteConnection(id) {
    const connections = this.readConnections();
    const filtered = connections.filter(c => c.id !== id);
    this.writeConnections(filtered);
    
    // 删除相关的历史记录
    const history = this.readHistory();
    const filteredHistory = history.filter(h => !(h.type === 'connection' && h.value === id.toString()));
    this.writeHistory(filteredHistory);
  }

  async getHistory(side, limit = 10) {
    const history = this.readHistory();
    const filtered = history
      .filter(h => h.side === side)
      .sort((a, b) => new Date(b.lastUsed).getTime() - new Date(a.lastUsed).getTime())
      .slice(0, limit);
    return filtered;
  }

  async addHistory(history) {
    const historyList = this.readHistory();
    const newId = historyList.length > 0 ? Math.max(...historyList.map(h => h.id || 0)) + 1 : 1;
    history.id = newId;
    historyList.push(history);
    this.writeHistory(historyList);
    return newId;
  }

  async updateHistoryLastUsed(id) {
    const history = this.readHistory();
    const index = history.findIndex(h => h.id === id);
    if (index !== -1) {
      history[index].lastUsed = new Date().toISOString();
      this.writeHistory(history);
    }
  }

  close() {
    // 文件系统存储不需要关闭连接
  }
}

module.exports = { DatabaseManager }; 