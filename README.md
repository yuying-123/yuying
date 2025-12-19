# 企业数字化转型指数查询系统

## 项目介绍
这是一个基于Streamlit框架开发的企业数字化转型指数查询与可视化系统，支持通过股票代码和年份查询企业的数字化转型指数，并展示历年指数趋势。

## 功能特点
- 📊 **数据概览**：显示总记录数、年份范围和企业数量
- 🔍 **精确查询**：通过股票代码和年份查询企业数字化转型指数
- 📈 **趋势分析**：展示企业历年数字化转型指数变化趋势
- 📱 **响应式设计**：适配不同设备的显示需求

## 文件结构
```
.
├── stock_index_query_app.py    # 主应用文件
├── 历年数字化转型指数汇总.xlsx    # 数据文件
├── requirements.txt            # 依赖包配置
└── README.md                   # 项目说明
```

## 快速开始

### 本地运行
1. 安装依赖包：
   ```bash
   pip install -r requirements.txt
   ```

2. 运行应用：
   ```bash
   streamlit run stock_index_query_app.py
   ```

3. 在浏览器中打开 http://localhost:8501

### 部署到互联网（所有人可访问）

#### 步骤1：创建GitHub仓库
1. 登录GitHub，创建一个新的**公开**仓库
2. 命名为 `digital-transformation-index`（或其他名称）

#### 步骤2：上传文件
将以下文件上传到GitHub仓库：
- `stock_index_query_app.py`
- `历年数字化转型指数汇总.xlsx`
- `requirements.txt`
- `README.md`

#### 步骤3：部署到Streamlit Cloud
1. 访问 [Streamlit Community Cloud](https://share.streamlit.io/)
2. 点击 "Sign in with GitHub" 登录
3. 点击 "New app"
4. 在 "Repository" 选择你的GitHub仓库
5. 在 "Main file path" 输入 `stock_index_query_app.py`
6. 点击 "Deploy!"

#### 步骤4：获取公开URL
部署完成后，你将获得一个公开URL（如：`https://share.streamlit.io/yourusername/digital-transformation-index/main/stock_index_query_app.py`）

## 使用说明
1. 在左侧选择股票代码
2. 选择要查询的年份
3. 查看查询结果和历年指数趋势图

## 技术栈
- Python 3.7+
- Streamlit - Web应用框架
- Pandas - 数据处理
- Matplotlib - 数据可视化
- Openpyxl - Excel文件读取

## 注意事项
- 确保数据文件与应用文件在同一目录
- 部署时确保仓库为公开仓库，否则无法被Streamlit Cloud访问
- 如果数据文件过大，可能需要考虑数据压缩或使用云存储服务