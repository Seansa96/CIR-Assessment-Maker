import yaml, os, json

base = 'data/assessments'

# Groups to merge
groups = {
    'shm': ['physics-simple-harmonic-motion', 'physics-shm-energy', 'physics-shm-circular-motion', 'physics-pendulums'],
    'damped': ['physics-damped-oscillations', 'physics-forced-oscillations'],
    'wave-mechanics': ['physics-traveling-waves', 'physics-wave-mathematics', 'physics-stretched-string-wave-speed', 'physics-standing-waves-resonance'],
    'acoustics': ['physics-sound-waves', 'physics-speed-of-sound', 'physics-sound-intensity', 'physics-standing-sound-modes', 'physics-musical-sound-sources', 'physics-beats', 'physics-doppler-effect', 'physics-shock-waves'],
}

for group, topics in groups.items():
    print(f'=== GROUP: {group} ===')
    for topic in topics:
        for fn in sorted(os.listdir(base)):
            if topic in fn and fn.endswith('.yaml'):
                filepath = f'{base}/{fn}'
                try:
                    with open(filepath, encoding='utf-8') as f:
                        d = yaml.safe_load(f)
                    atype = d.get('assessmentType', '')
                    title = d.get('title', '')
                    print(f'  FILE: {fn} [{atype}] - {title}')
                    if atype == 'glossary':
                        secs = d.get('sections', []) or []
                        for s in secs:
                            sid = s.get('id', '')
                            stitle = s.get('title', '')
                            print(f'    SECTION: {sid} - {stitle}')
                            for e in (s.get('entries', []) or []):
                                print(f'      ENTRY: {e.get("term", "")}')
                    elif atype == 'recallDrill':
                        items = d.get('items', []) or []
                        print(f'    ITEMS: {len(items)} items')
                        for it in items[:2]:
                            prompt = str(it.get('prompt', ''))[:80]
                            print(f'      - {prompt}')
                except Exception as e:
                    print(f'  ERROR in {fn}: {e}')
    print()
