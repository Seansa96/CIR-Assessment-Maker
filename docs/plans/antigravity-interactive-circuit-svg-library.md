# Antigravity Implementation Plan: Interactive Circuit SVG Library

## Status

- **Audience:** Antigravity IDE agent
- **Project:** CIR Assessment Maker
- **Feature:** Interactive circuit SVG library, authoring tools, and assessment support
- **Plan state:** Decision complete
- **Simulation policy:** No electrical simulation in V1
- **Symbol convention:** ANSI-first, with IEC alternatives where useful

Before implementation, read:

- `AGENTS.md`
- `docs/agent-coexistence.md`
- `docs/assessment-yaml-latex.md`
- Current domain models and assessment validation code
- Existing electronics category and area definitions

Check `git status --short` before editing. Do not revert or overwrite unrelated user, Codex, Gemini, or runtime-state changes.

## Summary

Add a trusted, reusable circuit-symbol SVG library, visual circuit editor, and backend-authoritative `circuit` question type.

V1 must support:

- Clicking and selecting circuit components, nodes, and branches
- Placing measurement instruments correctly
- Entering component values and labels
- Building circuits from a component palette
- Grading topology independently from visual placement and wire routing
- Authoring through both a visual editor and readable YAML/JSON

V1 must not implement:

- SPICE or other electrical simulation
- Kirchhoff equation solving
- Transient, frequency-domain, or nonlinear analysis
- Arbitrary SVG upload
- Electrical-equivalence transformations such as delta-wye conversion

SVG.js should provide the browser manipulation layer. Assessment data must describe structured components and nets; raw SVG markup must not be the grading source of truth.

## Domain And Schema

Add `QuestionType.Circuit` with YAML/JSON wire value:

```yaml
type: circuit
```

Add a `CircuitQuestionDefinition` attached to `QuestionDefinition`.

Required conceptual shape:

```yaml
- id: q001
  type: circuit
  prompt: |
    Build a series circuit containing a battery, switch, and two resistors.
  circuit:
    schemaVersion: 1
    catalogVersion: 1
    interactionMode: build
    paletteSymbolIds:
      - source.cell
      - switch.spst
      - resistor.ansi
    editableProperties:
      - value
      - label
      - rotation
    diagram:
      width: 900
      height: 520
      components: []
      nodes: []
      wires: []
      annotations: []
  answer:
    circuit:
      topology:
        requiredComponents:
          - symbolId: source.cell
            count: 1
          - symbolId: switch.spst
            count: 1
          - symbolId: resistor.ansi
            count: 2
        requiredConnections:
          mode: singleSeriesLoop
  explanation: |
    A series circuit has one uninterrupted current path.
```

### Interaction Modes

Support exactly these V1 values:

- `select`
- `meterPlacement`
- `valueEntry`
- `build`

### Diagram Model

The diagram must contain structured data:

- Canvas width and height
- Component instances
- Terminals
- Explicit nodes
- Wires
- Labels and annotations
- Optional current arrows and polarity markings

Component instance fields:

- Stable instance ID
- Catalog symbol ID
- Position
- Rotation
- Optional value
- Optional label
- Optional property overrides

Catalog terminal fields:

- Stable terminal ID
- Relative terminal position
- Electrical role where applicable
- Accessible label

Wire fields:

- Stable wire ID
- Source terminal/node ID
- Target terminal/node ID
- Optional orthogonal route points

Connectivity must be determined exclusively from terminal and node references. Never infer electrical connectivity from screen coordinates or intersecting paths.

### Submitted Answer

Extend `SubmittedAnswer` with a nullable `CircuitAnswer`.

It must support:

- Selected component IDs
- Selected node IDs
- Selected branch/wire IDs
- Meter type
- Meter target node pair or branch
- Meter polarity/orientation where required
- Values keyed by component or target ID
- Learner-built component instances
- Learner-built nodes and wires

Persist the complete submitted circuit answer through the current attempt and SQLite serialization.

### Results And Feedback

Add structured circuit feedback:

- Missing components
- Extra components
- Incorrect component types
- Missing connections
- Extra or invalid connections
- Incorrect selected targets
- Incorrect meter placement
- Incorrect polarity
- Incorrect values
- Expected/highlight target IDs

Do not expose expected targets during scored attempts until completion.

## SVG Symbol Library

Create a versioned symbol catalog with stable IDs.

Each symbol entry must define:

- Symbol ID
- Catalog version
- Display title
- Category
- Search tags
- ANSI/IEC convention
- Default dimensions
- View box
- Rotation policy
- Terminal definitions
- SVG geometry
- Accessible title and description

Use original, repository-owned SVG geometry. Do not copy KiCad artwork or third-party symbol SVGs without explicit licensing review.

### Required Catalog Coverage

#### Connectivity And Annotation

- Wire
- Junction
- Wire crossover
- Terminal
- Test point
- Earth ground
- Chassis ground
- Signal ground
- Net label
- Current arrow
- Voltage polarity
- Generic value and component labels

#### Sources

- Cell
- Battery
- DC voltage source
- AC voltage source
- Current source
- Dependent voltage source
- Dependent current source

#### Passive Components

- ANSI resistor
- IEC resistor
- Variable resistor
- Potentiometer
- Non-polarized capacitor
- Polarized capacitor
- Variable capacitor
- Inductor
- Variable inductor
- Transformer

#### Loads And Protection

- Lamp
- Heater/load
- Motor
- Speaker
- Microphone
- Fuse

#### Switching

- SPST switch
- SPDT switch
- Normally open pushbutton
- Normally closed pushbutton
- Relay coil and contacts

#### Measurement

- Ammeter
- Voltmeter
- Ohmmeter
- Generic meter
- Positive/negative probes

#### Diodes

- Rectifier diode
- Zener diode
- LED
- Photodiode
- Bridge rectifier

#### Transistors

- NPN BJT
- PNP BJT
- N-channel MOSFET
- P-channel MOSFET
- N-channel JFET
- P-channel JFET

#### Analog Blocks

- Operational amplifier
- Comparator
- Generic amplifier block

#### Digital Logic

- AND
- OR
- NOT
- NAND
- NOR
- XOR
- XNOR
- Schmitt trigger
- Buffer
- Tri-state buffer
- Logic input and output
- Clock
- Flip-flop
- Multiplexer
- Demultiplexer
- Counter

#### Generic Devices

- Generic IC block
- Connector
- Multi-pin header
- Generic two-terminal device

ANSI is the default variant. IEC symbols should be separate catalog entries when their geometry materially differs.

## Frontend Circuit Canvas

Add SVG.js and its appropriate drag and pan/zoom plugins.

Implement a reusable circuit-canvas module rather than placing all behavior directly into the existing Astro page.

The canvas must support:

- Searchable and filterable symbol palette
- Drag/drop or click-to-place
- Grid snapping
- Terminal snapping
- Orthogonal wire creation
- Junction creation
- Component selection
- Multi-selection
- Move
- Rotate
- Duplicate
- Delete
- Property editing
- Value and label editing
- Undo and redo
- Zoom and pan
- Fit to view
- Reset view
- Keyboard controls
- Clear focus and selection indicators
- Accessible names for components and terminals

Stable layout dimensions must prevent toolbar and canvas shifts during selection or feedback.

### Authoring Integration

Add a circuit-question editor to the quiz/test creator.

Author controls:

- Interaction-mode segmented control
- Diagram canvas
- Symbol palette
- Allowed learner palette
- Editable property configuration
- Expected target selection
- Expected meter placement configuration
- Expected values and tolerances
- Expected/reference topology
- YAML/JSON preview
- Validation preview

Visual authoring and direct YAML/JSON authoring must round-trip without losing IDs, terminal references, topology, or metadata.

Circuit questions may also be used as Worked Example steps because Worked Examples reuse question definitions.

Do not add frontend authoring support for entire Worked Example, Recall Drill, or Guided Project assessment types as part of this feature.

### Learner Interaction

#### Select

- Learner clicks permitted components, nodes, branches, or labels.
- Clearly indicate selected and hover states.
- Support single or multiple selection according to schema.

#### Meter Placement

- Learner chooses an ammeter or voltmeter.
- Voltmeter is placed across two nodes.
- Ammeter is placed into a branch.
- Support polarity/probe direction when required.

#### Value Entry

- Learner selects a target and enters a value or label.
- Support exact text, numeric tolerance, or symbolic equivalence per target.
- Reuse existing numeric and symbolic input infrastructure where possible.

#### Build

- Learner creates a circuit from an allowed symbol palette.
- Components and wires remain editable until submission.
- The UI should show connectivity and incomplete terminals without providing correctness in scored mode.

## Backend Scoring

Add:

- `ICircuitQuestionScorer`
- A Core implementation for deterministic grading
- Circuit canonicalization and topology comparison helpers

Keep scoring backend-authoritative.

### Select Scoring

- Compare stable target IDs.
- Support ordered or unordered comparison as configured.
- Reject targets outside the allowed target kind.

### Meter Placement Scoring

- Voltmeter: compare an unordered node pair unless polarity is required.
- Ammeter: compare the selected branch or the equivalent split branch representation.
- Validate meter type.
- Validate polarity/orientation only when the question opts in.

### Value Entry Scoring

Each expected value defines one mode:

- Exact text
- Numeric with tolerance
- Symbolic expression equivalence

Reuse existing numeric rules and symbolic math adapter rather than duplicating those systems.

### Build Scoring

Convert expected and submitted diagrams into canonical typed netlists.

Canonicalization must ignore:

- Component instance IDs
- Positions
- Rotation
- Wire route points
- Visual ordering

Canonicalization must preserve:

- Symbol/component type
- Terminal identity and role
- Node connectivity
- Required component values
- Required labels/properties when configured

Compare circuits using typed graph isomorphism.

Interchangeable components of the same required type must be considered equivalent.

Do not treat circuits as electrically equivalent unless their authored topology matches under these rules.

No simulation or equation solving belongs in V1.

## Validation And Security

### Validation

Validate:

- Supported interaction mode
- Valid circuit schema and catalog versions
- Unique component IDs
- Unique node IDs
- Unique wire IDs
- Valid catalog symbol IDs
- Valid terminal IDs
- Valid wire endpoints
- No illegal self-loop wires
- Valid selection targets
- Valid meter targets
- Build palette contains required symbol types
- Expected topology is satisfiable
- Positive numeric tolerances
- Supported symbolic value modes
- Canvas and payload limits

Initial limits:

- Maximum 100 components
- Maximum 250 wires
- Maximum 200 nodes
- Maximum 1 MB serialized circuit answer

### SVG Security

Interactive SVG expands the browser attack surface.

V1 must:

- Render only trusted catalog geometry.
- Construct SVG elements through DOM APIs/SVG.js.
- Reject scripts.
- Reject event-handler attributes.
- Reject external resource links.
- Reject `<foreignObject>`.
- Reject arbitrary style injection.
- Reject arbitrary SVG assessment markup.

Do not implement arbitrary SVG upload/import.

If custom-symbol imports are added later, sanitize them using a strict SVG profile and independently validate the resulting element/attribute allowlist.

## API And Persistence

Keep the current answer-submission endpoint unless payload size requires a documented limit increase.

Public type changes are additive:

- `QuestionType.Circuit`
- `CircuitQuestionDefinition`
- `CircuitDiagramDefinition`
- `CircuitComponentDefinition`
- `CircuitNodeDefinition`
- `CircuitWireDefinition`
- `CircuitAnswer`
- `CircuitFeedback`

Update:

- File DTOs
- YAML/JSON mapper
- Assessment validator
- API request contracts
- Attempt JSON serialization
- SQLite retention serialization
- Frontend TypeScript interfaces
- Result/review rendering
- Question-type analytics

Existing assessments and image media must remain compatible.

## Example Assessments

Add at least:

1. **Circuit Components And Nodes Worked Example**
   - Identify symbols
   - Identify nodes and branches
   - Trace a current path
   - Place a voltmeter and ammeter

2. **Circuit Identification And Measurement Quiz**
   - Component selection
   - Node/branch selection
   - Meter placement
   - Value entry

3. **Series And Parallel Circuit Builder**
   - Build one series loop
   - Build two parallel branches
   - Build a simple mixed series/parallel topology

Use the existing `electronics-and-circuits` category and appropriate subcategories.

## Implementation Order

1. Define catalog/schema/domain types and validation.
2. Build a small representative symbol subset and catalog renderer.
3. Implement circuit answer persistence and selection scoring.
4. Implement reusable SVG.js canvas and interaction states.
5. Implement meter placement and value-entry scoring/UI.
6. Implement build-mode wiring and topology canonicalization.
7. Expand the symbol catalog to the complete V1 list.
8. Add visual creator integration.
9. Add review/feedback rendering and analytics.
10. Add sample assessments.
11. Run full regression and browser verification.

Do not create the entire symbol catalog before proving component terminals, wiring, persistence, and topology grading with the representative subset.

Representative subset:

- Wire
- Junction
- Ground
- Cell
- ANSI resistor
- SPST switch
- Ammeter
- Voltmeter
- Capacitor
- Diode
- NPN BJT
- Op-amp
- AND gate

## Test Plan

### Backend

- Valid circuit questions load from YAML and JSON.
- Invalid symbol, terminal, wire, node, target, and palette references fail validation.
- All four interaction modes round-trip through file mapping.
- Circuit answers round-trip through attempt JSON and SQLite.
- Selection scoring handles ordered and unordered targets.
- Voltmeter node-pair scoring is order independent.
- Ammeter branch placement scores correctly.
- Numeric value tolerance works.
- Symbolic value comparison uses the existing symbolic engine.
- Build scoring accepts moved, rotated, reordered, and renamed equivalent circuits.
- Build scoring accepts interchangeable same-type components.
- Build scoring rejects missing/extra components and wrong nets.
- Practice/scored feedback visibility remains correct.
- Analytics records circuit question performance.

### Frontend

- Every catalog symbol renders without clipping.
- Terminals remain aligned after rotation.
- Grid and terminal snapping are stable.
- Wires create correct node references.
- Junction behavior is deterministic.
- Undo/redo restores structured state.
- Keyboard actions work.
- Mobile and desktop layouts do not overlap.
- Authoring preview round-trips to the same structured model.
- Existing image-based questions still render normally.

### Browser Smoke Flow

Verify:

1. Create a circuit question visually.
2. Save and reload it.
3. Start a practice attempt.
4. Complete selection, meter, value, and build questions.
5. Confirm immediate practice feedback.
6. Save and quit.
7. Resume with the circuit state restored.
8. Complete and review.
9. Repeat in scored mode and confirm hidden feedback.

### Regression

```powershell
dotnet test backend\QuizApp.sln --no-restore
```

```powershell
Set-Location frontend
npm run build
```

Use browser screenshots and interaction checks for the circuit canvas at desktop and mobile widths.

## Acceptance Criteria

The feature is complete when:

- The full V1 symbol catalog is available through stable IDs.
- Authors can create circuit questions visually or in YAML/JSON.
- Learners can select, place meters, enter values, and build circuits.
- Answers persist through save/resume and SQLite retention.
- Backend grading is independent of visual layout.
- Practice and scored feedback follow existing application rules.
- No arbitrary SVG markup is executed.
- Existing assessments remain compatible.
- All automated regression checks pass.

## Future Extensions

Explicitly deferred:

- DC circuit solver
- SPICE/ngspice integration
- AC/transient simulation
- Semiconductor operating-point simulation
- Animated current flow
- Oscilloscope and waveform interaction
- Fault insertion/troubleshooting simulation
- KiCad import/export
- Arbitrary SVG symbol import
- Electrical-equivalence transformations
- PCB layout or breadboard simulation

Simulation should later be added behind an adapter so circuit questions remain testable without the external service.

## Technical References

- SVG.js: <https://svgjs.dev/docs/3.2/>
- W3C SVG structure and reusable symbols: <https://www.w3.org/TR/SVG2/struct.html#SymbolElement>
- DOMPurify SVG sanitization guidance: <https://github.com/cure53/DOMPurify>
