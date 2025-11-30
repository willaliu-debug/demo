# 📊 返点指标分析系统 (Web版)

一个功能完整的Web应用，用于上传、处理和分析Excel数据，支持在线查看报告和运管监控。

## ✨ 功能特性

### 🌐 Web界面
- **文件上传**: 支持拖拽上传Excel文件 (.xlsx, .xls)
- **实时处理**: 自动处理Excel数据并生成分析报告
- **在线预览**: 数据按行展示，支持查看前10行
- **一键下载**: 处理完成后可直接下载结果文件

### 📈 数据分析
- 分析四个核心指标的变化趋势：
  - 合住率
  - 返点率
  - 预算使用率
  - 入住均价
- 自动计算统计信息和平均值
- 生成详细的数据分析报告

### 🔧 运管监控
- **实时监控**: 系统处理状态实时更新
- **统计展示**: 总处理次数、成功率、失败率
- **历史记录**: 所有处理历史按时间排序
- **自动刷新**: 每30秒自动更新数据

## 🚀 快速开始

### 方式1: Docker 部署 (推荐)

```bash
# 1. 克隆项目
git clone https://github.com/willaliu-debug/demo.git
cd demo

# 2. 使用 Docker Compose 启动
docker-compose up -d

# 3. 访问Web应用
# 主页: http://localhost:5000
# 运管监控: http://localhost:5000/admin

# 4. 查看日志
docker-compose logs -f

# 5. 停止服务
docker-compose down
```

### 方式2: 本地环境

```bash
# 1. 克隆项目
git clone https://github.com/willaliu-debug/demo.git
cd demo

# 2. 创建虚拟环境
python3 -m venv venv
source venv/bin/activate  # macOS/Linux

# 3. 安装依赖
pip install -r requirements.txt

# 4. 运行Web应用
python src/app.py

# 5. 访问Web应用
# 主页: http://localhost:5000
# 运管监控: http://localhost:5000/admin
```

## 📁 项目结构

```
.
├── src/
│   ├── app.py                        # Flask Web应用主程序
│   ├── generate_metrics_report.py   # 报告生成器 (命令行版本)
│   ├── templates/                    # HTML模板
│   │   ├── index.html               # 主页 - 文件上传和处理
│   │   └── admin.html               # 运管监控页面
│   └── static/                       # 静态资源 (CSS/JS)
├── requirements.txt                  # Python依赖
├── Dockerfile                        # Docker配置
├── docker-compose.yml               # Docker Compose配置
├── .env.example                     # 环境变量示例
└── README.md                        # 项目文档
```

## 🎯 使用指南

### 1. 上传Excel文件
- 访问 http://localhost:5000
- 点击上传区域或拖拽文件
- 支持 .xlsx 和 .xls 格式
- 最大文件大小: 16MB

### 2. 查看处理结果
- 自动显示处理统计信息
- 预览数据表格 (前10行)
- 查看计算的指标统计

### 3. 下载处理后的文件
- 点击"下载处理后的文件"按钮
- 文件包含处理结果和统计信息

### 4. 运管监控
- 访问 http://localhost:5000/admin
- 查看实时系统状态
- 查看处理历史记录
- 自动刷新数据 (30秒)

## 🔌 API 接口

### POST /upload
上传并处理Excel文件

**请求**:
- Content-Type: multipart/form-data
- file: Excel文件

**响应**:
```json
{
  "success": true,
  "message": "文件处理成功",
  "data": {
    "filename": "processed_20250101_120000_data.xlsx",
    "rows": 100,
    "columns": 8,
    "preview": [...],
    "stats": {...}
  }
}
```

### GET /download/<filename>
下载处理后的文件

### GET /history
获取处理历史记录

### GET /api/stats
获取系统统计信息

### GET /health
健康检查端点

## ⚙️ 配置说明

### 环境变量

复制 `.env.example` 为 `.env` 并修改配置：

```bash
# Flask配置
FLASK_ENV=production
FLASK_DEBUG=0

# 服务器配置
HOST=0.0.0.0
PORT=5000

# 文件上传配置
MAX_CONTENT_LENGTH=16777216  # 16MB
UPLOAD_FOLDER=/tmp/uploads
PROCESSED_FOLDER=/tmp/processed
```

### Docker配置

在 `docker-compose.yml` 中调整：
- 端口映射
- 资源限制
- 数据卷挂载

## 📊 输入数据格式

Excel文件应包含以下列（支持"基础数据"工作表）：

| 列名 | 说明 | 必需 |
|------|------|------|
| 月份 | 数据月份 | 是 |
| 总计算间夜 | 总间夜数 | 是 |
| 合住率 | 合住率百分比 | 否 |
| 返点率 | 返点率百分比 | 否 |
| 预算使用率 | 预算使用率百分比 | 否 |
| 入住均价 | 平均入住价格 | 否 |

## 🛡️ 安全特性

- 文件类型验证 (仅允许 .xlsx, .xls)
- 文件大小限制 (最大 16MB)
- 非root用户运行 (Docker)
- 临时文件自动清理
- CORS支持

## 📈 性能优化

- 使用 Werkzeug 安全文件名处理
- 异步文件处理
- 内存优化的数据处理
- Docker资源限制
- 健康检查机制

## 🐛 故障排查

### 问题1: 端口被占用

```bash
# 修改 docker-compose.yml 中的端口映射
ports:
  - "5001:5000"  # 改用5001端口
```

### 问题2: 文件上传失败

检查文件大小和格式，确保：
- 文件小于 16MB
- 文件格式为 .xlsx 或 .xls

### 问题3: 容器无法启动

```bash
# 查看详细日志
docker-compose logs -f

# 重新构建
docker-compose build --no-cache
docker-compose up -d
```

## 📝 开发

### 安装开发依赖

```bash
pip install -e ".[dev]"
```

### 本地开发

```bash
# 开启调试模式
export FLASK_ENV=development
export FLASK_DEBUG=1
python src/app.py
```

### 运行测试

```bash
pytest
```

## 📦 部署指南

详细的部署说明请查看 [DEPLOYMENT.md](DEPLOYMENT.md)

## 🤝 贡献

欢迎提交Issue和Pull Request！

## 📄 许可证

MIT License

## 👥 作者

返点指标分析系统开发团队

---

**🌟 功能亮点**
- ✅ 完整的Web界面
- ✅ 实时数据处理
- ✅ 运管监控仪表盘
- ✅ Docker容器化部署
- ✅ RESTful API支持
- ✅ 响应式设计
