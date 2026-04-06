![:astrbot_plugin_hello-bye](https://count.getloli.com/@:astrbot_plugin_hello-bye?theme=minecraft)
# hello-bye

> AstrBot 插件


## 🐔 使用说明
**在新成员进群或者老成员退群时，发送一条信息提示！**

### v1.11更新
- :bug: 修复机器人进群时欢迎自己的问题 (#20)
- :sparkles: 新增区分主动退群和被踢出群的功能 (#17)
  - 主动退群: 使用 `bye_text` / `bye_img` 配置
  - 被踢出群: 使用新增的 `kick_text` / `kick_img` 配置
  - 被踢消息支持 `{operator_name}` 和 `{operator_id}` 占位符

### v1.10更新

- 添加了本地图片的支持
如下图，在你的astrbot的文件夹下中找到`data/hello-bye`文件夹，然后将你所需要的图片放入，并且记住这个图片的名字。随后到插件配置中将图片名字放入即可
<img width="1330" height="888" alt="image" src="https://github.com/user-attachments/assets/09802538-f0d3-4e08-b74e-129f75b504bc" />
<img width="1136" height="165" alt="image" src="https://github.com/user-attachments/assets/0de500a8-d461-41af-918a-a45dde354fd1" />


### v1.9更新
- 新增配置：在发送欢迎信息的是否是否需要at，默认开启。
![image](https://github.com/user-attachments/assets/ec40ae32-4e31-4f11-91a8-c96fc0973e37)


### v1.8更新
- 新增了白名单，注意不要两个名单都配置了，否则会可能存在问题

### v1.7更新
- 获取不到图片继续发送文字，可以在控制台查看报错
- 支持多张图片然后随机发送一张


### v1.6更新
- 移除群每日打卡功能
- 将白名单修改为黑名单。
- 新增自定义退群信息，其中`{username}` 和 `{userid}` 会被替换为实际的昵称和qq号

![image](https://github.com/user-attachments/assets/7ae7dd5b-e41b-42ff-89aa-427afebdfc52)



### v1.5更新
- 新增：在不同群聊可以进行群欢迎词设置
- 指令：`/设置欢迎消息 <欢迎词>` 即可设置，   `/查看欢迎消息`即可查看

> [!TIP]\
> 不要忘记配置项里面的白名单以及其他的配置


![image](https://github.com/user-attachments/assets/982794eb-2d7c-4c44-86dd-b20a40e91c62)
![image](https://github.com/user-attachments/assets/a28add53-8fc8-4cfc-9844-df5123d5608a)


### v1.4更新
- 增加配置: 新增白名单 只有在白名单上的群组才会发送信息
![image](https://github.com/user-attachments/assets/7c286112-6db7-4cda-8761-f933f0acee40)

### v1.3更新
- 增加配置: 入群欢迎词，入群图片 可自定义入群欢迎词和图片！
- 修复群打卡


### v1.2更新
- 增加配置：是否开启欢迎词和退群词
- 新增群签到（大概可能能用）

## 👥 贡献指南

- 🌟 Star 这个项目！（点右上角的星星，感谢支持！）
- 🐛 提交 Issue 报告问题
- 💡 提出新功能建议
- 🔧 提交 Pull Request 改进代码
# 支持

[帮助文档](https://astrbot.app)
