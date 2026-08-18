import os

base = 'data/assessments'
retired_dir = os.path.join(base, 'retired')

if not os.path.exists(retired_dir):
    os.makedirs(retired_dir)

topic_map = {
    'physics-simple-harmonic-motion': 'physics-oscillations-shm',
    'physics-shm-energy': 'physics-oscillations-shm',
    'physics-shm-circular-motion': 'physics-oscillations-shm',
    'physics-pendulums': 'physics-oscillations-shm',
    'physics-damped-oscillations': 'physics-damped-forced-oscillations',
    'physics-forced-oscillations': 'physics-damped-forced-oscillations',
    'physics-traveling-waves': 'physics-wave-mechanics',
    'physics-wave-mathematics': 'physics-wave-mechanics',
    'physics-stretched-string-wave-speed': 'physics-wave-mechanics',
    'physics-standing-waves-resonance': 'physics-wave-mechanics',
    'physics-sound-waves': 'physics-acoustics',
    'physics-speed-of-sound': 'physics-acoustics',
    'physics-sound-intensity': 'physics-acoustics',
    'physics-standing-sound-modes': 'physics-acoustics',
    'physics-musical-sound-sources': 'physics-acoustics',
    'physics-beats': 'physics-acoustics',
    'physics-doppler-effect': 'physics-acoustics',
    'physics-shock-waves': 'physics-acoustics'
}

file_map = {
    'physics-terminal-velocity-derivation-worked-example.yaml': 'physics-calculus-derivations',
    'physics-linear-drag-velocity-derivation-worked-example.yaml': 'physics-calculus-derivations'
}

stubs_to_retire = [f"{t}-glossary.yaml" for t in topic_map.keys()] + [f"{t}-recall-drill.yaml" for t in topic_map.keys()]
concept_tests_to_retire = [
    'physics-angular-momentum-concept-test.yaml', 'physics-dynamics-concept-test.yaml',
    'physics-energy-momentum-concept-test.yaml', 'physics-fixed-axis-rotation-concept-test.yaml',
    'physics-fluid-mechanics-concept-test.yaml', 'physics-gravitation-concept-test.yaml',
    'physics-kinematics-concept-test.yaml', 'physics-oscillations-waves-acoustics-concept-test.yaml',
    'physics-properties-of-matter-concept-test.yaml'
]
files_to_retire = set(stubs_to_retire + concept_tests_to_retire)

for fn in os.listdir(base):
    if not fn.endswith('.yaml'): continue
    filepath = os.path.join(base, fn)
    
    if fn in files_to_retire:
        print(f"Retiring: {fn}")
        os.rename(filepath, os.path.join(retired_dir, fn))
        continue
        
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        modified = False
        new_topic = None
        
        if fn in file_map:
            new_topic = file_map[fn]
        else:
            for old_t, new_t in topic_map.items():
                if f"topicId: {old_t}" in content:
                    new_topic = new_t
                    break
                    
        if new_topic:
            print(f"Retargeting {fn} to {new_topic}")
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if line.startswith('topicId:'):
                    lines[i] = f"topicId: {new_topic}"
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write('\n'.join(lines))
    except Exception as e:
        print(f"Error processing {fn}: {e}")

print("Done phase 3 and 4.")
