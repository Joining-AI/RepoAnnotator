// 这行代码是在告诉我们的程序，去加载一个样式文件，这个文件在项目的某个地方，它能让我们的网页看起来更漂亮。
import "@/styles/globals.css";

// 这里我们从一个叫做"next"的工具箱里拿出一个叫Script的东西。这个工具箱能帮助我们做很多网页开发的工作。
import Script from "next/script";

// 下面这行代码是定义了一个特殊的功能，我们把它叫做App。这个功能会根据传入的一些信息，生成我们看到的网页内容。
export default function App({ Component, pageProps }) {

  // 然后我们开始描述App这个功能具体要做的事情：
  
  // 我们先放一段特殊的代码，它会去互联网上的一个地方，找一个叫做"flowbite.min.js"的文件。这个文件里有很多已经写好的代码，可以帮我们快速做出好看的网页按钮、输入框等东西。而且，我们希望这个文件在网页其他部分之前就加载好，这样网页加载起来会更快。
  return (
    <>
      <Script
        src="https://cdnjs.cloudflare.com/ajax/libs/flowbite/1.7.0/flowbite.min.js"
        strategy="beforeInteractive"
      />

      // 接下来，我们把之前提到的Component和pageProps这两样东西用起来。Component就像是一个模板，告诉我们网页上要显示什么内容；而pageProps则是给这个模板提供一些额外的信息，比如用户的数据或者设置。
      // 所以，这里就是让我们的网页按照Component的模板来显示内容，同时把这些额外的信息也用上。
      <Component {...pageProps} />
      
      // 最后，我们用<>和</>把上面的代码包起来，这是为了让它们能在React这个框架里正常工作。
    </>
  );
}

