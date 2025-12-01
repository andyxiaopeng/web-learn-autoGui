import cv2
import numpy as np
import pyautogui
import time
import os
from PIL import Image
from pathlib import Path


class AutoClicker:
    def __init__(self):
        # 设置pyautogui的安全措施
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.5
        
        # 获取src目录路径
        self.src_dir = Path(__file__).parent / "src"
        self.screenshot_path = self.src_dir / "页面截图.png"
        self.target_path = self.src_dir / "目标.png"
        
    def load_images(self):
        """加载页面截图和目标图片"""
        if not self.screenshot_path.exists():
            raise FileNotFoundError(f"页面截图文件不存在: {self.screenshot_path}")
        if not self.target_path.exists():
            raise FileNotFoundError(f"目标图片文件不存在: {self.target_path}")
            
        # 使用PIL读取图片，然后转换为OpenCV格式
        screenshot_pil = Image.open(self.screenshot_path)
        target_pil = Image.open(self.target_path)
        
        # 转换为OpenCV格式
        screenshot = cv2.cvtColor(np.array(screenshot_pil), cv2.COLOR_RGB2BGR)
        target = cv2.cvtColor(np.array(target_pil), cv2.COLOR_RGB2BGR)
            
        return screenshot, target
    
    def find_target_position(self, screenshot, target, threshold=0.8):
        """在截图中查找目标位置"""
        # 获取目标图片的尺寸
        target_h, target_w = target.shape[:2]
        
        # 使用模板匹配查找目标
        result = cv2.matchTemplate(screenshot, target, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        
        print(f"匹配度: {max_val:.3f} (阈值: {threshold})")
        
        if max_val >= threshold:
            # 计算目标中心位置
            center_x = max_loc[0] + target_w // 2
            center_y = max_loc[1] + target_h // 2
            return center_x, center_y, max_val
        else:
            return None, None, max_val
    
    def click_target(self, x, y, offset_x=0, offset_y=0):
        """点击指定位置"""
        # 应用偏移量
        click_x = x + offset_x
        click_y = y + offset_y
        
        print(f"目标位置: ({x}, {y}), 偏移量: ({offset_x}, {offset_y}), 实际点击位置: ({click_x}, {click_y})")
        
        # 移动鼠标到目标位置
        pyautogui.moveTo(click_x, click_y, duration=0.5)
        
        # 点击
        pyautogui.click()
        
        print("点击完成!")

    def move_target(self, x, y, offset_x=0, offset_y=0):
        """移动到指定位置"""
        # 应用偏移量
        click_x = x + offset_x
        click_y = y + offset_y
        
        print(f"目标位置: ({x}, {y}), 偏移量: ({offset_x}, {offset_y}), 实际点击位置: ({click_x}, {click_y})")
        
        # 移动鼠标到目标位置
        pyautogui.moveTo(click_x, click_y, duration=0.5)
        
        print("移动完成!")
    
    def capture_current_screen(self):
        """捕获当前屏幕"""
        screenshot = pyautogui.screenshot()
        screenshot_cv = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        return screenshot_cv
    
    def run(self, mode="test", threshold=0.8, loop=True, interval=2.0, max_attempts=None, offset_x=0, offset_y=0):
        """
        运行自动点击程序
        
        Args:
            mode: "test" - 测试模式，使用现有的截图文件
                  "live" - 实时模式，捕获当前屏幕并查找目标
            threshold: 匹配阈值，范围0-1
            loop: 是否循环执行
            interval: 循环间隔时间（秒）
            max_attempts: 最大尝试次数，None表示无限循环
        """
        print("=" * 50)
        print("自动点击程序启动")
        print(f"运行模式: {mode}")
        print(f"匹配阈值: {threshold}")
        print(f"循环模式: {loop}")
        if loop:
            print(f"检查间隔: {interval}秒")
            if max_attempts:
                print(f"最大尝试次数: {max_attempts}")
        print("=" * 50)
        
        attempt_count = 0
        target_found = False
        
        try:
            while True:
                attempt_count += 1
                
                # 检查是否达到最大尝试次数
                if max_attempts and attempt_count > max_attempts:
                    print(f"已达到最大尝试次数 {max_attempts}，程序退出")
                    break
                
                if mode == "test":
                    # 测试模式：使用现有截图
                    if attempt_count == 1:
                        print("使用测试模式，加载现有截图...")
                        screenshot, target = self.load_images()
                    else:
                        print("测试模式：重复使用现有截图...")
                else:
                    # 实时模式：捕获当前屏幕
                    print(f"第 {attempt_count} 次检查，捕获当前屏幕...")
                    screenshot = self.capture_current_screen()
                    if attempt_count == 1:
                        _, target = self.load_images()
                
                # 查找目标位置
                x, y, confidence = self.find_target_position(screenshot, target, threshold)
                
                if x is not None and y is not None:
                    print(f"找到目标! 位置: ({x}, {y}), 置信度: {confidence:.3f}")
                    target_found = True
                    
                    if mode == "live":
                        # 实时模式下执行点击
                        self.click_target(x, y, offset_x, offset_y)
                        # self.move_target(x, y, offset_x, offset_y)      # 测试使用
                        
                        # 点击后等待一段时间再继续
                        if loop:
                            print(f"点击完成，等待 {interval} 秒后继续检查...")
                            time.sleep(interval)
                        else:
                            break
                    else:
                        print("测试模式：仅显示位置，不执行点击")
                        if not loop:
                            break
                        else:
                            print(f"等待 {interval} 秒后继续检查...")
                            time.sleep(interval)
                else:
                    print(f"未找到目标，最高匹配度: {confidence:.3f}")
                    if not loop:
                        print("建议:")
                        print("1. 检查目标图片是否正确")
                        print("2. 尝试降低匹配阈值")
                        print("3. 确保目标在当前屏幕可见")
                        break
                    else:
                        print(f"等待 {interval} 秒后重新检查...")
                        time.sleep(interval)
                
        except KeyboardInterrupt:
            print("\n用户中断程序")
            return True
        except Exception as e:
            print(f"程序运行出错: {e}")
            return False
        
        if target_found:
            print("程序执行完成，成功找到并处理目标!")
        else:
            print("程序执行完成，未找到目标")
        
        return True


def main():
    """主函数"""
    clicker = AutoClicker()
    
    print("请选择运行模式:")
    print("1. 测试模式 (使用现有截图)")
    print("2. 实时模式 (捕获屏幕并点击)")
    
    choice = input("请输入选择 (1 或 2): ").strip()
    
    if choice == "1":
        mode = "test"
    elif choice == "2":
        mode = "live"
    else:
        print("无效选择，使用测试模式")
        mode = "test"
    
    # 询问是否使用循环模式
    loop_choice = input("是否启用循环模式? (y/n, 默认y): ").strip().lower()
    loop = loop_choice != 'n'
    
    # 循环模式下的参数设置
    interval = 2.0  # 默认2秒间隔
    max_attempts = None  # 默认无限循环
    
    if loop:
        try:
            interval_input = input("请输入检查间隔时间(秒，默认2.0): ").strip()
            if interval_input:
                interval = float(interval_input)
            
            max_attempts_input = input("请输入最大尝试次数(留空表示无限循环): ").strip()
            if max_attempts_input:
                max_attempts = int(max_attempts_input)
        except ValueError:
            print("输入无效，使用默认值")
    
    # 可以调整匹配阈值，默认0.8
    try:
        threshold_input = input("请输入匹配阈值(0-1, 默认0.8): ").strip()
        threshold = float(threshold_input) if threshold_input else 0.8
        threshold = max(0.0, min(1.0, threshold))  # 确保在0-1范围内
    except ValueError:
        threshold = 0.8
    
    # 获取鼠标点击偏移量
    offset_x = 0
    offset_y = 0
    try:
        offset_x_input = input("请输入X轴偏移量(像素，默认0): ").strip()
        if offset_x_input:
            offset_x = int(offset_x_input)
        
        offset_y_input = input("请输入Y轴偏移量(像素，默认0): ").strip()
        if offset_y_input:
            offset_y = int(offset_y_input)
    except ValueError:
        print("偏移量输入无效，使用默认值0")
    
    print("\n程序配置:")
    print(f"运行模式: {mode}")
    print(f"循环模式: {'是' if loop else '否'}")
    if loop:
        print(f"检查间隔: {interval}秒")
        if max_attempts:
            print(f"最大尝试次数: {max_attempts}")
        else:
            print("最大尝试次数: 无限循环")
    print(f"匹配阈值: {threshold}")
    print(f"鼠标偏移量: X={offset_x}, Y={offset_y}")
    print("\n按 Ctrl+C 可以随时停止程序")
    input("按回车键开始运行...")
    
    # 运行程序
    success = clicker.run(mode, threshold, loop, interval, max_attempts, offset_x, offset_y)
    
    if success:
        print("\n程序执行完成!")
    else:
        print("\n程序执行失败!")


if __name__ == "__main__":
    main()
