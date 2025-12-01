#!/usr/bin/env python3
"""
测试完整的自动点击功能
"""
from main import AutoClicker


def test_autoclick():
    """测试自动点击功能"""
    print("=" * 50)
    print("测试自动点击功能")
    print("=" * 50)
    
    clicker = AutoClicker()
    
    # 测试模式
    print("\n1. 测试模式验证...")
    success = clicker.run(mode="test", threshold=0.8)
    
    if success:
        print("✅ 测试模式运行成功")
    else:
        print("❌ 测试模式运行失败")
        return False
    
    print("\n2. 功能说明:")
    print("   - 测试模式：验证图像识别功能，不执行实际点击")
    print("   - 实时模式：捕获当前屏幕，找到目标后自动点击")
    print("   - 匹配阈值：可以根据实际情况调整（0-1之间）")
    
    print("\n3. 使用方法:")
    print("   运行 'uv run python main.py' 选择模式")
    print("   - 选择1：测试模式（安全，仅验证识别）")
    print("   - 选择2：实时模式（会执行实际点击）")
    
    print("\n✅ 所有测试完成!")
    return True


if __name__ == "__main__":
    test_autoclick()