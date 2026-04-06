# core.py
# 实现图像识别、鼠标点击、窗口管理等基础功能

import cv2
import numpy as np
import pyautogui
import time
import logging
import config
import win32gui
import win32con

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def find_image(template_path, threshold=0.8):
    """
    在屏幕上查找模板图片（自动转为灰度图匹配）
    返回中心点坐标 (x, y)，未找到返回 None
    """
    # 1. 截屏并转为 OpenCV 格式
    screenshot = pyautogui.screenshot()
    screenshot = np.array(screenshot)
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)

    # 2. 加载模板
    template = cv2.imread(template_path)
    if template is None:
        print(f"[错误] 无法加载图片: {template_path}")
        return None

    # 3. 转为灰度图（关键步骤）
    screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
    template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

    # 4. 模板匹配
    result = cv2.matchTemplate(screenshot_gray, template_gray, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    # 5. 判断是否匹配成功
    if max_val >= threshold:
        h, w = template_gray.shape[:2]
        center_x = max_loc[0] + w // 2
        center_y = max_loc[1] + h // 2
        return (center_x, center_y)
    else:
        return None

def click_image(template_path, threshold=None, delay=None, retry=None):
    """
    查找并点击图片，包含重试机制
    :param template_path: 目标图片路径
    :param threshold: 识别阈值
    :param delay: 点击后的等待时间
    :param retry: 重试次数
    :return: 点击成功返回 True，否则返回 False
    """
    if threshold is None:
        threshold = config.DEFAULT_THRESHOLD
    if delay is None:
        delay = config.CLICK_DELAY
    if retry is None:
        retry = config.RETRY_COUNT

    for attempt in range(retry):
        pos = find_image(template_path, threshold)
        if pos:
            pyautogui.click(pos[0], pos[1])
            time.sleep(delay)
            logging.info(f"点击成功: {template_path}")
            return True
        else:
            logging.warning(f"第 {attempt+1}/{retry} 次重试: 未找到 {template_path}")
            time.sleep(1)
    logging.error(f"多次重试后仍无法点击: {template_path}")
    return False

def wait_for_image(template_path, timeout=None, threshold=None):
    """
    等待目标图片在屏幕上出现
    :param template_path: 目标图片路径
    :param timeout: 最长等待时间（秒）
    :param threshold: 识别阈值
    :return: 在超时时间内找到返回 True，否则返回 False
    """
    if timeout is None:
        timeout = config.WAIT_TIMEOUT
    if threshold is None:
        threshold = config.DEFAULT_THRESHOLD

    start_time = time.time()
    while time.time() - start_time < timeout:
        if find_image(template_path, threshold):
            logging.info(f"图片已出现: {template_path}")
            return True
        time.sleep(0.5)
    logging.error(f"等待图片超时 ({timeout}s): {template_path}")
    return False

def focus_game_window(window_title=None):
    """
    激活游戏窗口（使用 pygetwindow，更稳定）
    如果未安装 pygetwindow，请执行: pip install pygetwindow
    """
    if window_title is None:
        window_title = config.GAME_WINDOW_TITLE

    try:
        import pygetwindow as gw
        windows = gw.getWindowsWithTitle(window_title)
        if not windows:
            logging.error(f"未找到标题包含 '{window_title}' 的窗口")
            return False
        win = windows[0]
        if win.isMinimized:
            win.restore()
        win.activate()
        time.sleep(0.5)  # 等待窗口激活
        logging.info(f"已激活游戏窗口: {win.title}")
        return True
    except ImportError:
        logging.error("请安装 pygetwindow: pip install pygetwindow")
        return False
    except Exception as e:
        logging.error(f"激活窗口失败: {e}")
        return False


def swipe_relative(start_x, start_y, end_x, end_y, duration=1, delay=0.5, window_title=config.GAME_WINDOW_TITLE):
    """
    相对于游戏窗口滑动

    :param start_x, start_y: 相对于窗口左上角的起点坐标
    :param end_x, end_y: 相对于窗口左上角的终点坐标
    :param duration: 滑动持续时间（秒）
    :param delay: 滑动后的等待时间（秒）
    :param window_title: 窗口标题
    """
    hwnd = win32gui.FindWindow(None, window_title)
    if not hwnd:
        print(f"[错误] 未找到窗口: {window_title}")
        return False

    rect = win32gui.GetWindowRect(hwnd)
    left, top = rect[0], rect[1]

    abs_start = (left + start_x, top + start_y)
    abs_end = (left + end_x, top + end_y)

    pyautogui.moveTo(abs_start[0], abs_start[1])
    pyautogui.drag(abs_end[0] - abs_start[0], abs_end[1] - abs_start[1], duration=duration, button='left')
    time.sleep(delay)
    print(f"[操作] 相对滑动: ({start_x},{start_y}) → ({end_x},{end_y})")
    return True

def resize_window(width=1920, height=1080, window_title=config.GAME_WINDOW_TITLE):
    """
    调整窗口大小（不移动位置）
    """
    hwnd = win32gui.FindWindow(None, window_title)
    if not hwnd:
        print(f"未找到窗口: {window_title}")
        return False
    # 设置窗口大小（宽、高）
    win32gui.SetWindowPos(hwnd, win32con.HWND_TOP, 0, 0, width, height, win32con.SWP_NOMOVE)
    print(f"窗口已调整为 {width}x{height}")
    return True


def click_relative(x, y, window_title=config.GAME_WINDOW_TITLE, delay=0.1):
    """
    相对于游戏窗口的坐标点击
    :param x: 相对于窗口左上角的横坐标（像素）
    :param y: 相对于窗口左上角的纵坐标（像素）
    :param window_title: 游戏窗口标题（部分匹配即可）
    :param delay: 点击后等待时间（秒）
    """
    # 查找窗口句柄
    hwnd = win32gui.FindWindow(None, window_title)
    if not hwnd:
        print(f"错误：未找到标题包含 '{window_title}' 的窗口")
        return False

    # 获取窗口位置（相对于屏幕）
    rect = win32gui.GetWindowRect(hwnd)
    left, top = rect[0], rect[1]

    # 计算绝对坐标
    abs_x = left + x
    abs_y = top + y

    # 点击
    pyautogui.click(abs_x, abs_y)
    time.sleep(delay)
    print(f"点击相对坐标 ({x}, {y}) -> 绝对坐标 ({abs_x}, {abs_y})")
    return True

def send_p_enter():
    """
    发送 P 键 + Enter 键
    """
    pyautogui.press('p')
    time.sleep(0.05)  # 极短间隔，防止按键冲突
    pyautogui.press('enter')
    logging.info("已发送按键组合: P + Enter")


def wait_and_press_until(
    target_image_path,      # 检测到该图片时执行按键
    stop_image_path,        # 检测到该图片时停止循环
    check_interval=1.0,     # 每次检测间隔（秒）
    max_loops=None,         # 最大循环次数，防止死循环
    threshold=0.8
):
    """
    循环检测 target_image，检测到就发送 P+Enter，直到 stop_image 出现。
    :param target_image_path: 触发按键的图片路径
    :param stop_image_path: 停止循环的图片路径
    :param check_interval: 每次检测间隔（秒）
    :param max_loops: 最大循环次数（None 表示无限）
    :param threshold: 图像识别阈值
    """

    loop_count = 0
    while max_loops is None or loop_count < max_loops:
        # 优先检查是否应该停止
        if find_image(stop_image_path, threshold):
            logging.info("检测到停止图片，战斗按键循环结束")
            click_image(stop_image_path, delay=2, retry=2)
            break

        # 检测目标图片
        if find_image(target_image_path, threshold):
            logging.info("检测到目标图片，发送 P+Enter")
            send_p_enter()
            # 发送按键后稍等一下，避免重复触发（可选）
            time.sleep(0.5)
        else:
            time.sleep(check_interval)
        loop_count += 1

    if max_loops and loop_count >= max_loops:
        logging.warning("达到最大循环次数，强制退出")