# main.py
# 游戏自动化任务主程序

import time
import logging
from core import click_image, wait_for_image, focus_game_window, swipe_relative, resize_window,click_relative, wait_and_press_until
import config

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def back_main_window():
    """
       回到玻璃窗
    """
    click_image("images/auto_claim_daily_1.png",delay=2)
    logging.info("回到玻璃窗")


def auto_claim_daily():
    """
    自动领取每日奖励
    """
    logging.info("开始执行：自动领取每日奖励")
    back_main_window()
    for attempt in range(config.MAX_CLAIM_ATTEMPTS):
        if click_image('images/event_btn.png', delay=1):
            if click_image('images/daily_gift_get.png', delay=2):
                if click_image('images/auto_change_Cake_3.png', delay=1):
                    logging.info("自动领取每日奖励完成")
                    click_image('images/cancel.png', delay=1)
                    break
                else:
                    click_image('images/cancel.png', delay=1)
                    break
            else:
                click_image('images/cancel.png', delay=1)

            time.sleep(1)
        else:
            continue


def auto_change_Cake():
    """
    自动换饼
    """
    logging.info("开始执行：自动收取任务奖励")
    try:
        if click_image('images/auto_change_Cake_1.png', retry=2):
            if click_image('images/auto_change_Cake_2.png', retry=2):
                if click_image('images/auto_change_Cake_3.png', retry=2) or click_image('images/auto_change_Cake_3 (2).png', retry=2):
                    logging.info("任务奖励收取成功")
                    click_image('images/auto_change_Cake_cancel.png', retry=2)
                    time.sleep(1)
                    back_main_window()

        else:
            logging.info("暂无已完成任务")
    except:
        logging.info("发生错误")


def auto_Experience_Dungeon():
    """
        自动经验副本
    """
    logging.info("开始执行：自动经验副本")
    if click_image('images/auto_Experience_Dungeon_1.png', delay=2, retry=2):
        if click_image('images/auto_Experience_Dungeon_2.png', delay=1, retry=2):
            for _ in range(3):
                swipe_relative(1675, 911, 961, 911)
            click_relative(1651, 733)
            for _ in range(3):
                swipe_relative(190, 535, 190, 900)
            click_relative(180, 488)
            #
            if click_image('images/auto_Experience_Dungeon_6.png', delay=1, retry=2):
                logging.info("开始战斗")
                auto_Battle()

    logging.info("自动经验副本完成")
    time.sleep(1)
    click_image('images/auto_Experience_Dungeon_7.png', delay=1, retry=2)
    back_main_window()



def auto_Spindle_Dungeon():
    """
        自动纺锤副本
    """
    logging.info("开始执行：自动经验副本")
    if click_image('images/auto_Experience_Dungeon_1.png', delay=2, retry=2):
        if click_image('images/auto_Experience_Dungeon_2.png', delay=1, retry=2):
            if click_image('images/auto_Spindle_Dungeon_1.png', delay=1, retry=2):
                click_relative(547, 727, delay=0.5)
                click_relative(970, 748, delay=0.5)
                for _ in range(3):
                    swipe_relative(190, 535, 190, 900)
                click_relative(180, 488)

                if click_image('images/auto_Experience_Dungeon_6.png', delay=1, retry=2):
                    logging.info("开始战斗")
                    auto_Battle()

    logging.info("自动纺锤副本完成")
    time.sleep(1)
    click_image('images/auto_Experience_Dungeon_7.png', delay=2, retry=2)
    back_main_window()


def auto_Battle():
    """
        自动战斗模块
    """
    wait_and_press_until("images/auto_Battle_1.png","images/auto_Battle_2.png")








def run_daily_tasks():
    """
    串联每日任务
    """
    logging.info("====== 开始执行日常任务 ======")
    auto_claim_daily()
    auto_change_Cake()
    auto_Experience_Dungeon()
    auto_Spindle_Dungeon()
    logging.info("====== 日常任务执行完毕 ======")


def main():
    # 1. 激活游戏窗口
    if not focus_game_window():
        logging.error("无法激活游戏窗口，请确认游戏已启动且窗口标题正确")
        return

    # 2. 等待游戏主界面加载（例如等待某个标志性图片出现）
    # 你需要自行截取一个主界面上必定出现的图片，如 images/main_screen_flag.png
    resize_window()
    if not wait_for_image('images/main_screen_flag.png', timeout=20):
        logging.error("游戏主界面未加载成功，请检查窗口是否在前台或图片是否正确")
        return

    # 3. 执行日常任务
    run_daily_tasks()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logging.info("用户中断脚本")
    except Exception as e:
        logging.exception(f"脚本运行出错: {e}")
        input("按 Enter 键退出...")