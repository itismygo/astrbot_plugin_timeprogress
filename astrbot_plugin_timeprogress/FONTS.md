# 字体配置文档

本文档记录了 AstrBot 时间进度卡片插件的字体配置和安装方法。

---

## 📋 字体加载优先级

插件会按以下顺序尝试加载字体:

### 主字体 (标题和百分比)
1. **Google Noto Sans CJK SC** (Linux 推荐 - 无衬线,适合界面)
2. **微软雅黑** (Windows)
3. **文泉驿微米黑** (Linux 备用)
4. **Arial / Liberation Sans** (通用备用)
5. **默认字体** (最后备用)

### 详情字体 (当前值/总值)
1. **Google Noto Sans Mono CJK SC** (Linux 推荐 - 等宽)
2. **Consolas** (Windows)
3. **主字体** (备用)

---

## 🐧 Linux 字体安装

### CentOS / RHEL / Fedora

```bash
# Sans 字体 (无衬线) - 适合界面、网页
dnf install google-noto-sans-cjk-sc-fonts

# Serif 字体 (衬线) - 适合正式文档
dnf install google-noto-serif-cjk-sc-fonts

# Mono 字体 (等宽) - 适合代码编辑
dnf install google-noto-sans-mono-cjk-sc-fonts
```

### Debian / Ubuntu

```bash
# 安装 Google Noto CJK 字体
sudo apt-get update
sudo apt-get install fonts-noto-cjk

# 或者安装文泉驿微米黑 (备用)
sudo apt-get install fonts-wqy-microhei
```

### Arch Linux

```bash
# 安装 Google Noto CJK 字体
sudo pacman -S noto-fonts-cjk

# 或者安装文泉驿微米黑 (备用)
sudo pacman -S wqy-microhei
```

---

## 🪟 Windows 字体

Windows 系统通常已预装以下字体:
- **微软雅黑** (msyh.ttc) - 主字体
- **Consolas** (consola.ttf) - 等宽字体

如果缺失,可以从以下途径获取:
1. 从其他 Windows 系统复制字体文件到 `C:\Windows\Fonts\`
2. 下载并安装 Google Noto CJK 字体

---

## 📂 字体文件路径

### Linux 常见路径

#### Google Noto Sans CJK SC (无衬线)
```
/usr/share/fonts/google-noto-cjk/NotoSansCJK-Regular.ttc
/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc
```

#### Google Noto Sans Mono CJK SC (等宽)
```
/usr/share/fonts/google-noto-cjk/NotoSansMonoCJK-Regular.ttc
/usr/share/fonts/opentype/noto/NotoSansMonoCJK-Regular.ttc
```

#### Google Noto Serif CJK SC (衬线)
```
/usr/share/fonts/google-noto-cjk/NotoSerifCJK-Regular.ttc
/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc
```

#### 文泉驿微米黑 (备用)
```
/usr/share/fonts/truetype/wqy/wqy-microhei.ttc
```

### Windows 常见路径

#### 微软雅黑
```
msyh.ttc
C:\Windows\Fonts\msyh.ttc
```

#### Consolas (等宽)
```
consola.ttf
C:\Windows\Fonts\consola.ttf
```

---

## 🔍 验证字体安装

### Linux

```bash
# 查看已安装的 Noto 字体
fc-list | grep -i noto

# 查看已安装的中文字体
fc-list :lang=zh

# 查看字体详细信息
fc-list | grep -i "noto sans cjk"
```

### 预期输出示例

```
/usr/share/fonts/google-noto-cjk/NotoSansCJK-Regular.ttc: Noto Sans CJK SC:style=Regular
/usr/share/fonts/google-noto-cjk/NotoSansMonoCJK-Regular.ttc: Noto Sans Mono CJK SC:style=Regular
/usr/share/fonts/google-noto-cjk/NotoSerifCJK-Regular.ttc: Noto Serif CJK SC:style=Regular
```

---

## 🎨 字体使用说明

### 插件中的字体配置

插件在 `main.py` 的 `draw_time_card()` 方法中配置字体:

```python
# 主字体路径列表
font_paths = [
    # Google Noto Sans CJK SC (Linux - 无衬线,适合界面)
    "/usr/share/fonts/google-noto-cjk/NotoSansCJK-Regular.ttc",
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    # 微软雅黑 (Windows)
    "msyh.ttc",
    "C:\\Windows\\Fonts\\msyh.ttc",
    # 文泉驿微米黑 (Linux 备用)
    "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
    # Arial (通用备用)
    "arial.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
]

# 详情字体路径 (等宽字体)
detail_font_paths = [
    # Google Noto Sans Mono CJK SC (Linux - 等宽)
    "/usr/share/fonts/google-noto-cjk/NotoSansMonoCJK-Regular.ttc",
    "/usr/share/fonts/opentype/noto/NotoSansMonoCJK-Regular.ttc",
    # Consolas (Windows)
    "consola.ttf",
    "C:\\Windows\\Fonts\\consola.ttf",
] + font_paths
```

### 字体大小

- **标题**: 28px (显示"今天"、"本周"等)
- **百分比**: 18px (显示"35.2%"等)
- **详情**: 11px (显示"8/24 小时"等)

---

## 🐛 故障排除

### 问题: 中文显示为方块 (□□)

**原因**: 系统未安装中文字体

**解决方案**:

1. **Linux**: 安装 Google Noto CJK 字体
   ```bash
   # CentOS/RHEL/Fedora
   dnf install google-noto-sans-cjk-sc-fonts

   # Debian/Ubuntu
   sudo apt-get install fonts-noto-cjk
   ```

2. **检查日志**: 查看 AstrBot 日志中的字体加载信息
   ```
   [INFO] 成功加载字体: /usr/share/fonts/google-noto-cjk/NotoSansCJK-Regular.ttc
   ```
   或
   ```
   [WARN] 无法加载中文字体,使用默认字体,中文可能显示为方块
   ```

3. **重启插件**: 安装字体后重新加载插件

### 问题: 字体加载失败

**检查步骤**:

1. 确认字体文件存在:
   ```bash
   ls -la /usr/share/fonts/google-noto-cjk/
   ```

2. 确认字体权限:
   ```bash
   # 字体文件应该可读
   chmod 644 /usr/share/fonts/google-noto-cjk/*.ttc
   ```

3. 更新字体缓存:
   ```bash
   fc-cache -fv
   ```

4. 查看插件日志:
   ```bash
   # 查看 AstrBot 日志中的字体加载信息
   tail -f /path/to/astrbot/logs/astrbot.log | grep "字体"
   ```

---

## 📚 字体特性对比

| 字体 | 类型 | 适用场景 | 中文支持 | 等宽 |
|------|------|----------|----------|------|
| **Noto Sans CJK SC** | 无衬线 | 界面、网页 | ✅ 完美 | ❌ |
| **Noto Serif CJK SC** | 衬线 | 正式文档 | ✅ 完美 | ❌ |
| **Noto Sans Mono CJK SC** | 无衬线 | 代码、数据 | ✅ 完美 | ✅ |
| **微软雅黑** | 无衬线 | 界面、网页 | ✅ 完美 | ❌ |
| **Consolas** | 无衬线 | 代码、数据 | ❌ 无 | ✅ |
| **文泉驿微米黑** | 无衬线 | 通用 | ✅ 良好 | ❌ |

---

## 🔗 相关资源

- [Google Noto Fonts 官网](https://fonts.google.com/noto)
- [Google Noto CJK GitHub](https://github.com/googlefonts/noto-cjk)
- [文泉驿字体项目](http://wenq.org/)
- [Pillow 字体文档](https://pillow.readthedocs.io/en/stable/reference/ImageFont.html)

---

## 📝 更新日志

### v1.0.0 (2025-11-24)
- ✅ 添加 Google Noto Sans CJK SC 支持
- ✅ 添加 Google Noto Sans Mono CJK SC 支持
- ✅ 优化字体加载逻辑,支持多路径尝试
- ✅ 添加字体加载日志输出
- ✅ 支持 Windows 和 Linux 双平台

---

## 💡 开发者注意事项

### 添加新字体路径

如果需要添加新的字体路径,请在 `main.py` 的 `font_paths` 列表中添加:

```python
font_paths = [
    # 新字体路径
    "/path/to/your/font.ttc",
    # 现有路径...
]
```

### 修改字体大小

在 `draw_time_card()` 方法中修改字体大小参数:

```python
title_font = ImageFont.truetype(font_path, 28)      # 标题大小
percentage_font = ImageFont.truetype(font_path, 18) # 百分比大小
detail_font = ImageFont.truetype(font_path, 11)     # 详情大小
```

### 测试字体加载

可以在插件日志中查看字体加载情况:

```python
logger.info(f"成功加载字体: {font_path}")
logger.warning("无法加载中文字体,使用默认字体,中文可能显示为方块")
```

---

**文档版本**: 1.0.0
**最后更新**: 2025-11-24
**维护者**: TimeProgress Plugin Team
