# 返点指标分析报告生成器

一个用于分析返点指标变化趋势并生成报告的Python工具。

## 功能特性

- 分析四个核心指标的变化趋势：
  - 合住率
  - 返点率
  - 预算使用率
  - 入住均价
- 生成详细的Markdown格式分析报告
- 提供月度对比分析和关键建议

## 项目结构

```
.
├── src/                              # 源代码目录
│   └── generate_metrics_report.py   # 主程序
├── requirements.txt                  # 项目依赖
├── pyproject.toml                    # Python项目配置
├── .python-version                   # Python版本指定
├── .gitignore                        # Git忽略文件
└── README.md                         # 项目文档
```

## 环境要求

- Python >= 3.8
- 依赖包：
  - pandas >= 2.0.0
  - numpy >= 1.24.0
  - openpyxl >= 3.1.0

## 安装步骤

### 1. 克隆项目

```bash
cd /Users/anker/demo
```

### 2. 创建虚拟环境

```bash
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# 或
venv\Scripts\activate  # Windows
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

## 使用方法

### 运行报告生成器

```bash
python src/generate_metrics_report.py
```

### 自定义数据路径

编辑 [src/generate_metrics_report.py](src/generate_metrics_report.py) 中的路径：

```python
# 修改这两行以指定你的数据文件路径
data_file = "/path/to/your/指标计算结果.xlsx"
output_file = "/path/to/your/指标分析报告.md"
```

## 输入数据格式

程序需要一个Excel文件，包含名为"基础数据"的工作表，列包括：

- 月份
- 总计算间夜
- 总订单价
- 预算汇总
- 合住率
- 返点率
- 预算使用率
- 入住均价

## 输出报告

程序会生成一个Markdown格式的分析报告，包含：

1. 整体概览
2. 四个核心指标变化趋势分析
3. 月度对比分析表格
4. 基于数据的关键建议

## 开发

### 安装开发依赖

```bash
pip install -e ".[dev]"
```

### 运行测试

```bash
pytest
```

### 代码格式化

```bash
black src/
```

## 许可证

[根据需要添加许可证信息]

## 作者

[根据需要添加作者信息]

## 贡献

欢迎提交Issue和Pull Request！
