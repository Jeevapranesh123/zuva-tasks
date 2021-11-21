import json
with open('/home/jeeva/Developer/flask-api/config.json','r') as f:
  config=json.load(f)

print(config)