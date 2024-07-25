// 这是一个特殊的函数，它会被其他部分的代码调用，来生成我们看到的网页布局。
export default function PageWrapper({ children }) {
  // 下面开始写这个函数里面的内容，用来描述网页的样子。

  // 我们要返回一些东西，这些“东西”就是网页上的布局和内容。
  return (
    // 使用<>和</>来包裹我们的布局，这叫做Fragment，就像是用一张大纸把所有的小纸片包起来。
    <>
      // 这是一个<div>标签，就像是一块大的积木，我们要在这个积木里放其他小积木。
      <div className="flex pt-4 px-4 sm:ml-64 min-h-screen">
        // 在这个大积木里，我们再放一个小一点的积木，它会根据屏幕大小自动调整位置和大小。
        <div className="flex-grow pt-4 px-4 rounded-lg">
          // 这里的{children}就像是变魔术一样，它会显示其他地方传进来的任何东西，比如文字、图片或其他积木。
          {children}
        </div>
      </div>
    </>
  );
}

