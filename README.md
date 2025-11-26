# AstrBot 时间进度卡片插件

一个用于生成精美时间进度可视化卡片的 AstrBot 插件。

## 功能特点

- 生成高清时间进度卡片图片
- 支持多种时间维度：今天、本月、本年
- 使用 Playwright 浏览器渲染，保证最佳清晰度
- 支持自定义时区设置
- 自动处理闰年和大小月
- 简洁美观的卡片设计

## 效果预览

卡片展示时间进度，包含：
- 当前进度值和总值
- 进度条可视化
- 百分比显示

## 安装

### 1. 安装插件

将插件放入 AstrBot 的插件目录中。

### 2. 安装依赖

本插件依赖 Playwright 进行图片渲染，请确保安装：

```bash
pip install playwright
playwright install chromium
```

## 使用方法

发送以下命令查看时间进度：

```
/time   # 查看今天的时间进度（0-24小时）
/month  # 查看本月的时间进度（1-28/29/30/31天）
/year   # 查看本年的时间进度（1-365/366天）
```

## 配置项

在插件配置中可以设置以下选项：

| 配置项 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| `timezone` | string | `Asia/Shanghai` | 时区设置，如 `Asia/Shanghai`（北京）、`UTC`、`America/New_York` 等 |
| `debug_time` | bool | `false` | 开启后会在日志中输出详细的时间信息，用于调试时间不准确的问题 |

## 常见时区

- `Asia/Shanghai` - 北京时间
- `Asia/Tokyo` - 东京时间
- `America/New_York` - 纽约时间
- `Europe/London` - 伦敦时间
- `UTC` - 协调世界时

## 技术实现

- 使用 Playwright 无头浏览器渲染 HTML 模板
- 2 倍分辨率渲染，确保高清输出
- 自动清理临时文件

## 作者

**Willixrain**

## 许可证

MIT License

## 相关链接

- [GitHub 仓库](https://github.com/itismygo/astrbot_plugin_timeprogress)
- [AstrBot 项目](https://github.com/Soulter/AstrBot)
