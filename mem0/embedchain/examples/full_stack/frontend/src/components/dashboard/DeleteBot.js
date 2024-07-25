// 引入React中的useEffect和useState钩子函数
import { useEffect, useState } from "react";
// 引入Next.js的路由工具，用于页面导航
import { useRouter } from "next/router";

// 定义一个名为DeleteBot的组件
export default function DeleteBot() {
  // 使用useState创建一个状态变量bots，初始值为空数组
  const [bots, setBots] = useState([]);
  // 使用useRouter获取路由对象，可以用来重载页面
  const router = useRouter();

  // 使用useEffect执行副作用，当组件挂载时运行一次
  useEffect(() => {
    // 定义一个异步函数fetchBots来获取机器人数据
    const fetchBots = async () => {
      // 发送GET请求到"/api/get_bots"获取机器人数据
      const response = await fetch("/api/get_bots");
      // 将响应体转换为JSON格式的数据
      const data = await response.json();
      // 更新状态变量bots，设置为从服务器获取的数据
      setBots(data);
    };
    // 调用fetchBots函数
    fetchBots();
  }, []); // 依赖数组为空，意味着这个副作用只在组件挂载时运行一次

  // 定义一个处理删除机器人的函数handleDeleteBot
  const handleDeleteBot = async (event) => {
    // 阻止表单默认提交行为
    event.preventDefault();
    // 获取被选中的机器人slug
    const selectedBotSlug = event.target.bot_name.value;
    // 如果没有选择任何机器人，则直接返回不做任何操作
    if (selectedBotSlug === "none") {
      return;
    }
    // 发送POST请求到"/api/delete_bot"删除指定的机器人
    const response = await fetch("/api/delete_bot", {
      // 请求方法为POST
      method: "POST",
      // 请求体包含要删除的机器人的slug
      body: JSON.stringify({ slug: selectedBotSlug }),
      // 设置请求头Content-Type为application/json
      headers: {
        "Content-Type": "application/json",
      },
    });

    // 如果服务器响应成功，则刷新页面
    if (response.ok) {
      router.reload();
    }
  };

  // 返回JSX代码，渲染删除机器人界面
  return (
    <>
      {/* 当bots数组不为空时显示以下内容 */}
      {bots.length !== 0 && (
        <div className="w-full">
          {/* 标题：删除机器人 */}
          <h2 className="text-xl font-bold text-gray-800">DELETE BOTS</h2>
          {/* 删除机器人的表单 */}
          <form className="py-2" onSubmit={handleDeleteBot}>
            {/* 标签：机器人列表 */}
            <label className="block mb-2 text-sm font-medium text-gray-900">
              List of Bots
            </label>
            {/* 下拉菜单和删除按钮 */}
            <div className="flex flex-col sm:flex-row gap-x-4 gap-y-4">
              {/* 下拉菜单，用于选择要删除的机器人 */}
              <select
                name="bot_name"
                defaultValue="none"
                className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5"
              >
                {/* 默认选项 */}
                <option value="none">Select a Bot</option>
                {/* 根据bots数组动态生成下拉菜单选项 */}
                {bots.map((bot) => (
                  <option key={bot.slug} value={bot.slug}>
                    {bot.name}
                  </option>
                ))}
              </select>
              {/* 删除按钮 */}
              <button
                type="submit"
                className="h-fit text-white bg-red-600 hover:bg-red-600/90 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm w-full sm:w-auto px-5 py-2.5 text-center"
              >
                Delete
              </button>
            </div>
          </form>
        </div>
      )}
    </>
  );
}

