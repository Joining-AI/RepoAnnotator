# 导入pytest库，这是一个用于编写测试用例的库。
import pytest

# 导入responses库，这个库可以帮助我们模拟网络请求和响应。
import responses

# 导入BeautifulSoup库，这是一个帮助我们解析HTML文档的库。
from bs4 import BeautifulSoup

# 下面开始定义我们的第一个测试参数列表。
# 这个列表中的每个元素都是一个HTML标签的例子，这些标签通常被忽略。
# 我们还给每个例子起了个名字（ids），方便我们识别它们。
@pytest.mark.parametrize(
    # 这个变量叫做"ignored_tag"，它会依次取下面列表中的每一个值。
    "ignored_tag",
    # 下面是那些会被忽略的HTML标签的例子：
    [
        # 第一个例子是一个导航栏（nav）标签。
        "<nav>This is a navigation bar.</nav>",
        # 第二个例子是一个侧边栏（aside）标签。
        "<aside>This is an aside.</aside>",
        # 第三个例子是一个表单（form）标签。
        "<form>This is a form.</form>",
        # 第四个例子是一个头部（header）标签。
        "<header>This is a header.</header>",
        # 第五个例子是一个没有脚本执行功能的标签（noscript）。
        "<noscript>This is a noscript.</noscript>",
        # 第六个例子是一个SVG图像标签。
        "<svg>This is an SVG.</svg>",
        # 第七个例子是一个画布（canvas）标签。
        "<canvas>This is a canvas.</canvas>",
        # 第八个例子是一个页脚（footer）标签。
        "<footer>This is a footer.</footer>",
        # 第九个例子是一个脚本（script）标签。
        "<script>This is a script.</script>",
        # 第十个例子是一个样式（style）标签。
        "<style>This is a style.</style>",
    ],
    # 给每个例子起个名字，这样更容易理解。
    ids=["nav", "aside", "form", "header", "noscript", "svg", "canvas", "footer", "script", "style"],
)

# 接下来定义第二个测试参数列表。
# 这个列表包含了一些常见的HTML结构，我们将把上面的"ignored_tag"放到这些结构里。
# 每个例子也有自己的名字（ids）。
@pytest.mark.parametrize(
    # 这个变量叫做"selectee"，它会依次取下面列表中的每一个值。
    "selectee",
    [
        # 第一个例子是一个带有"class"属性的文章标签（article）。
        """
<article class="bd-article">
    <h2>Article Title</h2>
    <p>Article content goes here.</p>
    {ignored_tag}
</article>
""",
        # 第二个例子是一个带有"role"属性的文章标签（article）。
        """
<article role="main">
    <h2>Main Article Title</h2>
    <p>Main article content goes here.</p>
    {ignored_tag}
</article>
""",
        # 第三个例子是一个带有"class"属性的div标签。
        """
<div class="md-content">
    <h2>Markdown Content</h2>
    <p>Markdown content goes here.</p>
    {ignored_tag}
</div>
""",
        # 第四个例子是一个带有"role"属性的div标签。
        """
<div role="main">
    <h2>Main Content</h2>
    <p>Main content goes here.</p>
    {ignored_tag}
</div>
""",
        # 第五个例子是一个带有"class"属性的容器div标签。
        """
<div class="container">
    <h2>Container</h2>
    <p>Container content goes here.</p>
    {ignored_tag}
</div>
        """,
        # 第六个例子是一个带有"class"属性的section标签。
        """
<div class="section">
    <h2>Section</h2>
    <p>Section content goes here.</p>
    {ignored_tag}
</div>
        """,
        # 第七个例子是一个普通的文章标签（article）。
        """
<article>
    <h2>Generic Article</h2>
    <p>Generic article content goes here.</p>
    {ignored_tag}
</article>
        """,
        # 第八个例子是一个主内容标签（main）。
        """
<main>
    <h2>Main Content</h2>
    <p>Main content goes here.</p>
    {ignored_tag}
</main>
""",
    ],
    # 给每个例子起个名字，这样更容易理解。
    ids=[
        "article.bd-article",
        'article[role="main"]',
        "div.md-content",
        'div[role="main"]',
        "div.container",
        "div.section",
        "article",
        "main",
    ],
)

# 这个函数用来测试加载器如何根据选择器和忽略的标签获取数据。
def test_load_data_gets_by_selectors_and_ignored_tags(selectee, ignored_tag, loader, mocked_responses, mocker):

