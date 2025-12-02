# AstrBot 时间进度卡片插件

一个用于生成精美时间进度可视化卡片的 AstrBot 插件。

## 功能特点

- 生成高清时间进度卡片图片
- 支持多种时间维度：今天、本周、本月、本年
- 年度进度支持两种可视化样式：进度条和点阵矩阵
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

### /time - 今天时间进度

显示今天的时间进度卡片。

**基础用法：**
```
/time
```
显示从 0:00 到当前时间的进度（0-24小时）

**自定义时间段：**
```
/time 14:00 21:00
```
显示从 14:00 到 21:00 的时间进度（7小时）

**跨天时间段：**
```
/time 22:00 02:00
```
显示从今天 22:00 到明天 02:00 的进度（4小时）

**说明：**
- 时间格式必须为 `HH:MM`（24小时制）
- 当结束时间小于开始时间时，自动识别为跨天
- 支持任意时间段的进度可视化

### /week - 本周进度

显示本周的时间进度卡片。

**用法：**
```
/week
```
显示本周已过天数和总天数（1-7天，周一为第1天）

**说明：**
- 周一为一周的开始，周日为一周的结束
- 精确到小时级别的进度计算

### /month - 本月进度

显示本月的时间进度卡片。

**用法：**
```
/month
```
显示本月已过天数和总天数（1-28/29/30/31天）

**说明：**
- 自动处理大小月和闰年
- 精确到小时级别的进度计算

### /year - 本年进度

显示本年的时间进度卡片，支持两种可视化样式。

**用法：**
```
/year
```
显示进度条样式（默认）

```
/year 0
```
显示进度条样式

```
/year 1
```
显示点阵矩阵样式（19×20 网格，每个点代表一天）

**说明：**
- 自动识别闰年（365/366天）
- 精确到小时级别的进度计算
- 点阵矩阵样式：已过天数显示为白色，当天显示为琥珀色并带有脉冲动画，未来天数显示为灰色

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

## 自定义字体

插件默认使用 [霞鹜文楷](https://github.com/lxgw/LxgwWenKai) 字体。如需更换为其他字体，请按以下步骤操作：

### 更换字体方法

1. **准备字体文件**
   - 下载你想使用的 TTF 格式字体文件
   - 确保字体支持中文显示

2. **替换字体文件**
   - 进入插件目录下的 `fonts` 文件夹
   - 将原有的 `LXGWWenKai-Regular.ttf` 文件备份或删除
   - 将新字体文件重命名为 `LXGWWenKai-Regular.ttf` 并放入该目录

3. **重启 AstrBot**
   - 重启后插件会自动加载新字体

### 推荐字体

| 字体名称 | 风格 | 下载地址 |
|---------|------|----------|
| 霞鹜文楷 | 楷体，优雅 | [GitHub](https://github.com/lxgw/LxgwWenKai) |
| 思源黑体 | 黑体，现代 | [GitHub](https://github.com/adobe-fonts/source-han-sans) |
| 思源宋体 | 宋体，传统 | [GitHub](https://github.com/adobe-fonts/source-han-serif) |
| 得意黑 | 现代创意 | [GitHub](https://github.com/atelier-anchor/smiley-sans) |
| 仓耳今楷 | 楷体变体 | [仓耳字库](http://tsanger.cn/) |

### 注意事项

- 字体文件必须是 `.ttf` 格式
- 文件名必须为 `LXGWWenKai-Regular.ttf`（区分大小写）
- 如果字体文件不存在或加载失败，插件会自动使用系统备用字体（Noto Sans CJK SC）
- 较大的字体文件可能会略微增加图片生成时间

## 技术实现

- 使用 Playwright 无头浏览器渲染 HTML 模板
- 高分辨率渲染（2-3 倍），确保高清输出
- 点阵矩阵样式采用 CSS Grid 布局和动画效果
- 字体文件通过 Base64 编码嵌入 HTML，确保跨平台一致性
- 自动清理临时文件

## 作者

**Willixrain**

## 许可证

MIT License

## 相关链接

- [GitHub 仓库](https://github.com/itismygo/astrbot_plugin_timeprogress)
- [AstrBot 项目](https://github.com/Soulter/AstrBot)
