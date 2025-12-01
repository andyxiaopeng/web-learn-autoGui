#!/usr/bin/env python3
"""
测试图像识别功能
"""
import cv2
import numpy as np
from pathlib import Path


def test_image_matching():
    """测试图像匹配功能"""
    print("=" * 50)
    print("测试图像匹配功能")
    print("=" * 50)
    
    # 获取src目录路径
    src_dir = Path(__file__).parent / "src"
    screenshot_path = src_dir / "页面截图.png"
    target_path = src_dir / "目标.png"
    
    # 检查文件是否存在
    if not screenshot_path.exists():
        print(f"❌ 页面截图文件不存在: {screenshot_path}")
        return False
    
    if not target_path.exists():
        print(f"❌ 目标图片文件不存在: {target_path}")
        return False
    
    print("✅ 文件检查通过")
    
    # 读取图片
    screenshot = cv2.imread(str(screenshot_path.resolve()))
    target = cv2.imread(str(target_path.resolve()))
    
    if screenshot is None:
        print(f"❌ 无法读取页面截图: {screenshot_path}")
        return False
        
    if target is None:
        print(f"❌ 无法读取目标图片: {target_path}")
        return False
    
    print("✅ 图片加载成功")
    
    # 获取图片信息
    screenshot_h, screenshot_w = screenshot.shape[:2]
    target_h, target_w = target.shape[:2]
    
    print(f"截图尺寸: {screenshot_w}x{screenshot_h}")
    print(f"目标尺寸: {target_w}x{target_h}")
    
    # 使用模板匹配查找目标
    result = cv2.matchTemplate(screenshot, target, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    
    print(f"匹配度: {max_val:.3f}")
    print(f"最佳匹配位置: ({max_loc[0]}, {max_loc[1]})")
    
    if max_val >= 0.8:
        # 计算目标中心位置
        center_x = max_loc[0] + target_w // 2
        center_y = max_loc[1] + target_h // 2
        print(f"✅ 找到目标! 中心位置: ({center_x}, {center_y})")
        print(f"   置信度: {max_val:.3f}")
        return True
    else:
        print("❌ 未找到目标或匹配度过低")
        print("   建议:")
        print("   1. 检查目标图片是否正确截取")
        print("   2. 尝试降低匹配阈值")
        print("   3. 确保目标在页面截图中存在")
        return False


if __name__ == "__main__":
    test_image_matching()