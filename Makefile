.PHONY: help install run clean test format

help:
	@echo "可用命令:"
	@echo "  make install  - 创建虚拟环境并安装依赖"
	@echo "  make run      - 运行报告生成器"
	@echo "  make clean    - 清理临时文件"
	@echo "  make test     - 运行测试"
	@echo "  make format   - 格式化代码"

install:
	python3 -m venv venv
	. venv/bin/activate && pip install --upgrade pip
	. venv/bin/activate && pip install -r requirements.txt

run:
	. venv/bin/activate && python src/generate_metrics_report.py

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.log" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf build/ dist/ .pytest_cache/ .coverage htmlcov/

test:
	. venv/bin/activate && pytest

format:
	. venv/bin/activate && black src/
