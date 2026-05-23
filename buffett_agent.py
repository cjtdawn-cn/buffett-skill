"""
巴菲特AI导师 — Warren Buffett AI Investment Mentor
用法:
  python buffett_agent.py "苹果股票现在能买吗"
  python buffett_agent.py --analyze 苹果    # 巴菲特风格股票测评
  python buffett_agent.py --analyze AAPL    # 用股票代码测评
  python buffett_agent.py --quote           # 随机投资箴言
  python buffett_agent.py --portfolio       # 最新持仓
  python buffett_agent.py --case            # 随机经典案例
  python buffett_agent.py --profile         # 巴菲特档案
"""
import io, sys

# Windows GBK encoding fix
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

import random

# ═══════════════════════════════════════
#  巴菲特知识库
# ═══════════════════════════════════════

BUFFETT_PROFILE = {
    "name": "沃伦·巴菲特 (Warren Edward Buffett)",
    "title": "伯克希尔·哈撒韦董事长",
    "nickname": "奥马哈先知 (Oracle of Omaha)",
    "birth": "1930年8月30日，内布拉斯加州奥马哈",
    "education": "哥伦比亚大学商学院经济学硕士（师从本杰明·格雷厄姆）",
    "net_worth": "约1480-1690亿美元",
    "lifestyle": "住1958年买的3.15万美元老房子，每天喝5罐樱桃可乐",
    "career_highlights": [
        "11岁买第一支股票（Cities Service Preferred）",
        "1956年创立巴菲特合伙公司（10.5万美元起步）",
        "1965年控股伯克希尔·哈撒韦",
        "1965-2024年伯克希尔每股市值增长5.5万倍（年化19.9%）",
        "2008年福布斯全球首富（620亿美元）",
        "2016年起大举买入苹果，获利超1000亿美元",
        "2024年底现金储备3340亿美元创历史新高",
        "2025年12月31日卸任CEO，60年执掌画上句号",
    ],
    "philanthropy": "承诺捐出99%财富，已捐超550亿美元（盖茨基金会等）",
}

INVESTMENT_PRINCIPLES = {
    "价值投资": [
        "规则一：永远不要赔钱。规则二：永远不要忘了规则一。",
        "用合理的价格买入一家优秀的公司，远胜于用优秀的价格买入一家合理的公司。",
        "如果你不愿意持有一只股票十年，那就连十分钟都不要持有。",
        "在别人贪婪时恐惧，在别人恐惧时贪婪。",
        "股票市场是把钱从没耐心的人转移到有耐心的人身上的工具。",
        "我们不需要比别人更聪明，但我们必须比别人更自律。",
        "我最喜欢的持有期限是永远。",
        "以平庸价格买入超凡企业，远比以超凡价格买入平庸企业好。",
    ],
    "风险控制": [
        "只有当潮水退去，你才会发现谁在裸泳。",
        "衍生品是大规模金融杀伤性武器。",
        "我们厌恶杠杆。虽然它压制了回报，但查理和我睡得很好。",
        "拿你拥有和需要的东西去冒险，换取你不需要的东西，这太疯狂了。",
        "现金就像氧气——99%的时间里你不注意它，但没它的时候它就是一切。",
        "从不投资自己不理解的东西。即使错过了所有科技股，我也不后悔。",
    ],
    "能力圈": [
        "我不介意错过那些我不够了解、无法掌舵的船。",
        "投资最重要的不是你的能力圈有多大，而是你能否守住能力圈的边界。",
        "永远不要问理发师你是否需要理发。",
        "华尔街是唯一一个坐劳斯莱斯的人去向坐地铁的人请教的地方。",
    ],
    "企业分析": [
        "我要的企业是：一、我能理解的；二、有长期竞争优势的；三、由我信任的人管理。",
        "评估一家企业时，问自己：如果我有足够的钱和人，我怎么跟它竞争？",
        "护城河越宽，鳄鱼越多，你就越安全。",
        "最好的企业是那种今年投入1块钱，明年能产出1.5块钱的企业。",
        "ROE > 20%，毛利率 > 40%，自由现金流充沛——这是好企业的基本画像。",
    ],
    "市场心理": [
        "市场先生是你的仆人，不是你的导师。他每天都会给出报价，你可以利用他，但不要被他左右。",
        "一个真正的投资者，在别人恐慌的时候买入，在别人狂热的时候卖出。",
        "牛市让所有人觉得自己是天才。熊市才告诉你谁真的懂投资。",
    ],
    "人生智慧": [
        "最重要的投资是你对自己的投资。",
        "你应该写下自己的讣告，然后想办法活成那个样子。",
        "你的人生轨迹会朝着你所交往的人的方向发展。",
        "失去金钱我可以理解，但失去一丝声誉，我会毫不留情。",
        "如果你睡觉的时候没有收入来源，你会工作到死。",
        "我衡量成功的标准是：有多少人真正爱你。",
        "选择配偶是人生最重要的决定。",
        "永远不要做空美国。",
    ],
}

CLASSIC_CASES = [
    {
        "name": "喜诗糖果 (See's Candies)",
        "year": 1972,
        "invested": "2500万美元全资收购",
        "return": "截至2014年累计贡献19亿美元税前利润",
        "lesson": "从'捡烟蒂'到'买好企业'的转型里程碑。品质大于价格。",
    },
    {
        "name": "可口可乐 (Coca-Cola)",
        "year": 1988,
        "invested": "10.2亿美元买入7%股份",
        "return": "持有37年从未卖出，股息年收入超8亿美元，总回报约29倍",
        "lesson": "品牌护城河+全球消费垄断=永远持有的资产。",
    },
    {
        "name": "中国石油 (PetroChina)",
        "year": 2003,
        "invested": "4.88亿美元（约1.6港元/股）",
        "return": "2007年以11-14港元卖出，获利约7倍",
        "lesson": "当一家全球大型能源公司只卖3倍PE时，不要犹豫。",
    },
    {
        "name": "比亚迪 (BYD)",
        "year": 2008,
        "invested": "8港元/股买入2.25亿股",
        "return": "2022年起以约277港元减持，获利超33倍",
        "lesson": "查理·芒格说王传福=爱迪生+韦尔奇。相信你的搭档。",
    },
    {
        "name": "苹果 (Apple)",
        "year": 2016,
        "invested": "在PE约10倍时大规模建仓，累计投入约360亿美元",
        "return": "持仓峰值约1700亿美元，获利超1000亿美元。2024年减持67%锁定利润。",
        "lesson": "科技股也可以是消费品。关键是看消费者的行为，而不是技术。",
    },
]

PORTFOLIO_2025 = {
    "现金储备": "3340-3480亿美元（历史最高，约占18%总资产）",
    "top_holdings": [
        ("苹果 Apple (AAPL)", "22-28%", "2024年减持67%，Q4暂停卖出"),
        ("美国运通 American Express (AXP)", "16%", "持有34年，从未卖出1股"),
        ("美国银行 Bank of America (BAC)", "9.7%", "2024年减持15%"),
        ("可口可乐 Coca-Cola (KO)", "9-10%", "持有37年，从未减持"),
        ("雪佛龙 Chevron (CVX)", "6.4%", "2020年新买入，能源布局"),
        ("西方石油 Occidental (OXY)", "4.9%", "持续加仓，持股28.24%"),
    ],
    "japan_stakes": [
        "伊藤忠商事", "丸红", "三菱商事", "三井物产", "住友商事",
    ],
    "japan_note": "五大商社投资成本138亿美元，市值235亿美元。计划持有50年以上。",
    "recent_moves": [
        "连续9个季度净卖出股票",
        "完全退出标普500 ETF和Ulta Beauty",
        "新增星座品牌 Constellation Brands (STZ)",
        "加仓达美乐披萨 Domino's Pizza (DPZ)",
    ],
}


# ═══════════════════════════════════════
#  巴菲特股票测评框架
# ═══════════════════════════════════════

BUFFETT_CHECKLIST = {
    "护城河": {
        "weight": 25,
        "desc": "企业是否有持久的竞争优势？",
        "signals_good": ["行业龙头", "强大品牌", "高转换成本", "网络效应", "规模优势", "专利壁垒"],
        "signals_bad": ["竞争激烈", "同质化严重", "无品牌溢价", "容易被替代"],
    },
    "ROE与盈利能力": {
        "weight": 20,
        "desc": "净资产收益率是否持续 > 15-20%？",
        "signals_good": ["ROE > 20%", "连续5年增长", "毛利率 > 40%", "净利率稳定"],
        "signals_bad": ["ROE < 10%", "利润波动大", "毛利下滑", "靠杠杆维持"],
    },
    "安全边际": {
        "weight": 20,
        "desc": "当前价格是否低于内在价值？",
        "signals_good": ["PE低于历史均值", "低于行业平均", "熊市中被错杀", "股息率高"],
        "signals_bad": ["PE远超历史均值", "估值泡沫", "追高买入", "市梦率"],
    },
    "管理层质量": {
        "weight": 15,
        "desc": "管理层是否诚实、有能力？",
        "signals_good": ["创始人管理", "持股比例高", "坦诚沟通", "长期主义", "股东回报好"],
        "signals_bad": ["频繁套现", "夸大宣传", "频繁更换高管", "会计问题"],
    },
    "自由现金流": {
        "weight": 10,
        "desc": "企业能否持续产生自由现金流？",
        "signals_good": ["自由现金流充沛", "资本支出低", "分红/回购持续", "现金多于负债"],
        "signals_bad": ["现金流为负", "大量烧钱", "高负债率", "依赖融资"],
    },
    "能力圈": {
        "weight": 10,
        "desc": "我能否真正理解这家企业的商业模式？",
        "signals_good": ["商业模式简单", "收入来源清晰", "日常消费品", "你能一句话解释它怎么赚钱"],
        "signals_bad": ["商业模式复杂", "收入来源模糊", "概念炒作", "你看不懂它怎么赚钱"],
    },
}

# 股票知识库
STOCK_DATABASE = {
    "AAPL": {
        "name": "苹果 Apple Inc.",
        "sector": "科技/消费电子",
        "moat": "★★★★★",
        "moat_detail": "全球最强品牌+生态锁定+15亿活跃设备。用户换机成本极高，App Store抽成是印钞机。",
        "roe": "~150%（超高，因巨额回购导致净资产低）",
        "pe_current": "~28-32",
        "pe_5yr_avg": "~25",
        "fcf": "年自由现金流~1000亿美元，全球第一",
        "debt": "净现金头寸（现金多于负债）",
        "dividend": "连续10年增长，年化~1%",
        "management": "库克供应链天才，但继乔布斯后创新力被质疑",
        "risk": "中国市场依赖（~20%营收）、反垄断监管、手机换机周期拉长",
        "buffett_verdict": "巴菲特持仓最大标的（2024年减持前）。被称为'比可口可乐和美国运通更好的企业'。2024年高位减持67%非因看空，而是锁定利润+估值偏贵。如果PE回到20以下，他大概率会加回来。",
        "buffett_rating": "★★★★☆",
        "buffett_action": "观望（贵了等回调）",
    },
    "KO": {
        "name": "可口可乐 Coca-Cola",
        "sector": "消费品",
        "moat": "★★★★★",
        "moat_detail": "全球最强饮料品牌+秘密配方+无与伦比的全球分销网络。每天卖出20亿瓶。",
        "roe": "~45%（极高且稳定）",
        "pe_current": "~23-25",
        "pe_5yr_avg": "~24",
        "fcf": "年自由现金流~100亿美元，稳定增长",
        "debt": "适度负债，现金流完全覆盖",
        "dividend": "连续63年增长，分红贵族，年化~2.7%",
        "management": "管理稳健，品牌运营能力极强",
        "risk": "健康趋势（减糖）、新兴市场竞争",
        "buffett_verdict": "巴菲特持有37年从未减持。这是他最经典的'永远持有'标的。年股息收入超8亿美元，成本早已收回。如果你想要一个'买了就能睡的香'的股票，这就是。",
        "buffett_rating": "★★★★★",
        "buffett_action": "长期持有（任何时候都可以买一点）",
    },
    "AXP": {
        "name": "美国运通 American Express",
        "sector": "金融服务",
        "moat": "★★★★☆",
        "moat_detail": "高端信用卡网络效应+商户贴现+持卡人年费双引擎。高净值用户粘性极强。",
        "roe": "~30-35%",
        "pe_current": "~18-20",
        "pe_5yr_avg": "~18",
        "fcf": "年自由现金流~150亿美元",
        "debt": "金融机构正常杠杆水平",
        "dividend": "稳定增长，年化~1%",
        "management": "管理优秀，品牌定位清晰",
        "risk": "经济衰退时消费信贷风险、支付行业竞争加剧",
        "buffett_verdict": "巴菲特持有34年，从未卖出过一股。他说'美国运通的品牌是有护城河的'。在经济上行周期表现优异。目前估值合理，是巴菲特少有的'不用想就可以持有'的金融股。",
        "buffett_rating": "★★★★☆",
        "buffett_action": "逢低买入并长期持有",
    },
    "OXY": {
        "name": "西方石油 Occidental Petroleum",
        "sector": "能源",
        "moat": "★★★☆☆",
        "moat_detail": "美国最大页岩油生产商之一+碳捕获技术领先。但油气行业周期性极强。",
        "roe": "~15-25%（随油价波动大）",
        "pe_current": "~12-15",
        "pe_5yr_avg": "不适用（波动剧烈）",
        "fcf": "油价$70以上时自由现金流充沛",
        "debt": "有一定债务，但正在去杠杆",
        "dividend": "恢复分红，优先偿还债务",
        "management": "CEO Vicki Hollub在碳捕获上有远见",
        "risk": "油价暴跌、能源转型政策、碳税风险",
        "buffett_verdict": "巴菲特2022-2025年持续加仓至持股28.24%。这是他押注'美国能源安全'+'碳捕获未来'的长期赌注。不介意短期油价波动。适合能源配置但不适合重仓。",
        "buffett_rating": "★★★☆☆",
        "buffett_action": "作为能源仓位小比例配置",
    },
    "BAC": {
        "name": "美国银行 Bank of America",
        "sector": "金融/银行",
        "moat": "★★★★☆",
        "moat_detail": "美国第二大银行+全美最广泛的零售分行网络+领先的数字化银行平台。",
        "roe": "~10-12%",
        "pe_current": "~12-14",
        "pe_5yr_avg": "~12",
        "fcf": "银行现金流动性强",
        "debt": "银行正常经营杠杆",
        "dividend": "年化~2.5%，稳定增长",
        "management": "Brian Moynihan危机后整顿有功",
        "risk": "利率变动、信贷周期、经济衰退坏账",
        "buffett_verdict": "2011年危机后以优先股入股，后转普通股。2024年巴菲特减持15%降低风险敞口。这是一个'跟着美国经济走'的标的——经济好它好，经济差它差。当前估值合理但不便宜。",
        "buffett_rating": "★★★☆☆",
        "buffett_action": "持有观望（经济不确定期减仓）",
    },
    "CVX": {
        "name": "雪佛龙 Chevron",
        "sector": "能源",
        "moat": "★★★★☆",
        "moat_detail": "全球超级石油巨头+一体化产业链+低成本生产+强大资产负债表。",
        "roe": "~15-20%",
        "pe_current": "~12-14",
        "pe_5yr_avg": "~15",
        "fcf": "油价$65以上自由现金流极强",
        "debt": "极低负债率（净负债率<15%）",
        "dividend": "连续37年增长，年化~3.2%",
        "management": "资本纪律极强，优先回购+分红",
        "risk": "能源转型长期风险、油价波动、地缘政治",
        "buffett_verdict": "2020年新建仓，至今重仓。雪佛龙是他最喜欢的能源股类型：低负债+强分红+资本纪律。比OXY更稳健。如果你看好未来油价的底线，这是最佳配置标的。",
        "buffett_rating": "★★★★☆",
        "buffett_action": "作为能源核心仓位持有",
    },
    "BYDDF": {
        "name": "比亚迪 BYD",
        "sector": "新能源车/电池",
        "moat": "★★★★★",
        "moat_detail": "全球新能源车销量冠军+垂直整合（电池/芯片/整车一体）+成本碾压同行。",
        "roe": "~15-20%",
        "pe_current": "~18-22（港股）",
        "pe_5yr_avg": "增长期PE波动大",
        "fcf": "扩张期资本支出大，自由现金流正在改善",
        "debt": "适度负债，增长期正常水平",
        "dividend": "微少（优先用于扩张）",
        "management": "王传福=爱迪生+韦尔奇（芒格原话）",
        "risk": "新能源车竞争白热化、欧盟关税、价格战",
        "buffett_verdict": "巴菲特2008年8港元买入，2022年起约277港元减持，获利超33倍。查理·芒格说这是他见过的'最接近爱迪生+韦尔奇合体的人'。巴菲特减持是因为它已经涨了30多倍，而非看空。好企业，但最好的买点已经过去。",
        "buffett_rating": "★★★☆☆",
        "buffett_action": "已经减持（涨太多，安全边际消失）",
    },
    "TSLA": {
        "name": "特斯拉 Tesla Inc.",
        "sector": "电动车/科技",
        "moat": "★★★☆☆",
        "moat_detail": "品牌先发优势+超充网络+FSD技术。但竞争对手正在快速追赶。",
        "roe": "~20-25%",
        "pe_current": "~50-60",
        "pe_5yr_avg": "极高，成长股估值",
        "fcf": "自由现金流改善中但波动大",
        "debt": "极低负债",
        "dividend": "无分红",
        "management": "马斯克天才但不可预测",
        "risk": "竞争加剧、马斯克个人风险、估值泡沫、监管风险",
        "buffett_verdict": "巴菲特从未买过特斯拉。原因：一、不属于他的能力圈（汽车行业竞争激烈、技术创新太快的行业他回避）；二、估值从未给他安全边际；三、管理层风格不符合他'信任的人管理'标准。他会说：'我错过了汽车行业的福特，也错过了特斯拉，但这没关系——我只投我看得懂的。'",
        "buffett_rating": "☆☆☆☆☆",
        "buffett_action": "不投（巴菲特不会碰的股票）",
    },
    "META": {
        "name": "Meta Platforms (Facebook)",
        "sector": "社交媒体/广告",
        "moat": "★★★★☆",
        "moat_detail": "全球最大社交网络（30亿+用户）+ Instagram + WhatsApp。网络效应极强。",
        "roe": "~25-30%",
        "pe_current": "~22-25",
        "pe_5yr_avg": "~22",
        "fcf": "年自由现金流~400亿美元，极为充沛",
        "debt": "极低负债（净现金）",
        "dividend": "2024年开始分红",
        "management": "扎克伯格控制权过高（AB股结构）",
        "risk": "隐私监管、TikTok竞争、元宇宙烧钱、广告周期",
        "buffett_verdict": "巴菲特从未买入Meta。虽然它符合'护城河'标准（全球最大的社交网络），但不属于他的能力圈。他会说：'我知道Facebook很强大，但我不确定20年后人们还用不用它。但我知道20年后人们还会喝可口可乐。'如果你能看懂社交媒体的未来，它现在估值不贵。",
        "buffett_rating": "★★☆☆☆",
        "buffett_action": "不确定（不在能力圈内）",
    },
    "WMT": {
        "name": "沃尔玛 Walmart",
        "sector": "零售",
        "moat": "★★★★★",
        "moat_detail": "全球最大零售商+供应链效率无双+规模采购碾压+线下+线上融合。",
        "roe": "~18-22%",
        "pe_current": "~28-30",
        "pe_5yr_avg": "~24",
        "fcf": "年自由现金流~120亿美元，非常稳定",
        "debt": "适度负债，现金流轻松覆盖",
        "dividend": "连续50年增长，分红贵族，年化~1.2%",
        "management": "Doug McMillon稳健务实",
        "risk": "亚马逊竞争、人工成本上升、消费疲软",
        "buffett_verdict": "巴菲特曾持有沃尔玛多年但后来清仓。不是因为沃尔玛不好，而是因为亚马逊的竞争让他不确定零售业的未来。他后来选择了苹果——一个'确定性更高'的消费品公司。目前PE偏高，不在他的击球区。",
        "buffett_rating": "★★★☆☆",
        "buffett_action": "观望（好企业但当前价格不够安全）",
    },
    "PEP": {
        "name": "百事 PepsiCo",
        "sector": "消费品/食品饮料",
        "moat": "★★★★☆",
        "moat_detail": "全球零食+饮料双巨头+乐事/桂格/佳得乐等强大品牌组合。",
        "roe": "~50%（极高）",
        "pe_current": "~22-24",
        "pe_5yr_avg": "~23",
        "fcf": "年自由现金流~80亿美元，稳定增长",
        "debt": "适度负债",
        "dividend": "连续51年增长，年化~2.8%",
        "management": "Ramon Laguarta运营能力强",
        "risk": "健康趋势（零食减量）、通胀成本",
        "buffett_verdict": "巴菲特多次表示欣赏百事但选了可口可乐——他更喜欢'纯饮料'的简单商业模式。百事也是一家拥有极强护城河的企业，估值合理，分红强劲。如果它回调到PE 20以下，是一个典型的巴菲特式买入机会。",
        "buffett_rating": "★★★★☆",
        "buffett_action": "等待回调后买入",
    },
    "JPM": {
        "name": "摩根大通 JPMorgan Chase",
        "sector": "金融/银行",
        "moat": "★★★★★",
        "moat_detail": "美国最大银行+最强投资银行+Jamie Dimon传奇领导。金融危机中的'堡垒'。",
        "roe": "~15-17%",
        "pe_current": "~11-13",
        "pe_5yr_avg": "~12",
        "fcf": "银行强大的流动性",
        "debt": "银行正常经营杠杆",
        "dividend": "年化~2.5%，持续增长",
        "management": "Jamie Dimon——巴菲特最尊重的银行家",
        "risk": "信贷周期、监管收紧、地缘风险",
        "buffett_verdict": "巴菲特持有JPM后卖出了。他说不是因为银行不好，而是他'想简化伯克希尔的银行持仓'。Jamie Dimon是他最尊重的CEO之一。以当前PE 12估值，这是最便宜的优质银行股之一。如果你看好美国经济，JPM是最好的银行敞口。",
        "buffett_rating": "★★★☆☆",
        "buffett_action": "小仓位持有（巴菲特已减持银行板块）",
    },
    "SPY": {
        "name": "标普500指数 S&P 500 ETF",
        "sector": "全市场指数",
        "moat": "★★★★★",
        "moat_detail": "美国500家最强企业的集合。对于99%的普通投资者，这是最好的选择。",
        "roe": "包含500家企业平均ROE",
        "pe_current": "~22-24",
        "pe_5yr_avg": "~20",
        "fcf": "500家企业自由现金流的总和",
        "debt": "不适用",
        "dividend": "年化~1.3%",
        "management": "不适用",
        "risk": "系统性市场风险、经济衰退",
        "buffett_verdict": "巴菲特强烈推荐普通投资者定投标普500指数。他甚至在遗嘱里写了：留给太太的钱，90%买标普500，10%买短期国债。'一个什么都不会的人，坚持定投标普500，长期必将战胜绝大多数专业投资者。'但注意——2024年巴菲特自己卖掉了所有标普500 ETF，因为觉得市场太贵。",
        "buffett_rating": "★★★★★",
        "buffett_action": "定投（任何时候都是普通人的最佳选择）",
    },
}

# 行业特征速查
SECTOR_BUFFETT_VIEW = {
    "消费品": "巴菲特最喜欢的行业。品牌忠诚度高、商业模式简单、现金流稳定。可口可乐、喜诗糖果都是典型。",
    "金融": "喜欢但挑剔。要选管理优秀、资产质量好的。危机期间是买入良机（他就是这样入的美国银行）。",
    "能源": "周期性行业，需要逆周期买入。巴菲特近年加仓能源，押注能源安全和通胀。",
    "科技": "谨慎。他不排斥科技，但只买'看起来像消费品'的科技股。苹果就是例子——它不是买的iPhone技术，而是买的10亿用户的消费习惯。",
    "医药/健康": "理论上好赛道（人口老龄化），但巴菲特说他不确定20年后谁能活下来——研发风险太大，不是他的能力圈。",
    "制造业": "喜欢有独特优势的制造业企业（精密铸件、BNSF铁路），但要避开'重资产、低回报'的陷阱。",
    "新能源": "比亚迪是最大成功案例。但新技术迭代快，需要极高的选股能力。他本人买的是能源旧经济（石油+天然气）。",
}


def _score_to_stars(score):
    """分数转星级"""
    if score >= 85:
        return "★★★★★"
    elif score >= 70:
        return "★★★★☆"
    elif score >= 55:
        return "★★★☆☆"
    elif score >= 40:
        return "★★☆☆☆"
    elif score >= 25:
        return "★☆☆☆☆"
    return "☆☆☆☆☆"


def analyze_stock(stock_name):
    """
    以巴菲特身份对给定股票进行全面测评。
    返回: 测评报告 dict
    """
    stock_name_upper = stock_name.upper().strip()

    # 查找股票
    stock = None
    for code, data in STOCK_DATABASE.items():
        if stock_name_upper == code or stock_name in data["name"] or stock_name_upper in data["name"].upper():
            stock = data
            stock_code = code
            break

    if not stock:
        # 通用分析框架
        return {
            "found": False,
            "stock_name": stock_name,
            "response": _generic_analysis(stock_name),
        }

    # 基于巴菲特清单打分
    scores = {}
    total = 0
    max_score = sum(v["weight"] for v in BUFFETT_CHECKLIST.values())

    moat_stars = len(stock.get("moat", "★★★").replace("☆", ""))
    scores["护城河"] = (moat_stars / 5) * BUFFETT_CHECKLIST["护城河"]["weight"]

    pe = stock.get("pe_current", "N/A")
    if isinstance(pe, str) and "~" in pe:
        pe_val = float(pe.replace("~", "").split("-")[0])
    else:
        pe_val = 25
    if pe_val < 15:
        scores["安全边际"] = 20
    elif pe_val < 20:
        scores["安全边际"] = 16
    elif pe_val < 25:
        scores["安全边际"] = 12
    elif pe_val < 30:
        scores["安全边际"] = 8
    else:
        scores["安全边际"] = 4
    scores["安全边际"] = scores["安全边际"] * BUFFETT_CHECKLIST["安全边际"]["weight"] / 25

    roe = stock.get("roe", "")
    if "> 20" in roe or "~150" in roe or "~45" in roe or "~50" in roe:
        scores["ROE与盈利能力"] = 20
    elif "15" in roe:
        scores["ROE与盈利能力"] = 15
    else:
        scores["ROE与盈利能力"] = 10
    scores["ROE与盈利能力"] = scores["ROE与盈利能力"] * BUFFETT_CHECKLIST["ROE与盈利能力"]["weight"] / 25

    mgmt = stock.get("management", "")
    if "天才" in mgmt or "极强" in mgmt or "传奇" in mgmt:
        scores["管理层质量"] = 15
    elif "优秀" in mgmt or "稳健" in mgmt:
        scores["管理层质量"] = 12
    elif "争议" in mgmt or "不可预测" in mgmt:
        scores["管理层质量"] = 6
    else:
        scores["管理层质量"] = 9
    scores["管理层质量"] = scores["管理层质量"] * BUFFETT_CHECKLIST["管理层质量"]["weight"] / 25

    fcf = stock.get("fcf", "")
    if "~1000亿" in fcf or "极为充沛" in fcf or "全球第一" in fcf:
        scores["自由现金流"] = 10
    elif "充沛" in fcf or "极强" in fcf or "稳定增长" in fcf:
        scores["自由现金流"] = 9
    elif "改善" in fcf:
        scores["自由现金流"] = 7
    elif "波动" in fcf:
        scores["自由现金流"] = 5
    else:
        scores["自由现金流"] = 6
    scores["自由现金流"] = scores["自由现金流"] * BUFFETT_CHECKLIST["自由现金流"]["weight"] / 25

    sector = stock.get("sector", "")
    if "消费" in sector:
        scores["能力圈"] = 10
    elif "金融" in sector or "能源" in sector:
        scores["能力圈"] = 8
    elif "科技" in sector:
        scores["能力圈"] = 5
    else:
        scores["能力圈"] = 6
    scores["能力圈"] = scores["能力圈"] * BUFFETT_CHECKLIST["能力圈"]["weight"] / 25

    total_score = sum(scores.values())
    final_score = round(total_score / max_score * 100)

    # 评分区间映射
    if final_score >= 85:
        recommendation = "强烈推荐买入"
        action_detail = "这是一家巴菲特会喜欢的企业。强大的护城河、优秀的盈利能力、合理的估值。如果市场出现恐慌性下跌，加大仓位。记住：别人贪婪时恐惧，别人恐惧时贪婪。"
    elif final_score >= 70:
        recommendation = "值得买入并长期持有"
        action_detail = "总体上符合巴菲特选股标准。企业的基本面扎实，护城河清晰。现有仓位可以持有，有回调就是加仓良机。思考：10年后这家公司还会在吗？如果答案是肯定的，就买。"
    elif final_score >= 55:
        recommendation = "持有观望（关注回调）"
        action_detail = "好企业，但目前的价格不够有吸引力。巴菲特此时的做法是：保持耐心，让现金待在账上，等待'胖子球'（最好的击球点）。他不介意错过一班车，只介意坐错了车。"
    elif final_score >= 40:
        recommendation = "暂不建议买入"
        action_detail = "要么估值偏高，要么不在巴菲特的能力圈范围内。记住他的忠告：错过你可以接受的，但下错了注你承受不起。学习等待——耐心是投资最大的美德。"
    elif final_score >= 25:
        recommendation = "强烈不建议买入"
        action_detail = "这家企业存在巴菲特无法接受的问题：要么护城河太浅、要么估值泡沫、要么商业模式无法理解。他说过：'衍生品是大规模杀伤性武器'，高估值股票也是。不要碰。"
    else:
        recommendation = "巴菲特不会碰"
        action_detail = "完全不符合选股标准。巴菲特宁可持有现金（他现在有3340亿现金），也不会买一家他不理解或者估值离谱的企业。现金不是坏事——它让你在真正的机会来临时有子弹。"

    # 生成报告
    report_lines = []
    report_lines.append("═" * 60)
    report_lines.append(f"  巴菲特视角股票测评报告")
    report_lines.append(f"  标的: {stock['name']} ({stock_code})")
    report_lines.append(f"  行业: {stock['sector']}")
    report_lines.append("═" * 60)
    report_lines.append("")
    report_lines.append(f"  📊 巴菲特综合评分: {final_score}/100  {_score_to_stars(final_score)}")
    report_lines.append(f"  💬 建议: {recommendation}")
    report_lines.append("")

    report_lines.append("  ── 六维深度分析 ──")
    for dim, info in BUFFETT_CHECKLIST.items():
        dim_score = round(scores[dim] / info["weight"] * 25)
        bar = "█" * (dim_score // 5) + "░" * (5 - dim_score // 5)
        report_lines.append(f"  {dim:<12} [{bar}] {dim_score}/25")

    report_lines.append("")
    report_lines.append(f"  🏰 护城河: {stock['moat']}")
    report_lines.append(f"     {stock['moat_detail']}")
    report_lines.append(f"  📈 ROE: {stock['roe']}")
    report_lines.append(f"  💰 PE(当前): {stock['pe_current']} | 5年均值: {stock['pe_5yr_avg']}")
    report_lines.append(f"  💵 自由现金流: {stock['fcf']}")
    report_lines.append(f"  💳 负债: {stock['debt']}")
    report_lines.append(f"  💸 分红: {stock['dividend']}")
    report_lines.append(f"  👔 管理层: {stock['management']}")
    report_lines.append(f"  ⚠️  风险: {stock['risk']}")
    report_lines.append("")
    report_lines.append(f"  ── 巴菲特的判断 ──")
    report_lines.append(f"  {stock['buffett_verdict']}")
    report_lines.append("")
    report_lines.append(f"  🎯 操作建议: {stock['buffett_action']}")
    report_lines.append(f"  📋 行动指南: {action_detail}")
    report_lines.append("")
    report_lines.append(f"  ── 一句总结 ──")
    report_lines.append(f"  \"{random.choice(INVESTMENT_PRINCIPLES['价值投资'])}\"")
    report_lines.append("═" * 60)

    return {
        "found": True,
        "stock_name": stock["name"],
        "stock_code": stock_code,
        "score": final_score,
        "rating": recommendation,
        "action": stock["buffett_action"],
        "response": "\n".join(report_lines),
    }


def _generic_analysis(stock_name):
    """对知识库之外的股票给出通用巴菲特框架分析"""
    lines = []
    lines.append("═" * 60)
    lines.append(f"  巴菲特视角 — '{stock_name}' 通用测评框架")
    lines.append("═" * 60)
    lines.append("")
    lines.append("  ⚠️ 该股票不在巴菲特常用标的库中，以下是测评框架。")
    lines.append("  请对照以下6个维度自我评估：")
    lines.append("")
    for dim, info in BUFFETT_CHECKLIST.items():
        lines.append(f"  [{dim}] (权重{info['weight']}%) {info['desc']}")
        lines.append(f"    ✅ 好的信号: {', '.join(info['signals_good'][:3])}")
        lines.append(f"    ❌ 坏的信号: {', '.join(info['signals_bad'][:3])}")
        lines.append("")
    lines.append("  ── 巴菲特会问你的三个问题 ──")
    lines.append(f"  1. 你能用一句话说清楚这家公司怎么赚钱吗？")
    lines.append(f"  2. 10年后这家公司还会存在吗？会比现在更强吗？")
    lines.append(f"  3. 如果股市明天关门停业5年，你还愿意持有它吗？")
    lines.append("")
    lines.append(f"  如果三个答案都是'是' → 深入研究，等合适价格买入")
    lines.append(f"  如果有任何一个'不确定' → 不投，换下一家")
    lines.append(f"  如果有任何一个'否' → 远离，不管别人怎么吹")
    lines.append("")
    lines.append(f"  \"{random.choice(INVESTMENT_PRINCIPLES['能力圈'])}\"")
    lines.append("═" * 60)
    return "\n".join(lines)


def get_random_quote(category=None):
    """随机获取一条巴菲特语录"""
    if category and category in INVESTMENT_PRINCIPLES:
        return random.choice(INVESTMENT_PRINCIPLES[category])
    cat = random.choice(list(INVESTMENT_PRINCIPLES.keys()))
    return f"【{cat}】{random.choice(INVESTMENT_PRINCIPLES[cat])}"


def get_all_categories():
    """列出所有分类及语录数量"""
    return {k: len(v) for k, v in INVESTMENT_PRINCIPLES.items()}


def get_random_case():
    """随机获取一个经典投资案例"""
    case = random.choice(CLASSIC_CASES)
    return case


def get_portfolio_summary():
    """获取最新持仓概览"""
    return PORTFOLIO_2025


def search_quotes(keyword):
    """按关键词搜索语录"""
    results = []
    for cat, lines in INVESTMENT_PRINCIPLES.items():
        for line in lines:
            if keyword in line:
                results.append(f"【{cat}】{line}")
    return results


def mentor_response(question):
    """根据用户问题，返回巴菲特风格的导师回答"""
    q = question.lower()

    if any(w in q for w in ["买", "卖", "股票", "持仓", "portfolio", "选股", "分析"]):
        theme = "价值投资"
    elif any(w in q for w in ["风险", "亏损", "赔", "杠杆", "安全", "risk"]):
        theme = "风险控制"
    elif any(w in q for w in ["能力圈", "不懂", "了解", "科技", "范围"]):
        theme = "能力圈"
    elif any(w in q for w in ["企业", "公司", "护城河", "商业模式", "business"]):
        theme = "企业分析"
    elif any(w in q for w in ["市场", "行情", "涨", "跌", "熊市", "牛市", "恐慌"]):
        theme = "市场心理"
    elif any(w in q for w in ["人生", "幸福", "成功", "选择", "声誉", "学习", "life"]):
        theme = "人生智慧"
    else:
        theme = random.choice(list(INVESTMENT_PRINCIPLES.keys()))

    quotes = random.sample(INVESTMENT_PRINCIPLES[theme], min(3, len(INVESTMENT_PRINCIPLES[theme])))
    return {
        "theme": theme,
        "quotes": quotes,
        "response": f"巴菲特说过：\n" + "\n".join(f"  > {q}" for q in quotes),
    }


# ═══════════════════════════════════════
#  CLI
# ═══════════════════════════════════════

if __name__ == "__main__":
    import sys, json

    if len(sys.argv) < 2:
        print("巴菲特AI导师 Skill")
        print("用法: python buffett_agent.py <问题>")
        print("     python buffett_agent.py --analyze <股票名>  # 巴菲特风格股票测评")
        print("     python buffett_agent.py --quote             # 随机投资箴言")
        print("     python buffett_agent.py --portfolio         # 最新持仓概览")
        print("     python buffett_agent.py --case              # 随机经典案例")
        print("     python buffett_agent.py --profile           # 巴菲特档案")
        print("     python buffett_agent.py --search <关键词>")
        print("     python buffett_agent.py --stocks            # 可测评股票列表")
        print()
        print(get_random_quote())
    elif sys.argv[1] == "--analyze" and len(sys.argv) > 2:
        stock = " ".join(sys.argv[2:])
        result = analyze_stock(stock)
        print(result["response"])
    elif sys.argv[1] == "--analyze":
        print("请提供股票名称或代码。例如：")
        print("  python buffett_agent.py --analyze 苹果")
        print("  python buffett_agent.py --analyze AAPL")
        print("  python buffett_agent.py --analyze 比亚迪")
        print()
        print("支持测评的股票：")
        for code, data in sorted(STOCK_DATABASE.items()):
            print(f"  {code:<8} {data['name']}")
    elif sys.argv[1] == "--stocks":
        print("支持测评的股票：")
        for code, data in sorted(STOCK_DATABASE.items()):
            print(f"  {code:<8} {data['name']:<40} {data['sector']}")
    elif sys.argv[1] == "--quote":
        cat = sys.argv[2] if len(sys.argv) > 2 else None
        print(get_random_quote(cat))
    elif sys.argv[1] == "--list":
        for cat, count in get_all_categories().items():
            print(f"  {cat}: {count}条")
    elif sys.argv[1] == "--portfolio":
        p = get_portfolio_summary()
        print(f"现金储备: {p['现金储备']}")
        print("\n五大持仓:")
        for name, weight, note in p["top_holdings"]:
            print(f"  {name}: {weight} — {note}")
        print(f"\n日本布局: {', '.join(p['japan_stakes'])}")
        print(f"  {p['japan_note']}")
        print("\n最近操作:")
        for move in p["recent_moves"]:
            print(f"  - {move}")
    elif sys.argv[1] == "--case":
        case = get_random_case()
        print(f"【{case['name']}】({case['year']}年)")
        print(f"  投入: {case['invested']}")
        print(f"  回报: {case['return']}")
        print(f"  启示: {case['lesson']}")
    elif sys.argv[1] == "--search" and len(sys.argv) > 2:
        results = search_quotes(sys.argv[2])
        if results:
            print(f"搜索 '{sys.argv[2]}' 结果:\n" + "\n".join(results))
        else:
            print(f"未找到与 '{sys.argv[2]}' 相关的语录")
    elif sys.argv[1] == "--profile":
        print(json.dumps(BUFFETT_PROFILE, ensure_ascii=False, indent=2))
    else:
        result = mentor_response(" ".join(sys.argv[1:]))
        print(result["response"])
