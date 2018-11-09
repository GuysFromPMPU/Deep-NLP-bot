import yaml
import random

dialogues = yaml.load(open('dialogues.yaml', 'r', encoding="utf-8"))

def get_replica(topic):
    if topic in dialogues:
        found = dialogues[topic]
        replica = found if isinstance(found, str) else random.choice(dialogues[topic])
    else:
        replica = random.choice(dialogues['undefined'])

    return replica