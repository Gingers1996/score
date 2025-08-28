#!/bin/bash

echo "🚀 启动学生成绩计算系统..."
echo "📊 正在启动Streamlit应用..."

# 检查是否已有程序在运行
if pgrep -f "streamlit run app.py" > /dev/null; then
    echo "⚠️  检测到已有程序在运行，正在停止..."
    pkill -f "streamlit run app.py"
    sleep 2
fi

# 启动程序
echo "🎯 启动新程序..."
streamlit run app.py --server.headless true --server.port 8501 &

# 等待程序启动
echo "⏳ 等待程序启动..."
sleep 5

# 检查程序是否成功启动
if curl -s http://localhost:8501 > /dev/null; then
    echo "✅ 程序启动成功！"
    echo "🌐 请在浏览器中访问：http://localhost:8501"
    echo "📁 可以使用 '示例学生成绩.xlsx' 文件进行测试"
    echo ""
    echo "💡 提示："
    echo "   - 按 Ctrl+C 停止程序"
    echo "   - 如果无法访问，请尝试刷新浏览器"
else
    echo "❌ 程序启动失败，请检查错误信息"
fi
