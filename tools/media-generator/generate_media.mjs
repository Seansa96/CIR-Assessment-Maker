import fs from 'fs';
import path from 'path';

// Output directory is frontend/public/media/placeholders
const outDir = path.resolve('../../frontend/public/media/placeholders');

if (!fs.existsSync(outDir)) {
    fs.mkdirSync(outDir, { recursive: true });
}

function beakerSVG(title, subtitle, amount, color) {
    // Generate a simple SVG beaker
    return `<svg width="200" height="250" xmlns="http://www.w3.org/2000/svg">
        <rect x="50" y="50" width="100" height="150" rx="10" fill="none" stroke="#333" stroke-width="4"/>
        <line x1="40" y1="50" x2="160" y2="50" stroke="#333" stroke-width="4" stroke-linecap="round"/>
        
        <!-- Fill level based on 'amount' parameter (0-1) -->
        <rect x="52" y="${200 - (146 * amount)}" width="96" height="${146 * amount}" rx="8" fill="${color}" opacity="0.7">
            <animate attributeName="height" from="0" to="${146 * amount}" dur="1.5s" fill="freeze" />
            <animate attributeName="y" from="200" to="${200 - (146 * amount)}" dur="1.5s" fill="freeze" />
        </rect>
        
        <text x="100" y="30" font-family="sans-serif" font-size="16" font-weight="bold" text-anchor="middle" fill="#333">${title}</text>
        <text x="100" y="230" font-family="sans-serif" font-size="14" text-anchor="middle" fill="#555">${subtitle}</text>
    </svg>`;
}

function boxSVG(title, lines, color) {
    let tspan = lines.map((l, i) => `<tspan x="100" dy="${i===0 ? 0 : 25}">${l}</tspan>`).join('');
    return `<svg width="200" height="250" xmlns="http://www.w3.org/2000/svg">
        <rect x="10" y="40" width="180" height="180" rx="8" fill="${color}" opacity="0.3" stroke="#333" stroke-width="2"/>
        <text x="100" y="25" font-family="sans-serif" font-size="16" font-weight="bold" text-anchor="middle" fill="#111">${title}</text>
        <text x="100" y="80" font-family="sans-serif" font-size="14" text-anchor="middle" fill="#333">${tspan}</text>
    </svg>`;
}

function moleculeNodeSVG(type) {
    if (type === 'benzene') {
        return `<svg width="200" height="250" xmlns="http://www.w3.org/2000/svg">
            <polygon points="100,50 160,85 160,155 100,190 40,155 40,85" fill="none" stroke="#333" stroke-width="4"/>
            <circle cx="100" cy="120" r="45" fill="none" stroke="#333" stroke-width="4"/>
            <text x="100" y="230" font-family="sans-serif" font-size="16" font-weight="bold" text-anchor="middle" fill="#333">Benzene (C6H6)</text>
        </svg>`;
    } else {
        return `<svg width="200" height="250" xmlns="http://www.w3.org/2000/svg">
            <polygon points="100,50 160,85 160,155 100,190 40,155 40,85" fill="none" stroke="#333" stroke-width="4"/>
            <text x="100" y="220" font-family="sans-serif" font-size="16" font-weight="bold" text-anchor="middle" fill="#333">Cyclohexane</text>
            <text x="100" y="240" font-family="sans-serif" font-size="16" font-weight="bold" text-anchor="middle" fill="#333">(C6H12)</text>
        </svg>`;
    }
}

function sideBySide(svgs, title) {
    const totalWidth = svgs.length * 200 + (svgs.length - 1) * 20;
    
    let inner = '';
    let xOffset = 0;
    for (const svg of svgs) {
        const content = svg.replace(/<svg[^>]*>([\s\S]*?)<\/svg>/i, '$1');
        inner += `<g transform="translate(${xOffset}, 40)">${content}</g>`;
        xOffset += 220;
    }
    
    return `<svg width="${Math.max(totalWidth, 400)}" height="320" xmlns="http://www.w3.org/2000/svg">
        <rect width="100%" height="100%" fill="#ffffff" />
        <text x="${Math.max(totalWidth, 400)/2}" y="25" font-family="sans-serif" font-size="20" font-weight="bold" text-anchor="middle" fill="#111">${title}</text>
        ${inner}
    </svg>`;
}

// 1. Mole-to-Mole
fs.writeFileSync(path.join(outDir, 'stoich-mole-lab.svg'), sideBySide([
    beakerSVG('Reactant', '5.00 mol H2', 0.2, '#aadaff'),
    beakerSVG('Product', '1.67 mol N2', 0.1, '#ffc0a0')
], 'Lab Scale Ammonia Reaction'));

fs.writeFileSync(path.join(outDir, 'stoich-mole-pilot.svg'), sideBySide([
    beakerSVG('Reactant', '500.0 mol H2', 0.5, '#aadaff'),
    beakerSVG('Product', '166.7 mol N2', 0.25, '#ffc0a0')
], 'Pilot Scale Ammonia Reaction'));

fs.writeFileSync(path.join(outDir, 'stoich-mole-industrial.svg'), sideBySide([
    beakerSVG('Reactant', '50000 mol H2', 0.9, '#aadaff'),
    beakerSVG('Product', '16667 mol N2', 0.45, '#ffc0a0')
], 'Industrial Scale Ammonia Reaction'));

// 2. Limiting Reactant
fs.writeFileSync(path.join(outDir, 'stoich-limiting-small.svg'), sideBySide([
    beakerSVG('H2 (Excess)', '25.0g (12.4mol)', 0.5, '#aadaff'),
    beakerSVG('O2 (Limiting)', '75.0g (2.3mol)', 0.1, '#ffd0d0'),
    beakerSVG('H2O Yield', '78.5g (93%)', 0.2, '#c0e0c0')
], 'Small Reactor (Limiting Reactant)'));

fs.writeFileSync(path.join(outDir, 'stoich-limiting-large.svg'), sideBySide([
    beakerSVG('H2 (Excess)', '250g (124mol)', 0.9, '#aadaff'),
    beakerSVG('O2 (Limiting)', '750g (23.4mol)', 0.2, '#ffd0d0'),
    beakerSVG('H2O Yield', '785g (93%)', 0.4, '#c0e0c0')
], 'Large Reactor (Limiting Reactant)'));

// 3. Complete Stoichiometry
fs.writeFileSync(path.join(outDir, 'stoich-complete-small.svg'), sideBySide([
    beakerSVG('Fe (Limiting)', '15.0g', 0.1, '#e0e0e0'),
    beakerSVG('HCl (Excess)', '30.0g', 0.3, '#ffffb0'),
    beakerSVG('FeCl2 Yield', '34.04g', 0.2, '#d0e0ff')
], 'Small Experiment (Mass to Mass)'));

fs.writeFileSync(path.join(outDir, 'stoich-complete-scaled.svg'), sideBySide([
    beakerSVG('Fe (Limiting)', '150.0g', 0.3, '#e0e0e0'),
    beakerSVG('HCl (Excess)', '300.0g', 0.9, '#ffffb0'),
    beakerSVG('FeCl2 Yield', '340.5g', 0.6, '#d0e0ff')
], 'Scaled Experiment (Mass to Mass)'));

// 4. Combustion Empirical
fs.writeFileSync(path.join(outDir, 'combustion-empirical-small.svg'), sideBySide([
    boxSVG('Sample (1.0g)', ['C: 0.4000g', 'H: 0.0671g', 'O: 0.5329g'], '#ffeadb'),
    boxSVG('Result', ['Empirical', 'Formula:', 'CH2O'], '#dbffea')
], 'Combustion Analysis (Small Sample)'));

fs.writeFileSync(path.join(outDir, 'combustion-empirical-scaled.svg'), sideBySide([
    boxSVG('Sample (10.0g)', ['C: 4.000g', 'H: 0.671g', 'O: 5.329g'], '#ffeadb'),
    boxSVG('Result', ['Empirical', 'Formula:', 'CH2O'], '#dbffea')
], 'Combustion Analysis (Scaled Sample)'));

// 5. Formula Molecular
fs.writeFileSync(path.join(outDir, 'formula-molecular-first.svg'), sideBySide([
    boxSVG('Data', ['EF: CH2 (14g/mol)', 'MM: 84.2 g/mol', 'n = 6'], '#e5dbff'),
    moleculeNodeSVG('cyclohexane')
], 'Molecular Formula (Unknown 1)'));

fs.writeFileSync(path.join(outDir, 'formula-molecular-second.svg'), sideBySide([
    boxSVG('Data', ['EF: CH (13g/mol)', 'MM: 78.1 g/mol', 'n = 6'], '#e5dbff'),
    moleculeNodeSVG('benzene')
], 'Molecular Formula (Unknown 2)'));

// 6. Mole Grams
fs.writeFileSync(path.join(outDir, 'mole-grams-basic.svg'), sideBySide([
    boxSVG('Na', ['Mass: 45.98 g', 'Moles: 2.00 mol'], '#dbeaff'),
    boxSVG('CaCO3', ['Moles: 3.25 mol', 'Mass: 325.3 g'], '#ffdbe6')
], 'Basic Conversions'));

fs.writeFileSync(path.join(outDir, 'mole-grams-scaled.svg'), sideBySide([
    boxSVG('Na', ['Mass: 459.8 g', 'Moles: 20.0 mol'], '#dbeaff'),
    boxSVG('CaCO3', ['Moles: 32.5 mol', 'Mass: 3253 g'], '#ffdbe6')
], 'Scaled Conversions'));

// 7. Mole Particles
fs.writeFileSync(path.join(outDir, 'mole-particles-glass.svg'), sideBySide([
    beakerSVG('Glass of Water', '250 mL', 0.3, '#aaccff'),
    boxSVG('Molecules', ['8.36 × 10²⁴', 'water molecules'], '#e0ffdb')
], 'Particles in a Glass'));

fs.writeFileSync(path.join(outDir, 'mole-particles-pool.svg'), sideBySide([
    beakerSVG('Swimming Pool', '2.5 × 10⁶ mL', 0.9, '#aaccff'),
    boxSVG('Molecules', ['8.36 × 10²⁸', 'water molecules'], '#e0ffdb')
], 'Particles in a Pool'));

// 8. Molar Mass
fs.writeFileSync(path.join(outDir, 'molar-mass-iron.svg'), sideBySide([
    boxSVG('Fe2O3', ['M: 159.69 g/mol', 'Fe: 69.94%'], '#ffe5cc'),
    boxSVG('Fe3O4', ['M: 231.53 g/mol', 'Fe: 72.36%'], '#ffcc99')
], 'Iron Oxides Analysis'));

fs.writeFileSync(path.join(outDir, 'molar-mass-copper.svg'), sideBySide([
    boxSVG('CuO', ['M: 79.55 g/mol', 'Cu: 79.89%'], '#ccffcc'),
    boxSVG('Cu2O', ['M: 143.09 g/mol', 'Cu: 88.82%'], '#99ff99')
], 'Copper Oxides Analysis'));

console.log('Successfully generated all STEM SVG media placeholers to ' + outDir);
