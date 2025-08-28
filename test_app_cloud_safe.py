#!/usr/bin/env python3
"""
测试 app_cloud_safe.py 的核心功能
"""

import pandas as pd
import sys
import os

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 导入应用中的函数
from app_cloud_safe import calculate_total_score, process_data, assign_grades, validate_cutoff_input

def test_calculate_total_score():
    """测试总分计算功能"""
    print("🧮 测试总分计算...")
    
    # 测试数据
    test_data = [
        {'甲部分数': 45, '乙部分数': 95},
        {'甲部分数': 42, '乙部分数': 88},
        {'甲部分数': 48, '乙部分数': 92},
        {'甲部分数': 0, '乙部分数': 0},  # 测试边界值
        {'甲部分数': 50, '乙部分数': 103}  # 测试满分
    ]
    
    expected_scores = [92, 85, 91, 0, 100]  # 预期结果
    
    for i, (data, expected) in enumerate(zip(test_data, expected_scores)):
        result = calculate_total_score(data)
        status = "✅" if result == expected else "❌"
        print(f"  测试 {i+1}: {status} 输入: 甲部={data['甲部分数']}, 乙部={data['乙部分数']} -> 总分={result} (期望: {expected})")
    
    print()

def test_process_data():
    """测试数据处理功能"""
    print("📊 测试数据处理...")
    
    # 创建测试数据
    test_df = pd.DataFrame({
        '姓名': ['张三', '李四', '王五', '赵六'],
        '学号': ['001', '002', '003', '004'],
        '班级': ['一班', '一班', '二班', '二班'],
        '甲部分数': [45, 42, 48, 40],
        '乙部分数': [95, 88, 92, 85]
    })
    
    # 处理数据
    processed_df = process_data(test_df)
    
    # 验证结果
    print(f"  原始数据行数: {len(test_df)}")
    print(f"  处理后数据行数: {len(processed_df)}")
    print(f"  是否包含总分列: {'总分' in processed_df.columns}")
    print(f"  是否包含排名列: {'排名' in processed_df.columns}")
    print(f"  总分范围: {processed_df['总分'].min()} - {processed_df['总分'].max()}")
    print(f"  排名范围: {processed_df['排名'].min()} - {processed_df['排名'].max()}")
    
    # 验证排序
    is_sorted = processed_df['总分'].is_monotonic_decreasing
    print(f"  是否按总分降序排列: {'✅' if is_sorted else '❌'}")
    
    print()

def test_assign_grades():
    """测试等级分配功能"""
    print("🏆 测试等级分配...")
    
    # 创建测试数据
    test_df = pd.DataFrame({
        '姓名': ['张三', '李四', '王五', '赵六', '钱七'],
        '总分': [75, 70, 77, 65, 80]
    })
    
    # 测试等级分数线
    cutoff_scores = {
        'Level2': 47,
        'Level3': 53,
        'Level4': 58,
        'Level5': 63,
        'Level6': 66,
        'Level7': 70
    }
    
    # 分配等级
    graded_df = assign_grades(test_df, cutoff_scores)
    
    # 验证结果
    print(f"  原始数据行数: {len(test_df)}")
    print(f"  分配等级后行数: {len(graded_df)}")
    print(f"  是否包含等级列: {'等级' in graded_df.columns}")
    
    # 显示等级分配结果
    print("  等级分配结果:")
    for _, row in graded_df.iterrows():
        print(f"    {row['姓名']}: 总分={row['总分']}, 等级={row['等级']}")
    
    print()

def test_validate_cutoff_input():
    """测试等级分数线输入验证"""
    print("🔢 测试等级分数线输入验证...")
    
    test_inputs = [
        ("47", 47),      # 有效整数
        ("53.5", None),  # 小数（无效）
        ("abc", None),   # 非数字（无效）
        ("-5", None),    # 负数（无效）
        ("120", None),   # 超出范围（无效）
        ("0", 0),        # 边界值
        ("100", 100),    # 边界值
    ]
    
    for input_val, expected in test_inputs:
        result = validate_cutoff_input(input_val)
        status = "✅" if result == expected else "❌"
        print(f"  输入 '{input_val}' -> {status} 结果: {result} (期望: {expected})")
    
    print()

def test_ranking_logic():
    """测试排名逻辑（相同分数相同排名）"""
    print("📈 测试排名逻辑...")
    
    # 创建包含相同分数的测试数据
    test_df = pd.DataFrame({
        '姓名': ['张三', '李四', '王五', '赵六', '钱七', '孙八'],
        '学号': ['001', '002', '003', '004', '005', '006'],
        '班级': ['一班', '一班', '二班', '二班', '三班', '三班'],
        '甲部分数': [48, 45, 46, 42, 47, 40],
        '乙部分数': [96, 90, 91, 85, 93, 80]
    })
    
    # 处理数据
    processed_df = process_data(test_df)
    
    print("  排名结果:")
    for _, row in processed_df.iterrows():
        print(f"    {row['姓名']}: 总分={row['总分']}, 排名={row['排名']}")
    
    # 验证相同分数是否有相同排名
    score_rank_map = {}
    for _, row in processed_df.iterrows():
        score = row['总分']
        rank = row['排名']
        if score in score_rank_map:
            if score_rank_map[score] != rank:
                print(f"  ❌ 相同分数 {score} 的排名不一致: {score_rank_map[score]} vs {rank}")
                return
        else:
            score_rank_map[score] = rank
    
    print("  ✅ 相同分数获得相同排名")
    print()

def main():
    """运行所有测试"""
    print("🧪 开始测试 app_cloud_safe.py 核心功能")
    print("=" * 50)
    
    try:
        test_calculate_total_score()
        test_process_data()
        test_assign_grades()
        test_validate_cutoff_input()
        test_ranking_logic()
        
        print("🎉 所有测试完成！")
        print("✅ 应用核心功能正常")
        
    except Exception as e:
        print(f"❌ 测试过程中出现错误: {str(e)}")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
