#!/usr/bin/env python3
import requests
import time

def test_app_connection():
    """测试应用程序连接"""
    url = "http://localhost:8501"
    
    print("🔍 测试应用程序连接...")
    print(f"🌐 目标地址: {url}")
    
    try:
        # 测试连接
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            print("✅ 连接成功！")
            print("🎉 程序正在正常运行")
            print(f"📊 响应状态码: {response.status_code}")
            print(f"📄 响应大小: {len(response.content)} 字节")
            
            # 检查是否包含Streamlit特征
            if "Streamlit" in response.text:
                print("✅ 确认是Streamlit应用")
            else:
                print("⚠️  可能是其他应用")
                
            print("\n🌐 请在浏览器中访问以下地址：")
            print(f"   {url}")
            print("\n📁 测试文件：")
            print("   示例学生成绩.xlsx")
            
        else:
            print(f"❌ 连接失败，状态码: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到应用程序")
        print("💡 请确保程序正在运行")
        
    except requests.exceptions.Timeout:
        print("❌ 连接超时")
        
    except Exception as e:
        print(f"❌ 发生错误: {e}")

if __name__ == "__main__":
    test_app_connection()
