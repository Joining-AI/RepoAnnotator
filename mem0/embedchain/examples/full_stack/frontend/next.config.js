// 这段代码是设置一个叫做Next.js的应用程序的一些特殊规则。
// Next.js是一个帮助我们创建网页的工具。

// 定义一个变量nextConfig，它将包含我们的配置信息。
// 这个变量会告诉Next.js如何工作。
const nextConfig = {

  // 这是一个特殊的功能，叫做重写规则（rewrites）。
  // 当有人尝试访问像"/api/something"这样的地址时，
  // 我们会告诉Next.js把请求转到另一个地方，比如我们的后端服务器。
  // 这样做是为了让前端和后端可以分开工作，但看起来像是一个整体。
  async rewrites() {
    return [
      // 这里是一个具体的规则：
      // 如果有人访问以"/api/"开始的任何网址，
      // 把这个请求转到"http://backend:8000/api/"后面加上原来网址的剩余部分。
      {
        source: "/api/:path*",  // 源地址，匹配以"/api/"开头的任何路径
        destination: "http://backend:8000/api/:path*",  // 目标地址，把请求发送到这里
      },
    ];
  },

  // 这个选项告诉Next.js在开发模式下更严格地检查React组件，
  // 这样可以帮助我们找到并修复错误。
  reactStrictMode: true,

  // 这里是一些实验性的设置，可能还在测试中。
  // 例如，这里设置了一个代理超时时间，如果请求超过这个时间没有响应，就会被取消。
  // 设置为6000000毫秒，也就是10分钟。
  experimental: {
    proxyTimeout: 6000000,
  },

  // Webpack是一个工具，用来把我们的代码打包成浏览器可以理解的形式。
  // 这里我们告诉Webpack如何处理SVG图片文件。
  // SVG是一种可以在网页上显示的图片格式。
  webpack(config) {
    // 添加一个新的规则到Webpack的规则列表中。
    // 当Webpack遇到.svg结尾的文件时，
    // 并且这个文件是在JS或TSX文件中引用的，
    // 使用"@svgr/webpack"这个工具来处理这些SVG文件。
    config.module.rules.push({
      test: /\.svg$/i,  // 匹配所有.svg结尾的文件
      issuer: /\.[jt]sx?$/,  // 确保这个文件是在JS或TSX文件中引用的
      use: ["@svgr/webpack"],  // 使用这个工具来处理SVG文件
    });

    // 最后返回修改后的配置。
    return config;
  },
};

// 把我们定义的nextConfig导出，这样其他文件就可以使用它了。
module.exports = nextConfig;

