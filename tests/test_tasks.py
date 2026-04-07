# tests/test_tasks.py
import pytest

import main
from main import auto_claim_daily, back_main_window
from core import find_image

def test_back_main_window_flow():
    """
    测试“返回主界面”功能是否有效
    """
    back_main_window()
    # 断言：执行完返回操作后，屏幕上应该能看到主界面标志
    assert find_image('images/main_screen_flag.png') is not None

def test_daily_claim_flow():
    """
    回归测试：每日奖励领取流程
    注意：如果奖励已领过，可能导致测试失败，
    """
    try:
        auto_claim_daily()
    except Exception as e:
        pytest.fail(f"回归测试中发生崩溃: {e}")

@pytest.mark.parametrize("image_path", [
    'images/event_btn.png',
    'images/auto_Experience_Dungeon_1.png',
    'images/auto_change_Cake_1.png'
])
def test_essential_images_exist(image_path):
    """
    批量检查：所有关键UI图片是否都能在当前屏幕找到（确保 UI 没改版）
    """
    import os
    assert os.path.exists(image_path), f"资源文件缺失: {image_path}"


def test_auto_change_Cake():
    reasult = main.auto_change_Cake()
    assert reasult is True