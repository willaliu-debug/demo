# 部署指南

## 🐳 Docker 部署

### 前提条件

- Docker >= 20.10
- Docker Compose >= 2.0 (可选)
- Git

### 快速部署

#### 方法1: 使用 Docker Compose (推荐)

```bash
# 1. 克隆仓库
git clone https://github.com/willaliu-debug/demo.git
cd demo

# 2. 准备数据文件
# 将Excel数据文件放到 ./data 目录

# 3. 构建并启动
docker-compose up -d

# 4. 查看日志
docker-compose logs -f

# 5. 停止服务
docker-compose down
```

#### 方法2: 直接使用 Docker

```bash
# 1. 构建镜像
docker build -t metrics-report-generator:latest .

# 2. 运行容器
docker run -d \
  --name metrics-report \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/output:/app/output \
  -e TZ=Asia/Shanghai \
  metrics-report-generator:latest

# 3. 查看日志
docker logs -f metrics-report

# 4. 停止容器
docker stop metrics-report
docker rm metrics-report
```

### 配置说明

#### 环境变量

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| `TZ` | 时区设置 | `Asia/Shanghai` |
| `PYTHONUNBUFFERED` | Python输出缓冲 | `1` |

#### 数据卷挂载

| 容器路径 | 主机路径 | 说明 |
|----------|----------|------|
| `/app/data` | `./data` | 输入数据文件目录 |
| `/app/output` | `./output` | 输出报告目录 |

### 健康检查

容器内置健康检查，每30秒检查一次Python环境状态：

```bash
docker ps  # 查看HEALTH状态
```

### 资源限制

默认配置：
- CPU限制: 1核
- 内存限制: 1GB
- CPU预留: 0.5核
- 内存预留: 512MB

可在 [docker-compose.yml](docker-compose.yml) 中调整。

## 📦 生产环境部署建议

### 1. 使用特定版本标签

```bash
docker build -t metrics-report-generator:1.0.0 .
docker tag metrics-report-generator:1.0.0 your-registry.com/metrics-report-generator:1.0.0
docker push your-registry.com/metrics-report-generator:1.0.0
```

### 2. 配置持久化存储

```yaml
volumes:
  - /path/to/persistent/data:/app/data
  - /path/to/persistent/output:/app/output
```

### 3. 配置日志收集

```yaml
logging:
  driver: "json-file"
  options:
    max-size: "100m"
    max-file: "5"
```

### 4. 使用secrets管理敏感信息

```yaml
secrets:
  - source: db_password
    target: /run/secrets/db_password
```

## 🔧 故障排查

### 问题1: NullPointerException

**原因**: 缺少Dockerfile配置文件

**解决**: 确保仓库根目录包含 `Dockerfile`

### 问题2: 容器启动失败

```bash
# 查看详细日志
docker logs metrics-report

# 进入容器调试
docker exec -it metrics-report /bin/bash
```

### 问题3: 数据文件找不到

**解决**: 检查数据卷挂载路径和文件权限

```bash
# 检查挂载
docker inspect metrics-report | grep -A 10 Mounts

# 修改文件权限
chmod 644 data/*.xlsx
```

### 问题4: 内存不足

**解决**: 增加内存限制

```yaml
deploy:
  resources:
    limits:
      memory: 2G
```

## 🚀 CI/CD 集成

### GitHub Actions 示例

```yaml
name: Build and Deploy

on:
  push:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Build Docker image
        run: docker build -t metrics-report:${{ github.sha }} .

      - name: Push to registry
        run: |
          echo ${{ secrets.DOCKER_PASSWORD }} | docker login -u ${{ secrets.DOCKER_USERNAME }} --password-stdin
          docker push metrics-report:${{ github.sha }}
```

## 📊 监控

### 查看容器状态

```bash
docker stats metrics-report
```

### 导出容器日志

```bash
docker logs metrics-report > app.log 2>&1
```

## 🔄 更新部署

```bash
# 1. 拉取最新代码
git pull origin main

# 2. 重新构建
docker-compose build

# 3. 重启服务
docker-compose up -d

# 4. 清理旧镜像
docker image prune -f
```

## 📞 支持

如有问题，请提交 [Issue](https://github.com/willaliu-debug/demo/issues)
