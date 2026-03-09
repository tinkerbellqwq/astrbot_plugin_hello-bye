import json
import os
import aiohttp
import random
from pathlib import Path

from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
from astrbot.core import AstrBotConfig
import astrbot.api.message_components as Comp


async def is_valid_image_url(url: str):
    """检查网络图片 URL 是否有效"""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.head(url, timeout=5) as response:
                return response.status == 200
    except Exception as e:
        logger.error(f"Error checking image URL: {e}")
        return False


@register("astrbot_plugin_hello-bye", "tinker", "一个简单的入群和退群信息提示插件", "1.1.0")
class MyPlugin(Star):
    def __init__(self, context: Context, config: AstrBotConfig):
        super().__init__(context)
        self.is_send_welcome = config.get("is_send_welcome", False)
        self.is_at = config.get("is_at", True)
        self.is_send_bye = config.get("is_send_bye", True)
        self.is_debug = config.get("is_debug", False)
        self.black_groups = config.get("black_groups", [])
        self.white_groups = config.get("white_groups", [])
        self.welcome_text = config.get("welcome_text", "欢迎新成员加入！")
        self.welcome_img = config.get("welcome_img", [])
        self.bye_text = config.get("bye_text", "群友{username}({userid})退群了!")
        self.bye_img = config.get("bye_img", [])

        # 数据目录
        data_dir = Path("data/hello-bye")
        data_dir.mkdir(parents=True, exist_ok=True)
        self.json_path = data_dir / "data.json"

    async def initialize(self):
        pass

    async def terminate(self):
        pass

    @filter.permission_type(filter.PermissionType.ADMIN)
    @filter.command("设置欢迎消息", alias={"设置入群信息", "设置入群提示", "设置欢迎信息"})
    async def set_hello_message(self, event: AstrMessageEvent, message: str):
        """设置当前群欢迎文字"""
        if event.is_private_chat():
            yield event.plain_result("请在群聊中使用此命令")
            return
        group_id = event.get_group_id()
        if not self.json_path.exists():
            with open(self.json_path, "w", encoding="utf-8") as f:
                json.dump({}, f)

        with open(self.json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        if str(group_id) not in data or not isinstance(data[str(group_id)], dict):
            data[str(group_id)] = {}

        data[str(group_id)]["welcome_text"] = message

        with open(self.json_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)

        yield event.plain_result(f"欢迎消息已设置为：{message}")

    @filter.command("设置欢迎图片", alias={"设置入群图片", "设置入群欢迎图片"})
    async def set_hello_image(self, event: AstrMessageEvent, message: str):
        """设置当前群欢迎图片（支持网络图片URL或本地文件名）"""
        if event.is_private_chat():
            yield event.plain_result("请在群聊中使用此命令")
            return
        group_id = event.get_group_id()
        if not self.json_path.exists():
            with open(self.json_path, "w", encoding="utf-8") as f:
                json.dump({}, f)

        with open(self.json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        if str(group_id) not in data or not isinstance(data[str(group_id)], dict):
            data[str(group_id)] = {}

        data[str(group_id)]["welcome_img"] = message

        with open(self.json_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)

        yield event.plain_result(f"欢迎图片已设置为：{message}")

    @filter.command("查看欢迎消息", alias={"查看入群信息", "查看入群提示", "查看欢迎信息"})
    async def get_hello_message(self, event: AstrMessageEvent):
        """查看当前群欢迎文字"""
        if event.is_private_chat():
            yield event.plain_result("请在群聊中使用此命令")
            return
        group_id = event.get_group_id()

        if not self.json_path.exists():
            yield event.plain_result("数据文件不存在")
            return

        with open(self.json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        msg = None
        if str(group_id) in data:
            if isinstance(data[str(group_id)], dict) and "welcome_text" in data[str(group_id)]:
                msg = data[str(group_id)]["welcome_text"]
                msg = msg.replace("\\n", "\n")
            elif isinstance(data[str(group_id)], str):
                msg = data[str(group_id)]
                msg = msg.replace("\\n", "\n")

        if msg:
            msg = msg.replace("\\n", "\n")
            yield event.plain_result(f"欢迎消息为：{msg}")
        else:
            yield event.plain_result("没有设置欢迎消息")

    def check_send(self, group_id: str) -> bool:
        """检查是否发送欢迎或退群消息"""
        if self.black_groups and str(group_id) in self.black_groups:
            return False
        if self.white_groups and str(group_id) not in self.white_groups:
            return False
        return True

    @filter.command("查看欢迎图片", alias={"查看入群图片", "查看入群欢迎图片"})
    async def get_hello_image(self, event: AstrMessageEvent):
        """查看当前群欢迎图片"""
        if event.is_private_chat():
            yield event.plain_result("请在群聊中使用此命令")
            return
        group_id = event.get_group_id()

        if not self.json_path.exists():
            yield event.plain_result("数据文件不存在")
            return

        with open(self.json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        image_path = None
        if str(group_id) in data and isinstance(data[str(group_id)], dict):
            image_path = data[str(group_id)].get("welcome_img")

        if not image_path:
            yield event.plain_result("当前群没有设置欢迎图片")
            return

        # 根据图片类型返回
        if image_path.startswith("http://") or image_path.startswith("https://"):
            valid_image = await is_valid_image_url(image_path)
            if valid_image:
                yield event.chain_result([Comp.Image.fromURL(image_path)])
            else:
                yield event.plain_result(f"当前群设置的欢迎图片无效：{image_path}")
        else:
            local_path = os.path.join(Path("data/hello-bye"), image_path)
            if os.path.exists(local_path):
                yield event.chain_result([Comp.Image.fromFileSystem(local_path)])
            else:
                yield event.plain_result(f"本地图片文件不存在：{local_path}")

    @filter.event_message_type(filter.EventMessageType.ALL)
    async def handle_group_add(self, event: AstrMessageEvent):
        """处理入群和退群事件"""
        if not hasattr(event, "message_obj") or not hasattr(event.message_obj, "raw_message"):
            return

        raw_message = event.message_obj.raw_message
        if not raw_message or not isinstance(raw_message, dict):
            return
        if raw_message.get("post_type") != "notice":
            return

        if raw_message.get("notice_type") == "group_increase":
            if not self.is_send_welcome:
                return
            group_id = raw_message.get("group_id")
            if not self.check_send(group_id):
                return
            user_id = raw_message.get("user_id")

            welcome_message = self.welcome_text
            group_image = None

            if self.json_path.exists():
                with open(self.json_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if str(group_id) in data:
                        if isinstance(data[str(group_id)], dict):
                            if "welcome_text" in data[str(group_id)]:
                                welcome_message = data[str(group_id)]["welcome_text"]
                            if "welcome_img" in data[str(group_id)]:
                                group_image = data[str(group_id)]["welcome_img"]
                        else:
                            welcome_message = data[str(group_id)]

            welcome_message = welcome_message.replace("\\n", "\n")

            image_to_use = group_image or (random.choice(self.welcome_img) if self.welcome_img else None)

            if image_to_use:
                if image_to_use.startswith("http://") or image_to_use.startswith("https://"):
                    valid_image = await is_valid_image_url(image_to_use)
                    if valid_image:
                        chain = [
                            Comp.At(qq=user_id) if self.is_at else Comp.Plain(""),
                            Comp.Plain(welcome_message),
                            Comp.Image.fromURL(image_to_use),
                        ]
                    else:
                        logger.warning(f"Invalid image URL: {image_to_use}")
                        chain = [
                            Comp.At(qq=user_id) if self.is_at else Comp.Plain(""),
                            Comp.Plain(welcome_message),
                        ]
                else:
                    chain = [
                        Comp.At(qq=user_id) if self.is_at else Comp.Plain(""),
                        Comp.Plain(welcome_message),
                        Comp.Image.fromFileSystem(os.path.join(Path("data/hello-bye"), image_to_use)),
                    ]
                yield event.chain_result(chain)
            else:
                chain = [
                    Comp.At(qq=user_id) if self.is_at else Comp.Plain(""),
                    Comp.Plain(welcome_message),
                ]
                yield event.chain_result(chain)

        elif raw_message.get("notice_type") == "group_decrease":
            if not self.is_send_bye:
                return
            group_id = raw_message.get("group_id")
            if not self.check_send(group_id):
                return
            user_id = raw_message.get("user_id")
            from astrbot.core.platform.sources.aiocqhttp.aiocqhttp_message_event import AiocqhttpMessageEvent
            assert isinstance(event, AiocqhttpMessageEvent)
            client = event.bot
            info = await client.get_stranger_info(user_id=user_id, no_cache=True)
            username = info.get("nickname", "未知用户")
            goodbye_message = self.bye_text.replace("\\n", "\n").format(username=username, userid=user_id)
            yield event.plain_result(goodbye_message)
