import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

# 读取数据
def load_data():
    try:
        # 定义数据文件的相对路径
        file_paths = [
            '历年数字化转型指数汇总.xlsx'
        ]
        
        for file_path in file_paths:
            if os.path.exists(file_path):
                # 读取Excel文件
                data = pd.read_excel(file_path)
                return data
        
        st.error("数据文件不存在，请检查以下路径是否正确:")
        for path in file_paths:
            st.error(path)
        return None
        
    except Exception as e:
        st.error(f"读取数据失败: {e}")
        return None

# 主应用
def main():
    # 设置页面标题
    st.title('企业数字化转型指数查询与可视化')
    st.markdown("---")
    
    # 加载数据
    data = load_data()
    
    if data is not None:
        # 数据概览
        st.sidebar.header('📊 数据概况')
        st.sidebar.markdown(f"**总记录数:** {len(data)}")
        st.sidebar.markdown(f"**年份范围:** {data['年份'].min()} - {data['年份'].max()}")
        st.sidebar.markdown(f"**企业数量:** {data['企业名称'].nunique()}")
        
        # 查询功能
        st.header('🔍 股票代码与年份查询')
        
        # 创建两列布局
        col1, col2 = st.columns(2)
        
        with col1:
            # 股票代码选择
            stock_codes = sorted(data['股票代码'].unique())
            selected_code = st.selectbox('选择股票代码:', stock_codes)
        
        with col2:
            # 年份选择
            years = sorted(data['年份'].unique())
            selected_year = st.selectbox('选择年份:', years)
        
        # 查询结果显示
        st.markdown("---")
        st.subheader('查询结果')
        
        # 筛选数据
        result = data[(data['股票代码'] == selected_code) & (data['年份'] == selected_year)]
        
        if not result.empty:
            # 显示企业信息
            company_name = result['企业名称'].values[0]
            index_value = result['数字化转型指数'].values[0]
            
            # 使用卡片式布局显示结果
            st.success('✅ 查询成功!')
            
            # 创建结果卡片
            st.markdown("### 📋 企业详情")
            col_info1, col_info2 = st.columns(2)
            with col_info1:
                st.markdown(f"**企业名称:** {company_name}")
                st.markdown(f"**股票代码:** {selected_code}")
            with col_info2:
                st.markdown(f"**年份:** {selected_year}")
                st.markdown(f"**数字化转型指数:** {index_value:.4f}")
            
            # 显示详细数据
            st.dataframe(result)
        else:
            st.warning('⚠️ 未找到匹配的数据')
        
        # 历年指数趋势图
        st.markdown("---")
        st.subheader('📈 历年数字化转型指数趋势')
        
        # 获取该股票代码的所有年份数据
        company_data = data[data['股票代码'] == selected_code].sort_values('年份')
        
        if not company_data.empty:
            # 获取企业名称
            company_name = company_data['企业名称'].values[0]
            
            # 创建折线图
            fig, ax = plt.subplots(figsize=(12, 6))
            
            # 绘制折线图
            ax.plot(company_data['年份'], company_data['数字化转型指数'], 
                    marker='o', linewidth=2, markersize=8, color='steelblue', 
                    label=f'{company_name} ({selected_code})')
            
            # 添加数值标签
            for i, v in enumerate(company_data['数字化转型指数']):
                ax.text(company_data['年份'].values[i], v + 0.001, 
                        f'{v:.4f}', ha='center', va='bottom', fontsize=9)
            
            # 设置图表标题和标签
            ax.set_title(f'{company_name} ({selected_code}) 历年数字化转型指数趋势', 
                       fontsize=14, fontweight='bold')
            ax.set_xlabel('年份', fontsize=12)
            ax.set_ylabel('数字化转型指数', fontsize=12)
            
            # 设置网格
            ax.grid(True, linestyle='--', alpha=0.7)
            
            # 设置X轴刻度
            ax.set_xticks(company_data['年份'])
            ax.set_xticklabels(company_data['年份'], rotation=45)
            
            # 添加图例
            ax.legend(loc='upper left')
            
            # 调整布局
            plt.tight_layout()
            
            # 显示图表
            st.pyplot(fig)
            
            # 显示详细数据
            st.markdown("### 📊 历年指数数据")
            st.dataframe(company_data[['年份', '数字化转型指数']].sort_values('年份'))
        else:
            st.warning('⚠️ 未找到该企业的历史数据')

# 运行应用
if __name__ == '__main__':
    main()