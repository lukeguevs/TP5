from collections import Counter, defaultdict
import re
from datetime import datetime
import string

patterns = [
    (re.compile(r'/login', re.IGNORECASE), 'login'),
    (re.compile(r'/feed', re.IGNORECASE), 'view_feed'),
    (re.compile(r'/post', re.IGNORECASE), 'post'),
    (re.compile(r'/like', re.IGNORECASE), 'like'),
    (re.compile(r'/follow', re.IGNORECASE), 'follow'),
    (re.compile(r'/profile', re.IGNORECASE), 'view_profile'),
]

with open('logs.txt', 'rb') as f:
    raw_data = f.read()
text = raw_data.decode('utf-16-le', errors='ignore')
lines = [''.join(ch for ch in line if ch in string.printable) for line in text.split('\n') if line.strip()]

re_date = re.compile(r'\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\]')

dates = []
actions = []
charge_globale = Counter()  # <--- Il FAUT déclarer ici !

for line in lines:
    date_match = re_date.search(line)
    action_label = None
    for pattern, label in patterns:
        if pattern.search(line):
            action_label = label
            charge_globale[label] += 1      # <--- On compte chaque action globale ici !
            break
    if date_match and action_label:
        date = date_match.group(1)
        dates.append(date)
        actions.append(action_label)

start_date = min(dates) if dates else None
end_date = max(dates) if dates else None

interval = None
if start_date and end_date:
    t1 = datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S')
    t2 = datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S')
    interval = str(t2 - t1)

# Résultats
print(f'Date de début: {start_date}')
print(f'Date de fin: {end_date}')
print(f'Intervalle: {interval}')

print('Charge globale:')
for key, val in charge_globale.items():
    print(f'{key}: {val}')

# Chaîne de Markov
transition_counts = defaultdict(Counter)
for (prev, nxt) in zip(actions, actions[1:]):
    transition_counts[prev][nxt] += 1

transition_probs = { src: {dst: cnt/sum(counter.values()) for dst, cnt in counter.items()} for src, counter in transition_counts.items() }
print('Transitions (Markov):')
for src, dsts in transition_probs.items():
    print(f'{src} -> {dsts}')
