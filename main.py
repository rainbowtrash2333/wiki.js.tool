import configparser

from scipy.stats import describe

from wikijstool import wikijs_tool

if __name__ == "__main__":
    # 创建 ConfigParser 对象
    config = configparser.ConfigParser()

    # 读取配置文件
    config.read(r'E:\Twikura\config.ini')  # 确保文件路径正确

    # 获取配置项
    token = config.get('API', 'token')
    url = config.get('API', 'url')

    tool = wikijs_tool(token, url)
    message = tool.create_page(title='test2', content='#head test', description='desc', path="/home/test2",
                               tags=["tag1", "tag2"])
    print(message)
