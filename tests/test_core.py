# tests/test_core.py
import pytest
from core import find_image, wait_for_image
import config

def test_find_main_screen():
    """
    验证主界面标志图是否能被识别（回归测试中最基础的一环）
    """
    # 假设主界面有个 flag 图片
    pos = find_image('images/main_screen_flag.png', threshold=0.8)
    assert pos is not None, "主界面标志未找到，识别算法或图片可能失效"
    assert len(pos) == 2

def test_wait_timeout():
    """
    验证等待图片的超时机制是否正常（故意找一个不存在的图）
    """
    result = wait_for_image('images/non_existent.png', timeout=2)
    assert result is False, "wait_for_image 应该在找不到图片时返回 False"