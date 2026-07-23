import glob
import re

files = glob.glob('data/assessments/physics-elasticity*.yaml') + glob.glob('data/assessments/physics-universal-gravitation*.yaml')

replacements = {
    '  difficultyDimensions: 2': '  difficultyDimensions:\n  - ModelOrDerivation\n  - Simplification',
    '  difficultyDimensions: 3': '  difficultyDimensions:\n  - ModelOrDerivation\n  - Simplification\n  - IdentityConstruction',
    '  difficultyDimensions: 4': '  difficultyDimensions:\n  - ModelOrDerivation\n  - Simplification\n  - IdentityConstruction\n  - AuxiliaryTechnique',
    '  difficultyDimensions: 5': '  difficultyDimensions:\n  - ModelOrDerivation\n  - Simplification\n  - IdentityConstruction\n  - AuxiliaryTechnique\n  - RepresentationTransfer'
}

for f in files:
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    modified = False
    for k, v in replacements.items():
        if k in content:
            content = content.replace(k, v)
            modified = True
            
    if modified:
        with open(f, 'w', encoding='utf-8') as file:
            file.write(content)
        print(f"Fixed {f}")
