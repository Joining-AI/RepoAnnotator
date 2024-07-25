# 导入了一个叫做WhatsAppBot的类，这个类包含启动WhatsApp机器人的功能。
from embedchain.bots.whatsapp import WhatsAppBot

# 定义了一个叫main的函数，这个函数会创建并启动WhatsApp机器人。
def main():
    # 创建一个WhatsAppBot类的实例，就像用积木搭出一个具体的机器人玩具。
    whatsapp_bot = WhatsAppBot()
    # 让上面创建的WhatsApp机器人开始工作。
    whatsapp_bot.start()

# 检查一下是否直接运行这个文件（而不是作为模块被其他文件导入）。
# 如果是直接运行，就调用main函数来创建和启动WhatsApp机器人。
if __name__ == "__main__":
    main()

