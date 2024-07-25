// 我们从一个神奇的地方导入一些工具，这些工具帮助我们构建网页。
import { Html, Head, Main, NextScript } from "next/document";

// 现在，我们要定义一个特别的功能，叫做Document，它会告诉我们网页长什么样子。
export default function Document() {
  // 这里，我们开始描述整个网页的外观，就像画一幅大图。
  return (
    // 我们说这个网页的语言是英文，这样全世界的人都能看懂。
    <Html lang="en">
      // 接下来，我们要放一些东西在网页的头部，比如我们的帽子。
      <Head>
        // 这里，我们从互联网上拿了一个漂亮的样式表，让我们的网页看起来更酷。
        <link
          href="https://cdnjs.cloudflare.com/ajax/libs/flowbite/1.7.0/flowbite.min.css"
          rel="stylesheet"
        />
      </Head>
      // 现在，我们要开始写网页的主体部分，就像写信的正文。
      <body>
        // 这个地方，我们会放网页的主要内容，就像是故事的主角。
        <Main />
        // 最后，我们需要一些特别的脚本，它们会在网页加载完之后做些事情。
        <NextScript />
      </body>
    </Html>
  );
}

