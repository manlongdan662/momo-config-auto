import json
import urllib.request

# 两个远程文件 URL
URLS = [
    "https://raw.githubusercontent.com/manlongdan/rule_set/refs/heads/main/config/config.json",
    "https://raw.githubusercontent.com/manlongdan/rule_set/refs/heads/main/config/my_sub_momo.json"
]

def fetch_json(url):
    with urllib.request.urlopen(url) as response:
        return json.load(response)

# 读取 base 配置
base = fetch_json(URLS[0])
custom = fetch_json(URLS[1])

# 合并 rule_set（保留 base 优先，custom 后覆盖/追加）
base_rule_sets = {r["tag"]: r for r in base.get("route", {}).get("rule_set", [])}
for r in custom.get("route", {}).get("rule_set", []):
    base_rule_sets[r["tag"]] = r
base.setdefault("route", {})["rule_set"] = list(base_rule_sets.values())

# 合并 rules（追加 custom.rules 到末尾）
base_rules = base.get("route", {}).get("rules", [])
custom_rules = custom.get("route", {}).get("rules", [])
base_rules.extend(custom_rules)
base["route"]["rules"] = base_rules

# 输出最终文件
with open("merged_momo.json", "w", encoding="utf-8") as f:
    json.dump(base, f, ensure_ascii=False, indent=2)

print("✅ 合并完成 -> merged_momo.json")
