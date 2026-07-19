content = """import JXG from 'jsxgraph';

export interface GraphPoint {
    x: number;
    y: number;
}

export interface SubmittedGraphAnswer {
    shape: string;
    points: GraphPoint[];
    expression?: string | null;
}

export type GraphShapeTool = 'point' | 'line' | 'parabola' | 'ellipse' | 'circle' | 'select' | null;

export class GraphingCanvas {
    private board: any;
    private containerElement: HTMLElement;
    private currentShape: string = '';
    private points: any[] = [];
    private drawnElements: any[] = [];
    private activeTool: GraphShapeTool = null;
    private isReadonly: boolean = false;
    private isDrawing: boolean = false;

    constructor(container: HTMLElement, readonly: boolean = false) {
        this.containerElement = container;
        this.isReadonly = readonly;
        
        // Initialize board
        this.board = JXG.JSXGraph.initBoard(this.containerElement.id, {
            boundingbox: [-10, 10, 10, -10],
            axis: true,
            grid: true,
            showCopyright: false,
            pan: { enabled: !readonly },
            zoom: { enabled: !readonly }
        });

        if (!this.isReadonly) {
            this.board.on('down', this.handleDown.bind(this));
            this.board.on('move', this.handleMove.bind(this));
            this.board.on('up', this.handleUp.bind(this));
        }
    }

    public setTool(tool: GraphShapeTool) {
        this.activeTool = tool;
        // If selecting, enable dragging on points
        const fixed = (tool !== 'select');
        this.points.forEach(p => {
            p.setAttribute({ fixed: fixed });
        });
    }

    private getMouseCoords(e: any): {x: number, y: number} | null {
        let i = 0;
        if (e && e[JXG.touchProperty]) {
            i = 0;
        }
        const coords = this.board.getUsrCoordsOfMouse(e, i);
        if (!coords || !coords.usrCoords) return null;
        return { x: coords.usrCoords[1], y: coords.usrCoords[2] };
    }

    private handleDown(e: any) {
        if (this.isReadonly || !this.activeTool || this.activeTool === 'select') return;
        
        // If they click on an existing element, JSXGraph might fire down.
        // We only want to draw if we are not exceeding max elements.
        // Actually, we replace the previous shape if they draw a new one,
        // because they are only supposed to submit one shape!
        this.clear(); 
        
        const coords = this.getMouseCoords(e);
        if (!coords) return;

        this.isDrawing = true;
        this.currentShape = this.activeTool;

        if (this.activeTool === 'point') {
            const p = this.board.create('point', [coords.x, coords.y], { size: 4, name: '', fixed: true });
            this.points.push(p);
            this.isDrawing = false; // Point is instantaneous
        } else if (this.activeTool === 'line') {
            const p1 = this.board.create('point', [coords.x, coords.y], { size: 4, name: '', fixed: true, visible: true });
            const p2 = this.board.create('point', [coords.x, coords.y], { size: 4, name: '', fixed: true, visible: true });
            this.points.push(p1, p2);
            const line = this.board.create('line', [p1, p2], { strokeColor: 'blue', hasInnerPoints: true });
            this.drawnElements.push(line);
        } else if (this.activeTool === 'circle') {
            const center = this.board.create('point', [coords.x, coords.y], { size: 4, name: '', fixed: true, visible: true });
            const edge = this.board.create('point', [coords.x, coords.y], { size: 4, name: '', fixed: true, visible: true });
            this.points.push(center, edge);
            const circle = this.board.create('circle', [center, edge], { strokeColor: 'orange', hasInnerPoints: true });
            this.drawnElements.push(circle);
        } else if (this.activeTool === 'parabola') {
            const vertex = this.board.create('point', [coords.x, coords.y], { size: 4, name: '', fixed: true, visible: true });
            const pt = this.board.create('point', [coords.x, coords.y], { size: 4, name: '', fixed: true, visible: true });
            this.points.push(vertex, pt);
            
            const h = () => vertex.X();
            const k = () => vertex.Y();
            const a = () => {
                const dx = pt.X() - h();
                if (Math.abs(dx) < 0.001) return 1;
                return (pt.Y() - k()) / (dx * dx);
            };
            const f = (x: number) => a() * Math.pow(x - h(), 2) + k();
            const parabola = this.board.create('functiongraph', [f], { strokeColor: 'green' });
            this.drawnElements.push(parabola);
        } else if (this.activeTool === 'ellipse') {
            // Draw via bounding box
            const p1 = this.board.create('point', [coords.x, coords.y], { size: 4, name: '', fixed: true, visible: true });
            const p2 = this.board.create('point', [coords.x, coords.y], { size: 4, name: '', fixed: true, visible: true });
            this.points.push(p1, p2);
            
            const center = this.board.create('point', [() => (p1.X()+p2.X())/2, () => (p1.Y()+p2.Y())/2], {visible: false});
            const axis1 = this.board.create('point', [() => center.X(), () => p1.Y()], {visible: false});
            const axis2 = this.board.create('point', [() => p1.X(), () => center.Y()], {visible: false});
            this.drawnElements.push(center, axis1, axis2);
            
            const ellipse = this.board.create('ellipse', [center, axis1, axis2], { strokeColor: 'purple', hasInnerPoints: true });
            this.drawnElements.push(ellipse);
        }
        
        this.board.update();
    }

    private handleMove(e: any) {
        if (!this.isDrawing || this.isReadonly || this.points.length < 2) return;
        
        const coords = this.getMouseCoords(e);
        if (!coords) return;

        // The second point is always the one being dragged
        const p2 = this.points[1];
        p2.setPosition(JXG.COORDS_BY_USER, [coords.x, coords.y]);
        this.board.update();
    }

    private handleUp(e: any) {
        if (!this.isDrawing) return;
        this.isDrawing = false;
        
        // Setup drag listeners for when user switches to 'select' tool
        this.points.forEach(p => {
            p.on('drag', () => {
                this.board.update();
            });
        });
    }

    public undo() {
        this.clear();
    }

    public getAnswer(): SubmittedGraphAnswer | null {
        if (this.points.length === 0) return null;
        
        return {
            shape: this.currentShape,
            points: this.points.map(p => ({ x: p.X(), y: p.Y() }))
        };
    }

    public restoreAnswer(answer: SubmittedGraphAnswer) {
        this.clear();
        this.currentShape = answer.shape;
        this.activeTool = (answer.shape as GraphShapeTool) || 'point';
        
        // We simulate the points creation based on the answer
        if (answer.points.length > 0) {
            answer.points.forEach(pt => {
                const p = this.board.create('point', [pt.x, pt.y], { size: 4, name: '', fixed: this.isReadonly });
                this.points.push(p);
                p.on('drag', () => this.board.update());
            });
            
            if (this.currentShape === 'line' && this.points.length >= 2) {
                const line = this.board.create('line', [this.points[0], this.points[1]], { strokeColor: 'blue', hasInnerPoints: true });
                this.drawnElements.push(line);
            } else if (this.currentShape === 'circle' && this.points.length >= 2) {
                const circle = this.board.create('circle', [this.points[0], this.points[1]], { strokeColor: 'orange', hasInnerPoints: true });
                this.drawnElements.push(circle);
            } else if (this.currentShape === 'parabola' && this.points.length >= 2) {
                const vertex = this.points[0];
                const pt = this.points[1];
                const h = () => vertex.X();
                const k = () => vertex.Y();
                const a = () => {
                    const dx = pt.X() - h();
                    if (Math.abs(dx) < 0.001) return 1;
                    return (pt.Y() - k()) / (dx * dx);
                };
                const f = (x: number) => a() * Math.pow(x - h(), 2) + k();
                const parabola = this.board.create('functiongraph', [f], { strokeColor: 'green' });
                this.drawnElements.push(parabola);
            } else if (this.currentShape === 'ellipse' && this.points.length >= 2) {
                const p1 = this.points[0];
                const p2 = this.points[1];
                const center = this.board.create('point', [() => (p1.X()+p2.X())/2, () => (p1.Y()+p2.Y())/2], {visible: false});
                const axis1 = this.board.create('point', [() => center.X(), () => p1.Y()], {visible: false});
                const axis2 = this.board.create('point', [() => p1.X(), () => center.Y()], {visible: false});
                this.drawnElements.push(center, axis1, axis2);
                
                const ellipse = this.board.create('ellipse', [center, axis1, axis2], { strokeColor: 'purple', hasInnerPoints: true });
                this.drawnElements.push(ellipse);
            }
        }
        
        this.board.update();
    }

    public clear() {
        this.drawnElements.forEach(el => this.board.removeObject(el));
        this.points.forEach(p => this.board.removeObject(p));
        this.drawnElements = [];
        this.points = [];
        this.currentShape = '';
    }

    public destroy() {
        if (this.board) {
            JXG.JSXGraph.freeBoard(this.board);
        }
    }
}
"""

with open("frontend/src/scripts/GraphingCanvas.ts", "w") as f:
    f.write(content)
print("Updated GraphingCanvas.ts")
