import os
import yaml

def add_media_to_lessons():
    assessments_dir = r"c:\Users\SeanS\Downloads\cir_app\data\assessments"
    
    # 1. Chapter 7
    ch7_path = os.path.join(assessments_dir, "ec-ch7-lesson1.yaml")
    if os.path.exists(ch7_path):
        with open(ch7_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        if 'workedExamples' in data and len(data['workedExamples']) > 0:
            we = data['workedExamples'][0]
            if 'steps' in we and len(we['steps']) > 0:
                step = we['steps'][0]
                step['media'] = [
                    {
                        "type": "image",
                        "src": "/assessments/electronics-and-circuits/rc-step-response.svg",
                        "alt": "Step response of a first-order RC circuit showing the time constant tau."
                    }
                ]
        with open(ch7_path, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, sort_keys=False, allow_unicode=True)
            print("Added media to ch7 lesson")

    # 2. Chapter 8
    ch8_path = os.path.join(assessments_dir, "ec-ch8-lesson1.yaml")
    if os.path.exists(ch8_path):
        with open(ch8_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        if 'workedExamples' in data and len(data['workedExamples']) > 0:
            we = data['workedExamples'][0]
            if 'steps' in we and len(we['steps']) > 0:
                step = we['steps'][0]
                step['media'] = [
                    {
                        "type": "image",
                        "src": "/assessments/electronics-and-circuits/rlc-natural-response.svg",
                        "alt": "Natural response of an RLC circuit showing underdamped, critically damped, and overdamped cases."
                    }
                ]
        with open(ch8_path, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, sort_keys=False, allow_unicode=True)
            print("Added media to ch8 lesson")

if __name__ == "__main__":
    add_media_to_lessons()
