#!/usr/bin/env python3
import json
import os

template_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mc_template.py')
tweaks_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tweaks.json')
mc_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mc')

with open(template_file, 'r', encoding='utf-8') as f:
    template = f.read()

with open(tweaks_file, 'r', encoding='utf-8') as f:
    tweaks = json.load(f)

final = template.replace('__TWEAKS_JSON_PLACEHOLDER__', json.dumps(tweaks, ensure_ascii=False, indent=2))

with open(mc_file, 'w', encoding='utf-8') as f:
    f.write(final)

os.chmod(mc_file, 0o755)
print('Successfully generated scripts/mc with 100 bilingual tweaks embedded!')
