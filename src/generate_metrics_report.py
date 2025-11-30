#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
返点指标分析报告生成器
功能：分析四个核心指标的变化趋势并生成报告
"""

import pandas as pd
import numpy as np
from datetime import datetime
import os

def load_metrics_data(file_path):
    """加载指标计算结果"""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"找不到文件: {file_path}")

    df_basic = pd.read_excel(file_path, sheet_name='基础数据')
    return df_basic

def analyze_metric_trend(df, metric_name, is_percentage=False):
    """分析单个指标的变化趋势"""
    result = {
        'metric_name': metric_name,
        'is_percentage': is_percentage,
        'values': [],
        'trend': None,
        'avg': None,
        'max_month': None,
        'min_month': None,
        'change_rate': None
    }

    # 提取有效数据（非NaN且非0）
    valid_data = df[df[metric_name].notna() & (df[metric_name] != 0)]

    if len(valid_data) == 0:
        return result

    # 记录每月数据
    for _, row in valid_data.iterrows():
        result['values'].append({
            'month': row['月份'],
            'value': row[metric_name]
        })

    # 计算统计值
    values = valid_data[metric_name].values
    result['avg'] = round(np.mean(values), 2)
    result['max_month'] = valid_data.loc[valid_data[metric_name].idxmax(), '月份']
    result['min_month'] = valid_data.loc[valid_data[metric_name].idxmin(), '月份']

    # 计算变化趋势（如果有至少2个数据点）
    if len(values) >= 2:
        first_val = values[0]
        last_val = values[-1]
        change = last_val - first_val
        result['change_rate'] = round((change / first_val * 100), 2) if first_val != 0 else 0

        if change > 0:
            result['trend'] = '上升'
        elif change < 0:
            result['trend'] = '下降'
        else:
            result['trend'] = '持平'

    return result

def generate_markdown_report(df_basic, output_path=None):
    """生成Markdown格式的分析报告"""

    report_lines = []
    report_lines.append("# 返点指标分析报告")
    report_lines.append("")
    report_lines.append(f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report_lines.append("")
    report_lines.append("---")
    report_lines.append("")

    # 1. 整体概览
    report_lines.append("## 📊 整体概览")
    report_lines.append("")
    report_lines.append(f"- **数据周期**: {df_basic['月份'].min()} 至 {df_basic['月份'].max()}")
    report_lines.append(f"- **总计算间夜**: {df_basic['总计算间夜'].sum():,.0f} 间夜")
    report_lines.append(f"- **总订单价**: ¥{df_basic['总订单价'].sum():,.2f} 元")
    report_lines.append(f"- **总预算**: ¥{df_basic['预算汇总'].sum():,.2f} 元")
    report_lines.append("")
    report_lines.append("---")
    report_lines.append("")

    # 2. 四个核心指标分析
    report_lines.append("## 📈 四个核心指标变化趋势")
    report_lines.append("")

    # 分析四个核心指标
    metrics_to_analyze = [
        ('合住率', True),
        ('返点率', True),
        ('预算使用率', True),
        ('入住均价', False)
    ]

    for metric_name, is_percentage in metrics_to_analyze:
        analysis = analyze_metric_trend(df_basic, metric_name, is_percentage)

        report_lines.append(f"### {metric_name}")
        report_lines.append("")

        if len(analysis['values']) == 0:
            report_lines.append("⚠️ 暂无有效数据")
            report_lines.append("")
            continue

        # 趋势总结
        if analysis['trend']:
            trend_emoji = "📈" if analysis['trend'] == '上升' else "📉" if analysis['trend'] == '下降' else "➡️"
            report_lines.append(f"**趋势**: {trend_emoji} {analysis['trend']}")
            if analysis['change_rate'] is not None:
                report_lines.append(f"**变化幅度**: {analysis['change_rate']:+.2f}%")

        # 统计值
        unit = "%" if is_percentage else "元"
        report_lines.append(f"**平均值**: {analysis['avg']}{unit}")
        report_lines.append(f"**最高月份**: {analysis['max_month']}")
        report_lines.append(f"**最低月份**: {analysis['min_month']}")
        report_lines.append("")

        # 月度数据表格
        report_lines.append("| 月份 | 数值 |")
        report_lines.append("|------|------|")
        for item in analysis['values']:
            report_lines.append(f"| {item['month']} | {item['value']}{unit} |")
        report_lines.append("")

        # 关键洞察
        report_lines.append("**关键洞察**:")
        report_lines.append("")

        if metric_name == '合住率':
            avg = analysis['avg']
            if avg < 5:
                report_lines.append(f"- 合住率平均为{avg}%，处于较低水平，说明大部分出差为单人入住")
            elif avg < 10:
                report_lines.append(f"- 合住率平均为{avg}%，处于中等水平")
            else:
                report_lines.append(f"- 合住率平均为{avg}%，处于较高水平，团队出差较多")

        elif metric_name == '返点率':
            if len(analysis['values']) > 0:
                report_lines.append(f"- 返点率反映了符合返点条件的入住天数占比")
                if analysis['trend'] == '上升':
                    report_lines.append("- 返点条件符合度在提升，说明订房规范性在改善")
                elif analysis['trend'] == '下降':
                    report_lines.append("- 返点条件符合度在下降，需关注订房规范性")

        elif metric_name == '预算使用率':
            avg = analysis['avg']
            if avg < 70:
                report_lines.append(f"- 预算使用率平均为{avg}%，整体控制良好，有较大节约空间")
            elif avg < 90:
                report_lines.append(f"- 预算使用率平均为{avg}%，预算使用合理")
            else:
                report_lines.append(f"- 预算使用率平均为{avg}%，接近或超出预算，需注意成本控制")

        elif metric_name == '入住均价':
            if analysis['trend'] == '上升':
                report_lines.append(f"- 入住均价呈上升趋势（{analysis['change_rate']:+.2f}%），可能因为酒店选择升级或市场价格上涨")
            elif analysis['trend'] == '下降':
                report_lines.append(f"- 入住均价呈下降趋势（{analysis['change_rate']:+.2f}%），成本控制效果显著")

        report_lines.append("")
        report_lines.append("---")
        report_lines.append("")

    # 3. 月度对比分析
    report_lines.append("## 📅 月度对比分析")
    report_lines.append("")
    report_lines.append("| 月份 | 总计算间夜 | 合住率 | 返点率 | 预算使用率 | 入住均价 |")
    report_lines.append("|------|-----------|--------|--------|-----------|---------|")

    for _, row in df_basic.iterrows():
        month = row['月份']
        nights = f"{row['总计算间夜']:,.0f}"
        shared = f"{row['合住率']:.2f}%" if pd.notna(row['合住率']) else "-"
        rebate = f"{row['返点率']:.2f}%" if pd.notna(row['返点率']) and row['返点率'] > 0 else "-"
        budget = f"{row['预算使用率']:.2f}%" if pd.notna(row['预算使用率']) else "-"
        price = f"¥{row['入住均价']:.2f}" if pd.notna(row['入住均价']) else "-"

        report_lines.append(f"| {month} | {nights} | {shared} | {rebate} | {budget} | {price} |")

    report_lines.append("")
    report_lines.append("---")
    report_lines.append("")

    # 4. 关键建议
    report_lines.append("## 💡 关键建议")
    report_lines.append("")

    # 基于数据生成建议
    avg_shared_rate = df_basic['合住率'].mean()
    avg_budget_rate = df_basic['预算使用率'].mean()

    suggestions = []

    if avg_shared_rate < 5:
        suggestions.append("- **优化合住安排**: 当前合住率较低，建议对团队出差进行合理的合住安排，可有效降低成本")

    if avg_budget_rate > 90:
        suggestions.append("- **加强成本控制**: 预算使用率较高，建议加强酒店选择的成本控制，优先选择符合预算标准的酒店")
    elif avg_budget_rate < 70:
        suggestions.append("- **预算执行良好**: 预算使用率控制在合理范围内，继续保持")

    # 检查返点率数据
    rebate_data = df_basic[df_basic['返点率'].notna() & (df_basic['返点率'] > 0)]
    if len(rebate_data) > 0:
        avg_rebate_rate = rebate_data['返点率'].mean()
        if avg_rebate_rate < 15:
            suggestions.append("- **提高返点率**: 当前返点率较低，建议培训员工提高订房规范性，确保符合返点条件")

    # 检查入住均价趋势
    price_data = df_basic[df_basic['入住均价'].notna()]
    if len(price_data) >= 2:
        price_values = price_data['入住均价'].values
        if price_values[-1] > price_values[0] * 1.1:
            suggestions.append("- **关注价格上涨**: 入住均价呈明显上升趋势，建议审查酒店选择策略")

    if len(suggestions) == 0:
        suggestions.append("- 当前各项指标整体表现良好，继续保持")

    for suggestion in suggestions:
        report_lines.append(suggestion)

    report_lines.append("")
    report_lines.append("---")
    report_lines.append("")
    report_lines.append(f"**报告生成**: 返点指标计算系统 v1.0")
    report_lines.append(f"**数据来源**: `/Users/anker/rebate_checker/data/指标计算结果.xlsx`")
    report_lines.append("")

    # 生成报告文本
    report_text = "\n".join(report_lines)

    # 如果指定了输出路径，则保存到文件
    if output_path:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report_text)
        print(f"✅ 报告已保存至: {output_path}")

    return report_text

def main():
    """主函数"""
    print("=" * 60)
    print("  返点指标分析报告生成器")
    print("=" * 60)
    print("")

    # 数据文件路径
    data_file = "/Users/anker/rebate_checker/data/指标计算结果.xlsx"
    output_file = "/Users/anker/rebate_checker/data/指标分析报告.md"

    try:
        # 加载数据
        print("加载数据...")
        df_basic = load_metrics_data(data_file)
        print(f"✅ 数据加载完成（{len(df_basic)} 个月份）")
        print("")

        # 生成报告
        print("生成分析报告...")
        report_text = generate_markdown_report(df_basic, output_file)
        print("")

        print("=" * 60)
        print("✅ 报告生成完成！")
        print("=" * 60)
        print("")
        print(f"输出文件: {output_file}")
        print("")
        print("可以使用以下命令查看报告:")
        print(f"  cat {output_file}")
        print(f"  open {output_file}")
        print("")

        return True

    except Exception as e:
        print("")
        print("=" * 60)
        print(f"❌ 错误: {str(e)}")
        print("=" * 60)
        return False

if __name__ == "__main__":
    main()
