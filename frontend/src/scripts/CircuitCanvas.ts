import { SVG, Container as SvgContainer, G as SvgGroup } from "@svgdotjs/svg.js";

export interface CircuitComponent {
  id: string;
  symbolId: string;
  x: number;
  y: number;
  rotation: number;
  value?: string;
  label?: string;
}

export interface CircuitNode {
  id: string;
  label?: string;
  x?: number | null;
  y?: number | null;
}

export interface CircuitPoint {
  x: number;
  y: number;
}

export interface CircuitWire {
  id: string;
  sourceId: string;
  targetId: string;
  routePoints?: CircuitPoint[] | null;
}

export interface CircuitDiagram {
  width: number;
  height: number;
  components: CircuitComponent[];
  nodes: CircuitNode[];
  wires: CircuitWire[];
  annotations?: unknown[];
}

export interface CircuitCanvasState {
  selectedIds?: string[];
  meterType?: string | null;
  meterPositiveTerminalId?: string | null;
  meterNegativeTerminalId?: string | null;
  meterTargetBranchId?: string | null;
  values?: Record<string, string> | null;
}

type CircuitMode = "select" | "meterPlacement" | "valueEntry" | "build" | "preview" | string;
type ProbeKind = "pos" | "neg";

interface SymbolDefinition {
  label: string;
  width: number;
  height: number;
  terminals: Record<string, CircuitPoint>;
  render: (group: SvgGroup, color: string, fill: string, strokeWidth: number) => void;
}

interface ComponentRef {
  group: SvgGroup;
  outline: any;
}

interface WireRef {
  visible: any;
  hit: any;
}

interface NodeRef {
  visible: any;
  hit: any;
}

interface ComponentDrag {
  pointerId: number;
  component: CircuitComponent;
  startPointer: CircuitPoint;
  startPosition: CircuitPoint;
  pendingPointer: CircuitPoint;
  moved: boolean;
}

interface ProbeDrag {
  pointerId: number;
  kind: ProbeKind;
  pendingPointer: CircuitPoint;
  candidateTarget: string | null;
}

const GRID_SIZE = 20;
const DRAG_THRESHOLD = 4;

export function snapToGrid(value: number, gridSize = GRID_SIZE): number {
  return Math.round(value / gridSize) * gridSize;
}

export function rotatePoint(point: CircuitPoint, degrees: number): CircuitPoint {
  const radians = (degrees * Math.PI) / 180;
  return {
    x: point.x * Math.cos(radians) - point.y * Math.sin(radians),
    y: point.x * Math.sin(radians) + point.y * Math.cos(radians)
  };
}

export function normalizeCircuitDiagram(source: CircuitDiagram): CircuitDiagram {
  const diagram = JSON.parse(JSON.stringify(source ?? {})) as CircuitDiagram;
  diagram.width = Math.max(240, Number(diagram.width) || 600);
  diagram.height = Math.max(200, Number(diagram.height) || 400);
  diagram.components = diagram.components ?? [];
  diagram.nodes = (diagram.nodes ?? []).map((node, index) => ({
    ...node,
    x: node.x !== null && node.x !== undefined && Number.isFinite(Number(node.x))
      ? Number(node.x)
      : 80 + (index % 6) * 80,
    y: node.y !== null && node.y !== undefined && Number.isFinite(Number(node.y))
      ? Number(node.y)
      : 80 + Math.floor(index / 6) * 80
  }));
  diagram.wires = diagram.wires ?? [];
  diagram.annotations = diagram.annotations ?? [];
  return diagram;
}

export class CircuitCanvas {
  private readonly container: HTMLElement;
  private readonly wrapper: HTMLDivElement;
  private readonly draw: SvgContainer;
  private readonly svgNode: SVGSVGElement;
  private readonly mode: CircuitMode;
  private readonly onChange: () => void;
  private readonly statusElement: HTMLDivElement;
  private readonly gridLayer: SvgGroup;
  private readonly wireLayer: SvgGroup;
  private readonly nodeLayer: SvgGroup;
  private readonly componentLayer: SvgGroup;
  private readonly interactionLayer: SvgGroup;
  private readonly probeLayer: SvgGroup;
  private readonly overlayLayer: SvgGroup;

  private diagram: CircuitDiagram;
  private selectedIds = new Set<string>();
  private enteredValues = new Map<string, string>();
  private componentRefs = new Map<string, ComponentRef>();
  private wireRefs = new Map<string, WireRef>();
  private nodeRefs = new Map<string, NodeRef>();
  private terminalTargets = new Map<string, any>();
  private activeWireStart: string | null = null;
  private wirePreview: any = null;
  private meterType: string | null = null;
  private meterPosTarget: string | null = null;
  private meterNegTarget: string | null = null;
  private meterBranchTarget: string | null = null;
  private floatingProbePositions: Record<ProbeKind, CircuitPoint>;
  private nextProbeKind: ProbeKind = "pos";
  private componentDrag: ComponentDrag | null = null;
  private probeDrag: ProbeDrag | null = null;
  private animationFrame: number | null = null;
  private destroyed = false;
  private suppressClickUntil = 0;
  private valueEditor: HTMLDivElement | null = null;

  private readonly onPointerMoveBound = (event: PointerEvent) => this.handlePointerMove(event);
  private readonly onPointerUpBound = (event: PointerEvent) => this.handlePointerUp(event);
  private readonly onPointerCancelBound = (event: PointerEvent) => this.handlePointerCancel(event);
  private readonly onKeyDownBound = (event: KeyboardEvent) => this.handleKeyDown(event);
  private readonly onCanvasPointerDownBound = (event: PointerEvent) => this.handleCanvasPointerDown(event);

  constructor(container: HTMLElement, diagram: CircuitDiagram, mode: string, onChange: () => void) {
    this.container = container;
    this.diagram = normalizeCircuitDiagram(diagram);
    this.mode = mode;
    this.onChange = onChange;
    this.floatingProbePositions = {
      pos: { x: this.diagram.width - 70, y: 70 },
      neg: { x: this.diagram.width - 35, y: 70 }
    };

    this.container.innerHTML = "";
    this.wrapper = document.createElement("div");
    this.wrapper.className = `circuit-canvas-frame ${this.isReadOnly() ? "is-readonly" : "is-interactive"}`;
    this.wrapper.style.setProperty("--circuit-aspect", `${this.diagram.width} / ${this.diagram.height}`);
    this.container.appendChild(this.wrapper);

    this.draw = SVG().addTo(this.wrapper).size("100%", "100%");
    this.draw.viewbox(0, 0, this.diagram.width, this.diagram.height);
    this.svgNode = this.draw.node as SVGSVGElement;
    this.svgNode.classList.add("circuit-svg-viewport");
    this.svgNode.setAttribute("tabindex", this.isReadOnly() ? "-1" : "0");
    this.svgNode.setAttribute("role", "application");
    this.svgNode.setAttribute("aria-label", "Interactive circuit diagram");

    this.gridLayer = this.draw.group().addClass("circuit-layer-grid");
    this.wireLayer = this.draw.group().addClass("circuit-layer-wires");
    this.nodeLayer = this.draw.group().addClass("circuit-layer-nodes");
    this.componentLayer = this.draw.group().addClass("circuit-layer-components");
    this.interactionLayer = this.draw.group().addClass("circuit-layer-interactions");
    this.probeLayer = this.draw.group().addClass("circuit-layer-probes");
    this.overlayLayer = this.draw.group().addClass("circuit-layer-overlays");

    this.statusElement = document.createElement("div");
    this.statusElement.className = "circuit-status";
    this.statusElement.setAttribute("aria-live", "polite");
    this.wrapper.appendChild(this.statusElement);

    for (const component of this.diagram.components) {
      if (component.value) this.enteredValues.set(component.id, component.value);
    }

    this.drawGrid();
    this.rebuildScene();
    this.bindRootEvents();
    this.updateStatus();
  }

  public destroy(): void {
    if (this.destroyed) return;
    this.destroyed = true;
    if (this.animationFrame !== null) cancelAnimationFrame(this.animationFrame);
    this.animationFrame = null;
    this.closeValueEditor();
    this.releasePointerCapture(this.componentDrag?.pointerId);
    this.releasePointerCapture(this.probeDrag?.pointerId);
    this.svgNode.removeEventListener("pointermove", this.onPointerMoveBound);
    this.svgNode.removeEventListener("pointerup", this.onPointerUpBound);
    this.svgNode.removeEventListener("pointercancel", this.onPointerCancelBound);
    this.svgNode.removeEventListener("keydown", this.onKeyDownBound);
    this.svgNode.removeEventListener("pointerdown", this.onCanvasPointerDownBound);
    this.componentDrag = null;
    this.probeDrag = null;
  }

  public getSelectedIds(): string[] {
    return Array.from(this.selectedIds);
  }

  public getMeterType(): string | null {
    return this.meterType;
  }

  public getMeterPositiveTerminalId(): string | null {
    return this.meterPosTarget;
  }

  public getMeterNegativeTerminalId(): string | null {
    return this.meterNegTarget;
  }

  public getMeterTargetBranchId(): string | null {
    return this.meterBranchTarget;
  }

  public getValues(): Record<string, string> {
    return Object.fromEntries(this.enteredValues.entries());
  }

  public getDiagram(): CircuitDiagram {
    return JSON.parse(JSON.stringify(this.diagram));
  }

  public restoreState(state: CircuitCanvasState): void {
    this.selectedIds = new Set(state.selectedIds ?? []);
    this.meterType = state.meterType ?? null;
    this.meterPosTarget = state.meterPositiveTerminalId ?? null;
    this.meterNegTarget = state.meterNegativeTerminalId ?? null;
    this.meterBranchTarget = state.meterTargetBranchId ?? null;
    this.enteredValues.clear();
    for (const component of this.diagram.components) {
      if (component.value) this.enteredValues.set(component.id, component.value);
    }
    for (const [id, value] of Object.entries(state.values ?? {})) {
      this.enteredValues.set(id, value);
      const component = this.diagram.components.find((candidate) => candidate.id === id);
      if (component) component.value = value;
    }
    this.rebuildScene();
  }

  public setSelection(ids: string[]): void {
    this.selectedIds = new Set(ids);
    this.updateSelectionStyles();
    this.updateStatus();
  }

  public setMeterPlacement(
    type: string | null,
    positiveTerminalId: string | null = null,
    negativeTerminalId: string | null = null,
    targetBranchId: string | null = null
  ): void {
    this.meterType = type;
    this.meterPosTarget = positiveTerminalId;
    this.meterNegTarget = negativeTerminalId;
    this.meterBranchTarget = targetBranchId;
    this.nextProbeKind = positiveTerminalId && !negativeTerminalId ? "neg" : "pos";
    this.renderMeterTargets();
    this.renderMeterProbes();
    this.updateWireStyles();
    this.updateStatus();
  }

  public setMeterType(type: string | null): void {
    this.setMeterPlacement(type);
    this.onChange();
  }

  public setValues(values: Record<string, string>): void {
    for (const [id, value] of Object.entries(values)) {
      this.enteredValues.set(id, value);
      const component = this.diagram.components.find((candidate) => candidate.id === id);
      if (component) component.value = value;
    }
    this.rebuildComponents();
  }

  public refresh(): void {
    this.diagram = normalizeCircuitDiagram(this.diagram);
    this.rebuildScene();
  }

  public addComponent(symbolId: string, x = this.diagram.width / 2, y = this.diagram.height / 2): void {
    const prefix = this.symbolPrefix(symbolId);
    const component: CircuitComponent = {
      id: this.nextId(prefix, [
        ...this.diagram.components.map((item) => item.id),
        ...this.diagram.nodes.map((item) => item.id),
        ...this.diagram.wires.map((item) => item.id)
      ]),
      symbolId,
      x: snapToGrid(x),
      y: snapToGrid(y),
      rotation: 0,
      value: ""
    };
    this.diagram.components.push(component);
    this.rebuildComponents();
    this.updateAllWires();
    this.setSelection([component.id]);
    this.onChange();
  }

  public addNode(x = this.diagram.width / 2, y = this.diagram.height / 2): void {
    const id = this.nextId("n", [
      ...this.diagram.components.map((item) => item.id),
      ...this.diagram.nodes.map((item) => item.id),
      ...this.diagram.wires.map((item) => item.id)
    ]);
    this.diagram.nodes.push({ id, label: id, x: snapToGrid(x), y: snapToGrid(y) });
    this.rebuildNodes();
    this.setSelection([id]);
    this.onChange();
  }

  public deleteSelected(): void {
    if (this.selectedIds.size === 0) return;
    const removed = new Set(this.selectedIds);
    this.diagram.components = this.diagram.components.filter((component) => !removed.has(component.id));
    this.diagram.nodes = this.diagram.nodes.filter((node) => !removed.has(node.id));
    this.diagram.wires = this.diagram.wires.filter((wire) =>
      !removed.has(wire.id)
      && !Array.from(removed).some((id) => wire.sourceId.startsWith(`${id}.`) || wire.targetId.startsWith(`${id}.`))
      && !removed.has(wire.sourceId)
      && !removed.has(wire.targetId)
    );
    this.selectedIds.clear();
    this.activeWireStart = null;
    this.rebuildScene();
    this.onChange();
  }

  public rotateSelected(): void {
    let changed = false;
    for (const component of this.diagram.components) {
      if (!this.selectedIds.has(component.id)) continue;
      component.rotation = (component.rotation + 90) % 360;
      this.updateComponentTransform(component);
      this.updateConnectedWires(component.id);
      changed = true;
    }
    if (changed) {
      this.renderMeterTargets();
      this.renderMeterProbes();
      this.onChange();
    }
  }

  public undo(): void {
    // History is intentionally deferred. This method remains for API compatibility.
  }

  private bindRootEvents(): void {
    if (this.isReadOnly()) return;
    this.svgNode.addEventListener("pointermove", this.onPointerMoveBound);
    this.svgNode.addEventListener("pointerup", this.onPointerUpBound);
    this.svgNode.addEventListener("pointercancel", this.onPointerCancelBound);
    this.svgNode.addEventListener("keydown", this.onKeyDownBound);
    this.svgNode.addEventListener("pointerdown", this.onCanvasPointerDownBound);
  }

  private drawGrid(): void {
    this.gridLayer.clear();
    const pattern = this.draw.pattern(GRID_SIZE, GRID_SIZE, (add) => {
      add.circle(2).center(GRID_SIZE / 2, GRID_SIZE / 2).fill("#c7cdd0");
    });
    this.gridLayer.rect(this.diagram.width, this.diagram.height)
      .fill(pattern)
      .addClass("circuit-grid-background");
  }

  private rebuildScene(): void {
    this.rebuildWires();
    this.rebuildNodes();
    this.rebuildComponents();
    this.renderMeterTargets();
    this.renderMeterProbes();
    this.renderWirePreview();
    this.updateSelectionStyles();
    this.updateStatus();
  }

  private rebuildWires(): void {
    this.wireLayer.clear();
    this.wireRefs.clear();
    for (const wire of this.diagram.wires) {
      const points = this.getWirePoints(wire);
      const visible = this.wireLayer.polyline(points).fill("none");
      const hit = this.wireLayer.polyline(points).fill("none")
        .stroke({ color: "#000", width: 16, opacity: 0.001 })
        .addClass("circuit-hit-target circuit-wire-hit");
      this.wireRefs.set(wire.id, { visible, hit });
      this.bindWireEvents(wire, hit);
    }
    this.updateWireStyles();
  }

  private rebuildNodes(): void {
    this.nodeLayer.clear();
    this.nodeRefs.clear();
    for (const node of this.diagram.nodes) {
      const point = this.getNodeCoordinates(node.id);
      const visible = this.nodeLayer.circle(9).center(point.x, point.y);
      const hit = this.nodeLayer.circle(30).center(point.x, point.y)
        .fill({ color: "#000", opacity: 0.001 })
        .addClass("circuit-hit-target circuit-node-hit");
      this.nodeRefs.set(node.id, { visible, hit });
      this.bindNodeEvents(node, hit);
    }
    this.updateNodeStyles();
  }

  private rebuildComponents(): void {
    this.componentLayer.clear();
    this.componentRefs.clear();
    for (const component of this.diagram.components) this.createComponent(component);
    this.updateSelectionStyles();
  }

  private createComponent(component: CircuitComponent): void {
    const definition = this.getSymbolDefinition(component.symbolId);
    const group = this.componentLayer.group().addClass("circuit-component");
    this.setComponentTransform(group, component);

    const hit = group.rect(Math.max(44, definition.width + 18), Math.max(44, definition.height + 18))
      .center(0, 0)
      .fill({ color: "#000", opacity: 0.001 })
      .addClass("circuit-hit-target circuit-component-hit");

    const body = group.group().addClass("circuit-component-body");
    definition.render(body, "#313b40", "#fff", 2);
    body.attr("pointer-events", "none");

    const outline = group.rect(Math.max(48, definition.width + 12), Math.max(48, definition.height + 12))
      .center(0, 0)
      .radius(6)
      .fill("none")
      .stroke({ color: "#087f8c", width: 2, dasharray: "5 3" })
      .hide()
      .addClass("circuit-selection-outline");
    outline.attr("pointer-events", "none");

    const value = this.enteredValues.get(component.id) ?? component.value ?? "";
    if (component.label || value) {
      const labels = group.group().addClass("circuit-component-labels");
      labels.attr("transform", `rotate(${-component.rotation})`);
      labels.attr("pointer-events", "none");
      if (component.label) {
        labels.text(component.label).font({ size: 12, weight: "bold" }).center(0, -32).fill("#313b40");
      }
      if (value) labels.text(value).font({ size: 11 }).center(0, 28).fill("#59666c");
    }

    if (this.mode === "build") {
      for (const [terminalId, offset] of Object.entries(definition.terminals)) {
        const endpointId = `${component.id}.${terminalId}`;
        const isWireStart = this.activeWireStart === endpointId;
        const isInvalidTarget = Boolean(
          this.activeWireStart
          && (isWireStart || this.hasWireBetween(this.activeWireStart, endpointId))
        );
        const terminal = group.circle(isWireStart ? 12 : 9)
          .center(offset.x, offset.y)
          .fill(isWireStart ? "#e85d04" : isInvalidTarget ? "#b42318" : "#168b58")
          .stroke({ width: 2, color: "#fff" })
          .addClass("circuit-terminal circuit-hit-target");
        terminal.attr("data-wire-target", isInvalidTarget ? "invalid" : "valid");
        this.bindTerminalEvents(endpointId, terminal);
      }
    }

    if (!this.isReadOnly()) {
      hit.attr("tabindex", "0");
      hit.attr("aria-label", `${definition.label} ${component.label ?? component.id}`);
      hit.on("pointerdown", (event: PointerEvent) => this.handleComponentPointerDown(event, component));
      hit.on("click", (event: MouseEvent) => this.handleComponentClick(event, component));
      hit.on("dblclick", (event: MouseEvent) => {
        if (this.mode !== "valueEntry" && this.mode !== "build") return;
        event.stopPropagation();
        this.openValueEditor(component, event.clientX, event.clientY);
      });
      hit.on("pointerenter", () => {
        if (!this.selectedIds.has(component.id)) outline.show().opacity(0.45);
      });
      hit.on("pointerleave", () => {
        if (!this.selectedIds.has(component.id)) outline.hide().opacity(1);
      });
    }

    this.componentRefs.set(component.id, { group, outline });
  }

  private bindWireEvents(wire: CircuitWire, hit: any): void {
    if (this.isReadOnly()) return;
    hit.attr("tabindex", "0");
    hit.attr("aria-label", `Wire ${wire.id}`);
    hit.on("pointerdown", (event: PointerEvent) => {
      event.stopPropagation();
      if (this.mode === "meterPlacement" && this.meterType === "ammeter") {
        this.meterBranchTarget = wire.id;
        this.updateWireStyles();
        this.renderMeterProbes();
        this.updateStatus();
        this.onChange();
        return;
      }
      if (this.mode === "select" || this.mode === "build") {
        this.selectId(wire.id, event.shiftKey || event.ctrlKey || event.metaKey);
      }
    });
  }

  private bindNodeEvents(node: CircuitNode, hit: any): void {
    if (this.isReadOnly()) return;
    hit.attr("tabindex", "0");
    hit.attr("aria-label", `Node ${node.label ?? node.id}`);
    hit.on("pointerdown", (event: PointerEvent) => {
      event.stopPropagation();
      if (this.mode === "meterPlacement" && this.meterType === "voltmeter") {
        this.placeNextProbe(node.id);
        return;
      }
      if (this.mode === "build" && this.activeWireStart) {
        this.completeWire(node.id);
        return;
      }
      if (this.mode === "select" || this.mode === "build") {
        this.selectId(node.id, event.shiftKey || event.ctrlKey || event.metaKey);
      }
    });
  }

  private bindTerminalEvents(terminalId: string, terminal: any): void {
    terminal.attr("tabindex", "0");
    terminal.attr("aria-label", `Terminal ${terminalId}`);
    terminal.on("pointerdown", (event: PointerEvent) => {
      event.stopPropagation();
      if (this.mode === "meterPlacement" && this.meterType === "voltmeter") {
        this.placeNextProbe(terminalId);
        return;
      }
      if (this.mode !== "build") return;
      if (this.activeWireStart) this.completeWire(terminalId);
      else {
        this.activeWireStart = terminalId;
        this.renderWirePreview();
        this.rebuildComponents();
        this.updateStatus();
      }
    });
  }

  private handleComponentPointerDown(event: PointerEvent, component: CircuitComponent): void {
    if (this.mode !== "build" || event.button !== 0) return;
    event.stopPropagation();
    this.closeValueEditor();
    this.selectId(component.id, event.shiftKey || event.ctrlKey || event.metaKey);
    const pointer = this.clientToSvg(event.clientX, event.clientY);
    this.componentDrag = {
      pointerId: event.pointerId,
      component,
      startPointer: pointer,
      startPosition: { x: component.x, y: component.y },
      pendingPointer: pointer,
      moved: false
    };
    this.capturePointer(event.pointerId);
    this.svgNode.classList.add("is-dragging");
  }

  private handleComponentClick(event: MouseEvent, component: CircuitComponent): void {
    event.stopPropagation();
    if (performance.now() < this.suppressClickUntil) return;
    if (this.mode === "select") {
      this.selectId(component.id, event.shiftKey || event.ctrlKey || event.metaKey);
    } else if (this.mode === "valueEntry") {
      this.openValueEditor(component, event.clientX, event.clientY);
    }
  }

  private handleCanvasPointerDown(event: PointerEvent): void {
    if (event.target !== this.svgNode && !(event.target as Element).classList?.contains("circuit-grid-background")) return;
    this.closeValueEditor();
    if (this.activeWireStart) {
      this.activeWireStart = null;
      this.renderWirePreview();
      this.rebuildComponents();
      this.updateStatus();
      return;
    }
    if (this.mode === "select" || this.mode === "build") this.setSelection([]);
  }

  private handlePointerMove(event: PointerEvent): void {
    if (this.componentDrag?.pointerId === event.pointerId) {
      this.componentDrag.pendingPointer = this.clientToSvg(event.clientX, event.clientY);
      if (Math.hypot(
        this.componentDrag.pendingPointer.x - this.componentDrag.startPointer.x,
        this.componentDrag.pendingPointer.y - this.componentDrag.startPointer.y
      ) >= DRAG_THRESHOLD) this.componentDrag.moved = true;
      this.scheduleFrame();
      return;
    }

    if (this.probeDrag?.pointerId === event.pointerId) {
      this.probeDrag.pendingPointer = this.clientToSvg(event.clientX, event.clientY);
      this.scheduleFrame();
      return;
    }

    if (this.activeWireStart) {
      this.updateWirePreview(this.clientToSvg(event.clientX, event.clientY));
    }
  }

  private handlePointerUp(event: PointerEvent): void {
    if (this.componentDrag?.pointerId === event.pointerId) {
      this.flushFrame();
      const drag = this.componentDrag;
      drag.component.x = snapToGrid(drag.component.x);
      drag.component.y = snapToGrid(drag.component.y);
      this.updateComponentTransform(drag.component);
      this.updateConnectedWires(drag.component.id);
      this.componentDrag = null;
      this.releasePointerCapture(event.pointerId);
      this.svgNode.classList.remove("is-dragging");
      if (drag.moved) {
        this.suppressClickUntil = performance.now() + 250;
        this.renderMeterTargets();
        this.onChange();
      }
      return;
    }

    if (this.probeDrag?.pointerId === event.pointerId) {
      this.flushFrame();
      const drag = this.probeDrag;
      if (drag.candidateTarget) {
        if (drag.kind === "pos") this.meterPosTarget = drag.candidateTarget;
        else this.meterNegTarget = drag.candidateTarget;
        this.nextProbeKind = drag.kind === "pos" ? "neg" : "pos";
      }
      this.probeDrag = null;
      this.releasePointerCapture(event.pointerId);
      this.renderMeterTargets();
      this.renderMeterProbes();
      this.updateStatus();
      this.onChange();
    }
  }

  private handlePointerCancel(event: PointerEvent): void {
    if (this.componentDrag?.pointerId === event.pointerId) {
      const drag = this.componentDrag;
      drag.component.x = drag.startPosition.x;
      drag.component.y = drag.startPosition.y;
      this.updateComponentTransform(drag.component);
      this.updateConnectedWires(drag.component.id);
      this.componentDrag = null;
    }
    if (this.probeDrag?.pointerId === event.pointerId) this.probeDrag = null;
    this.releasePointerCapture(event.pointerId);
    this.svgNode.classList.remove("is-dragging");
    this.renderMeterTargets();
    this.renderMeterProbes();
  }

  private handleKeyDown(event: KeyboardEvent): void {
    if (this.isReadOnly()) return;
    if (event.key === "Escape") {
      this.activeWireStart = null;
      this.closeValueEditor();
      this.renderWirePreview();
      this.rebuildComponents();
      this.updateStatus();
      return;
    }
    if ((event.key === "Delete" || event.key === "Backspace") && this.selectedIds.size > 0) {
      event.preventDefault();
      this.deleteSelected();
      return;
    }
    if (event.key.toLowerCase() === "r" && this.mode === "build") {
      event.preventDefault();
      this.rotateSelected();
      return;
    }

    const movement: Record<string, CircuitPoint> = {
      ArrowLeft: { x: -1, y: 0 },
      ArrowRight: { x: 1, y: 0 },
      ArrowUp: { x: 0, y: -1 },
      ArrowDown: { x: 0, y: 1 }
    };
    const direction = movement[event.key];
    if (!direction || this.mode !== "build") return;
    const distance = event.shiftKey ? GRID_SIZE : 4;
    let changed = false;
    for (const component of this.diagram.components) {
      if (!this.selectedIds.has(component.id)) continue;
      component.x += direction.x * distance;
      component.y += direction.y * distance;
      this.updateComponentTransform(component);
      this.updateConnectedWires(component.id);
      changed = true;
    }
    for (const node of this.diagram.nodes) {
      if (!this.selectedIds.has(node.id)) continue;
      node.x = Number(node.x) + direction.x * distance;
      node.y = Number(node.y) + direction.y * distance;
      this.updateNodeGeometry(node);
      this.updateConnectedNodeWires(node.id);
      changed = true;
    }
    if (changed) {
      event.preventDefault();
      this.onChange();
    }
  }

  private scheduleFrame(): void {
    if (this.animationFrame !== null) return;
    this.animationFrame = requestAnimationFrame(() => {
      this.animationFrame = null;
      this.applyPendingInteraction();
    });
  }

  private flushFrame(): void {
    if (this.animationFrame !== null) cancelAnimationFrame(this.animationFrame);
    this.animationFrame = null;
    this.applyPendingInteraction();
  }

  private applyPendingInteraction(): void {
    if (this.componentDrag) {
      const drag = this.componentDrag;
      drag.component.x = drag.startPosition.x + drag.pendingPointer.x - drag.startPointer.x;
      drag.component.y = drag.startPosition.y + drag.pendingPointer.y - drag.startPointer.y;
      this.updateComponentTransform(drag.component);
      this.updateConnectedWires(drag.component.id);
    }
    if (this.probeDrag) {
      const drag = this.probeDrag;
      this.floatingProbePositions[drag.kind] = drag.pendingPointer;
      drag.candidateTarget = this.findNearestSnapPoint(drag.pendingPointer, 26);
      this.renderMeterTargets(drag.candidateTarget);
      this.renderMeterProbes(drag.kind, drag.pendingPointer);
    }
  }

  private completeWire(targetId: string): void {
    const sourceId = this.activeWireStart;
    this.activeWireStart = null;
    const source = sourceId ? this.getEndpointCoordinates(sourceId) : null;
    const target = this.getEndpointCoordinates(targetId);
    const zeroLength = source
      ? Math.hypot(source.x - target.x, source.y - target.y) < 0.5
      : false;
    if (!sourceId || sourceId === targetId || zeroLength || this.hasWireBetween(sourceId, targetId)) {
      this.renderWirePreview();
      this.rebuildComponents();
      this.updateStatus();
      return;
    }
    this.diagram.wires.push({
      id: this.nextId("w", this.diagram.wires.map((wire) => wire.id)),
      sourceId,
      targetId
    });
    this.rebuildWires();
    this.rebuildComponents();
    this.renderWirePreview();
    this.updateStatus();
    this.onChange();
  }

  private hasWireBetween(sourceId: string, targetId: string): boolean {
    return this.diagram.wires.some((wire) =>
      (wire.sourceId === sourceId && wire.targetId === targetId)
      || (wire.sourceId === targetId && wire.targetId === sourceId)
    );
  }

  private renderWirePreview(): void {
    this.wirePreview?.remove();
    this.wirePreview = null;
    if (!this.activeWireStart) return;
    const start = this.getEndpointCoordinates(this.activeWireStart);
    this.wirePreview = this.overlayLayer.line(start.x, start.y, start.x, start.y)
      .stroke({ color: "#e85d04", width: 2, dasharray: "6 4" })
      .addClass("circuit-wire-preview");
  }

  private updateWirePreview(point: CircuitPoint): void {
    if (!this.activeWireStart || !this.wirePreview) return;
    const start = this.getEndpointCoordinates(this.activeWireStart);
    this.wirePreview.plot(start.x, start.y, point.x, point.y);
  }

  private renderMeterTargets(candidateTarget: string | null = null): void {
    this.interactionLayer.clear();
    this.terminalTargets.clear();
    if (this.mode !== "meterPlacement" || this.meterType !== "voltmeter" || this.isReadOnly()) return;

    for (const node of this.diagram.nodes) this.createMeterTarget(node.id, this.getNodeCoordinates(node.id), candidateTarget);
    for (const component of this.diagram.components) {
      const definition = this.getSymbolDefinition(component.symbolId);
      for (const terminalId of Object.keys(definition.terminals)) {
        const id = `${component.id}.${terminalId}`;
        this.createMeterTarget(id, this.getEndpointCoordinates(id), candidateTarget);
      }
    }
  }

  private createMeterTarget(id: string, point: CircuitPoint, candidateTarget: string | null): void {
    const selected = id === this.meterPosTarget || id === this.meterNegTarget;
    const candidate = id === candidateTarget;
    const target = this.interactionLayer.circle(candidate ? 20 : 16)
      .center(point.x, point.y)
      .fill({ color: candidate ? "#f4a261" : selected ? "#087f8c" : "#fff", opacity: candidate || selected ? 0.75 : 0.18 })
      .stroke({ color: candidate ? "#e85d04" : "#087f8c", width: candidate ? 3 : 1.5 })
      .addClass("circuit-meter-target circuit-hit-target");
    target.on("pointerdown", (event: PointerEvent) => {
      event.stopPropagation();
      this.placeNextProbe(id);
    });
    this.terminalTargets.set(id, target);
  }

  private placeNextProbe(targetId: string): void {
    if (this.nextProbeKind === "pos") {
      this.meterPosTarget = targetId;
      this.nextProbeKind = "neg";
    } else {
      this.meterNegTarget = targetId;
      this.nextProbeKind = "pos";
    }
    this.renderMeterTargets();
    this.renderMeterProbes();
    this.updateStatus();
    this.onChange();
  }

  private renderMeterProbes(dragKind: ProbeKind | null = null, dragPoint: CircuitPoint | null = null): void {
    this.probeLayer.clear();
    if ((this.mode !== "meterPlacement" && this.mode !== "preview") || !this.meterType) return;

    const panelX = this.diagram.width - 130;
    const panelY = 18;
    const panel = this.probeLayer.group().attr("transform", `translate(${panelX} ${panelY})`);
    panel.rect(110, 46).radius(6).fill("#eef1f2").stroke({ color: "#aeb8bc", width: 1 });
    panel.text(this.meterType.toUpperCase()).font({ size: 11, weight: "bold" }).move(10, 5).fill("#313b40");
    panel.circle(8).center(28, 34).fill("#cc3344");
    panel.circle(8).center(82, 34).fill("#20272a");

    const positive = dragKind === "pos" && dragPoint
      ? dragPoint
      : this.meterPosTarget ? this.getEndpointCoordinates(this.meterPosTarget) : this.floatingProbePositions.pos;
    const negative = dragKind === "neg" && dragPoint
      ? dragPoint
      : this.meterNegTarget ? this.getEndpointCoordinates(this.meterNegTarget) : this.floatingProbePositions.neg;

    this.probeLayer.line(panelX + 28, panelY + 34, positive.x, positive.y)
      .stroke({ color: "#cc3344", width: 1.6, dasharray: "4 3" });
    this.probeLayer.line(panelX + 82, panelY + 34, negative.x, negative.y)
      .stroke({ color: "#20272a", width: 1.6, dasharray: "4 3" });

    this.createProbeHandle("pos", positive, "#cc3344", "+");
    this.createProbeHandle("neg", negative, "#20272a", "-");

    if (this.meterType === "ammeter" && this.meterBranchTarget) {
      const wire = this.diagram.wires.find((candidate) => candidate.id === this.meterBranchTarget);
      if (wire) {
        const points = this.getWirePoints(wire);
        const first = points[0];
        const last = points[points.length - 1];
        const middle = { x: (first[0] + last[0]) / 2, y: (first[1] + last[1]) / 2 };
        this.probeLayer.circle(20).center(middle.x, middle.y).fill("#fff3bf").stroke({ color: "#cc3344", width: 2 });
        this.probeLayer.text("A").font({ size: 11, weight: "bold" }).center(middle.x, middle.y).fill("#cc3344");
      }
    }
  }

  private createProbeHandle(kind: ProbeKind, point: CircuitPoint, color: string, text: string): void {
    const group = this.probeLayer.group().addClass("circuit-probe");
    group.circle(26).center(point.x, point.y).fill({ color, opacity: 0.001 }).addClass("circuit-hit-target");
    group.line(point.x - 12, point.y - 12, point.x, point.y).stroke({ color, width: 3 });
    group.circle(13).center(point.x, point.y).fill(color).stroke({ color: "#fff", width: 1 });
    group.text(text).font({ size: 10, weight: "bold" }).center(point.x, point.y - 1).fill("#fff");
    if (this.isReadOnly()) return;
    group.on("pointerdown", (event: PointerEvent) => {
      event.stopPropagation();
      this.probeDrag = {
        pointerId: event.pointerId,
        kind,
        pendingPointer: this.clientToSvg(event.clientX, event.clientY),
        candidateTarget: null
      };
      this.capturePointer(event.pointerId);
    });
  }

  private openValueEditor(component: CircuitComponent, clientX: number, clientY: number): void {
    if (this.isReadOnly()) return;
    this.closeValueEditor();
    const editor = document.createElement("div");
    editor.className = "circuit-value-editor";
    const label = document.createElement("label");
    label.textContent = `Value for ${component.label ?? component.id}`;
    const input = document.createElement("input");
    input.type = "text";
    input.value = this.enteredValues.get(component.id) ?? component.value ?? "";
    const actions = document.createElement("div");
    actions.className = "circuit-value-actions";
    const apply = document.createElement("button");
    apply.type = "button";
    apply.textContent = "Apply";
    const cancel = document.createElement("button");
    cancel.type = "button";
    cancel.textContent = "Cancel";
    actions.append(apply, cancel);
    editor.append(label, input, actions);
    this.wrapper.appendChild(editor);
    this.valueEditor = editor;

    const rect = this.wrapper.getBoundingClientRect();
    editor.style.left = `${Math.max(8, Math.min(clientX - rect.left, rect.width - 230))}px`;
    editor.style.top = `${Math.max(8, Math.min(clientY - rect.top, rect.height - 110))}px`;

    const commit = () => {
      const value = input.value.trim();
      this.enteredValues.set(component.id, value);
      component.value = value;
      this.closeValueEditor();
      this.rebuildComponents();
      this.onChange();
    };
    apply.addEventListener("click", commit);
    cancel.addEventListener("click", () => this.closeValueEditor());
    input.addEventListener("keydown", (event) => {
      if (event.key === "Enter") {
        event.preventDefault();
        commit();
      } else if (event.key === "Escape") {
        event.preventDefault();
        this.closeValueEditor();
      }
    });
    input.focus();
    input.select();
  }

  private closeValueEditor(): void {
    this.valueEditor?.remove();
    this.valueEditor = null;
  }

  private selectId(id: string, additive: boolean): void {
    if (!additive) this.selectedIds.clear();
    if (additive && this.selectedIds.has(id)) this.selectedIds.delete(id);
    else this.selectedIds.add(id);
    this.updateSelectionStyles();
    this.updateStatus();
    this.onChange();
  }

  private updateSelectionStyles(): void {
    for (const [id, ref] of this.componentRefs) {
      if (this.selectedIds.has(id)) ref.outline.show().opacity(1);
      else ref.outline.hide().opacity(1);
    }
    this.updateWireStyles();
    this.updateNodeStyles();
  }

  private updateWireStyles(): void {
    for (const [id, ref] of this.wireRefs) {
      const selected = this.selectedIds.has(id);
      const meterSelected = this.meterBranchTarget === id;
      ref.visible.stroke({
        color: meterSelected ? "#cc3344" : selected ? "#087f8c" : "#313b40",
        width: meterSelected || selected ? 4 : 2
      });
    }
  }

  private updateNodeStyles(): void {
    for (const [id, ref] of this.nodeRefs) {
      const selected = this.selectedIds.has(id);
      const isInvalidTarget = Boolean(
        this.activeWireStart
        && (this.activeWireStart === id || this.hasWireBetween(this.activeWireStart, id))
      );
      const isWireTarget = Boolean(this.activeWireStart);
      ref.visible
        .size(selected ? 13 : 9)
        .center(this.getNodeCoordinates(id).x, this.getNodeCoordinates(id).y)
        .fill(selected ? "#087f8c" : isInvalidTarget ? "#b42318" : isWireTarget ? "#168b58" : "#313b40")
        .stroke({ color: selected ? "#fff" : "#313b40", width: selected ? 2 : 0 });
    }
  }

  private updateNodeGeometry(node: CircuitNode): void {
    const ref = this.nodeRefs.get(node.id);
    if (!ref) return;
    const point = this.getNodeCoordinates(node.id);
    ref.visible.center(point.x, point.y);
    ref.hit.center(point.x, point.y);
  }

  private updateComponentTransform(component: CircuitComponent): void {
    const ref = this.componentRefs.get(component.id);
    if (ref) this.setComponentTransform(ref.group, component);
  }

  private setComponentTransform(group: SvgGroup, component: CircuitComponent): void {
    group.attr("transform", `translate(${component.x} ${component.y}) rotate(${component.rotation})`);
  }

  private updateConnectedWires(componentId: string): void {
    for (const wire of this.diagram.wires) {
      if (wire.sourceId.startsWith(`${componentId}.`) || wire.targetId.startsWith(`${componentId}.`)) {
        this.updateWireGeometry(wire);
      }
    }
    if (this.activeWireStart?.startsWith(`${componentId}.`)) {
      const start = this.getEndpointCoordinates(this.activeWireStart);
      this.wirePreview?.plot(start.x, start.y, start.x, start.y);
    }
  }

  private updateConnectedNodeWires(nodeId: string): void {
    for (const wire of this.diagram.wires) {
      if (wire.sourceId === nodeId || wire.targetId === nodeId) this.updateWireGeometry(wire);
    }
  }

  private updateAllWires(): void {
    for (const wire of this.diagram.wires) this.updateWireGeometry(wire);
  }

  private updateWireGeometry(wire: CircuitWire): void {
    const ref = this.wireRefs.get(wire.id);
    if (!ref) return;
    const points = this.getWirePoints(wire);
    ref.visible.plot(points);
    ref.hit.plot(points);
  }

  private getWirePoints(wire: CircuitWire): number[][] {
    const start = this.getEndpointCoordinates(wire.sourceId);
    const end = this.getEndpointCoordinates(wire.targetId);
    return [
      [start.x, start.y],
      ...(wire.routePoints ?? []).map((point) => [point.x, point.y]),
      [end.x, end.y]
    ];
  }

  private getEndpointCoordinates(endpointId: string): CircuitPoint {
    if (!endpointId.includes(".")) return this.getNodeCoordinates(endpointId);
    const separator = endpointId.indexOf(".");
    const componentId = endpointId.slice(0, separator);
    const terminalId = endpointId.slice(separator + 1);
    const component = this.diagram.components.find((candidate) => candidate.id === componentId);
    if (!component) return { x: 0, y: 0 };
    const terminal = this.getSymbolDefinition(component.symbolId).terminals[terminalId] ?? { x: 0, y: 0 };
    const rotated = rotatePoint(terminal, component.rotation);
    return { x: component.x + rotated.x, y: component.y + rotated.y };
  }

  private getNodeCoordinates(nodeId: string): CircuitPoint {
    const node = this.diagram.nodes.find((candidate) => candidate.id === nodeId);
    return node
      ? { x: Number(node.x) || 0, y: Number(node.y) || 0 }
      : { x: 0, y: 0 };
  }

  private findNearestSnapPoint(point: CircuitPoint, cssRadius: number): string | null {
    const svgRadius = cssRadius * this.diagram.width / Math.max(1, this.svgNode.getBoundingClientRect().width);
    let nearest: { id: string; distance: number } | null = null;
    for (const node of this.diagram.nodes) {
      const coordinates = this.getNodeCoordinates(node.id);
      const distance = Math.hypot(coordinates.x - point.x, coordinates.y - point.y);
      if (distance <= svgRadius && (!nearest || distance < nearest.distance)) nearest = { id: node.id, distance };
    }
    for (const component of this.diagram.components) {
      for (const terminalId of Object.keys(this.getSymbolDefinition(component.symbolId).terminals)) {
        const id = `${component.id}.${terminalId}`;
        const coordinates = this.getEndpointCoordinates(id);
        const distance = Math.hypot(coordinates.x - point.x, coordinates.y - point.y);
        if (distance <= svgRadius && (!nearest || distance < nearest.distance)) nearest = { id, distance };
      }
    }
    return nearest?.id ?? null;
  }

  private clientToSvg(clientX: number, clientY: number): CircuitPoint {
    const point = this.svgNode.createSVGPoint();
    point.x = clientX;
    point.y = clientY;
    const matrix = this.svgNode.getScreenCTM();
    if (matrix) {
      const transformed = point.matrixTransform(matrix.inverse());
      return { x: transformed.x, y: transformed.y };
    }
    const rect = this.svgNode.getBoundingClientRect();
    return {
      x: (clientX - rect.left) * this.diagram.width / Math.max(1, rect.width),
      y: (clientY - rect.top) * this.diagram.height / Math.max(1, rect.height)
    };
  }

  private capturePointer(pointerId: number): void {
    try {
      this.svgNode.setPointerCapture(pointerId);
    } catch {
      // Pointer capture can fail if the pointer already ended.
    }
  }

  private releasePointerCapture(pointerId: number | undefined): void {
    if (pointerId === undefined) return;
    try {
      if (this.svgNode.hasPointerCapture(pointerId)) this.svgNode.releasePointerCapture(pointerId);
    } catch {
      // Ignore browsers that release capture automatically.
    }
  }

  private updateStatus(): void {
    if (this.isReadOnly()) {
      this.statusElement.textContent = "Read-only circuit review";
      return;
    }
    if (this.activeWireStart) {
      this.statusElement.textContent = `Wiring from ${this.activeWireStart}. Select another terminal or press Escape.`;
      return;
    }
    if (this.mode === "meterPlacement") {
      this.statusElement.textContent = this.meterType
        ? `${this.meterType === "voltmeter" ? "Voltmeter" : "Ammeter"} active. ${this.meterType === "voltmeter" ? `Place the ${this.nextProbeKind === "pos" ? "positive" : "negative"} probe.` : "Select a branch."}`
        : "Choose a meter tool.";
      return;
    }
    if (this.selectedIds.size > 0) {
      this.statusElement.textContent = `${this.selectedIds.size} item${this.selectedIds.size === 1 ? "" : "s"} selected.`;
      return;
    }
    this.statusElement.textContent = this.mode === "build"
      ? "Select or drag a component. Click terminals to connect them."
      : this.mode === "valueEntry"
        ? "Select a component to enter its value."
        : "Select a circuit item.";
  }

  private isReadOnly(): boolean {
    return this.mode === "preview";
  }

  private symbolPrefix(symbolId: string): string {
    const normalized = symbolId.toLowerCase();
    if (normalized.includes("resistor")) return "R";
    if (normalized.includes("battery") || normalized.includes("cell") || normalized.includes("source")) return "V";
    if (normalized.includes("capacitor")) return "C";
    if (normalized.includes("inductor")) return "L";
    if (normalized.includes("diode")) return "D";
    if (normalized.includes("switch")) return "S";
    return normalized.replace(/[^a-z0-9]/g, "").slice(0, 2).toUpperCase() || "X";
  }

  private nextId(prefix: string, ids: string[]): string {
    const used = new Set(ids);
    const escapedPrefix = prefix.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
    const pattern = new RegExp(`^${escapedPrefix}(\\d+)$`);
    let index = ids.reduce((maximum, id) => {
      const match = pattern.exec(id);
      return match ? Math.max(maximum, Number(match[1])) : maximum;
    }, 0) + 1;
    while (used.has(`${prefix}${index}`)) index++;
    return `${prefix}${index}`;
  }

  private getSymbolDefinition(symbolId: string): SymbolDefinition {
    const key = symbolId.toLowerCase();
    if (key.includes("resistor")) return SYMBOLS.resistor;
    if (key.includes("cell") || key.includes("battery")) return SYMBOLS.battery;
    if (key.includes("switch")) return SYMBOLS.switch;
    if (key.includes("ammeter")) return SYMBOLS.ammeter;
    if (key.includes("voltmeter")) return SYMBOLS.voltmeter;
    if (key.includes("capacitor")) return SYMBOLS.capacitor;
    if (key.includes("diode")) return SYMBOLS.diode;
    if (key.includes("npn") || key.includes("bjt")) return SYMBOLS.npn;
    if (key.includes("opamp")) return SYMBOLS.opamp;
    if (key.includes("and") && key.includes("gate")) return SYMBOLS.andGate;
    if (key.includes("ground") || key.includes("junction")) return SYMBOLS.junction;
    return this.fallbackSymbol(symbolId);
  }

  private fallbackSymbol(symbolId: string): SymbolDefinition {
    return {
      label: symbolId,
      width: 50,
      height: 34,
      terminals: { p1: { x: -30, y: 0 }, p2: { x: 30, y: 0 } },
      render: (group, color, fill, strokeWidth) => {
        group.line(-30, 0, -25, 0).stroke({ color, width: strokeWidth });
        group.rect(50, 28).center(0, 0).fill(fill).stroke({ color, width: strokeWidth });
        group.text(symbolId.slice(0, 4)).font({ size: 8 }).center(0, 0).fill(color);
        group.line(25, 0, 30, 0).stroke({ color, width: strokeWidth });
      }
    };
  }
}

const twoTerminal = { p1: { x: -30, y: 0 }, p2: { x: 30, y: 0 } };

const SYMBOLS: Record<string, SymbolDefinition> = {
  resistor: {
    label: "Resistor",
    width: 70,
    height: 32,
    terminals: twoTerminal,
    render: (group, color, _fill, strokeWidth) => {
      group.line(-30, 0, -15, 0).stroke({ color, width: strokeWidth });
      group.path("M -15 0 L -12.5 -8 L -7.5 8 L -2.5 -8 L 2.5 8 L 7.5 -8 L 12.5 8 L 15 0")
        .fill("none").stroke({ color, width: strokeWidth });
      group.line(15, 0, 30, 0).stroke({ color, width: strokeWidth });
    }
  },
  battery: {
    label: "Battery",
    width: 70,
    height: 42,
    terminals: twoTerminal,
    render: (group, color, _fill, strokeWidth) => {
      group.line(-30, 0, -5, 0).stroke({ color, width: strokeWidth });
      group.line(-5, -15, -5, 15).stroke({ color, width: strokeWidth });
      group.line(5, -8, 5, 8).stroke({ color, width: strokeWidth + 2 });
      group.line(5, 0, 30, 0).stroke({ color, width: strokeWidth });
    }
  },
  switch: {
    label: "Switch",
    width: 70,
    height: 42,
    terminals: twoTerminal,
    render: (group, color, _fill, strokeWidth) => {
      group.line(-30, 0, -15, 0).stroke({ color, width: strokeWidth });
      group.circle(4).center(-15, 0).fill(color);
      group.line(-15, 0, 10, -12).stroke({ color, width: strokeWidth });
      group.circle(4).center(15, 0).fill(color);
      group.line(15, 0, 30, 0).stroke({ color, width: strokeWidth });
    }
  },
  ammeter: meterSymbol("A", "Ammeter"),
  voltmeter: meterSymbol("V", "Voltmeter"),
  capacitor: {
    label: "Capacitor",
    width: 70,
    height: 42,
    terminals: twoTerminal,
    render: (group, color, _fill, strokeWidth) => {
      group.line(-30, 0, -4, 0).stroke({ color, width: strokeWidth });
      group.line(-4, -15, -4, 15).stroke({ color, width: strokeWidth });
      group.line(4, -15, 4, 15).stroke({ color, width: strokeWidth });
      group.line(4, 0, 30, 0).stroke({ color, width: strokeWidth });
    }
  },
  diode: {
    label: "Diode",
    width: 70,
    height: 38,
    terminals: twoTerminal,
    render: (group, color, fill, strokeWidth) => {
      group.line(-30, 0, -12, 0).stroke({ color, width: strokeWidth });
      group.path("M -12 -12 L 8 0 L -12 12 Z").fill(fill).stroke({ color, width: strokeWidth });
      group.line(8, -12, 8, 12).stroke({ color, width: strokeWidth });
      group.line(8, 0, 30, 0).stroke({ color, width: strokeWidth });
    }
  },
  npn: {
    label: "NPN transistor",
    width: 72,
    height: 72,
    terminals: { b: { x: -30, y: 0 }, c: { x: 15, y: -30 }, e: { x: 15, y: 30 } },
    render: (group, color, _fill, strokeWidth) => {
      group.circle(36).center(0, 0).fill("none").stroke({ color, width: strokeWidth });
      group.line(-10, -12, -10, 12).stroke({ color, width: strokeWidth + 1 });
      group.line(-30, 0, -10, 0).stroke({ color, width: strokeWidth });
      group.line(-10, -6, 15, -18).stroke({ color, width: strokeWidth });
      group.line(15, -18, 15, -30).stroke({ color, width: strokeWidth });
      group.line(-10, 6, 15, 18).stroke({ color, width: strokeWidth });
      group.line(15, 18, 15, 30).stroke({ color, width: strokeWidth });
      group.path("M 5 14 L 15 18 L 11 8 Z").fill(color);
    }
  },
  opamp: {
    label: "Operational amplifier",
    width: 70,
    height: 62,
    terminals: { in_pos: { x: -30, y: 10 }, in_neg: { x: -30, y: -10 }, out: { x: 30, y: 0 } },
    render: (group, color, fill, strokeWidth) => {
      group.line(-30, -10, -20, -10).stroke({ color, width: strokeWidth });
      group.line(-30, 10, -20, 10).stroke({ color, width: strokeWidth });
      group.path("M -20 -25 L 25 0 L -20 25 Z").fill(fill).stroke({ color, width: strokeWidth });
      group.text("-").font({ size: 14 }).center(-15, -10).fill(color);
      group.text("+").font({ size: 14 }).center(-15, 10).fill(color);
      group.line(25, 0, 30, 0).stroke({ color, width: strokeWidth });
    }
  },
  andGate: {
    label: "AND gate",
    width: 70,
    height: 60,
    terminals: { in1: { x: -30, y: -10 }, in2: { x: -30, y: 10 }, out: { x: 30, y: 0 } },
    render: (group, color, fill, strokeWidth) => {
      group.line(-30, -10, -20, -10).stroke({ color, width: strokeWidth });
      group.line(-30, 10, -20, 10).stroke({ color, width: strokeWidth });
      group.path("M -20 -20 L -5 -20 A 20 20 0 0 1 15 0 A 20 20 0 0 1 -5 20 L -20 20 Z")
        .fill(fill).stroke({ color, width: strokeWidth });
      group.line(15, 0, 30, 0).stroke({ color, width: strokeWidth });
    }
  },
  junction: {
    label: "Junction",
    width: 28,
    height: 28,
    terminals: { p1: { x: 0, y: 0 } },
    render: (group, color) => {
      group.circle(10).center(0, 0).fill(color);
    }
  }
};

function meterSymbol(letter: string, label: string): SymbolDefinition {
  return {
    label,
    width: 70,
    height: 48,
    terminals: twoTerminal,
    render: (group, color, fill, strokeWidth) => {
      group.line(-30, 0, -16, 0).stroke({ color, width: strokeWidth });
      group.circle(32).center(0, 0).fill(fill).stroke({ color, width: strokeWidth });
      group.text(letter).font({ size: 14, weight: "bold" }).center(0, 0).fill(color);
      group.line(16, 0, 30, 0).stroke({ color, width: strokeWidth });
    }
  };
}
