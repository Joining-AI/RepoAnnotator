// 这行代码定义了一个默认导出的函数组件，名字叫做BotWrapper。
export default function BotWrapper({ children }) {

  // 下面的return语句中，我们使用了JSX语法（一种HTML和JavaScript的混合写法），来描述这个组件的样子。
  return (

    // 这里使用了JSX中的片段语法<>...</>，因为一个React组件只能返回一个根元素，而这个组件需要返回多个div，所以需要用这个片段包裹起来。
    <>
    
      // 这个div给整个机器人对话框添加了一些样式，比如边角圆润的效果。
      <div className="rounded-lg">

        // 这个div是用来包裹对话框中的头像和消息的容器。
        <div className="flex flex-row items-center">

          // 这个div用来显示机器人的头像，设置成了黑色背景和白色文字，大小是10x10，中间显示一个字母'B'。
          <div className="flex items-center justify-center h-10 w-10 rounded-full bg-black text-white flex-shrink-0">
            B
          </div>

          // 这个div用来显示机器人的消息，设置了白色背景，边角圆润，以及一些内边距和阴影效果，使它看起来更像一个对话气泡。
          <div className="ml-3 text-sm bg-white py-2 px-4 shadow-lg rounded-xl">

            // 这里的{children}表示这个组件可以接收并展示子组件或者文本，也就是机器人要说的话。
            <div>{children}</div>

          </div>

        </div>

      </div>

    // 结束片段语法。
    </>

  );
}

