// 这里我们定义了一个叫做 HumanWrapper 的特殊“礼物盒”。
// 它可以用来包装一些内容，让它看起来像是一个人形小卡片。
export default function HumanWrapper({ children }) { // 函数的名字叫 HumanWrapper，它接收一个特别的礼物（children），就是你想放在卡片里面的东西。
  return ( // 现在我们要描述这个卡片长什么样子。
    <>
      <div className="rounded-lg"> // 首先，整个卡片是圆角的，看起来很舒服。
        <div className="flex items-center justify-start flex-row-reverse"> // 卡片里面，我们会放两样东西并排，但是顺序是从右向左排列。
          <div className="flex items-center justify-center h-10 w-10 rounded-full bg-blue-800 text-white flex-shrink-0"> // 第一样东西是一个蓝色圆形的小框框，大小是10x10，中间写了个白色的字母H。
            H // 这个字母H就放在那个蓝色圆形框框的正中间。
          </div>
          <div className="mr-3 text-sm bg-blue-200 py-2 px-4 shadow-lg rounded-xl"> // 第二样东西是一个稍微大一点的蓝色矩形框，有阴影效果，看起来很酷。
            <div>{children}</div> // 在这个框框里面，我们会放上你给我的那个特别的礼物（children）。
          </div>
        </div>
      </div>
    </>
  );
}

