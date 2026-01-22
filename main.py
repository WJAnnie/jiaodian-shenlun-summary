"""
焦点访谈申论总结
- 获取央视焦点访谈最新一期
- AI生成评论性申论文章
- 微信推送
"""

import requests
import os
from datetime import datetime

# ============ 配置 ============
SERVERCHAN_KEY = os.environ.get("SERVERCHAN_KEY", "")
DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY", "")


# ============ 焦点访谈爬取 ============
def fetch_jiaodian_fangtan():
    """获取央视焦点访谈最新一期"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }

    try:
        url = 'https://api.cntv.cn/NewVideo/getVideoListByColumn?id=TOPC1451558976694518&n=5&sort=desc&p=1&mode=0&serviceId=tvcctv'
        resp = requests.get(url, headers=headers, timeout=15)
        data = resp.json()

        if data.get('data') and data['data'].get('list'):
            video_list = data['data']['list']
            if video_list:
                latest = video_list[0]
                return {
                    'title': latest.get('title', ''),
                    'brief': latest.get('brief', ''),
                    'time': latest.get('time', ''),
                    'url': latest.get('url', ''),
                    'length': latest.get('length', '')
                }

        print("未获取到焦点访谈数据")
        return None

    except Exception as e:
        print(f"获取焦点访谈失败: {e}")
        return None


# ============ AI申论改写 ============
def rewrite_as_shenlun(title, content):
    """使用DeepSeek API生成评论性申论文章"""
    if not DEEPSEEK_API_KEY:
        return simple_rewrite(title, content)

    prompt = f"""请根据以下央视《焦点访谈》节目内容，写一篇评论性申论文章。

【严格格式要求】

文章结构：标题 + 五个自然段

1. 【标题】：简洁有力，体现文章核心观点，15-20字

2. 【第一段】（约200字）：
   - 开头引入方式三选一：①名人名言引入（中国古语或习近平讲话）②排比句式引入 ③时代发展背景引入
   - 不要过多复述新闻内容，只需点明主题即可
   - 语言要有文采和气势
   - 最后一句必须是全文的总论点（观点鲜明、概括全文）

3. 【第二段-分论点一】（约250字）：
   - 第一句话要对仗工整（如"xxx是xxx，xxx是xxx"的句式）
   - 包含一个具体案例（简短有力，30-50字）
   - 案例引出的道理论证要充分（150字以上）
   - 可引用习近平讲话或中国古语名言

4. 【第三段-分论点二】（约250字）：
   - 第一句话要对仗工整
   - 包含一个具体案例
   - 案例引出的道理论证要充分
   - 可引用习近平讲话或中国古语名言

5. 【第四段-分论点三】（约250字）：
   - 第一句话要对仗工整
   - 包含一个具体案例
   - 案例引出的道理论证要充分
   - 可引用习近平讲话或中国古语名言

6. 【第五段-结尾】（约100字）：
   - 第一句话要对应主题的高端句式，如对仗、排比、通用名言
   - 总结升华
   - 呼应总论点
   - 展望未来或发出号召

【写作要求】
- 论证方式：举例论证、道理论证相结合
- 名言出处：必须来自中国古语（如《论语》《孟子》《大学》等）或习近平重要讲话
- 案例选择：例子要简短精炼（30-50字），但引出的道理分析要深入（100字以上）
- 语言风格：规范严谨、逻辑清晰、有理有据
- 三个分论点的首句必须形成对仗，体现工整之美
- 字数需控制：同申论作文要求，在每行25格（标点符号算一格）的情况下，包含标点符号不超过1100格
- 文章内不要提到“节目”“本期”字眼，要举例子直接提就好了

节目标题：{title}
节目内容：{content}

请直接输出文章，格式如下：

【标题】
...

【正文】

（第一段，约200字，最后一句为总论点）

（第二段-分论点一，约250字，首句对仗）

（第三段-分论点二，约250字，首句对仗）

（第四段-分论点三，约250字，首句对仗）

（第五段-结尾，约100字）
"""

    try:
        resp = requests.post(
            "https://api.deepseek.com/chat/completions",
            headers={
                "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "deepseek-chat",
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 3000
            },
            timeout=120
        )
        result = resp.json()
        return result['choices'][0]['message']['content']
    except Exception as e:
        print(f"DeepSeek API调用失败: {e}")
        return simple_rewrite(title, content)


def simple_rewrite(title, content):
    """简单改写（无API时使用）"""
    return f"""【标题】
{title}

【正文】

{content[:200]}...

（需要配置DeepSeek API以生成完整申论文章）

建议观看完整节目了解详情。

关注时事，提升申论思维。"""


# ============ 微信推送 ============
def send_to_wechat(title, content):
    """通过Server酱推送到微信"""
    if not SERVERCHAN_KEY:
        print("未配置Server酱Key")
        return False

    url = f"https://sctapi.ftqq.com/{SERVERCHAN_KEY}.send"
    data = {"title": title[:100], "desp": content}

    try:
        resp = requests.post(url, data=data, timeout=10)
        result = resp.json()
        if result.get('code') == 0:
            print("微信推送成功！")
            return True
        else:
            print(f"推送失败: {result}")
            return False
    except Exception as e:
        print(f"推送异常: {e}")
        return False


# ============ 主流程 ============
def main():
    print(f"=== 焦点访谈申论总结 ===")
    print(f"运行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    # 1. 获取焦点访谈
    print("正在获取焦点访谈...")
    episode = fetch_jiaodian_fangtan()

    if not episode:
        send_to_wechat("获取失败", "今日未获取到焦点访谈")
        return

    print(f"获取到: {episode['title']}")
    print(f"播出时间: {episode['time']}")

    # 2. AI申论改写
    print("正在生成申论文章...")
    content = episode['brief'] or episode['title']
    shenlun = rewrite_as_shenlun(episode['title'], content)

    # 3. 组装推送内容
    today = datetime.now().strftime('%Y年%m月%d日')
    push_title = f"焦点访谈申论总结 - {today}"

    push_content = f"""## 今日焦点访谈申论总结

---

{shenlun}

---

### 原节目信息
- **节目**：{episode['title']}
- **播出时间**：{episode['time']}
- **链接**：{episode.get('url', '')}
"""

    # 4. 推送
    print("正在推送...")
    send_to_wechat(push_title, push_content)
    print("\n=== 完成 ===")


if __name__ == "__main__":
    main()
