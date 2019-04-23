import os

# 返回根目录路径
def get_root_path():
    now_path = os.getcwd()
    while not now_path.endswith("chanpay-test"):
        os.chdir(os.path.abspath('..'))
        now_path = os.getcwd()
    return now_path
