import streamlit as st
import pandas as pd
import io
import hashlib
import time

def calculate_total_score(row):
    """计算总分：总分=(乙部/103*0.7)*100+(甲部/50*0.3)*100"""
    try:
        jia_score = float(row['甲部分数'])
        yi_score = float(row['乙部分数'])
        
        # 计算加权分数
        jia_weighted = (jia_score / 50 * 0.3) * 100
        yi_weighted = (yi_score / 103 * 0.7) * 100
        
        # 四舍五入为整数
        return round(jia_weighted + yi_weighted)
    except:
        return 0

def process_data(df):
    """处理数据：计算总分、排序、排名"""
    processed_df = df.copy()
    
    # 计算总分
    processed_df['总分'] = processed_df.apply(calculate_total_score, axis=1)
    
    # 按总分降序排序
    processed_df = processed_df.sort_values('总分', ascending=False)
    
    # 计算排名（相同分数相同排名）
    processed_df['排名'] = processed_df['总分'].rank(method='min', ascending=False).astype(int)
    
    return processed_df

def assign_grades(df, cutoff_scores):
    """根据cutoff分数分配等级"""
    df_with_grades = df.copy()
    df_with_grades['等级'] = '未定级'
    
    # 按分数从低到高分配等级
    levels = ['Level2', 'Level3', 'Level4', 'Level5', 'Level6', 'Level7']
    
    for level in levels:
        if level in cutoff_scores and cutoff_scores[level] > 0:
            mask = df_with_grades['总分'] >= cutoff_scores[level]
            df_with_grades.loc[mask, '等级'] = level
    
    return df_with_grades

def main():
    st.set_page_config(
        page_title="学生成绩计算系统",
        page_icon="📊",
        layout="wide"
    )
    
    st.title("📊 学生成绩计算系统")
    st.markdown("---")
    
    # 侧边栏：等级 cutoff 设置
    st.sidebar.header("🏆 等级设置")
    
    # 默认cutoff值
    default_cutoffs = {
        'Level2': 47.0,
        'Level3': 53.0,
        'Level4': 58.0,
        'Level5': 63.0,
        'Level6': 66.0,
        'Level7': 70.0
    }
    
    # 等级设置表单
    with st.sidebar.form("cutoff_form"):
        st.caption("设置各等级的最低分数线（≥）")
        level2 = st.number_input("Level2 ≥", 0.0, 100.0, default_cutoffs['Level2'], 0.1)
        level3 = st.number_input("Level3 ≥", 0.0, 100.0, default_cutoffs['Level3'], 0.1)
        level4 = st.number_input("Level4 ≥", 0.0, 100.0, default_cutoffs['Level4'], 0.1)
        level5 = st.number_input("Level5 ≥", 0.0, 100.0, default_cutoffs['Level5'], 0.1)
        level6 = st.number_input("Level6 ≥", 0.0, 100.0, default_cutoffs['Level6'], 0.1)
        level7 = st.number_input("Level7 ≥", 0.0, 100.0, default_cutoffs['Level7'], 0.1)
        
        col1, col2 = st.columns(2)
        with col1:
            apply_btn = st.form_submit_button("应用设置")
        with col2:
            reset_btn = st.form_submit_button("恢复默认")
    
    # 处理按钮点击
    if reset_btn:
        st.sidebar.success("已恢复默认设置")
        current_cutoffs = default_cutoffs
    elif apply_btn:
        current_cutoffs = {
            'Level2': level2, 'Level3': level3, 'Level4': level4,
            'Level5': level5, 'Level6': level6, 'Level7': level7
        }
        st.sidebar.success("设置已应用")
    else:
        current_cutoffs = default_cutoffs
    
    # 文件上传
    st.header("📁 文件上传")
    uploaded_file = st.file_uploader(
        "请上传Excel或CSV文件",
        type=['xlsx', 'xls', 'csv'],
        help="文件应包含：姓名、学号、班级、甲部分数、乙部分数"
    )
    
    if uploaded_file is not None:
        try:
            # 读取文件
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            
            # 处理None值
            df = df.fillna(0)
            
            # 生成文件ID
            file_content = uploaded_file.read()
            file_hash = hashlib.md5(file_content).hexdigest()[:8]
            uploaded_file.seek(0)
            
            st.success(f"✅ 文件上传成功！共读取 {len(df)} 条记录")
            
            # 检查必要列
            required_columns = ['姓名', '学号', '班级', '甲部分数', '乙部分数']
            missing_columns = [col for col in required_columns if col not in df.columns]
            
            if missing_columns:
                st.error(f"❌ 文件缺少必要的列：{', '.join(missing_columns)}")
                return
            
            # 显示原始数据
            st.subheader("📋 原始数据")
            st.dataframe(df, use_container_width=True)
            
            # 处理数据
            processed_df = process_data(df)
            
            # 显示计算结果
            st.subheader("📊 计算结果")
            st.dataframe(processed_df, use_container_width=True)
            
            # 统计信息
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("总人数", len(processed_df))
            with col2:
                st.metric("平均分", f"{processed_df['总分'].mean():.1f}")
            with col3:
                st.metric("最高分", f"{processed_df['总分'].max():.0f}")
            with col4:
                st.metric("最低分", f"{processed_df['总分'].min():.0f}")
            
            # 等级划分
            final_df = assign_grades(processed_df, current_cutoffs)
            
            # 显示最终结果
            st.subheader("🎯 最终结果（含等级）")
            
            # 等级颜色映射
            level_colors = {
                'Level2': '#FFE6E6', 'Level3': '#FFF2E6', 'Level4': '#FFFFE6',
                'Level5': '#E6FFE6', 'Level6': '#E6F3FF', 'Level7': '#F0E6FF',
                '未定级': '#F5F5F5'
            }
            
            # 应用颜色样式
            def highlight_levels(df):
                styles = pd.DataFrame('', index=df.index, columns=df.columns)
                for i in range(len(df)):
                    level = df.iloc[i]['等级']
                    color = level_colors.get(level, '#F5F5F5')
                    for j in range(len(df.columns)):
                        styles.iloc[i, j] = f'background-color: {color}'
                return styles
            
            styled_df = final_df.style.apply(highlight_levels, axis=None)
            st.dataframe(styled_df, use_container_width=True)
            
            # 成绩分布
            st.subheader("📊 成绩分布")
            
            col1, col2 = st.columns(2)
            with col1:
                st.write("**等级分布**")
                grade_counts = final_df['等级'].value_counts().sort_index()
                for level, count in grade_counts.items():
                    percentage = (count / len(final_df)) * 100
                    st.write(f"{level}: {count}人 ({percentage:.1f}%)")
            
            with col2:
                st.write("**班级平均分**")
                class_avg = final_df.groupby('班级')['总分'].mean().sort_values(ascending=False)
                for class_name, avg_score in class_avg.items():
                    st.write(f"{class_name}: {avg_score:.1f}分")
            
            # 下载结果
            st.subheader("💾 下载结果")
            
            # 创建Excel文件
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                final_df.to_excel(writer, sheet_name='计算结果', index=False)
            
            output.seek(0)
            
            timestamp = int(time.time())
            filename = f"成绩计算结果_{file_hash}_{timestamp}.xlsx"
            
            st.download_button(
                label="📥 下载Excel文件",
                data=output.getvalue(),
                file_name=filename,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
            
        except Exception as e:
            st.error(f"❌ 处理文件时出错：{str(e)}")
            st.info("请检查文件格式是否正确")
    
    else:
        st.info("👆 请上传包含学生成绩的Excel或CSV文件")
        
        # 显示示例
        st.subheader("📝 文件格式示例")
        example_data = {
            '姓名': ['张三', '李四', '王五'],
            '学号': ['2021001', '2021002', '2021003'],
            '班级': ['一班', '一班', '二班'],
            '甲部分数': [45, 42, 48],
            '乙部分数': [95, 88, 92]
        }
        example_df = pd.DataFrame(example_data)
        st.dataframe(example_df, use_container_width=True)
        
        st.markdown("""
        **计算规则：**
        - 总分 = (乙部分数/103 × 0.7) × 100 + (甲部分数/50 × 0.3) × 100
        - 系统会自动按总分降序排序并计算排名
        - 您可以根据需要设置各等级的cutoff分数
        """)

if __name__ == "__main__":
    main()
