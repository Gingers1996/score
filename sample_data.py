import pandas as pd
import numpy as np

def generate_sample_data(num_students=30):
    """生成示例学生成绩数据"""
    np.random.seed(42)  # 设置随机种子，确保结果可重现
    
    # 生成学生姓名
    surnames = ['张', '李', '王', '刘', '陈', '杨', '赵', '黄', '周', '吴', '徐', '孙', '胡', '朱', '高', '林', '何', '郭', '马', '罗']
    names = ['伟', '芳', '娜', '秀英', '敏', '静', '丽', '强', '磊', '军', '洋', '勇', '艳', '杰', '娟', '涛', '明', '超', '秀兰', '霞']
    
    student_names = []
    for _ in range(num_students):
        name = np.random.choice(surnames) + np.random.choice(names)
        student_names.append(name)
    
    # 生成学号
    student_ids = [f"2024{str(i+1).zfill(4)}" for i in range(num_students)]
    
    # 生成班级
    classes = ['一班', '二班', '三班', '四班', '五班']
    student_classes = np.random.choice(classes, num_students)
    
    # 生成甲部分数 (满分50分)
    jia_scores = np.random.normal(35, 8, num_students)
    jia_scores = np.clip(jia_scores, 0, 50)  # 限制在0-50之间
    jia_scores = np.round(jia_scores, 1)
    
    # 生成乙部分数 (满分103分)
    yi_scores = np.random.normal(75, 15, num_students)
    yi_scores = np.clip(yi_scores, 0, 103)  # 限制在0-103之间
    yi_scores = np.round(yi_scores, 1)
    
    # 创建数据框
    data = {
        '姓名': student_names,
        '学号': student_ids,
        '班级': student_classes,
        '甲部分数': jia_scores,
        '乙部分数': yi_scores
    }
    
    df = pd.DataFrame(data)
    return df

if __name__ == "__main__":
    # 生成示例数据
    sample_df = generate_sample_data(30)
    
    # 保存为Excel文件
    sample_df.to_excel('示例学生成绩.xlsx', index=False)
    print("✅ 示例数据已生成并保存为 '示例学生成绩.xlsx'")
    print(f"📊 共生成 {len(sample_df)} 条学生记录")
    print("\n📋 数据预览：")
    print(sample_df.head())
