# config.py
# 存放配置参数，方便统一调整

# 图像识别相关
DEFAULT_THRESHOLD = 0.6      # 模板匹配相似度阈值 (0-1)，越高越精确
CLICK_DELAY = 0.5            # 点击后等待时间（秒）
RETRY_COUNT = 3              # 识别失败时的重试次数

# 超时设置
WAIT_TIMEOUT = 10            # 等待图片出现的最长时间（秒）

# 窗口相关
GAME_WINDOW_TITLE = "LimbusCompany"   # 游戏窗口标题（精确匹配，可用部分匹配）

# 任务相关
MAX_CLAIM_ATTEMPTS = 3      # 自动领取每日奖励时的最大尝试次数