import streamlit.web.cli as stcli# 导入streamlit命令行接口
import sys# 导入sys模块，用于修改命令行参数

app_file_path = "d:\\Nexus\\Data\\app_file_uploader.py"
sys.argv = ["streamlit", "run", app_file_path, "--server.headless=true", "--browser.gatherUsageStats=false"]# 非交互式模式，默认值为false
# 禁用浏览器统计信息收集，默认值为true
stcli.main()
