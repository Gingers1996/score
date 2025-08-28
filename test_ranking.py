#!/usr/bin/env python3
import pandas as pd
import numpy as np

def test_ranking_logic():
    """测试排名逻辑：相同分数相同排名"""
    print("🧪 测试排名逻辑...")
    
    # 创建包含相同分数的测试数据
    test_data = {
        '姓名': ['张三', '李四', '王五', '赵六', '钱七', '孙八'],
        '学号': ['2021001', '2021002', '2021003', '2021004', '2021005', '2021006'],
        '班级': ['一班', '一班', '二班', '二班', '三班', '三班'],
        '甲部分数': [45, 45, 42, 48, 40, 46],
        '乙部分数': [95, 95, 88, 92, 85, 90]
    }
    
    df = pd.DataFrame(test_data)
    print("📋 测试数据：")
    print(df)
    
    # 计算总分（四舍五入为整数）
    def calculate_total_score(row):
        jia_score = float(row['甲部分数'])
        yi_score = float(row['乙部分数'])
        jia_weighted = (jia_score / 50 * 0.3) * 100
        yi_weighted = (yi_score / 103 * 0.7) * 100
        return round(jia_weighted + yi_weighted)
    
    df['总分'] = df.apply(calculate_total_score, axis=1)
    df = df.sort_values('总分', ascending=False)
    
    # 使用WPS RANK函数逻辑计算排名
    df['排名'] = df['总分'].rank(method='min', ascending=False).astype(int)
    
    print("\n📊 计算结果（相同分数相同排名）：")
    print(df[['姓名', '总分', '排名']].to_string(index=False))
    
    # 验证排名逻辑
    print("\n🔍 排名验证：")
    unique_scores = df['总分'].unique()
    for score in sorted(unique_scores, reverse=True):
        students = df[df['总分'] == score]
        rank = students['排名'].iloc[0]
        names = ', '.join(students['姓名'].tolist())
        print(f"  总分 {score} 分：{names} → 排名 {rank}")
    
    print("\n✅ 排名逻辑测试完成！")
    return df

if __name__ == "__main__":
    result = test_ranking_logic()
