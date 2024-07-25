// 导入 React 中的 useState 函数，这个函数可以帮助我们在组件里记录和更新状态。
import { useState } from "react";

// 导入加号图标文件（PlusIcon）。
import PlusIcon from "../../public/icons/plus.svg";

// 导入叉号图标文件（CrossIcon）。
import CrossIcon from "../../public/icons/cross.svg";

// 导入 YouTube 图标文件（YoutubeIcon）。
import YoutubeIcon from "../../public/icons/youtube.svg";

// 导入 PDF 文件图标文件（PDFIcon）。
import PDFIcon from "../../public/icons/pdf.svg";

// 导入网页图标文件（WebIcon）。
import WebIcon from "../../public/icons/web.svg";

// 导入文档图标文件（DocIcon）。
import DocIcon from "../../public/icons/doc.svg";

// 导入网站地图图标文件（SitemapIcon）。
import SitemapIcon from "../../public/icons/sitemap.svg";

// 导入文本图标文件（TextIcon）。
import TextIcon from "../../public/icons/text.svg";

// 定义一个名为 SetSources 的组件，并让它可以接收参数（比如 { ... } 这样的对象）。
export default function SetSources({

// 这里我们接收了一些来自其他地方的信息，比如setChats用来更新聊天记录，
// embedding_model是一个模型，setSelectChat用来控制选择聊天的状态。
const setChats,
  embedding_model,
  setSelectChat,
}) {

// 我们先设置了一些空的“盒子”，用来放后面要用到的信息。
const [sourceName, setSourceName] = useState(""); // 存储数据来源的名字
const [sourceValue, setSourceValue] = useState(""); // 存储具体的数据值
const [isDropdownOpen, setIsDropdownOpen] = useState(false); // 控制下拉菜单是否打开
const [isLoading, setIsLoading] = useState(false); // 控制是否正在加载

// 下面定义了不同类型的数据，比如YouTube视频、PDF文件等。
const dataTypes = {
  youtube_video: "YouTube Video",
  pdf_file: "PDF File",
  web_page: "Web Page",
  doc_file: "Doc File",
  sitemap: "Sitemap",
  text: "Text",
};

// 对应每种类型，我们还准备了一个图标，让界面看起来更友好。
const dataIcons = {
  youtube_video: <YoutubeIcon className="w-5 h-5 mr-3" />,
  pdf_file: <PDFIcon className="w-5 h-5 mr-3" />,
  web_page: <WebIcon className="w-5 h-5 mr-3" />,
  doc_file: <DocIcon className="w-5 h-5 mr-3" />,
  sitemap: <SitemapIcon className="w-5 h-5 mr-3" />,
  text: <TextIcon className="w-5 h-5 mr-3" />,
};

// 当我们想要关闭下拉菜单时，这个函数会被调用。
const handleDropdownClose = () => {
  setIsDropdownOpen(false); // 关闭下拉菜单
  setSourceName(""); // 清空数据来源的名字
  setSelectChat(true); // 改变选择聊天的状态
};

// 当我们在下拉菜单中选择了某一项时，这个函数会被调用。
const handleDropdownSelect = (dataType) => {
  setSourceName(dataType); // 设置数据来源的名字
  setSourceValue(""); // 清空具体的数据值
  setIsDropdownOpen(false); // 关闭下拉菜单
  setSelectChat(false); // 再次改变选择聊天的状态
};

// 这个函数是在我们添加数据源时调用的，它会处理一系列操作。
const handleAddDataSource = async (e) => {
  e.preventDefault(); // 阻止默认的表单提交行为
  setIsLoading(true); // 开始加载状态

  // 准备要添加的数据源信息
  const addDataSourceEntry = {
    sender: "B",
    message: `Adding the following ${dataTypes[sourceName]}: ${sourceValue}`,
  };
  setChats((prevChats) => [...prevChats, addDataSourceEntry]); // 更新聊天记录

  // 获取数据源的名字和值
  let name = sourceName;
  let value = sourceValue;
  setSourceValue(""); // 清空数据值

  // 发送请求到服务器，添加数据源
  const response = await fetch("/api/add_sources", {
    method: "POST", // 使用POST方法
    body: JSON.stringify({ // 转换数据为JSON格式
      embedding_model,
      name,
      value,
    }),
    headers: { // 设置请求头
      "Content-Type": "application/json",
    },
  });

  // 根据服务器响应做不同的处理
  if (response.ok) { // 如果响应成功
    const successEntry = {
      sender: "B",
      message: `Successfully added ${dataTypes[sourceName]}!`,
    };
    setChats((prevChats) => [...prevChats, successEntry]); // 更新聊天记录
  } else { // 如果响应失败
    const errorEntry = {
      sender: "B",
      message: `Failed to add ${dataTypes[sourceName]}. Please try again.`,
    };
    setChats((prevChats) => [...prevChats, errorEntry]); // 更新聊天记录
  }

  setSourceName(""); // 清空数据来源的名字
  setIsLoading(false); // 结束加载状态
  setSelectChat(true); // 再次改变选择聊天的状态
};

// 下面是界面的部分，用于显示按钮、下拉菜单和输入框。
return (
  <>
    <div className="w-fit"> // 创建一个适合宽度的div容器
      <button // 创建一个按钮，点击时打开或关闭下拉菜单
        type="button"
        onClick={() => setIsDropdownOpen(!isDropdownOpen)}
        className="...style..." // 这里有很多样式，让按钮看起来更好看
      >
        <PlusIcon className="w-6 h-6" /> // 加号图标
      </button>

      {/* 如果下拉菜单是打开的，就显示下拉菜单 */}
      {isDropdownOpen && (
        <div className="...style..." > // 下拉菜单的样式
          <ul className="py-1"> // 列表样式
            <li // 第一项是关闭选项
              className="...style..." // 项的样式
              onClick={handleDropdownClose} // 点击时调用关闭函数
            >
              <span className="flex items-center text-red-600"> // 文字和图标
                <CrossIcon className="w-5 h-5 mr-3" /> // 关闭图标
                Close // 文字
              </span>
            </li>

            {/* 显示所有数据类型的列表 */}
            {Object.entries(dataTypes).map(([key, value]) => (
              <li // 每一项都是可点击的
                key={key} // 唯一标识符
                className="...style..." // 项的样式
                onClick={() => handleDropdownSelect(key)} // 点击时调用选择函数
              >
                <span className="flex items-center"> // 文字和图标
                  {dataIcons[key]} // 图标
                  {value} // 文字
                </span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* 如果选择了数据来源，就显示输入框和发送按钮 */}
      {sourceName && (
        <form // 表单，用于收集数据并提交
          onSubmit={handleAddDataSource} // 提交时调用函数
          className="...style..." // 表单样式
        >
          <div className="w-full"> // 输入框容器
            <input // 输入框，用于输入URL、数据或文件路径
              type="text"
              placeholder="Enter URL, Data or File path here..." // 提示文字
              className="...style..." // 输入框样式
              required // 必填
              value={sourceValue} // 当前值
              onChange={(e) => setSourceValue(e.target.value)} // 改变时更新值
            />
          </div>
          <div className="w-full sm:w-fit"> // 按钮容器
            <button // 发送按钮
              type="submit"
              disabled={isLoading} // 如果正在加载，则禁用按钮
              className={`...style...`} // 按钮样式
            >
              Send // 文字
            </button>
          </div>
        </form>
      )}
    </div>
  </>
);
}

