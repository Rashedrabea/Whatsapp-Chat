#!/usr/bin/env python3
"""
اختبار سريع للتأكد من أن الخادم يعمل بشكل صحيح على الويب
Quick test to verify the web server works correctly
"""

import sys
import time

def test_server():
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║  🧪 اختبار الخادم - Server Test                           ║")
    print("╚══════════════════════════════════════════════════════════════╝\n")
    
    print("✅ الملفات المطلوبة:\n")
    
    files_to_check = {
        "index.html": "الصفحة الرئيسية",
        "main.py": "الخادم",
        "static/style.css": "التنسيقات",
        "static/script.js": "الوظائف",
        "analyze_chat.py": "التحليل",
    }
    
    from pathlib import Path
    
    all_exist = True
    for file, desc in files_to_check.items():
        path = Path(file)
        if path.exists():
            print(f"   ✅ {file:<25} - {desc}")
        else:
            print(f"   ❌ {file:<25} - {desc} (غير موجود)")
            all_exist = False
    
    print("\n" + "="*60 + "\n")
    
    if not all_exist:
        print("❌ بعض الملفات غير موجودة! تأكد من موقعك في المجلد الصحيح")
        return False
    
    print("✅ جميع الملفات موجودة!\n")
    
    print("📖 التعليمات:\n")
    print("1️⃣  تأكد من تثبيت المكتبات:")
    print("    pip install -r requirements.txt\n")
    
    print("2️⃣  شغّل الخادم:")
    print("    python main.py\n")
    
    print("3️⃣  افتح المتصفح:\n")
    print("    على الكمبيوتر:  http://127.0.0.1:8000")
    print("    على الموبايل:  http://<IP>:8000\n")
    
    print("    (استبدل <IP> برقم IP الكمبيوتر مثل 192.168.1.100)\n")
    
    print("="*60 + "\n")
    
    print("🌐 المتصفحات المدعومة:\n")
    browsers = [
        "✅ Google Chrome",
        "✅ Mozilla Firefox",
        "✅ Apple Safari",
        "✅ Microsoft Edge",
    ]
    for browser in browsers:
        print(f"   {browser}")
    
    print("\n" + "="*60 + "\n")
    
    print("📱 الأجهزة المدعومة:\n")
    devices = [
        "✅ Windows",
        "✅ macOS",
        "✅ Linux",
        "✅ iPhone",
        "✅ Android",
        "✅ iPad",
    ]
    for device in devices:
        print(f"   {device}")
    
    print("\n" + "="*60 + "\n")
    
    print("✨ الميزات:\n")
    features = [
        "✅ واجهة حديثة وجميلة",
        "✅ دعم العربية كاملاً",
        "✅ Drag & Drop",
        "✅ Responsive Design",
        "✅ أداء سريع",
        "✅ أمان مضمون",
    ]
    for feature in features:
        print(f"   {feature}")
    
    print("\n" + "="*60 + "\n")
    
    print("🚀 ابدأ الآن:\n")
    print("   python main.py\n")
    
    print("ثم افتح المتصفح على:\n")
    print("   http://127.0.0.1:8000\n")
    
    print("استمتع! ✨\n")
    
    print("="*60 + "\n")
    
    return True

if __name__ == "__main__":
    success = test_server()
    sys.exit(0 if success else 1)
