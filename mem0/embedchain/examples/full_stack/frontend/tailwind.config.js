// 这里我们定义了一个配置文件，告诉 Tailwind CSS（一个帮助我们快速设计网页的工具）如何工作。
// 它的类型是根据 'tailwindcss' 模块来的，这样我们就能用它来配置我们的项目。

module.exports = { // 这句话的意思是：我要把接下来的东西“导出”，让别的地方可以使用。
  content: [ // 'content' 是一个数组，里面放的是 Tailwind CSS 需要知道的所有文件的位置。
    "./src/**/*.{js,ts,jsx,tsx,mdx}", // 这行代码说：“请查找 src 文件夹下所有 js、ts、jsx、tsx 和 mdx 的文件。”
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}", // 同上，但这次是在 pages 文件夹下找。
    "./src/containers/**/*.{js,ts,jsx,tsx,mdx}", // 在 containers 文件夹下找。
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}", // 在 components 文件夹下找。
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}", // 在 app 文件夹下找。
    "./node_modules/flowbite/**/*.js", // 在 node_modules 里的 flowbite 文件夹下找所有 js 文件。Flowbite 是另一个设计工具。
  ],
  theme: { // 'theme' 是一个对象，我们可以在这里自定义一些设计风格，比如颜色和字体大小。
    extend: {}, // 'extend' 是一个空对象，意味着我们现在没有添加任何自定义的设计风格。
  },
  plugins: [ // 'plugins' 是一个数组，这里我们可以添加一些插件，让 Tailwind CSS 更强大。
    require("flowbite/plugin"), // 这行代码是说：“我要使用 Flowbite 插件，让它帮助我设计网页。”
  ];
};

