# 引入embedchain库中的App类，这个类可以帮助我们创建一个智能的应用。
from embedchain import App

# 使用App类的一个方法`from_config`来创建一个应用实例。这个方法会读取一个名为"config.yaml"的配置文件，
# 这个文件告诉应用应该如何运行。
app = App.from_config("config.yaml")

# 把"/path/to/your/folder"这个文件夹里的所有内容添加到应用中去，这样应用就可以学习和理解这些文件了。
# `data_type="directory"`告诉应用这是一个文件夹。
app.add("/path/to/your/folder", data_type="directory")

# 开始一个无限循环，这个循环会一直运行，直到我们让它停下来。
while True:
    # 让用户输入一个问题，然后按回车键。输入会被保存在变量`user_input`里。
    user_input = input("Enter your question (type 'exit' to quit): ")

    # 如果用户输入的是"exit"（不区分大小写），那么就跳出循环，程序结束。
    if user_input.lower() == "exit":
        break

    # 否则，应用会处理用户的输入问题，并给出一个答案，这个答案会被保存在变量`response`里。
    response = app.chat(user_input)

    # 最后，打印出应用给出的答案，这样用户就能看到结果了。
    print(response)

