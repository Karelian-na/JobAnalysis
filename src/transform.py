
import json
from core.SpiderConfig import BossConfig, FiveOneConfig
from services.JobServices import JobService

# FILE = "./src/core/51data.json"
# CONFIG = FiveOneConfig
FILE = "./src/core/bossdata.json"
CONFIG = BossConfig

jobService = JobService()
jobs = []
config = CONFIG(10)
data = json.load(open(FILE, encoding="utf-8"))
items = config.getRawJobsList(data)
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

with open(FILE, mode="w+", encoding="utf-8") as file:
    file.write(json.dumps(data))