// 这里我们从"next/router"这个工具箱里拿出一个叫useRouter的小工具，它能帮我们在不同的网页间跳来跳去。
import { useRouter } from "next/router";

// 接下来，我们从React这个大玩具箱里拿出三个小玩具：useState、useEffect和React本身。
// useState是个魔术师，能帮助我们记住一些东西。
// useEffect是个机器人，它会在特定的时候自动做一些事情。
// 而React是我们的超级英雄，能帮助我们创建漂亮的用户界面。
import React, { useState, useEffect } from "react";

// 现在，我们从我们的项目文件夹中找到两个小部件：BotWrapper和HumanWrapper。
// 这两个小部件就像是聊天窗口里的机器人朋友和人类朋友。
import BotWrapper from "@/components/chat/BotWrapper";
import HumanWrapper from "@/components/chat/HumanWrapper";

// 我们再找一个叫做SetSources的小伙伴，它会帮我们设置一些信息来源。
import SetSources from "@/containers/SetSources";

// 下面，我们定义了一个特别的功能，名字叫ChatWindow。
// 这个功能需要一些参数：embedding_model（一种模型）、app_type（应用类型）和setBotTitle（设置机器人标题）。
// 这个功能的主要工作就是创建一个聊天窗口。
export default function ChatWindow({ embedding_model, app_type, setBotTitle }) {

const [bot, setBot] = useState(null); // 这里我们定义了一个叫做“bot”的变量，它开始时是空的（null），这个变量会存储机器人的信息。
const [chats, setChats] = useState([]); // 这个变量“chats”用来存储所有的聊天记录，开始时它是一个空数组。
const [isLoading, setIsLoading] = useState(false); // “isLoading”用来表示机器人是否正在思考回答，开始时是假（false）。
const [selectChat, setSelectChat] = useState(true); // “selectChat”决定是否显示输入框让用户提问，开始时是真（true）。

const router = useRouter(); // 这行代码获取了路由信息，帮助我们知道用户访问的是哪个页面。
const { bot_slug } = router.query; // 从路由中取出“bot_slug”，这是机器人的唯一标识符。

useEffect(() => { // 这段代码会在“bot_slug”改变时运行。
  if (bot_slug) { // 如果我们有“bot_slug”，就会去服务器获取对应的机器人信息。
    const fetchBots = async () => { // 定义一个异步函数来获取机器人数据。
      const response = await fetch("/api/get_bots"); // 向服务器请求所有机器人信息。
      const data = await response.json(); // 把接收到的数据转换成JavaScript对象。
      const matchingBot = data.find((item) => item.slug === bot_slug); // 找到和“bot_slug”匹配的那个机器人。
      setBot(matchingBot); // 更新“bot”变量，存储找到的机器人信息。
      setBotTitle(matchingBot.name); // 更新界面显示的机器人名字。（注意：这里没有定义setBotTitle，可能需要额外的代码来实现这个功能）
    };
    fetchBots(); // 调用函数，开始获取机器人信息。
  }
}, [bot_slug]); // 当“bot_slug”变化时，这段代码会被重新执行。

// 下面的代码和上面的很类似，但是它是为了加载之前保存的聊天记录。
useEffect(() => {
  const storedChats = localStorage.getItem(`chat_${bot_slug}_${app_type}`); // 从浏览器的本地存储中读取聊天记录。
  if (storedChats) { // 如果有保存的聊天记录。
    const parsedChats = JSON.parse(storedChats); // 把字符串形式的聊天记录转换回对象。
    setChats(parsedChats.chats); // 更新“chats”变量，加载这些聊天记录。
  }
}, [app_type, bot_slug]); // 当“app_type”或“bot_slug”变化时，这段代码会被重新执行。

const handleChatResponse = async (e) => { // 这个函数处理用户的提问。
  e.preventDefault(); // 阻止表单默认的提交行为。
  setIsLoading(true); // 开始加载动画，表示机器人正在思考。
  const queryInput = e.target.query.value; // 获取用户在输入框中写的问题。
  e.target.query.value = ""; // 清空输入框，准备下一次提问。
  const chatEntry = { // 创建一条聊天记录，表示用户提问。
    sender: "H", // “H”代表人类。
    message: queryInput, // 记录用户的问题。
  };
  setChats((prevChats) => [...prevChats, chatEntry]); // 更新“chats”变量，添加这条新记录。

  // 接下来，我们向服务器发送请求，获取机器人的回答。
  const response = await fetch("/api/get_answer", {
    method: "POST", // 使用POST方法发送数据。
    body: JSON.stringify({ // 把数据转换成JSON格式。
      query: queryInput, // 用户的问题。
      embedding_model, // 用于处理问题的模型。
      app_type, // 应用程序类型。
    }),
    headers: { // 设置HTTP头部。
      "Content-Type": "application/json", // 告诉服务器数据是JSON格式。
    },
  });

  const data = await response.json(); // 等待服务器返回数据。
  if (response.ok) { // 如果服务器返回成功。
    const botResponse = data.response; // 从数据中取出机器人的回答。
    const botEntry = { // 创建一条聊天记录，表示机器人的回答。
      sender: "B", // “B”代表机器人。
      message: botResponse, // 记录机器人的回答。
    };
    setIsLoading(false); // 停止加载动画。
    setChats((prevChats) => [...prevChats, botEntry]); // 更新“chats”变量，添加这条新记录。
    const savedChats = { // 准备将新的聊天记录保存到本地存储。
      chats: [...chats, chatEntry, botEntry], // 包括用户提问和机器人回答。
    };
    localStorage.setItem( // 保存聊天记录到浏览器的本地存储。
      `chat_${bot_slug}_${app_type}`, // 用机器人的标识和应用程序类型作为键名。
      JSON.stringify(savedChats) // 把聊天记录转换成字符串形式。
    );
  } else { // 如果服务器返回失败。
    router.reload(); // 刷新页面。
  }
};

