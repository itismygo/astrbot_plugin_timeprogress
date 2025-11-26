"""
AstrBot 时间进度卡片插件
使用 Playwright 浏览器渲染获得最高清晰度
"""

import os
import tempfile
import calendar
from datetime import datetime
from zoneinfo import ZoneInfo
from playwright.async_api import async_playwright
from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
from astrbot.api import logger


@register(
    "astrbot_plugin_timeprogress",
    "TimeProgress",
    "生成时间进度可视化卡片图片",
    "1.3.0",
    "https://github.com/example/astrbot_plugin_timeprogress"
)
class TimeProgressPlugin(Star):
    """时间进度卡片插件"""

    def __init__(self, context: Context):
        super().__init__(context)
        logger.info("时间进度卡片插件已加载")

    def parse_time_string(self, time_str: str):
        """解析时间字符串为小时和分钟"""
        try:
            parts = time_str.strip().split(':')
            if len(parts) != 2:
                return None
            hour = int(parts[0])
            minute = int(parts[1])
            if not (0 <= hour <= 23 and 0 <= minute <= 59):
                return None
            return (hour, minute)
        except (ValueError, AttributeError):
            return None

    def calculate_time_data(self, start_time: str = None, end_time: str = None) -> dict:
        """
        计算今天的时间数据

        Returns:
            包含时间数据的字典
        """
        # 获取配置
        config = self.context.get_config()
        timezone_str = config.get("timezone", "Asia/Shanghai")
        debug_time = config.get("debug_time", False)

        # 获取当前时间 - 支持时区
        try:
            tz = ZoneInfo(timezone_str)
            now = datetime.now(tz)
            if debug_time:
                logger.info(f"[时间调试] 使用时区: {timezone_str}")
        except Exception as e:
            logger.warning(f"时区 {timezone_str} 无效,使用系统本地时间: {e}")
            now = datetime.now()
            if debug_time:
                logger.info(f"[时间调试] 使用系统本地时间")

        # 输出调试信息
        if debug_time:
            logger.info(f"[时间调试] 当前时间: {now.strftime('%Y-%m-%d %H:%M:%S')}")
            logger.info(f"[时间调试] 年: {now.year}, 月: {now.month}, 日: {now.day}")
            logger.info(f"[时间调试] 时: {now.hour}, 分: {now.minute}, 秒: {now.second}")

        # 如果提供了自定义时间段
        if start_time and end_time:
            start_parsed = self.parse_time_string(start_time)
            end_parsed = self.parse_time_string(end_time)

            if start_parsed and end_parsed:
                start_h, start_m = start_parsed
                end_h, end_m = end_parsed

                current_hours = now.hour + (now.minute / 60)
                start_hours = start_h + (start_m / 60)
                end_hours = end_h + (end_m / 60)

                # 判断是否跨天
                if end_hours < start_hours:
                    # 跨天情况
                    total_hours = (24 - start_hours) + end_hours

                    # 计算当前进度（考虑跨天）
                    if current_hours >= start_hours:
                        # 当前时间在今天的开始时间之后
                        elapsed_hours = current_hours - start_hours
                    else:
                        # 当前时间在明天（已过午夜）
                        elapsed_hours = (24 - start_hours) + current_hours

                    elapsed_hours = max(0, min(elapsed_hours, total_hours))
                else:
                    # 同一天
                    total_hours = end_hours - start_hours
                    elapsed_hours = max(0, min(current_hours - start_hours, total_hours))

                percentage = (elapsed_hours / total_hours) * 100 if total_hours > 0 else 0

                return {
                    "title": f"{start_time}-{end_time}",
                    "current": f"{elapsed_hours:.1f}",
                    "total": f"{total_hours:.1f}",
                    "unit": "小时",
                    "percentage": percentage
                }

        # 默认行为：0:00 到当前时间
        hours = now.hour
        minutes = now.minute
        current_value = hours + (minutes / 60)
        total_value = 24
        percentage = (current_value / total_value) * 100

        return {
            "title": "今天",
            "current": str(hours),
            "total": "24",
            "unit": "小时",
            "percentage": percentage
        }

    def calculate_month_data(self) -> dict:
        """计算本月的时间数据"""
        config = self.context.get_config()
        timezone_str = config.get("timezone", "Asia/Shanghai")
        debug_time = config.get("debug_time", False)

        try:
            tz = ZoneInfo(timezone_str)
            now = datetime.now(tz)
            if debug_time:
                logger.info(f"[时间调试] 使用时区: {timezone_str}")
        except Exception as e:
            logger.warning(f"时区 {timezone_str} 无效,使用系统本地时间: {e}")
            now = datetime.now()

        total_days = calendar.monthrange(now.year, now.month)[1]
        hours_today = now.hour + (now.minute / 60)
        current_value = (now.day - 1) + (hours_today / 24)
        percentage = (current_value / total_days) * 100

        if debug_time:
            logger.info(f"[时间调试] 本月: {now.day}/{total_days}天, 进度{percentage:.1f}%")

        return {
            "title": "本月",
            "current": str(now.day),
            "total": str(total_days),
            "unit": "天",
            "percentage": percentage
        }

    def calculate_week_data(self) -> dict:
        """计算本周的时间数据"""
        config = self.context.get_config()
        timezone_str = config.get("timezone", "Asia/Shanghai")
        debug_time = config.get("debug_time", False)

        try:
            tz = ZoneInfo(timezone_str)
            now = datetime.now(tz)
            if debug_time:
                logger.info(f"[时间调试] 使用时区: {timezone_str}")
        except Exception as e:
            logger.warning(f"时区 {timezone_str} 无效,使用系统本地时间: {e}")
            now = datetime.now()

        weekday = now.weekday()
        current_day = weekday + 1
        hours_today = now.hour + (now.minute / 60)
        current_value = (current_day - 1) + (hours_today / 24)
        percentage = (current_value / 7) * 100

        if debug_time:
            logger.info(f"[时间调试] 本周: 第{current_day}天/7天, 进度{percentage:.1f}%")

        return {
            "title": "本周",
            "current": str(current_day),
            "total": "7",
            "unit": "天",
            "percentage": percentage
        }

    def calculate_year_data(self) -> dict:
        """计算本年的时间数据"""
        config = self.context.get_config()
        timezone_str = config.get("timezone", "Asia/Shanghai")
        debug_time = config.get("debug_time", False)

        try:
            tz = ZoneInfo(timezone_str)
            now = datetime.now(tz)
            if debug_time:
                logger.info(f"[时间调试] 使用时区: {timezone_str}")
        except Exception as e:
            logger.warning(f"时区 {timezone_str} 无效,使用系统本地时间: {e}")
            now = datetime.now()

        total_days = 366 if calendar.isleap(now.year) else 365
        day_of_year = now.timetuple().tm_yday
        hours_today = now.hour + (now.minute / 60)
        current_value = (day_of_year - 1) + (hours_today / 24)
        percentage = (current_value / total_days) * 100

        if debug_time:
            logger.info(f"[时间调试] 本年: 第{day_of_year}天/{total_days}天, 进度{percentage:.1f}%")

        return {
            "title": "本年",
            "current": str(day_of_year),
            "total": str(total_days),
            "unit": "天",
            "percentage": percentage
        }

    async def draw_time_card(self, data: dict) -> str:
        """
        使用 Playwright 异步渲染 HTML 生成高清时间卡片图片

        Args:
            data: 时间数据字典

        Returns:
            图片文件路径
        """
        # HTML 模板 - 基于原始 TimeCard.tsx 设计
        html_template = f'''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        @font-face {{
            font-family: 'Noto Sans CJK SC';
            src: local('Noto Sans CJK SC'), local('NotoSansCJKsc-Regular');
        }}

        body {{
            font-family: 'Noto Sans CJK SC', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Microsoft YaHei UI', sans-serif;
            background: #F2F2F7;
            padding: 0;
            margin: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            width: 680px;
            height: 360px;
        }}

        .card {{
            width: 680px;
            height: 360px;
            background: white;
            border-radius: 40px;
            padding: 40px;
            box-shadow: 0 8px 30px rgba(0, 0, 0, 0.04);
            border: 1px solid rgba(255, 255, 255, 0.5);
            display: flex;
            flex-direction: column;
        }}

        .title {{
            font-size: 72px;
            font-weight: 900;
            color: #000000;
            line-height: 1.2;
            letter-spacing: -1px;
            margin-bottom: 20px;
        }}

        .progress-container {{
            width: 100%;
            height: 80px;
            background: #E5E5EA;
            border-radius: 24px;
            overflow: hidden;
            position: relative;
            margin-bottom: 24px;
        }}

        .progress-fill {{
            height: 100%;
            background: #2C2C2E;
            border-radius: 24px;
            transition: width 1s ease-out;
            width: {data['percentage']}%;
        }}

        .stats {{
            display: flex;
            flex-direction: column;
            align-items: flex-end;
        }}

        .percentage {{
            font-size: 48px;
            font-weight: bold;
            color: #000000;
            letter-spacing: -1px;
            line-height: 1;
        }}

        .details {{
            font-size: 28px;
            color: #8E8E93;
            font-family: 'Noto Sans Mono CJK SC', 'Consolas', 'Monaco', monospace;
            margin-top: 8px;
            letter-spacing: 0.5px;
        }}
    </style>
</head>
<body>
    <div class="card">
        <div class="title">{data['title']}</div>
        <div class="progress-container">
            <div class="progress-fill"></div>
        </div>
        <div class="stats">
            <div class="percentage">{data['percentage']:.1f}%</div>
            <div class="details">{data['current']}/{data['total']} {data['unit']}</div>
        </div>
    </div>
</body>
</html>
        '''

        try:
            logger.info("使用 Playwright 异步渲染时间卡片...")

            async with async_playwright() as p:
                # 启动浏览器 (无头模式)
                browser = await p.chromium.launch(headless=True)

                # 创建页面,设置视口大小
                page = await browser.new_page(
                    viewport={'width': 680, 'height': 360},
                    device_scale_factor=2  # 2倍分辨率,提升清晰度
                )

                # 加载 HTML 内容
                await page.set_content(html_template)

                # 等待渲染完成
                await page.wait_for_timeout(500)

                # 截图保存
                temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
                await page.screenshot(
                    path=temp_file.name,
                    full_page=False,
                    type='png',
                    omit_background=False
                )

                await browser.close()

                logger.info(f"✅ 成功生成高清时间卡片: {temp_file.name} (Playwright异步渲染)")
                return temp_file.name

        except Exception as e:
            logger.error(f"❌ Playwright 渲染失败: {e}")
            logger.error("请确保已安装 Playwright: pip install playwright && playwright install chromium")
            raise

    async def generate_card_image(self) -> str:
        """
        生成时间卡片图片

        Returns:
            图片文件路径
        """
        try:
            # 计算时间数据
            data = self.calculate_time_data()

            # 绘制图片 (异步调用)
            image_path = await self.draw_time_card(data)

            logger.info("成功生成今天时间卡片图片")
            return image_path

        except Exception as e:
            logger.error(f"生成时间卡片图片失败: {e}")
            raise

    @filter.command("time")
    async def time_progress(self, event: AstrMessageEvent):
        """
        显示今天的时间进度卡片

        用法:
            /time - 显示今天的进度（0:00 到当前时间）
            /time 14:00 21:00 - 显示自定义时间段的进度
        """
        try:
            # 解析命令参数
            message_text = event.message_str.strip()
            parts = message_text.split()

            # 检查是否有参数
            if len(parts) == 3:  # /time HH:MM HH:MM
                start_time = parts[1]
                end_time = parts[2]

                # 验证时间格式
                start_parsed = self.parse_time_string(start_time)
                end_parsed = self.parse_time_string(end_time)

                if not start_parsed:
                    yield event.plain_result(f"❌ 开始时间格式错误，请使用 HH:MM 格式（如 14:00）")
                    return

                if not end_parsed:
                    yield event.plain_result(f"❌ 结束时间格式错误，请使用 HH:MM 格式（如 21:00）")
                    return

                # 生成自定义时间段卡片
                data = self.calculate_time_data(start_time, end_time)
                image_path = await self.draw_time_card(data)
                yield event.image_result(image_path)

                # 清理临时文件
                try:
                    os.unlink(image_path)
                except:
                    pass

            elif len(parts) == 1:  # /time（无参数）
                # 默认行为：生成并发送卡片
                image_path = await self.generate_card_image()
                yield event.image_result(image_path)

                # 清理临时文件
                try:
                    os.unlink(image_path)
                except:
                    pass

            else:
                # 参数数量错误
                yield event.plain_result(
                    "❌ 参数错误\n"
                    "用法：\n"
                    "  /time - 显示今天的进度\n"
                    "  /time 14:00 21:00 - 显示自定义时间段的进度"
                )

        except Exception as e:
            logger.error(f"处理时间进度指令失败: {e}")
            yield event.plain_result(f"❌ 生成时间卡片失败: {str(e)}")

    @filter.command("week")
    async def week_progress(self, event: AstrMessageEvent):
        """显示本周的时间进度卡片"""
        try:
            data = self.calculate_week_data()
            image_path = await self.draw_time_card(data)
            yield event.image_result(image_path)
            try:
                os.unlink(image_path)
            except:
                pass
        except Exception as e:
            logger.error(f"处理本周进度指令失败: {e}")
            yield event.plain_result(f"❌ 生成本周卡片失败: {str(e)}")

    @filter.command("month")
    async def month_progress(self, event: AstrMessageEvent):
        """显示本月的时间进度卡片"""
        try:
            data = self.calculate_month_data()
            image_path = await self.draw_time_card(data)
            yield event.image_result(image_path)
            try:
                os.unlink(image_path)
            except:
                pass
        except Exception as e:
            logger.error(f"处理本月进度指令失败: {e}")
            yield event.plain_result(f"❌ 生成本月卡片失败: {str(e)}")

    @filter.command("year")
    async def year_progress(self, event: AstrMessageEvent):
        """显示本年的时间进度卡片"""
        try:
            data = self.calculate_year_data()
            image_path = await self.draw_time_card(data)
            yield event.image_result(image_path)
            try:
                os.unlink(image_path)
            except:
                pass
        except Exception as e:
            logger.error(f"处理本年进度指令失败: {e}")
            yield event.plain_result(f"❌ 生成本年卡片失败: {str(e)}")
