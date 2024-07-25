# 定义一个函数create_app，接收三个参数：ctx（上下文）、app_name（应用名称）和docker（是否在Docker中运行）
def create_app(ctx, app_name, docker):

# 定义了一个叫做 start 的函数，它接受一个名字叫 docker 的参数。
def start(docker):
    # 如果 docker 参数是真（比如：不是空或者False），那么就执行下面这两行代码。
    if docker:
        # 这行代码会运行一个命令，启动一个叫做 docker-compose 的工具，并让它执行 up 命令。
        # 这个 up 命令会让 docker-compose 启动配置好的所有服务。
        subprocess.run(["docker-compose", "up"], check=True)
        # 函数结束，不再往下执行。
        return

    # 这两行代码设置了一些信号处理程序，当程序收到特定的信号时，会调用 signal_handler 函数。
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # 下面开始第一步：启动 API 服务器。
    try:
        # 改变当前的工作目录到 "api" 文件夹。
        os.chdir("api")
        # 使用 python 解释器运行 main 模块，并创建一个后台进程，这个进程就是我们的 API 服务器。
        api_process = subprocess.Popen(["python", "-m", "main"], stdout=None, stderr=None)
        # 把工作目录改回来，回到原来的文件夹。
        os.chdir("..")
        # 打印一条消息，告诉用户 API 服务器已经成功启动。
        console.print("✅ [bold green]API server started successfully.[/bold green]")
    # 如果在尝试启动 API 服务器的过程中出现了错误，就会执行这里的代码。
    except Exception as e:
        # 打印一条错误消息，告诉用户启动 API 服务器失败，并显示具体的错误信息。
        console.print(f"❌ [bold red]Failed to start the API server: {e}[/bold red]")
        # 发送一些匿名数据，记录这次启动失败的信息。
        anonymous_telemetry.capture(event_name="ec_start", properties={"success": False})
        # 函数结束，不再往下执行。
        return

    # 让程序暂停两秒钟，让用户有时间读取上面的消息。
    time.sleep(2)

    # 第二步：安装 UI 的依赖并启动 UI 服务器。
    try:
        # 改变当前的工作目录到 "ui" 文件夹。
        os.chdir("ui")
        # 运行 yarn 命令来安装项目中的依赖。
        subprocess.run(["yarn"], check=True)
        # 创建一个后台进程来启动 UI 服务器。
        ui_process = subprocess.Popen(["yarn", "dev"])
        # 打印一条消息，告诉用户 UI 服务器已经成功启动。
        console.print("✅ [bold green]UI server started successfully.[/bold green]")
        # 发送一些匿名数据，记录这次启动成功的信息。
        anonymous_telemetry.capture(event_name="ec_start", properties={"success": True})
    # 如果在尝试启动 UI 服务器的过程中出现了错误，就会执行这里的代码。
    except Exception as e:
        # 打印一条错误消息，告诉用户启动 UI 服务器失败，并显示具体的错误信息。
        console.print(f"❌ [bold red]Failed to start the UI server: {e}[/bold red]")
        # 发送一些匿名数据，记录这次启动失败的信息。
        anonymous_telemetry.capture(event_name="ec_start", properties={"success": False})

    # 让程序等待，直到 API 和 UI 服务器都被停止。
    try:
        api_process.wait()
        ui_process.wait()
    # 如果用户按下 Ctrl+C (中断信号)，则执行这里的代码。
    except KeyboardInterrupt:
        # 打印一条消息，告诉用户正在停止服务器。
        console.print("\n🛑 [bold yellow]Stopping server...[/bold yellow]")

# 这个函数用来运行Streamlit类型的应用。
def run_dev_streamlit_io():
    # 首先，它创建了一个列表，里面包含了运行Streamlit应用所需的命令。
    streamlit_run_cmd = ["streamlit", "run", "app.py"]
    
    # 然后尝试打印出一条信息，告诉你正在用什么命令运行Streamlit应用。
    try:
        console.print(f"🚀 [bold cyan]Running Streamlit app with command: {' '.join(streamlit_run_cmd)}[/bold cyan]")
        
        # 接着，它会实际运行这个命令。
        subprocess.run(streamlit_run_cmd, check=True)
        
    # 如果在运行过程中出现错误，它会打印出错误信息。
    except subprocess.CalledProcessError as e:
        console.print(f"❌ [bold red]An error occurred: {e}[/bold red]")
        
    # 如果用户按下了Ctrl+C（也就是键盘中断），它会通知你服务器已经停止了。
    except KeyboardInterrupt:
        console.print("\n🛑 [bold yellow]Streamlit server stopped[/bold yellow]")

