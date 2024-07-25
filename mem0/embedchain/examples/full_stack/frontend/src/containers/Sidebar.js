// 导入Next.js框架中的Link组件，用于页面间的跳转。
import Link from "next/link";

// 导入Next.js框架中的Image组件，它可以帮助我们更高效地加载图片。
import Image from "next/image";

// 导入React库中的useState和useEffect钩子，这些钩子可以让我们在不需要定义类的情况下，
// 在函数组件中添加一些交互逻辑，比如响应式状态管理和副作用操作。
import React, { useState, useEffect } from "react";

// 导入本地SVG图标文件，这些图标将用作侧边栏中的按钮或链接。
import DrawerIcon from "../../public/icons/drawer.svg";
import SettingsIcon from "../../public/icons/settings.svg";
import BotIcon from "../../public/icons/bot.svg";
import DropdownIcon from "../../public/icons/dropdown.svg";
import TwitterIcon from "../../public/icons/twitter.svg";
import GithubIcon from "../../public/icons/github.svg";
import LinkedinIcon from "../../public/icons/linkedin.svg";

// 定义一个名为Sidebar的React组件，这个组件会渲染出侧边栏的内容。
export default function Sidebar() {

const [bots, setBots] = useState([]);

