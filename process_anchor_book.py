#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
处理《从普通到卓越主播的技术》完整文本
"""

import os
import re
import webbrowser
from datetime import datetime

def process_text(text):
    """处理文本"""
    # 先去掉Markdown格式的*符号
    text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)
    text = re.sub(r'\*([^*]+)\*', r'\1', text)
    
    # 按段落分割
    paragraphs = text.split('\n\n')
    processed_paragraphs = []
    
    # 页面行数计算（285mm页面高度，减去上下边距45mm，实际内容区域240mm）
    # 12pt字体，1.6倍行距，每行约6.4mm，240mm可容纳约37行
    current_line_count = 0
    max_lines_per_page = 37
    
    for paragraph in paragraphs:
        paragraph = paragraph.strip()
        if not paragraph:
            continue
        
        # 估算段落行数
        estimated_lines = max(1, len(paragraph) // 80 + 1)
        
        # 检查是否需要分页
        if current_line_count > 0 and (current_line_count + estimated_lines) > max_lines_per_page:
            processed_paragraphs.append('<div class="page-break"></div>')
            current_line_count = 0
        
        # 处理主标题
        if paragraph == "从普通到卓越主播的技术":
            processed_paragraphs.append(f"<h1>{paragraph}</h1>")
            current_line_count += 3
        # 处理前言
        elif paragraph.startswith("前言："):
            if current_line_count > 0:
                processed_paragraphs.append('<div class="page-break"></div>')
                current_line_count = 0
            processed_paragraphs.append(f"<h1>{paragraph}</h1>")
            current_line_count += 3
        # 处理章节标题
        elif re.match(r'^第[一二三四五六七八九十\d]+章[:：]', paragraph):
            if current_line_count > 0:
                processed_paragraphs.append('<div class="page-break"></div>')
                current_line_count = 0
            processed_paragraphs.append(f"<h1>{paragraph}</h1>")
            current_line_count += 3
        # 处理小节标题
        elif paragraph in ["迅速增加许多观众的直播技术、迅速增加直播业绩的方法", 
                          "直播卖货就是消费心理学的技术", 
                          "哈佛大学、沃顿商学院的商业圣经",
                          "第一部分：认知破局——顶尖主播绝不会告诉你的秘密",
                          "从绝望到希望：一个普通主播的转变",
                          "震撼开场：小米汽车如何用 3 小时改写商业史",
                          "第一章：数据不说谎：为什么印尼是直播卖货的黄金沃土",
                          "全球奇迹与本地机遇",
                          "第二章：五大权威理论：揭秘直播卖货的底层逻辑",
                          "第三章：从 Ayu 到 Ayu 先生：一个真实的转变"]:
            processed_paragraphs.append(f"<h2>{paragraph}</h2>")
            current_line_count += 2
        # 处理引用内容
        elif '【' in paragraph and '】' in paragraph:
            quote_match = re.search(r'【([^】]+)】', paragraph)
            if quote_match:
                processed_paragraphs.append(f'<blockquote>{quote_match.group(1)}</blockquote>')
                current_line_count += 2
            else:
                processed_paragraphs.append(f'<p>{paragraph}</p>')
                current_line_count += estimated_lines
        # 处理问题
        elif paragraph.endswith('？') or paragraph == "为什么？":
            processed_paragraphs.append(f'<p class="question">{paragraph}</p>')
            current_line_count += 1
        # 处理列表项
        elif paragraph.startswith('•') or re.match(r'^\d+\.', paragraph) or paragraph.startswith('- '):
            lines = paragraph.split('\n')
            list_items = []
            for line in lines:
                line = line.strip()
                if line:
                    if line.startswith('•'):
                        list_items.append(f'<li>{line[1:].strip()}</li>')
                    elif re.match(r'^\d+\.', line):
                        list_items.append(f'<li>{line}</li>')
                    elif line.startswith('- '):
                        list_items.append(f'<li>{line[2:]}</li>')
            if list_items:
                processed_paragraphs.append(f'<ul>{"".join(list_items)}</ul>')
                current_line_count += len(list_items)
        else:
            paragraph = paragraph.replace('\n', ' ')
            processed_paragraphs.append(f'<p>{paragraph}</p>')
            current_line_count += estimated_lines
    
    processed_text = '\n'.join(processed_paragraphs)
    
    # 创建HTML模板
    html_template = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>从普通到卓越主播的技术 - 大卫排版</title>
    <style>
        @page { 
            size: 210mm 285mm; 
            margin: 25mm 25mm 20mm 25mm; 
        }
        
        body { 
            font-family: "Microsoft YaHei", "SimSun", serif; 
            line-height: 1.6; 
            margin: 0;
            padding: 0;
            background-color: #f8f8f8;
            color: #333;
        }
        
        .book-container {
            width: 21cm;
            min-height: 28.5cm;
            margin: 1cm auto;
            background-color: white;
            box-shadow: 0 0 20px rgba(0,0,0,0.1);
            padding: 25mm 25mm 20mm 25mm;
            box-sizing: border-box;
        }
        
        h1 { 
            font-size: 20pt;
            font-weight: bold; 
            color: #2c3e50; 
            margin: 30pt 0 15pt 0;
            text-align: center; 
            border-bottom: 2pt solid #2c3e50; 
            padding-bottom: 8pt;
            line-height: 1.3;
        }
        
        h2 { 
            font-size: 16pt;
            font-weight: bold; 
            color: #34495e; 
            margin: 20pt 0 12pt 0;
            border-left: 3pt solid #3498db;
            padding-left: 10pt;
            line-height: 1.4;
        }
        
        p { 
            font-size: 12pt;
            text-indent: 2em; 
            margin: 6pt 0; 
            line-height: 1.6; 
            text-align: justify;
        }
        
        p.question {
            font-size: 14pt;
            font-weight: bold;
            color: #e74c3c;
            text-align: center;
            margin: 15pt 0;
            text-indent: 0;
        }
        
        blockquote { 
            background-color: #f8f9fa; 
            border-left: 4pt solid #e74c3c; 
            margin: 12pt 0; 
            padding: 10pt 12pt; 
            font-style: italic; 
            font-weight: bold;
            font-size: 11pt;
            border-radius: 0 3pt 3pt 0;
        }
        
        li { 
            font-size: 12pt;
            margin: 3pt 0;
            line-height: 1.5;
        }
        
        ul, ol { 
            margin: 8pt 0;
            padding-left: 18pt;
        }
        
        .page-break {
            page-break-before: always;
            break-before: page;
        }
        
        @media print {
            body { 
                background-color: white; 
            }
            .book-container { 
                box-shadow: none; 
                margin: 0; 
                width: 100%; 
                min-height: 100vh; 
            }
            .page-break { 
                page-break-before: always; 
            }
        }
        
        @media screen {
            body { 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 20px 0;
            }
            .page-break { 
                border-top: 2px dashed #ccc; 
                margin: 30px 0; 
                padding: 10px 0; 
                text-align: center; 
                color: #666; 
                font-size: 10pt; 
            }
            .page-break::before { 
                content: "--- 分页 (28.5cm) ---"; 
            }
        }
    </style>
</head>
<body>
    <div class="book-container">
{content}
    </div>
</body>
</html>"""
    
    return html_template.replace('{content}', processed_text)

def main():
    print("=" * 60)
    print("处理《从普通到卓越主播的技术》完整文本")
    print("=" * 60)
    
    # 创建输出目录
    if not os.path.exists('output'):
        os.makedirs('output')
    
    # 你的完整文本
    text = """从普通到卓越主播的技术
小米汽车在三小时内卖掉 30 万辆，每辆汽车的售价是。这在人类历史上从来没有任何一种销售模式获得如此大的成功。直播卖货的奇迹。所以，你在任何行业想获得成功，唯一要学会的就是直播卖货！注意：我说的是任何行业，未来是注意力经济和流量经济。一个浅显的道理，世界首富无一例外是靠流量生意，比如马斯克、贝佐斯、扎克伯格等等。
迅速增加许多观众的直播技术、
迅速增加直播业绩的方法
直播卖货就是消费心理学的技术
哈佛大学、沃顿商学院的商业圣经

前言：1200 人的奇迹

2025 年，印尼正在发生一场商业革命。

最新数据显示，印尼电商市场总规模已经突破 850 亿美元（Google, Temasek & Bain, 2025），其中，直播带货的增长速度最惊人：仅 TikTok Shop 和 Shopee Live 的直播销售，就占据了整体电商的 80%以上。DHL 与 Ipsos 的研究进一步指出，直播的转化率最高能达到传统电商的 3 倍。换句话说，同样的产品，如果你放在普通网店里，可能一个星期卖不动；但在直播间里，它能在 30 秒内卖空库存。

这是机会，也是残酷的事实。机会在于：印尼数千万 UMKM（中小卖家）第一次有了和大公司站在同一起跑线的机会；残酷在于：绝大多数人仍旧失败，他们的直播间冷冷清清，观众寥寥无几。

为什么？

因为人们误解了直播。他们以为直播=能说会聊；以为直播=喊价格+卖便宜；以为直播=靠人缘或者靠运气。

然而，真相是：直播的本质不是"卖货"，而是"注意力争夺"。直播间不是闲聊，而是一场心理学战场。

这一点，Ayu 最有资格证明。

那一夜，Ayu 的直播间沸腾了。屏幕右上角的数字不断跳动，100 人、300 人、600 人……直到突破 1200 人。评论区飞快刷屏，有人狂点爱心，有人喊"快点上链接"，有人急着问："老师，黄色的上衣还剩几件？"

手机的麦克风几乎快被喊单声震碎。Ayu 的手在发抖，但心里比任何时候都清晰：这是她人生中第一次感受到"命运正在改变"。

可是，你敢信吗？就在一个月前，她的直播间持续只有 7 个观众，其中还有一个是她的表妹。

时间倒回一个月前。雅加达郊区，昏黄的出租屋。补光灯发出刺眼的白光，手机支架摇摇欲坠。Ayu 对着镜头挤出笑容，一件一件展示桌上仅有的几件衣服。

她努力模仿大主播的语气："Kakak 们，这件很合适你们哦，只要……" 可屏幕上冷冷的数字只写着"观看人数：7"。

十分钟后，只剩 3 个观众，评论区死一般的寂静。那一夜，她抱着卖不出去的衣服哭到凌晨三点，甚至想过放弃直播，回到传统市场摆摊。

就在她快要彻底绝望时，她遇见了 Rudy。

Rudy 是一个来自中国的教授直播技术的老师，在雅加达长期培训电商学员，TikTok 账号叫 AI Agen Pasar。他听完 Ayu 的故事，只是笑了笑："你以为直播就是开口说话吗？错。直播的本质，是一场消费心理学的战争。"

他在纸上写下七个词：开播话术、拉新话术、塑品话术、报价话术、憋单话术、促单话术、逼单话术。

然后解释道："这七个话术并不是主播的江湖经验，而是世界顶级商学院反复验证的心理学原理。开播话术对应注意力经济；拉新话术背后是社会认同；报价话术用的是锚定效应；憋单话术利用延迟满足；促单话术靠稀缺性原则；逼单话术其实就是损失厌恶。"

Ayu 目瞪口呆。她一直以为"话术"只是老主播的口头禅，没想到背后竟然是诺贝尔经济学奖得主们的理论。

为什么观众明明说"没钱买"，却在 30 秒倒计时里疯狂下单？因为他们不是理性买家，而是受稀缺性原则支配的情绪动物。

为什么观众看到"已经有 200 人买过"就立刻跟着买？因为社会认同告诉他们："别人买的不会错"。

为什么同样的衣服，先报一个高价再打折，成交率就高出几倍？因为锚定效应让人觉得"占了便宜"。

为什么一个观众停留时间越长，越容易买单？因为沉没成本效应在提醒他们："既然已经投入了时间和精力，不买就亏了"。

而你以为的"随口一句话"，其实是几十年心理学研究的落地结果。

Rudy 帮 Ayu 设计了一个新的直播开场。她不再一开始就推销，而是笑着说："今晚有一个秘密礼物，只送给第一个坚持到最后的人。"

短短几分钟，直播间人数迅速突破 50，再到 300。观众被钉在了屏幕前，因为他们害怕错过。半小时后，正在观看的人数跳到 1027。

她激动得眼泪差点流出来。

原来，直播不是运气，而是科学。

这本书，就是要揭开这个秘密。

为什么我要说它"颠覆你的常识"？因为绝大多数人仍然相信"直播就是能说会聊"，仍然觉得"有人长得好看，所以能卖货"，仍然把失败归因于"自己不够努力"。

可事实是：努力和经验从来不是决定性因素。真正的胜负手，是你有没有掌握这些心理学原理，并把它们变成具体的话术。

再回到冷冰冰的数据。2025 年，印尼电商市场是整个东南亚增速最快的市场。Shopee、Tokopedia、TikTok 三大平台的数据共同指向一个事实：未来三年，直播带货将成为印尼消费者的主流购物方式。而 TIKTOK 是全世界第四代电商的领先者，第四代电商也叫兴趣电商。第三代电商代表 SHOPEE 有本质不同，第三代电商叫做搜索电商，也叫货架式电商。未来属于兴趣电商，特别当商品已经过剩的年代。

这意味着：你要么成为其中的赢家，要么永远只能做观众。

——

你可能会震惊地发现：那些看似即兴的"喊单"、那些不经意的"限量提醒"、甚至那些主播的表情管理，其实都来自严谨的理论。

Herbert Simon 的注意力经济解释了为什么开播的 180 秒是生死关口。Robert Cialdini 的稀缺性原则和社会认同理论，揭示了为什么观众总是"怕错过"。Daniel Kahneman 的峰终定律，告诉你为什么收尾比开头更重要。卡尼曼与塞勒的沉没成本效应，揭开了观众"停留越久越容易买"的秘密。

这一切，不是江湖偏方，而是世界顶尖学术结晶。

所以，这不是一本教你"喊口号"的书，也不是一本让你"熬时间"的书，而是一部真正的作战手册。

它会一步一步告诉你：为什么直播卖货是印尼人的黄金机会；新手要如何打基础；如何用黄金三分钟锁住观众；怎样让观众停留并互动；如何用心理学推动成交；怎样憋单和催单；又如何在危机时救场；优秀主播如何感知流量的变化，如何利用卡库存积聚大量的观众涌进直播间。最后，如何从个人主播走向团队化运营。

更重要的是，你在这里看到的每一个话术，都不是凭空创造，而是有学术理论和真实数据做支撑。

——

回到 Ayu 的故事。如今，她的直播间已经能稳定吸引上千观众平均在线，她的收入足以迈入富豪级别，还雇了 5 个助手，准备扩大团队。她最常对新人说的一句话是："直播不是靠嘴，而是靠技术。如果我能做到，你也可以。"

2025 年，你也站在这样的机会窗口前。直播不是未来，它已经是现在。你要么进入，要么错过。

接下来的章节，会带你拆解每一个心理学原理，让你明白：如何把一个冷清的直播间，变成爆单的舞台。

第一部分：认知破局——顶尖主播绝不会告诉你的秘密

亲爱的朋友，当你打开这本书的时候，我相信，你正站在一个充满机遇却又令人迷茫的十字路口。你的手指或许还停留在手机屏幕上，刚刚结束了一场令人沮丧的直播——对着空荡荡的在线人数列表，说完了一整晚的热情。

从绝望到希望：一个普通主播的转变

在又一次"零销量"的直播后，Ayu（一位来自棉兰的 23 岁大学生）彻底陷入怀疑。她甚至想过要放弃直播，回到传统市场摆摊。"也许我真的不适合这个行业，"她看着镜子里疲惫的自己，"可能只有那些天生口才好、长得漂亮的人才能成功。"

请记住 Ayu 的故事，因为我们将在本章末尾看到她是如何逆转命运的。 如果她能做到，你也能。

我知道，你也可能正经历着和 Ayu 一样的困惑：
- 你的直播间就像一座数字孤岛，偶尔飘过的"Hi"和""像是过路客施舍的问候
- 你精心准备的产品介绍，换来的只是不断下滑的在线人数
- 算算电费和网络费，发现一场 4 小时的直播收入还不及雅加达一杯像样的咖啡

但今天，我要告诉你一个可能改变你一生的真相：如果你相信"直播成功=口才好+运气"，那么你正在错过这个时代赋予普通人的最大创富机会。

震撼开场：小米汽车如何用 3 小时改写商业史

在我告诉你如何改变之前，请你先看一个发生在 2024 年，震撼了整个商业世界的案例：

小米汽车 SU7 上市发布会，一场精心设计的"超长直播"
- 时间：3 小时
- 战绩：支付定金订单：30 万辆（锁定销售额超过 70 亿人民币）
- 意义：这创造了人类商业史上，单价在 20 万人民币以上的消费品，最快实现最大销售额的纪录。

请注意，他们卖的不是口红、不是零食，而是单价超过 20 万人民币的汽车！传统 4S 店的一个金牌销售，一年能卖出 100 辆车已经是顶尖水平。而小米，用一场直播，完成了 3000 个金牌销售一年的工作量。

**这个案例对你意味着什么？**

它意味着，直播卖货，是人类有史以来最高效、最强大、最颠覆的销售模式，没有之一！它不仅仅适用于小商品，它适用于汽车、房产、教育、金融——任何行业。

未来的商业，本质上只有两种：一种是拥抱直播和流量的，另一种是即将被淘汰的。世界首富们的生意——马斯克的特斯拉（流量焦点）、贝佐斯的亚马逊（流量商城）、扎克伯格的 Meta（流量生态）——无一例外，都是顶级流量生意。

所以，一个浅显而深刻的道理摆在你面前：你在任何行业想获得成功，在当下这个时代，唯一必须学会的技能，就是直播卖货（获取和转化流量的能力）。

这不是选择题，而是生存题。

第一章：数据不说谎：为什么印尼是直播卖货的黄金沃土

全球奇迹与本地机遇

小米的案例是全球性的证明，而印尼的数据则为你提供了触手可及的本地化机遇。让我们用最硬核的数据，击碎你所有的怀疑。

1. 平台数据揭示的财富密码

- TikTok Shop 印尼 80%的销售额依赖直播（2024 年最新数据）。这不是选择题，而是必答题。如果你不在直播中发力，你就自动放弃了 80%的市场机会。

- Shopee Live：83%的印尼用户曾在直播间下单。这个数字意味着什么？每 10 个印尼电商用户中，至少有 8 个已经养成了在直播间购物的习惯。市场教育已经完成，你现在入场，无需培养用户习惯，只需抢占他们的注意力。

- DHL 与 Ipsos 的联合研究显示：直播转化率是传统电商的 3 倍。这意味着，同样的流量，通过直播带来的订单数量是传统网店的 3 倍！你的每一份流量投入，在直播间能获得 3 倍的回报。

2. 货币的真实购买力：重新定义"成功"

我知道你担心什么。有人说"一场直播卖了 1 亿印尼盾"，但你可能不知道的是：
- 5000 万印尼盾（约 2000 元人民币）在雅加达意味着：支付一个月的公寓租金+日常开销+还能存下钱
- 1 亿印尼盾（约 4000 元人民币）对于许多印尼二三线城市的年轻人来说，已经是相当可观的月收入

这本书要帮你实现的，不是成为一夜赚取百亿的超级网红，而是通过系统性的技术学习，达到月入 5000 万至 1 亿印尼盾的切实目标——这已经足以改变你的生活质量和社会地位。

第二章：五大权威理论：揭秘直播卖货的底层逻辑

如果数据和案例是"是什么"，那么理论就是"为什么"。理解这些诺贝尔奖级别的理论，你就会明白：直播不是玄学，而是一门精确的科学。

1. 注意力经济（Attention Economy）

- 理论源头：诺贝尔经济学奖得主 Herbert Simon 提出，后被哈佛商学院广泛应用于数字营销领域。

- 核心观点：信息过剩的时代，人类的注意力是最稀缺的资源。商业的本质就是争夺注意力。小米汽车发布会，就是一场对全球注意力的完美收割。

- 你的应用：观众不是"不想买"，而是他们的注意力根本没在你身上。直播的前 180 秒不是销售时间，而是"注意力抢夺战"。你的开场音乐、肢体语言、福利噱头，都不是随意的，而是经过设计的"注意力钩子"。

- 记住："如果你不能用 3 秒钟抓住我的注意力，你就会永远失去我。"——这不是夸张，这是算法时代的生存法则。

2. 稀缺性原则（Scarcity Principle）**

- 理论源头：Robert Cialdini《影响力》（全球消费心理学经典，被哈佛、沃顿商学院纳入 MBA 课程）。

- 核心观点：人类对"稀缺"的东西有非理性的渴望。限时、限量、独家都是强大的购买触发器。**小米 SU7 的"限量首发"正是此道高手。**
- 你的应用："只剩最后 3 件！""直播结束后恢复原价""前 50 名下单送神秘礼物"...这些话术之所以有效，是因为它们触发了人性的 FOMO（恐惧错过）心理。
- 记住：观众不是因为理性分析才下单，而是因为"害怕失去"。你的任务不是介绍产品多好，而是制造"再不买就没了"的紧迫感。

3. 社会认同（Social Proof）

- 理论源头：同样来自 Cialdini 的《影响力》，在哈佛商学院的消费者行为研究中被反复验证。

- 核心观点：当人们不确定时，会参考他人的行为来做决定。这就是"从众心理"的科学解释。

- 你的应用：直播间里的点赞、评论、礼物、购买记录，都不是简单的互动，而是**给新观众看的"证据"**。"这款已经卖出 200 件""好多回头客都说好"，这些话术是在告诉犹豫的观众："别人都买了，你跟着买不会错。"

- 记住：人们不是在买产品，而是在买"安全感"。你的直播间必须看起来热闹、可信、受欢迎。

4. 峰终定律（Peak-End Rule）

- 理论源头：诺贝尔奖得主 Daniel Kahneman 提出，在消费者体验设计中广泛应用。
- 核心观点：人们对一段体验的记忆，由最高峰的时刻和结束的时刻决定，而不是平均体验。

- 你的应用：一场直播必须设计至少一个高潮点（比如抽奖、秒杀、大额优惠），让观众记住这个"爽点"。结束时必须优雅有力，让观众带着"期待"离开（如预告明天更大的福利）。
- 记住：如果你不能让观众在"高潮时刻"下单，并在结束时留下好印象，他们很快就会忘记你。

5. 沉没成本效应（Sunk Cost Effect）

- 理论源头：行为经济学核心理论，由诺贝尔奖得主 Richard Thaler 等人发展。
- 核心观点：人们不愿意放弃已经投入的时间、金钱或精力。
- 你的应用：通过长时间互动、提问、小游戏，让观众在你的直播间投入时间（"我都看了半小时了"）。发放小额优惠券（"这个 5 万印尼盾的优惠券不用就浪费了"）。这些投入会让观众更难以离开和拒绝购买。
- 记住：让观众先"投资"一点什么（哪怕是时间），他们就更可能"投资"更多。

第三章：从 Ayu 到 Ayu 先生：一个真实的转变

现在，让我们回到 Ayu 的故事。在理解了"流量即财富"的本质并学习了这些原理后，她做了这些改变：

1. 重新定位：她不再把自己看作"卖货的"，而是"为我的观众提供时尚解决方案的流量主"。
2. 开场钩子（应用注意力经济）：不再说"大家好欢迎来到我的直播间"，而是举着一个醒目的牌子："观看满 3 分钟，私信我领 5 千印尼盾优惠券"。
3. 互动设计（应用社会认同）：让表妹用小号在评论区提问："姐姐我昨天买的那个裙子还有吗？我朋友说好看也要买！" 瞬间带动真实用户询问。

4. 成交技巧（应用稀缺性）：展示产品时，她会说："这个款式工厂只给我 100 件，库存已经标红了，要买的赶紧扣 1。"
5. 峰值制造（应用峰终定律）：直播到一半，突然上线一个"秒杀福袋"，制造高潮。
6. 结束设计：下播前，她不再仓促说再见，而是说："明天晚上 8 点，我会上新一批设计师款，而且会有比今天更大的惊喜礼物，大家设定好闹钟哦！"

结果是什么？
Ayu 的直播间在线人数从个位数稳定到了**500-1000 人。她的月收入从几乎为零增长到了每月 15000-20000 万印尼盾。
虽然还不是顶级主播，但这份收入已经足够支付她的学费和整个家庭的生活费，给了她巨大的信心。更重要的是，她掌握了一套在任何行业都通用的流量变现能力。

Ayu 的成功可以复制吗？绝对可以。因为她没有改变自己的口才或外貌，她改变的只是——思维模式和策略方法。

本章结语：你不是在卖货，你是在经营现代商业的核心——流量

现在，请你再次思考开篇的小米案例。雷军做的事情，和你要做的事情，本质一模一样：
- **争夺注意力**（做直播）
- **建立信任**（讲解技术，展示实力）
- **制造稀缺**（限量发售，限时定金）
- **促成转化**（一键锁单，支付定金）

你们使用的是同一套底层逻辑，只是在不同的赛道和规模上。

旧认知：主播 = 能说会道的售货员 (Salesperson)
——把成败寄托于个人天赋和运气。

新认知：主播 = 流量运营官 + 消费心理设计师 + 信任建立者
= 未来商业的核心操盘手
——把结果交付于一套可学习、可复制、可优化的技术系统。这套系统，是你在未来任何行业安身立命的根本。

你已经站在了认知的拐点。在接下来的第二部分，我们将进入真正的实战环节，一步步教你如何搭建这套系统，如何从 0 到 1，从 1 到 100，实现你的财富逆转。

你的第一场爆单直播，不是从打开摄像头开始，而是从改变这一刻的思维开始。未来已来，你唯一的选择就是：拥抱它，学习它，主宰它。"""
    
    try:
        print("正在处理文本...")
        html_result = process_text(text)
        
        # 生成文件名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"从普通到卓越主播的技术_完整版_{timestamp}.html"
        filepath = os.path.join('output', filename)
        
        # 保存文件
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_result)
        
        print(f"✓ 处理完成！")
        print(f"✓ 输出文件: {filepath}")
        print(f"✓ 分页逻辑: 按28.5cm页面高度智能分页")
        
        # 打开文件
        webbrowser.open(f'file:///{os.path.abspath(filepath)}')
        print("✓ 已在浏览器中打开")
        
    except Exception as e:
        print(f"✗ 处理失败: {e}")

if __name__ == "__main__":
    main()
