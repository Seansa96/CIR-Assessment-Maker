import JXG from 'jsxgraph';

export interface GraphPoint {
    x: number;
    y: number;
}

export interface SubmittedGraphAnswer {
    shape: string;
    points: GraphPoint[];
    expression?: string | null;
}

export type GraphShapeTool = 'point' | 'line' | 'parabola' | 'ellipse' | 'circle' | null;

export class GraphingCanvas {
    private board: any;
    private containerElement: HTMLElement;
    private currentShape: string = '';
    private points: any[] = [];
    private drawnElements: any[] = [];
    private activeTool: GraphShapeTool = null;
    private isReadonly: boolean = false;

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
            this.board.on('down', this.handleBoardClick.bind(this));
        }
    }

    public setTool(tool: GraphShapeTool) {
        this.activeTool = tool;
    }

    private handleBoardClick(e: any) {
        if (this.isReadonly || !this.activeTool) return;
        
        const coords = this.board.getUsrCoordsOfMouse(e);
        const x = coords[0];
        const y = coords[1];

        // Check point limit
        const maxPts = {
            'point': 50,
            'line': 2,
            'circle': 2,
            'parabola': 2,
            'ellipse': 3
        }[this.activeTool as string] || 50;

        if (this.points.length >= maxPts) return;

        // Create point
        const p = this.board.create('point', [x, y], { size: 4, name: '', fixed: false });
        this.points.push(p);

        // When points are moved, we want to update the submitted answer
        p.on('drag', () => {
            this.board.update();
        });

        this.updateShape();
    }

    private updateShape() {
        // Clear previously drawn shapes (not points)
        this.drawnElements.forEach(el => this.board.removeObject(el));
        this.drawnElements = [];

        if (this.activeTool === 'line' && this.points.length >= 2) {
            const line = this.board.create('line', [this.points[0], this.points[1]], { strokeColor: 'blue', hasInnerPoints: true });
            this.drawnElements.push(line);
            this.currentShape = 'line';
        } else if (this.activeTool === 'parabola' && this.points.length >= 2) {
            // Draw parabola given vertex and a point
            // For MVP: let's use a function graph that interpolates the vertex and point
            // y = a(x - h)^2 + k
            const vertex = this.points[0];
            const pt = this.points[1];
            
            const h = () => vertex.X();
            const k = () => vertex.Y();
            const a = () => (pt.Y() - k()) / Math.pow(pt.X() - h(), 2);
            
            const f = (x: number) => a() * Math.pow(x - h(), 2) + k();
            const parabola = this.board.create('functiongraph', [f], { strokeColor: 'green' });
            this.drawnElements.push(parabola);
            this.currentShape = 'parabola';
        } else if (this.activeTool === 'ellipse' && this.points.length >= 3) {
            // Draw ellipse given center, and two axis points
            const center = this.points[0];
            const pt1 = this.points[1];
            const pt2 = this.points[2];
            const ellipse = this.board.create('ellipse', [center, pt1, pt2], { strokeColor: 'purple', hasInnerPoints: true });
            this.drawnElements.push(ellipse);
            this.currentShape = 'ellipse';
        } else if (this.activeTool === 'circle' && this.points.length >= 2) {
            const circle = this.board.create('circle', [this.points[0], this.points[1]], { strokeColor: 'orange', hasInnerPoints: true });
            this.drawnElements.push(circle);
            this.currentShape = 'circle';
        } else if (this.activeTool === 'point') {
            this.currentShape = 'point';
        }
    }

    public undo() {
        if (this.points.length > 0) {
            const p = this.points.pop();
            this.board.removeObject(p);
            this.updateShape();
        }
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
        
        // Re-create points
        for (const pt of answer.points) {
            const p = this.board.create('point', [pt.x, pt.y], { size: 4, name: '', fixed: this.isReadonly });
            this.points.push(p);
        }
        this.updateShape();
    }

    public clear() {
        this.drawnElements.forEach(el => this.board.removeObject(el));
        this.points.forEach(p => this.board.removeObject(p));
        this.drawnElements = [];
        this.points = [];
        this.currentShape = '';
    }

    public destroy() {
        JXG.JSXGraph.freeBoard(this.board);
    }
}
