// 导入React中的useState功能，用来处理组件内的状态变化。
import { useState } from "react";
// 导入Next.js框架中的useRouter功能，用于页面间的导航跳转。
import { useRouter } from "next/router";

// 使用export default定义一个名为CreateBot的函数组件。
export default function CreateBot() {
  // 使用useState初始化botName状态，初始值为空字符串。
  const [botName, setBotName] = useState("");
  // 使用useState初始化status状态，初始值为空字符串。
  const [status, setStatus] = useState("");
  // 使用useRouter获取路由管理器。
  const router = useRouter();

  // 定义一个异步函数handleCreateBot，用于处理创建机器人的逻辑。
  const handleCreateBot = async (e) => {
    // 阻止表单默认提交行为，避免页面刷新。
    e.preventDefault();
    // 创建一个data对象，包含要创建的机器人的名字。
    const data = {
      name: botName,
    };

    // 发送POST请求到"/api/create_bot"接口，请求体包含data对象。
    const response = await fetch("/api/create_bot", {
      method: "POST", // 请求方法为POST。
      headers: { // 设置请求头。
        "Content-Type": "application/json", // 指定数据格式为JSON。
      },
      body: JSON.stringify(data), // 将data对象转换成JSON字符串作为请求体。
    });

    // 如果响应成功（HTTP状态码200-299）：
    if (response.ok) {
      // 将botName转换为小写并替换空格为下划线，形成slug。
      const botSlug = botName.toLowerCase().replace(/\s+/g, "_");
      // 跳转到新创建机器人的详情页。
      router.push(`/${botSlug}/app`);
    } else { // 如果响应失败：
      // 清空botName输入框。
      setBotName("");
      // 设置status状态为"fail"，表示创建失败。
      setStatus("fail");
      // 3秒后清空status状态，移除错误提示。
      setTimeout(() => {
        setStatus("");
      }, 3000);
    }
  };

  // 返回React组件结构：
  return (
    // 开始返回HTML结构...
    <>
      <div className="w-full">
        {/* 页面标题：创建机器人 */}
        <h2 className="text-xl font-bold text-gray-800">CREATE BOT</h2>
        <form className="py-2" onSubmit={handleCreateBot}>
          {/* 标签：机器人名称 */}
          <label
            htmlFor="bot_name"
            className="block mb-2 text-sm font-medium text-gray-900"
          >
            Name of Bot
          </label>
          {/* 输入框和按钮布局 */}
          <div className="flex flex-col sm:flex-row gap-x-4 gap-y-4">
            {/* 文本输入框 */}
            <input
              type="text"
              id="bot_name"
              className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5"
              placeholder="Eg. Naval Ravikant" // 示例文本
              required // 必填项
              value={botName} // 绑定输入框值
              onChange={(e) => setBotName(e.target.value)} // 更新botName状态
            />
            {/* 提交按钮 */}
            <button
              type="submit"
              className="h-fit text-white bg-black hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm w-full sm:w-auto px-5 py-2.5 text-center"
            >
              Submit
            </button>
          </div>
          {/* 错误提示信息 */}
          {status === "fail" && (
            <div className="text-red-600 text-sm font-bold py-1">
              An error occurred while creating your bot!
            </div>
          )}
        </form>
      </div>
    </>
  );
}

