# 安装说明

## 系统要求

- Node.js 18.0.0 或更高版本
- npm 8.0.0 或更高版本

## 安装步骤

### 1. 检查Node.js版本

```bash
node --version
npm --version
```

如果版本过低，请先升级Node.js。

### 2. 安装依赖

```bash
npm install
```

如果遇到网络问题，可以尝试使用国内镜像：

```bash
npm install --registry=https://registry.npmmirror.com
```

### 3. 启动开发服务器

```bash
npm run dev
```

这将同时启动：
- Vite开发服务器（渲染进程）
- Electron主进程

### 4. 构建生产版本

```bash
npm run build
```

### 5. 打包分发

```bash
# Windows
npm run dist:win

# macOS
npm run dist:mac

# Linux
npm run dist:linux
```

## 常见问题

### 1. Node.js版本过低

如果看到类似错误：
```
Unsupported engine: package: 'vite@5.4.19', required: { node: '^18.0.0 || >=20.0.0' }
```

请升级Node.js到18.0.0或更高版本。

### 2. 网络连接问题

如果安装依赖时遇到网络问题，可以：

1. 使用国内镜像：
```bash
npm config set registry https://registry.npmmirror.com
```

2. 或者使用yarn：
```bash
npm install -g yarn
yarn install
```

### 3. Electron下载失败

如果Electron下载失败，可以：

1. 设置Electron镜像：
```bash
npm config set ELECTRON_MIRROR https://npmmirror.com/mirrors/electron/
```

2. 或者使用cnpm：
```bash
npm install -g cnpm --registry=https://registry.npmmirror.com
cnpm install
```

## 项目结构

```
dbcompare/
├── src/
│   ├── main/                 # Electron主进程 (JavaScript)
│   │   ├── main.js          # 主进程入口
│   │   ├── preload.js       # 预加载脚本
│   │   ├── database-manager.js  # 数据库管理
│   │   ├── sql-parser.js    # SQL解析器
│   │   ├── sql-generator.js # SQL生成器
│   │   └── db-connector.js  # 数据库连接器
│   └── renderer/            # 渲染进程(React应用)
│       ├── main.tsx         # React入口
│       ├── App.tsx          # 主应用组件
│       ├── components/      # React组件
│       ├── hooks/           # 自定义Hooks
│       └── types.ts         # 类型定义
├── package.json
├── vite.config.ts
└── README.md
```

## 开发说明

- 主进程使用JavaScript编写，避免TypeScript编译问题
- 渲染进程使用React + TypeScript
- 数据存储使用文件系统（JSON文件）
- 支持MySQL数据库连接和SQL文件比较 