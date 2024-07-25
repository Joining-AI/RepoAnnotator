# 这里我们从Python的一个特殊模块“enum”中导入了“Enum”。这个模块可以帮助我们创建枚举类型，
# 枚举类型就像是一个特殊的列表，它包含了一些固定的选项，不能随意添加或删除。
from enum import Enum

# 下面开始定义第一个枚举类型“DirectDataType”，它包含了直接存储数据的类型，比如文本。
# 我们这里只定义了一个类型：TEXT，表示纯文本。
class DirectDataType(Enum):
    TEXT = "text"

# 现在定义第二个枚举类型“IndirectDataType”，它包含了那些存储指向其他地方数据的引用的类型，
# 比如YouTube视频、PDF文件等。这些数据并不直接存储在这里，而是通过链接或ID去其他地方找。
class IndirectDataType(Enum):
    YOUTUBE_VIDEO = "youtube_video" # YouTube上的视频
    PDF_FILE = "pdf_file"           # PDF文档
    WEB_PAGE = "web_page"           # 网页
    SITEMAP = "sitemap"             # 网站地图
    XML = "xml"                     # XML文件
    DOCX = "docx"                   # Word文档
    DOCS_SITE = "docs_site"         # 文档网站
    NOTION = "notion"               # Notion文档
    CSV = "csv"                     # CSV表格
    MDX = "mdx"                     # MDX文件（Markdown扩展）
    IMAGE = "image"                 # 图片
    UNSTRUCTURED = "unstructured"   # 非结构化数据
    JSON = "json"                   # JSON格式的数据
    OPENAPI = "openapi"             # OpenAPI规格
    GMAIL = "gmail"                 # Gmail邮件
    SUBSTACK = "substack"           # Substack订阅
    YOUTUBE_CHANNEL = "youtube_channel" # YouTube频道
    DISCORD = "discord"             # Discord聊天
    CUSTOM = "custom"               # 自定义数据
    RSSFEED = "rss_feed"            # RSS订阅源
    BEEHIIV = "beehiiv"             # Beehiiv邮件服务
    GOOGLE_DRIVE = "google_drive"   # Google云端硬盘
    DIRECTORY = "directory"         # 文件夹
    SLACK = "slack"                 # Slack聊天
    DROPBOX = "dropbox"             # Dropbox网盘
    TEXT_FILE = "text_file"         # 文本文件
    EXCEL_FILE = "excel_file"       # Excel文件
    AUDIO = "audio"                 # 音频文件

# 接下来是第三个枚举类型“SpecialDataType”，它包含了既不是直接数据也不是间接数据的特殊类型，
# 或者是需要特别处理的数据类型。这里只有一个类型：QNA_PAIR，表示问答对。
class SpecialDataType(Enum):
    QNA_PAIR = "qna_pair"

# 最后，我们创建了一个“DataType”枚举类型，它把上面所有提到的数据类型都整合在一起。
# 这样做的目的是为了让使用这些数据类型时更方便，不用管它们是直接的、间接的还是特殊的。
class DataType(Enum):
    TEXT = DirectDataType.TEXT.value # 直接的文本数据
    YOUTUBE_VIDEO = IndirectDataType.YOUTUBE_VIDEO.value # YouTube视频的链接
    PDF_FILE = IndirectDataType.PDF_FILE.value # PDF文件的链接
    WEB_PAGE = IndirectDataType.WEB_PAGE.value # 网页的链接
    SITEMAP = IndirectDataType.SITEMAP.value # 网站地图的链接
    XML = IndirectDataType.XML.value # XML文件的链接
    DOCX = IndirectDataType.DOCX.value # Word文档的链接
    DOCS_SITE = IndirectDataType.DOCS_SITE.value # 文档网站的链接
    NOTION = IndirectDataType.NOTION.value # Notion文档的链接
    CSV = IndirectDataType.CSV.value # CSV表格的链接
    MDX = IndirectDataType.MDX.value # MDX文件的链接
    QNA_PAIR = SpecialDataType.QNA_PAIR.value # 问答对的特殊类型
    IMAGE = IndirectDataType.IMAGE.value # 图片的链接
    UNSTRUCTURED = IndirectDataType.UNSTRUCTURED.value # 非结构化数据的链接
    JSON = IndirectDataType.JSON.value # JSON数据的链接
    OPENAPI = IndirectDataType.OPENAPI.value # OpenAPI规格的链接
    GMAIL = IndirectDataType.GMAIL.value # Gmail邮件的链接
    SUBSTACK = IndirectDataType.SUBSTACK.value # Substack订阅的链接
    YOUTUBE_CHANNEL = IndirectDataType.YOUTUBE_CHANNEL.value # YouTube频道的链接
    DISCORD = IndirectDataType.DISCORD.value # Discord聊天的链接
    CUSTOM = IndirectDataType.CUSTOM.value # 自定义数据的链接
    RSSFEED = IndirectDataType.RSSFEED.value # RSS订阅源的链接
    BEEHIIV = IndirectDataType.BEEHIIV.value # Beehiiv邮件服务的链接
    GOOGLE_DRIVE = IndirectDataType.GOOGLE_DRIVE.value # Google云端硬盘的链接
    DIRECTORY = IndirectDataType.DIRECTORY.value # 文件夹的链接
    SLACK = IndirectDataType.SLACK.value # Slack聊天的链接
    DROPBOX = IndirectDataType.DROPBOX.value # Dropbox网盘的链接
    TEXT_FILE = IndirectDataType.TEXT_FILE.value # 文本文件的链接
    EXCEL_FILE = IndirectDataType.EXCEL_FILE.value # Excel文件的链接
    AUDIO = IndirectDataType.AUDIO.value # 音频文件的链接

