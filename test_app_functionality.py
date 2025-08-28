#!/usr/bin/env python3
import pandas as pd
import numpy as np

def test_calculation():
    """测试计算功能"""
    print("🧪 测试计算功能...")
    
    # 创建测试数据
    test_data = {
        '姓名': ['张三', '李四', '王五'],
        '学号': ['2021001', '2021002', '2021003'],
        '班级': ['一班', '一班', '二班'],
        '甲部分数': [45, 42, 48],
        '乙部分数': [95, 88, 92]
    }
    
    df = pd.DataFrame(test_data)
    print("📋 测试数据：")
    print(df)
    
    # 测试总分计算
    def calculate_total_score(row):
        jia_score = float(row['甲部分数'])
        yi_score = float(row['乙部分数'])
        jia_weighted = (jia_score / 50 * 0.3) * 100
        yi_weighted = (yi_score / 103 * 0.7) * 100
        return round(jia_weighted + yi_weighted)  # 四舍五入为整数
    
    df['总分'] = df.apply(calculate_total_score, axis=1)
    df = df.sort_values('总分', ascending=False)
    df['排名'] = df['总分'].rank(method='min', ascending=False).astype(int)  # 相同分数相同排名
    
    print("\n📊 计算结果：")
    print(df)
    
    # 测试等级分配
    cutoff_scores = {
        'Level2': 47.0,
        'Level3': 53.0,
        'Level4': 58.0,
        'Level5': 63.0,
        'Level6': 66.0,
        'Level7': 70.0
    }
    
    df['等级'] = '未定级'
    levels = ['Level2', 'Level3', 'Level4', 'Level5', 'Level6', 'Level7']
    
    for level in levels:
        if level in cutoff_scores and cutoff_scores[level] > 0:
            mask = df['总分'] >= cutoff_scores[level]
            df.loc[mask, '等级'] = level
    
    print("\n🎯 最终结果：")
    print(df)
    
    print("\n✅ 计算功能测试完成！")
    return df

if __name__ == "__main__":
    result = test_calculation()
    
    print("\n📝 使用说明：")
    print("1. 打开浏览器访问：http://localhost:8501")
    print("2. 上传 '示例学生成绩.xlsx' 文件")
    print("3. 查看计算结果和最终结果")
    print("4. 点击下载按钮导出Excel文件")
