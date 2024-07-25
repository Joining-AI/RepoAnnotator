// 这里我们从一个地方（就像从一个箱子里）拿出了一些工具
// 第一个工具叫 Wrapper，它帮助我们包装页面，让页面看起来更漂亮
import Wrapper from "@/components/PageWrapper";
// 第二个工具是 Sidebar，它会在页面的一边显示一些菜单或信息
import Sidebar from "@/containers/Sidebar";
// 第三个工具是 ChatWindow，它就像是一个聊天窗口，我们可以在这里和机器人说话
import ChatWindow from "@/containers/ChatWindow";
// 第四个工具是 useState，它来自 react，能帮我们记住一些东西，比如机器人的名字
import { useState } from "react";
// 最后一个工具是 Head，它来自 next.js，用来设置网页的标题
import Head from "next/head";

// 现在我们要做一个应用程序，就像做一个玩具屋，我们给它起名叫 App
export default function App() {
  // 我们用 useState 工具来记住机器人的名字，现在这个名字是空的，什么也没有
  const [botTitle, setBotTitle] = useState("");
  
  // 然后我们开始搭建我们的玩具屋
  return (
    // 这里我们用 <> 和 </> 来围住我们玩具屋的所有部分，就像是用大箱子装所有玩具
    <>
      // 首先，我们用 Head 工具来设置玩具屋的名字，这个名字会显示在浏览器的标签上
      <Head>
        <title>{botTitle}</title>
      </Head>
      // 接下来，我们把 Sidebar 这个工具放进去，这样在玩具屋的一边就有了一个漂亮的菜单
      <Sidebar />
      // 然后，我们用 Wrapper 把主要的部分包装起来，让它看起来更整洁
      <Wrapper>
        // 在这里，我们放进了 ChatWindow，这是玩具屋的核心，我们可以在这里和机器人聊天
        <ChatWindow
          // 我们告诉 ChatWindow 使用 open_ai 的模型来理解我们的话
          embedding_model="open_ai"
          // 我们还告诉它，这是一个应用类型的聊天窗口
          app_type="app"
          // 如果机器人有了名字，我们就用 setBotTitle 来记住它
          setBotTitle={setBotTitle}
        />
      </Wrapper>
    // 最后，我们关上了大箱子，玩具屋就完成了
    </>
  );
}

