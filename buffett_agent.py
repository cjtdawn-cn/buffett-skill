"""
巴菲特AI导师 — Warren Buffett AI Investment Mentor
用法:
  python buffett_agent.py "苹果股票现在能买吗"
  python buffett_agent.py --quote        # 随机投资箴言
  python buffett_agent.py --portfolio    # 最新持仓
  python buffett_agent.py --case         # 随机经典案例
  python buffett_agent.py --profile      # 巴菲特档案
"""
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
        print("     python buffett_agent.py --quote       随机投资箴言")
        print("     python buffett_agent.py --portfolio   最新持仓概览")
        print("     python buffett_agent.py --case        随机经典案例")
        print("     python buffett_agent.py --profile     巴菲特档案")
        print("     python buffett_agent.py --search <关键词>")
        print()
        print(get_random_quote())
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
