// 导入React中的useState钩子
import { useState } from "react";

// 定义一个名为PurgeChats的函数组件
export default function PurgeChats() {
  // 使用useState来管理状态，初始状态为空字符串
  const [status, setStatus] = useState(""); 
  // 定义一个处理清除聊天记录的函数
  const handleChatsPurge = (event) => {
    // 阻止表单默认提交行为，避免页面刷新
    event.preventDefault();
    // 清除浏览器的本地存储
    localStorage.clear();
    // 设置状态为"success"，表示操作成功
    setStatus("success");
    // 3秒后将状态设置回空，以便于下次点击时可以再次显示提示信息
    setTimeout(() => {
      setStatus(false);
    }, 3000);
  };

  // 返回JSX代码以渲染UI
  return (
    <>
      <div className="w-full">
        {/* 标题：清除聊天记录 */}
        <h2 className="text-xl font-bold text-gray-800">PURGE CHATS</h2>
        // 创建一个表单，当用户点击提交按钮时调用handleChatsPurge函数
        <form className="py-2" onSubmit={handleChatsPurge}>
          // 提示警告
          <label className="block mb-2 text-sm font-medium text-red-600">
            Warning
          </label>
          // 布局设计，包括警告文字和提交按钮
          <div className="flex flex-col sm:flex-row gap-x-4 gap-y-4">
            // 警告文字说明
            <div
              type="text" // 这里type属性实际上不会起作用，因为这是一个div标签
              className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5"
            >
              The following action will clear all your chat logs. Proceed with caution!
            </div>
            // 提交按钮，触发清除聊天记录的操作
            <button
              type="submit"
              className="h-fit text-white bg-red-600 hover:bg-red-600/80 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm w-full sm:w-auto px-5 py-2.5 text-center"
            >
              Purge
            </button>
          </div>
          // 如果状态是"success"，则显示已清除聊天记录的信息
          {status === "success" && (
            <div className="text-green-600 text-sm font-bold py-1">
              Your chats have been purged!
            </div>
          )}
        </form>
      </div>
    </>
  );
}

