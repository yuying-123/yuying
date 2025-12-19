# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import numpy as np
import os
import plotly.express as px
import plotly.graph_objects as go

# 设置页面配置
st.set_page_config(
    page_title="企业数字化转型指数趋势",
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
            
            # 添加应用信息到侧边栏
            st.sidebar.success("数据加载成功！")
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



# 使用Plotly绘制单个公司的趋势图（支持导航）
def plot_trend_with_navigation(company_name, company_data):
    """使用Plotly绘制支持导航的趋势图"""
    fig = px.line(
        company_data,
        x='年份',
        y='数字化转型指数',
        title=f'{company_name} 数字化转型指数趋势',
        markers=True,
        line_shape='linear'
    )
    
    # 增强图表交互功能
    fig.update_layout(
        hovermode='x unified',
        xaxis_title='年份',
        yaxis_title='数字化转型指数',
        dragmode='pan',
        selectdirection='h',
        font=dict(
            family="Microsoft YaHei, SimHei, sans-serif"
        )
    )
    
    # 添加缩放、平移、重置等导航按钮
    fig.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1年", step="year", stepmode="backward"),
                dict(count=3, label="3年", step="year", stepmode="backward"),
                dict(count=5, label="5年", step="year", stepmode="backward"),
                dict(step="all")
            ])
        )
    )
    
    # 显示图表
    st.plotly_chart(fig, use_container_width=True)

# 绘制所有公司所有年份的折线图
def plot_all_companies_trend(data):
    """绘制所有公司所有年份的数字化转型指数趋势图"""
    
    # 计算每年的平均指数（因为公司数量可能很多，直接绘制所有公司会很杂乱）
    annual_avg = data.groupby('年份')['数字化转型指数'].mean().reset_index()
    
    # 计算每年的中位数指数
    annual_median = data.groupby('年份')['数字化转型指数'].median().reset_index()
    
    # 计算每年的最高和最低指数
    annual_min = data.groupby('年份')['数字化转型指数'].min().reset_index()
    annual_max = data.groupby('年份')['数字化转型指数'].max().reset_index()
    
    # 创建图表
    fig = go.Figure()
    
    # 添加平均线
    fig.add_trace(go.Scatter(
        x=annual_avg['年份'],
        y=annual_avg['数字化转型指数'],
        mode='lines+markers',
        name='平均指数',
        line=dict(color='blue', width=3)
    ))
    
    # 添加中位数线
    fig.add_trace(go.Scatter(
        x=annual_median['年份'],
        y=annual_median['数字化转型指数'],
        mode='lines+markers',
        name='中位数指数',
        line=dict(color='green', width=2, dash='dash')
    ))
    
    # 添加最高和最低指数区域
    fig.add_trace(go.Scatter(
        x=annual_min['年份'],
        y=annual_min['数字化转型指数'],
        mode='lines',
        name='最低指数',
        line=dict(color='red', width=1),
        fill=None
    ))
    
    fig.add_trace(go.Scatter(
        x=annual_max['年份'],
        y=annual_max['数字化转型指数'],
        mode='lines',
        name='最高指数',
        line=dict(color='red', width=1),
        fill='tonexty',
        fillcolor='rgba(255, 0, 0, 0.1)'
    ))
    
    # 更新布局
    fig.update_layout(
        title='所有公司数字化转型指数年度趋势',
        xaxis_title='年份',
        yaxis_title='数字化转型指数',
        hovermode='x unified',
        dragmode='pan',
        selectdirection='h',
        font=dict(
            family="Microsoft YaHei, SimHei, sans-serif"
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    # 添加导航控件
    fig.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1年", step="year", stepmode="backward"),
                dict(count=3, label="3年", step="year", stepmode="backward"),
                dict(count=5, label="5年", step="year", stepmode="backward"),
                dict(step="all")
            ])
        )
    )
    
    # 显示图表
    st.plotly_chart(fig, use_container_width=True)

# 模拟绘制地图功能（基于企业分布）
def plot_company_map(data):
    """绘制企业分布地图（模拟数据）"""
    # 获取企业名称和股票代码
    companies = data[['企业名称', '股票代码']].drop_duplicates()
    
    # 为演示添加模拟的地理位置数据
    # 实际应用中，这里应该使用真实的企业地址经纬度数据
    companies['经度'] = np.random.uniform(73, 135, len(companies))
    companies['纬度'] = np.random.uniform(18, 53, len(companies))
    
    # 计算每个企业的平均数字化转型指数
    avg_index = data.groupby('企业名称')['数字化转型指数'].mean().reset_index()
    companies = companies.merge(avg_index, on='企业名称')
    
    # 绘制地图
    fig = px.scatter_mapbox(
        companies,
        lat="纬度",
        lon="经度",
        hover_name="企业名称",
        hover_data=["股票代码", "数字化转型指数"],
        color="数字化转型指数",
        size="数字化转型指数",
        color_continuous_scale=px.colors.cyclical.IceFire,
        size_max=15,
        zoom=4,
        title="企业数字化转型指数地图分布"
    )
    
    fig.update_layout(
        mapbox_style="carto-positron",
        margin={"r":0,"t":50,"l":0,"b":0},
        font=dict(
            family="Microsoft YaHei, SimHei, sans-serif"
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)



# 主函数
def main():
    # 设置应用标题
    st.title("📊 企业数字化转型指数趋势查询")
    st.markdown("---")
    
    # 加载数据
    data = load_data()
    
    if data is not None:
        # 获取股票代码列表
        available_stocks = sorted(data['股票代码'].unique())
        
        # 选择企业
        selected_stock = st.selectbox('选择股票代码:', available_stocks)
        
        if selected_stock:
            # 获取企业名称
            company_name = data[data['股票代码'] == selected_stock]['企业名称'].iloc[0]
            
            # 获取企业历史数据
            company_full_data = data[data['股票代码'] == selected_stock].sort_values('年份')
            
            # 添加年份范围选择
            min_year = company_full_data['年份'].min()
            max_year = company_full_data['年份'].max()
            available_years = sorted(company_full_data['年份'].unique())
            
            # 创建年份选择器
            st.markdown("#### 选择年份范围")
            col_start, col_end = st.columns(2)
            with col_start:
                start_year = st.selectbox(
                    '开始年份',
                    options=available_years,
                    index=0
                )
            with col_end:
                # 获取可选的结束年份
                available_end_years = [year for year in available_years if year >= start_year]
                # 选择默认结束年份（可选年份中的最大值）
                default_end_year = max(available_end_years) if available_end_years else start_year
                # 获取默认索引
                default_index = available_end_years.index(default_end_year) if available_end_years else 0
                
                end_year = st.selectbox(
                    '结束年份',
                    options=available_end_years,
                    index=default_index
                )
            
            # 设置选中的年份范围
            selected_years = (start_year, end_year)
            
            # 根据选择的年份过滤数据
            company_data = company_full_data[(company_full_data['年份'] >= selected_years[0]) & (company_full_data['年份'] <= selected_years[1])].sort_values('年份')
            
            # 绘制趋势图（支持导航）
            st.markdown(f"### {company_name} ({selected_stock}) 数字化转型指数趋势")
            plot_trend_with_navigation(company_name, company_data)
    
    # 绘制所有公司的整体趋势
    st.markdown("### 所有公司数字化转型指数整体趋势")
    plot_all_companies_trend(data)
    
    # 添加地图可视化
    st.markdown("### 企业数字化转型指数地图分布")
    plot_company_map(data)

# 运行应用
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        st.error(f"应用程序运行出错: {e}")
        st.error("请检查数据文件格式或联系技术支持")
        print(f"应用运行出错: {type(e).__name__}: {e}")