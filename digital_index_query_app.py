import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import re
from datetime import datetime

# 设置中文字体支持
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

# 设置页面配置
st.set_page_config(
    page_title="企业数字化转型指数查询系统",
    page_icon="📊",
    layout="wide"
)

# 数据加载函数
def load_data():
    """加载并预处理数字化转型指数数据"""
    try:
        # 获取当前应用所在目录
        app_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(app_dir, '历年数字化转型指数汇总.xlsx')
        
        if os.path.exists(file_path):
            # 读取Excel文件，将股票代码设为字符串类型
            data = pd.read_excel(file_path, dtype={'股票代码': str})
            
            # 验证必要列是否存在
            required_columns = ['股票代码', '企业名称', '年份', '数字化转型指数']
            missing_columns = [col for col in required_columns if col not in data.columns]
            
            if missing_columns:
                st.error(f"Excel文件缺少必要的列: {', '.join(missing_columns)}")
                st.error("请检查文件格式是否正确")
                return None
            
            # 数据类型转换
            data['年份'] = data['年份'].astype(int)
            data['数字化转型指数'] = data['数字化转型指数'].astype(float)
            
            # 数据清洗：去除空值
            data = data.dropna(subset=required_columns)
            
            # 添加应用信息
            st.sidebar.success(f"数据加载成功！")
            st.sidebar.info(f"记录总数: {len(data)}")
            st.sidebar.info(f"年份范围: {data['年份'].min()} - {data['年份'].max()}")
            st.sidebar.info(f"企业数量: {len(data['企业名称'].unique())}")
            
            return data
        else:
            st.error(f"数据文件不存在: {file_path}")
            st.error("请将Excel文件放置在应用程序同一目录下")
            return None
    except Exception as e:
        st.error(f"读取数据失败: {e}")
        st.error("请检查Excel文件格式是否正确")
        print(f"读取数据时出错: {type(e).__name__}: {e}")
        return None

# 绘制企业历史指数趋势图
def plot_enterprise_trend(data, company_name, company_data):
    """绘制企业历年数字化转型指数趋势图"""
    plt.figure(figsize=(12, 6))
    
    # 绘制折线图
    plt.plot(company_data['年份'], company_data['数字化转型指数'], 
             marker='o', markersize=8, linewidth=2, color='#1f77b4', 
             markerfacecolor='#ff7f0e', label='年度指数')
    
    # 计算趋势线
    x = company_data['年份']
    y = company_data['数字化转型指数']
    z = np.polyfit(x, y, 1)
    p = np.poly1d(z)
    plt.plot(x, p(x), "r--", linewidth=2, label=f'趋势线 (y={z[0]:.4f}x+{z[1]:.4f})')
    
    # 添加数据标签
    for i, txt in enumerate(company_data['数字化转型指数']):
        plt.annotate(f'{txt:.4f}', 
                    (company_data['年份'].iloc[i], company_data['数字化转型指数'].iloc[i]),
                    textcoords="offset points", xytext=(0,10), ha='center')
    
    plt.title(f'{company_name} 数字化转型指数历年趋势', fontsize=16)
    plt.xlabel('年份', fontsize=12)
    plt.ylabel('数字化转型指数', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend(fontsize=10)
    plt.xticks(company_data['年份'], rotation=45)
    plt.tight_layout()
    
    # 在Streamlit中显示图表
    st.pyplot(plt)
    plt.close()

# 绘制年度指数分布直方图
def plot_year_distribution(data, year):
    """绘制指定年份的指数分布直方图"""
    year_data = data[data['年份'] == year]
    plt.figure(figsize=(12, 6))
    
    plt.hist(year_data['数字化转型指数'], bins=20, 
             alpha=0.7, color='#2ca02c', 
             edgecolor='black', linewidth=1)
    
    plt.title(f'{year}年数字化转型指数分布', fontsize=16)
    plt.xlabel('数字化转型指数', fontsize=12)
    plt.ylabel('企业数量', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    
    st.pyplot(plt)
    plt.close()

# 绘制年度排名前10企业
def plot_top_10(year_data, year):
    """绘制指定年份排名前10的企业"""
    top10 = year_data.nlargest(10, '数字化转型指数')
    plt.figure(figsize=(12, 6))
    
    bars = plt.barh(top10['企业名称'], top10['数字化转型指数'], 
                    color='#9467bd', alpha=0.8)
    
    plt.title(f'{year}年数字化转型指数排名前10企业', fontsize=16)
    plt.xlabel('数字化转型指数', fontsize=12)
    plt.ylabel('企业名称', fontsize=12)
    plt.grid(True, axis='x', linestyle='--', alpha=0.7)
    
    # 添加数据标签
    for bar in bars:
        width = bar.get_width()
        plt.text(width + 0.001, bar.get_y() + bar.get_height()/2, 
                 f'{width:.4f}', ha='left', va='center')
    
    plt.tight_layout()
    st.pyplot(plt)
    plt.close()

# 主函数
def main():
    # 设置应用标题
    st.title("📊 企业数字化转型指数查询系统")
    st.markdown("---")
    
    # 添加应用信息
    st.markdown("**应用信息：**")
    st.markdown("- 基于Streamlit框架开发的企业数字化转型指数分析工具")
    st.markdown("- 支持数据查询、趋势分析和统计可视化")
    st.markdown("- 数据来源：历年数字化转型指数汇总.xlsx")
    st.markdown("---")
    
    # 加载数据
    data = load_data()
    
    if data is not None:
        # 获取基础统计信息
        min_year = data['年份'].min()
        max_year = data['年份'].max()
        available_years = sorted(data['年份'].unique())
        available_stocks = sorted(data['股票代码'].unique())
        
        # 侧边栏设置
        st.sidebar.title("功能导航")
        page = st.sidebar.radio(
            "选择功能:",
            ["快速查询", "高级查询", "趋势分析", "统计分布"]
        )
        
        # 快速查询页面
        if page == "快速查询":
            st.subheader("🔍 快速查询")
            
            # 查询条件
            col1, col2 = st.columns(2)
            with col1:
                selected_stock = st.selectbox('选择股票代码:', available_stocks)
            with col2:
                selected_year = st.selectbox('选择年份:', available_years)
            
            if st.button('执行查询'):
                # 过滤数据
                result = data[(data['股票代码'] == selected_stock) & (data['年份'] == selected_year)]
                
                if not result.empty:
                    st.success(f"查询到 {len(result)} 条记录")
                    
                    # 显示查询结果卡片
                    st.markdown("### 查询结果")
                    with st.container():
                        st.markdown("""
                        <style>
                        .result-card {
                            background-color: #f0f2f6;
                            border-radius: 10px;
                            padding: 20px;
                            margin: 10px 0;
                        }
                        </style>
                        """, unsafe_allow_html=True)
                        
                        for _, row in result.iterrows():
                            st.markdown(f"""
                            <div class="result-card">
                                <h4>{row['企业名称']} ({row['股票代码']})</h4>
                                <p>年份: {row['年份']}</p>
                                <p>数字化转型指数: {row['数字化转型指数']:.4f}</p>
                            </div>
                            """, unsafe_allow_html=True)
                else:
                    st.warning("未找到匹配的记录")
        
        # 高级查询页面
        elif page == "高级查询":
            st.subheader("🔎 高级查询")
            
            with st.expander("点击展开高级查询条件", expanded=True):
                col1, col2 = st.columns(2)
                
                with col1:
                    # 企业名称关键词搜索
                    company_name_search = st.text_input('输入企业名称关键词:')
                    
                    # 指数范围筛选
                    min_index = st.number_input('最小指数值:', min_value=0.0, max_value=1.0, value=0.0, step=0.001)
                
                with col2:
                    # 年份范围筛选
                    year_range = st.slider(
                        '选择年份范围:',
                        min_value=min_year,
                        max_value=max_year,
                        value=(min_year, max_year),
                        step=1
                    )
                    
                    max_index = st.number_input('最大指数值:', min_value=0.0, max_value=1.0, value=1.0, step=0.001)
            
            if st.button('执行高级查询'):
                # 应用筛选条件
                advanced_result = data.copy()
                
                # 企业名称筛选
                if company_name_search:
                    advanced_result = advanced_result[advanced_result['企业名称'].str.contains(company_name_search, case=False, na=False)]
                
                # 年份范围筛选
                advanced_result = advanced_result[(advanced_result['年份'] >= year_range[0]) & (advanced_result['年份'] <= year_range[1])]
                
                # 指数范围筛选
                advanced_result = advanced_result[(advanced_result['数字化转型指数'] >= min_index) & (advanced_result['数字化转型指数'] <= max_index)]
                
                if not advanced_result.empty:
                    st.success(f"找到 {len(advanced_result)} 条匹配记录")
                    
                    # 显示结果
                    st.dataframe(
                        advanced_result[['股票代码', '企业名称', '年份', '数字化转型指数']].sort_values(
                            ['年份', '数字化转型指数'], ascending=[False, False]
                        ),
                        use_container_width=True
                    )
                    
                    # 数据导出功能
                    st.markdown("---")
                    csv = advanced_result.to_csv(index=False, encoding='utf-8-sig')
                    st.download_button(
                        label="📥 下载查询结果 (CSV格式)",
                        data=csv,
                        file_name="数字化转型指数查询结果.csv",
                        mime="text/csv"
                    )
                else:
                    st.warning("未找到匹配的记录")
        
        # 趋势分析页面
        elif page == "趋势分析":
            st.subheader("📈 趋势分析")
            
            # 选择企业
            selected_stock = st.selectbox('选择股票代码:', available_stocks)
            
            if selected_stock:
                # 获取企业名称
                company_name = data[data['股票代码'] == selected_stock]['企业名称'].iloc[0]
                
                # 获取企业历史数据
                company_data = data[data['股票代码'] == selected_stock].sort_values('年份')
                
                # 显示企业基本信息
                st.markdown(f"### {company_name} ({selected_stock}) 历年指数趋势")
                st.write(f"数据区间: {company_data['年份'].min()} - {company_data['年份'].max()}")
                
                # 计算统计指标
                mean_index = company_data['数字化转型指数'].mean()
                median_index = company_data['数字化转型指数'].median()
                max_index = company_data['数字化转型指数'].max()
                min_index = company_data['数字化转型指数'].min()
                
                # 显示统计指标
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("平均指数", f"{mean_index:.4f}")
                with col2:
                    st.metric("中位数", f"{median_index:.4f}")
                with col3:
                    st.metric("最高指数", f"{max_index:.4f}")
                with col4:
                    st.metric("最低指数", f"{min_index:.4f}")
                
                # 绘制趋势图
                st.markdown("### 指数趋势图")
                plot_enterprise_trend(data, company_name, company_data)
                
                # 显示详细数据
                st.markdown("### 详细数据")
                st.dataframe(company_data[['年份', '数字化转型指数']].sort_values('年份'), use_container_width=True)
        
        # 统计分布页面
        elif page == "统计分布":
            st.subheader("📊 统计分布")
            
            # 选择年份
            selected_year = st.selectbox('选择年份:', available_years)
            
            if selected_year:
                # 获取当年数据
                year_data = data[data['年份'] == selected_year]
                
                # 计算统计指标
                mean_index = year_data['数字化转型指数'].mean()
                median_index = year_data['数字化转型指数'].median()
                max_index = year_data['数字化转型指数'].max()
                min_index = year_data['数字化转型指数'].min()
                
                # 显示统计指标
                st.markdown(f"### {selected_year}年行业统计指标")
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("平均指数", f"{mean_index:.4f}")
                with col2:
                    st.metric("中位数", f"{median_index:.4f}")
                with col3:
                    st.metric("最高指数", f"{max_index:.4f}")
                with col4:
                    st.metric("最低指数", f"{min_index:.4f}")
                
                # 绘制分布直方图
                st.markdown("### 指数分布直方图")
                plot_year_distribution(data, selected_year)
                
                # 绘制排名前10企业
                st.markdown("### 排名前10企业")
                plot_top_10(year_data, selected_year)
                
                # 显示当年数据
                st.markdown("### 当年完整数据")
                st.dataframe(
                    year_data[['股票代码', '企业名称', '数字化转型指数']].sort_values('数字化转型指数', ascending=False),
                    use_container_width=True
                )

# 运行应用
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        st.error(f"应用程序运行出错: {e}")
        st.error("请检查数据文件格式或联系技术支持")
        print(f"应用运行出错: {type(e).__name__}: {e}")