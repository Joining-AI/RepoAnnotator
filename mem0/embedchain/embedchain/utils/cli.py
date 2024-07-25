# 导入一些需要使用的工具包
import os
# 这个 `os` 是用来处理文件路径和检查文件是否存在等功能的。
import re
# `re` 是用来处理字符串中的一些特殊模式（正则表达式）的，但在这段代码里并没有用到它。
import shutil
# `shutil` 提供了高级操作文件的功能，比如复制、移动文件等。
import subprocess
# `subprocess` 可以帮助我们在程序里面执行其他命令行指令。
import pkg_resources
# `pkg_resources` 用于获取 Python 包的一些信息，比如安装位置。
from rich.console import Console
# `Console` 来自于 `rich` 库，可以帮助我们更漂亮地在控制台输出文字，比如加颜色。

console = Console()
# 创建一个 `Console` 实例，方便后面打印带有颜色和样式的文字。

def get_pkg_path_from_name(template: str):
    # 这个函数是用来找到某个模板在 `embedchain` 包里的具体位置的。
    try:
        # 尝试找到 `embedchain` 这个包的安装位置。
        package_path = pkg_resources.resource_filename("embedchain", "")
    except ImportError:
        # 如果找不到 `embedchain` 包，就输出错误信息并返回。
        console.print("❌ [bold red]Failed to locate the 'embedchain' package. Is it installed?[/bold red]")
        return

    # 构造模板的具体路径，比如 `embedchain/deployment/template`。
    src_path = os.path.join(package_path, "deployment", template)

    # 检查这个路径是否存在，如果不存在，则输出错误信息并返回。
    if not os.path.exists(src_path):
        console.print(f"❌ [bold red]Template '{template}' not found.[/bold red]")
        return

    # 如果一切正常，返回模板的完整路径。
    return src_path

def setup_fly_io_app(extra_args):
    # 这个函数用来设置 `fly.io` 平台上应用的部署。
    fly_launch_command = ["fly", "launch", "--region", "sjc", "--no-deploy"] + list(extra_args)
    # 构造一个命令列表，用来告诉 `fly` 命令行工具如何部署应用。
    try:
        # 输出将要执行的命令。
        console.print(f"🚀 [bold cyan]Running: {' '.join(fly_launch_command)}[/bold cyan]")
        # 把 `.env.example` 文件重命名为 `.env`，通常 `.env` 文件是用来保存环境变量的。
        shutil.move(".env.example", ".env")
        # 执行 `fly` 命令。
        subprocess.run(fly_launch_command, check=True)
        # 如果命令执行成功，输出成功信息。
        console.print("✅ [bold green]'fly launch' executed successfully.[/bold green]")
    except subprocess.CalledProcessError as e:
        # 如果命令执行出错，输出错误信息。
        console.print(f"❌ [bold red]An error occurred: {e}[/bold red]")
    except FileNotFoundError:
        # 如果没有找到 `fly` 命令，提示用户确保已经安装了 `Fly CLI` 工具。
        console.print(
            "❌ [bold red]'fly' command not found. Please ensure Fly CLI is installed and in your PATH.[/bold red]"
        )

def setup_modal_com_app(extra_args):
    # 这个函数用来设置 `modal.com` 平台上应用的部署。
    modal_setup_file = os.path.join(os.path.expanduser("~"), ".modal.toml")
    # 构造 `modal` 配置文件的路径，通常会放在用户的主目录下。
    if os.path.exists(modal_setup_file):
        # 如果配置文件已经存在，输出提示信息。
        console.print(
            """✅ [bold green]Modal setup already done. You can now install the dependencies by doing \n
            `pip install -r requirements.txt`[/bold green]"""
        )
    else:
        # 如果配置文件不存在，构造并执行 `modal setup` 命令来创建配置文件。
        modal_setup_cmd = ["modal", "setup"] + list(extra_args)
        console.print(f"🚀 [bold cyan]Running: {' '.join(modal_setup_cmd)}[/bold cyan]")
        subprocess.run(modal_setup_cmd, check=True)
    # 把 `.env.example` 文件重命名为 `.env`。
    shutil.move(".env.example", ".env")
    # 输出下一步的操作指引。
    console.print(
        """Great! Now you can install the dependencies by doing: \n
                  `pip install -r requirements.txt`\n
                  \n
                  To run your app locally:\n
                  `ec dev`
                  """
    )

def setup_render_com_app():
    # 这个函数用来设置 `render.com` 平台上应用的部署。
    render_setup_file = os.path.join(os.path.expanduser("~"), ".render/config.yaml")
    # 构造 `render` 配置文件的路径，通常会放在用户的主目录下。
    if os.path.exists(render_setup_file):
        # 如果配置文件已经存在，输出提示信息。
        console.print(
            """✅ [bold green]Render setup already done. You can now install the dependencies by doing \n
            `pip install -r requirements.txt`[/bold green]"""
        )
    else:
        # 如果配置文件不存在，构造并执行 `render config init` 命令来创建配置文件。
        render_setup_cmd = ["render", "config", "init"]
        console.print(f"🚀 [bold cyan]Running: {' '.join(render_setup_cmd)}[/bold cyan]")
        subprocess.run(render_setup_cmd, check=True)
    # 把 `.env.example` 文件重命名为 `.env`。
    shutil.move(".env.example", ".env")
    # 输出下一步的操作指引。
    console.print(
        """Great! Now you can install the dependencies by doing: \n
                  `pip install -r requirements.txt`\n
                  \n
                  To run your app locally:\n
                  `ec dev`
                  """
    )

def setup_streamlit_io_app():
    # 这个函数用来设置 `streamlit.io` 平台上应用的部署，但这里没有需要特别做的步骤。
    console.print("Great! Now you can install the dependencies by doing `pip install -r requirements.txt`")

def setup_gradio_app():
    # 这个函数用来设置 `gradio` 应用的部署，同样这里也没有需要特别做的步骤。
    console.print("Great! Now you can install the dependencies by doing `pip install -r requirements.txt`")

def setup_hf_app():

# 这个函数用来读取环境变量文件，并把它们变成字典形式返回。
def read_env_file(env_file_path):
    """
    这里是函数的说明文档，告诉别人这个函数是用来做什么的，需要什么参数，以及返回什么样的结果。
    """

    # 初始化一个空字典，用来存放环境变量。
    env_vars = {}

    # 使用正则表达式编译工具，提前准备好模式，这样在查找的时候可以更快。
    pattern = re.compile(r"(\w+)=(.*)")

    # 打开文件并读取所有行。`with open`确保文件使用完后会被自动关闭。
    with open(env_file_path, "r") as file:
        # 一次性读取所有行到列表中。
        lines = file.readlines()

        # 遍历每一行。
        for line in lines:
            # 去掉行尾的空白字符（比如换行符）。
            line = line.strip()

            # 如果这行不是空的并且不是以 `#` 开头（即不是注释），就继续处理。
            if line and not line.startswith("#"):
                # 假设每一行都是格式 `KEY=VALUE` 的形式。
                key_value_match = pattern.match(line)

                # 如果匹配成功，那么就获取 `KEY` 和 `VALUE`。
                if key_value_match:
                    key, value = key_value_match.groups()

                    # 把 `KEY` 和 `VALUE` 加入到字典中。
                    env_vars[key] = value

    # 最后返回装有环境变量的字典。
    return env_vars

def deploy_render():

