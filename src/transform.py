
import json
from core.SpiderConfig import BossConfig, FiveOneConfig, HookConfig
from services.JobServices import JobService

# FILE = "./src/core/51data.json"
# CONFIG = FiveOneConfig
# FILE = "./src/core/bossdata.json"
# CONFIG = BossConfig
FILE = "./src/core/hookdata.html"
CONFIG = HookConfig

jobService = JobService()
jobs = []
config = CONFIG("配置")
text = open(FILE, encoding="utf-8").read()
items = config.getRawJobsList(text)
idx = 0
while idx != len(items):
    item = items[idx]
    try:
        job = config.createRawJobInstance(item).toLocalJob()
        if job:
            jobService.add(job)
            items.pop(idx)
        else:
            idx = idx + 1
    except:
        idx = idx + 1
        continue
    
with open(FILE, encoding="utf-8", mode="w+") as file:
    file.write(json.dumps(config.__json_data__))