# 🚀 快速启动指南

## 1分钟快速启动Web应用

### 🐳 使用Docker（推荐）

```bash
# 1. 启动服务
docker-compose up -d

# 2. 打开浏览器
# 主页: http://localhost:5000
# 运管监控: http://localhost:5000/admin

# 3. 停止服务
docker-compose down
```

### 💻 本地运行

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 启动应用
python src/app.py

# 3. 打开浏览器
# 主页: http://localhost:5000
# 运管监控: http://localhost:5000/admin
```

## 📤 使用流程

### 步骤1: 上传Excel文件
1. 访问主页 http://localhost:5000
2. 点击上传区域或拖拽Excel文件
3. 支持 .xlsx 和 .xls 格式

### 步骤2: 查看处理结果
- 系统自动处理文件
- 显示统计信息卡片
- 预览数据表格（前10行）

### 步骤3: 下载处理后的文件
- 点击"下载处理后的文件"按钮
- 文件自动下载到本地

### 步骤4: 查看运管监控
- 访问 http://localhost:5000/admin
- 查看处理统计和历史记录
- 数据每30秒自动刷新

## 📊 界面预览

### 主页功能
- 📤 拖拽上传Excel
- 📊 实时数据统计
- 📋 数据表格预览
- ⬇️ 一键下载结果

### 运管监控
- 📈 总处理次数
- ✅ 成功率统计
- ❌ 失败次数
- ⏰ 实时时间
- 📜 历史记录

## 🔧 故障排查

### 端口被占用
```bash
# 修改端口为5001
# 编辑 docker-compose.yml:
ports:
  - "5001:5000"
```

### 依赖安装失败
```bash
# 升级pip
pip install --upgrade pip

# 重新安装依赖
pip install -r requirements.txt
```

### Docker构建失败
```bash
# 清理并重新构建
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

## 📞 获取帮助

- 查看完整文档: [README.md](README.md)
- 部署指南: [DEPLOYMENT.md](DEPLOYMENT.md)
- 提交Issue: https://github.com/willaliu-debug/demo/issues

---

**🎉 现在开始使用吧！**

访问 http://localhost:5000 开始体验
