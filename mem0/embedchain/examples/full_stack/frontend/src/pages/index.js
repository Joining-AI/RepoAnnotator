// 导入一些组件，这些组件会在页面上显示或做某些事情。
import Wrapper from "@/components/PageWrapper"; // 这是一个包装器，用来让页面看起来更整洁。
import Sidebar from "@/containers/Sidebar"; // 这是侧边栏，通常会显示菜单或者导航。
import CreateBot from "@/components/dashboard/CreateBot"; // 创建机器人的组件。
import SetOpenAIKey from "@/components/dashboard/SetOpenAIKey"; // 设置OpenAI密钥的组件。
import PurgeChats from "@/components/dashboard/PurgeChats"; // 清除聊天记录的组件。
import DeleteBot from "@/components/dashboard/DeleteBot"; // 删除机器人的组件。
import { useEffect, useState } from "react"; // 这些是从React库导入的工具，帮助我们管理页面的状态和执行某些操作。

// 这个函数定义了我们的主页。
export default function Home() {
  // 我们在这里创建了一个叫做isKeyPresent的变量，它开始时设为false。
  const [isKeyPresent, setIsKeyPresent] = useState(false);

  // useEffect是一个特殊的工具，它会在页面加载后自动运行一次。
  useEffect(() => {
    // 这里我们向服务器发送请求，检查OpenAI密钥是否已经设置。
    fetch("/api/check_key")
      .then((response) => response.json()) // 当服务器回应时，我们将结果转换成JSON格式。
      .then((data) => {
        // 如果数据中的状态是"ok"，那么我们把isKeyPresent设为true。
        if (data.status === "ok") {
          setIsKeyPresent(true);
        }
      });
  }, []); // 这里的空数组[]意味着这个操作只在页面首次加载时运行一次。

  // 这部分代码描述了页面上显示的内容。
  return (
    <>
      // 显示侧边栏。
      <Sidebar />
      // 包装器，让内容看起来更美观。
      <Wrapper>
        // 中心对齐的文字和标题。
        <div className="text-center">
          <h1>欢迎来到Embedchain游乐场</h1>
          <p>Embedchain是一个数据平台，用于处理大型语言模型的数据。</p>
        </div>
        // 根据isKeyPresent的值，显示不同的组件。
        <div
          className={`pt-6 gap-y-4 gap-x-8 ${ // 这里设置了一些样式。
            isKeyPresent ? "grid lg:grid-cols-2" : "w-[50%] mx-auto" // 如果密钥存在，显示网格布局；否则，显示更小的宽度。
          `}
        >
          // 允许设置OpenAI密钥的组件。
          <SetOpenAIKey setIsKeyPresent={setIsKeyPresent} />
          // 如果密钥存在，显示以下组件。
          {isKeyPresent && (
            <>
              // 创建机器人的组件。
              <CreateBot />
              // 删除机器人的组件。
              <DeleteBot />
              // 清除聊天记录的组件。
              <PurgeChats />
            </>
          )}
        </div>
      </Wrapper>
    </>
  );
}

