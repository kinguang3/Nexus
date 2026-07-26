#为整个项目添加统一的绝对路径
import os


def get_project_root():
    """
    获取项目根目录
    :return: 项目根目录
    abspath: 获取当前文件的绝对路径
    dirname: 获取目录名
    dirname(__file__): 获取当前文件所在目录
    """
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def get_abs_path(relative_path: str) -> str:
    """
    获取绝对路径
    :param relative_path: 相对路径
    :return: 绝对路径
    """
    return os.path.join(get_project_root(), relative_path)


if __name__ == "__main__":
    print(get_abs_path("app_qa.py"))