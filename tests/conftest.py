# tests/conftest.py
import pytest
import sys
import os

# 将根目录加入路径，确保能导入 core 和 main
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core import focus_game_window, resize_window

@pytest.fixture(scope="session", autouse=True)
def prepare_game():
    """
    所有测试开始前的准备工作：激活并调整窗口大小
    """
    print("\n[Setup] 正在准备游戏环境...")
    assert focus_game_window() is True, "无法激活游戏窗口，测试终止"
    resize_window()
    yield
    print("\n[Teardown] 测试结束")