#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
返点指标分析Web应用
提供Excel上传、处理和下载功能
"""

from flask import Flask, render_template, request, send_file, jsonify
from werkzeug.utils import secure_filename
import pandas as pd
import os
from datetime import datetime
import traceback
from pathlib import Path

app = Flask(__name__)

# 配置
UPLOAD_FOLDER = '/tmp/uploads'
PROCESSED_FOLDER = '/tmp/processed'
ALLOWED_EXTENSIONS = {'xlsx', 'xls'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PROCESSED_FOLDER'] = PROCESSED_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

# 确保目录存在
Path(UPLOAD_FOLDER).mkdir(parents=True, exist_ok=True)
Path(PROCESSED_FOLDER).mkdir(parents=True, exist_ok=True)

# 存储处理记录
processing_history = []


def allowed_file(filename):
    """检查文件类型是否允许"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def process_excel(input_path, output_path):
    """
    处理Excel文件的核心逻辑
    这里可以根据需求自定义处理逻辑
    """
    # 读取Excel文件
    df = pd.read_excel(input_path, sheet_name='基础数据' if 'Sheet1' not in pd.ExcelFile(input_path).sheet_names else None)

    # 示例处理：添加处理时间戳列
    df['处理时间'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # 如果存在指标数据，进行分析
    if '合住率' in df.columns:
        # 计算统计信息
        stats = {
            '合住率平均值': df['合住率'].mean() if '合住率' in df.columns else 0,
            '返点率平均值': df['返点率'].mean() if '返点率' in df.columns else 0,
            '预算使用率平均值': df['预算使用率'].mean() if '预算使用率' in df.columns else 0,
            '入住均价平均值': df['入住均价'].mean() if '入住均价' in df.columns else 0,
        }
    else:
        stats = {}

    # 保存处理后的文件
    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='处理结果', index=False)

        # 如果有统计信息，添加到新sheet
        if stats:
            stats_df = pd.DataFrame([stats])
            stats_df.to_excel(writer, sheet_name='统计信息', index=False)

    return df, stats


@app.route('/')
def index():
    """主页"""
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    """处理文件上传"""
    try:
        # 检查是否有文件
        if 'file' not in request.files:
            return jsonify({'error': '没有选择文件'}), 400

        file = request.files['file']

        if file.filename == '':
            return jsonify({'error': '没有选择文件'}), 400

        if not allowed_file(file.filename):
            return jsonify({'error': '只支持 .xlsx 和 .xls 文件'}), 400

        # 保存上传的文件
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        upload_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{timestamp}_{filename}")
        file.save(upload_path)

        # 处理文件
        output_filename = f"processed_{timestamp}_{filename}"
        output_path = os.path.join(app.config['PROCESSED_FOLDER'], output_filename)

        df, stats = process_excel(upload_path, output_path)

        # 记录处理历史
        record = {
            'id': len(processing_history) + 1,
            'original_filename': filename,
            'processed_filename': output_filename,
            'upload_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'rows': len(df),
            'columns': len(df.columns),
            'stats': stats,
            'status': 'success'
        }
        processing_history.append(record)

        # 返回处理结果
        return jsonify({
            'success': True,
            'message': '文件处理成功',
            'data': {
                'filename': output_filename,
                'rows': len(df),
                'columns': len(df.columns),
                'preview': df.head(10).to_dict('records'),
                'column_names': df.columns.tolist(),
                'stats': stats
            }
        })

    except Exception as e:
        error_msg = str(e)
        traceback.print_exc()

        # 记录失败
        record = {
            'id': len(processing_history) + 1,
            'original_filename': file.filename if 'file' in locals() else 'unknown',
            'upload_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'status': 'failed',
            'error': error_msg
        }
        processing_history.append(record)

        return jsonify({'error': f'处理文件时出错: {error_msg}'}), 500


@app.route('/download/<filename>')
def download_file(filename):
    """下载处理后的文件"""
    try:
        file_path = os.path.join(app.config['PROCESSED_FOLDER'], filename)

        if not os.path.exists(file_path):
            return jsonify({'error': '文件不存在'}), 404

        return send_file(
            file_path,
            as_attachment=True,
            download_name=filename,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
    except Exception as e:
        return jsonify({'error': f'下载文件时出错: {str(e)}'}), 500


@app.route('/history')
def get_history():
    """获取处理历史记录"""
    return jsonify({
        'success': True,
        'data': processing_history[::-1]  # 倒序显示，最新的在前
    })


@app.route('/admin')
def admin():
    """运管监控页面"""
    return render_template('admin.html')


@app.route('/api/stats')
def get_stats():
    """获取系统统计信息"""
    success_count = sum(1 for r in processing_history if r.get('status') == 'success')
    failed_count = sum(1 for r in processing_history if r.get('status') == 'failed')

    return jsonify({
        'success': True,
        'data': {
            'total_processed': len(processing_history),
            'success_count': success_count,
            'failed_count': failed_count,
            'success_rate': f"{(success_count / len(processing_history) * 100):.2f}%" if processing_history else "0%",
            'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    })


@app.route('/health')
def health_check():
    """健康检查端点"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat()
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
