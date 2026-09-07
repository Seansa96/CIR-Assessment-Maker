"""Restore stable q001...q010 order after deliberate bank additions."""
import sys
from pathlib import Path
import yaml

path = Path(sys.argv[1])
data = yaml.safe_load(path.read_text(encoding='utf-8'))
data['questions'].sort(key=lambda question: question['id'])
path.write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=True, width=110), encoding='utf-8')
