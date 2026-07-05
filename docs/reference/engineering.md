# Engineering Question Bank

**Legend:**
- `[C]` Conceptual — understanding definitions, behaviors, relationships
- `[P]` Procedural — step-by-step calculation
- `[CT]` Critical Thinking — multi-step, proof-adjacent, application
- `[N]` Novel — unusual framing, graphical, "what if," reverse engineering

---

## Circuit Theory

### Topic 1: DC Analysis (KCL, KVL, Thevenin, Norton)

**Q1.** `[C]` State Kirchhoff's Current Law (KCL) and Kirchhoff's Voltage Law (KVL). What conservation laws do they follow from?
> **Answer:** KCL: The sum of currents entering any node equals the sum leaving (charge conservation). KVL: The sum of voltage drops around any closed loop is zero (energy conservation / path independence of voltage).

**Q2.** `[C]` Explain the difference between an ideal voltage source and an ideal current source. How does a real battery differ from an ideal voltage source?
> **Answer:** Ideal voltage source maintains constant voltage regardless of current. Ideal current source maintains constant current regardless of voltage. Real battery has internal resistance $r$, so its terminal voltage drops as current increases: $V_{terminal}=\mathcal{E}-Ir$.

**Q3.** `[P]` Three resistors of $2\Omega$, $3\Omega$, and $6\Omega$ are connected in parallel. Find the equivalent resistance.
> **Answer:** $\frac{1}{R_{eq}}=\frac{1}{2}+\frac{1}{3}+\frac{1}{6}=\frac{3+2+1}{6}=1$. $R_{eq}=1\Omega$.

**Q4.** `[P]` A circuit has a $10\text{V}$ source, $4\Omega$ resistor, and $6\Omega$ resistor in series. Use the voltage divider rule to find the voltage across the $6\Omega$ resistor.
> **Answer:** $V_{6\Omega}=10\times\frac{6}{4+6}=6\text{V}$.

**Q5.** `[P]` Apply KCL to find the current through the $3\Omega$ resistor: a node has $5\text{A}$ entering, $2\text{A}$ leaving through a wire. The remaining current exits through the $3\Omega$ to a $6\text{V}$ source.
> **Answer:** KCL: $I_{3\Omega}=5-2=3\text{A}$.

**Q6.** `[P]` Find the Thevenin equivalent seen from terminals A-B of a circuit with a $12\text{V}$ source and $4\Omega$ internal, connected to a $6\Omega$ load.
> **Answer:** $V_{th}=12\times\frac{6}{4+6}=7.2\text{V}$ (open circuit voltage with load disconnected — actually $V_{th}=12\text{V}$ if no internal resistance between source and A). $R_{th}$: with source replaced by short, $R_{th}=4||6=2.4\Omega$ if the $4\Omega$ and $6\Omega$ are in the correct topology. (Specific answer depends on exact topology; demonstrate the method.)

**Q7.** `[P]` State and apply Norton's theorem to convert a Thevenin circuit ($V_{th}=10\text{V}$, $R_{th}=5\Omega$) to its Norton equivalent.
> **Answer:** $I_N=V_{th}/R_{th}=10/5=2\text{A}$. $R_N=R_{th}=5\Omega$. Norton circuit: 2 A current source in parallel with $5\Omega$.

**Q8.** `[P]` Use the superposition principle to find the current through $R=4\Omega$ in a circuit with a $12\text{V}$ source and a $6\text{A}$ source (specific topology assumed).
> **Answer:** (Step 1) With the current source open, find $I'$ from voltage source. (Step 2) With voltage source shorted, find $I''$ from current source. Total $I=I'+I''$ (with correct signs for each contribution).

**Q9.** `[CT]` Use KCL and KVL (nodal/mesh analysis) to find all branch currents in a circuit with two voltage sources ($\mathcal{E}_1=12\text{V}$, $\mathcal{E}_2=4\text{V}$) and resistors $R_1=6\Omega$, $R_2=2\Omega$, $R_3=4\Omega$ — Wheatstone bridge configuration.
> **Answer:** Set up two mesh current equations. Solve the $2\times2$ linear system. In a balanced Wheatstone bridge ($R_1/R_2=R_3/R_4$), no current flows through the galvanometer.

**Q10.** `[CT]` Prove that maximum power is transferred from a source with Thevenin resistance $R_{th}$ to a load $R_L$ when $R_L=R_{th}$.
> **Answer:** $P_L=I^2 R_L=(V_{th}/(R_{th}+R_L))^2 R_L$. Differentiate with respect to $R_L$ and set to zero. $dP_L/dR_L=V_{th}^2(R_{th}-R_L)/(R_{th}+R_L)^3=0 \implies R_L=R_{th}$.

**Q11.** `[N]` A voltmeter with internal resistance $1\text{M}\Omega$ is used to measure voltage across a $100\text{k}\Omega$ resistor. What is the percentage error introduced by the meter's loading?
> **Answer:** Without meter: $V_R=E\cdot\frac{R}{R+R_{rest}}$. With meter in parallel: $R_{eff}=\frac{1000\times100}{1100}\approx90.9\text{k}\Omega$. Ratio $=90.9/100=0.909$. Error $\approx9.1\%$.

**Q12.** `[N]` Why does connecting resistors in parallel always decrease the equivalent resistance below the smallest individual resistor?
> **Answer:** Adding a parallel path always provides an additional route for current, increasing total current for the same voltage. By $R_{eq}=V/I_{total}$, more current means smaller $R_{eq}$. Mathematically, $1/R_{eq}=1/R_1+1/R_2+\ldots$ always gives $R_{eq}<\min(R_1,R_2,\ldots)$.

**Q13.** `[P]` A ladder network has alternating series resistors $R_s=1\Omega$ and shunt resistors $R_p=2\Omega$. For a semi-infinite ladder, find the input resistance.
> **Answer:** Input resistance $R_{in}$ satisfies $R_{in}=R_s+R_p||R_{in}$. $R_{in}=1+\frac{2R_{in}}{2+R_{in}}$. Solving: $R_{in}(2+R_{in})=2+R_{in}+2R_{in}$. $2R_{in}+R_{in}^2=2+3R_{in}$. $R_{in}^2-R_{in}-2=0$. $(R_{in}-2)(R_{in}+1)=0$. $R_{in}=2\Omega$.

---

### Topic 2: Transient and AC Analysis

**Q14.** `[C]` Explain what the time constant $\tau$ means physically for an RC circuit.
> **Answer:** $\tau=RC$ is the time for the capacitor to charge to $1-1/e\approx63.2\%$ of its final value. After $5\tau$, the capacitor is considered fully charged (99.3%).

**Q15.** `[C]` Why does a capacitor act as an open circuit at DC steady state and a short circuit at very high frequencies? Why does an inductor act opposite?
> **Answer:** Capacitor: $Z_C=1/(j\omega C)$. As $\omega\to0$, $Z_C\to\infty$ (open). As $\omega\to\infty$, $Z_C\to0$ (short). Inductor: $Z_L=j\omega L$. As $\omega\to0$, $Z_L\to0$ (short). As $\omega\to\infty$, $Z_L\to\infty$ (open).

**Q16.** `[P]` An RL series circuit with $R=100\Omega$ and $L=0.5\text{H}$ is connected to a $50\text{V}$ DC source at $t=0$. Find $i(t)$.
> **Answer:** $\tau=L/R=0.005\text{s}$. $i_{ss}=50/100=0.5\text{A}$. $i(t)=0.5(1-e^{-200t})\text{A}$.

**Q17.** `[P]` A $10\mu\text{F}$ capacitor in series with $100\Omega$ is connected to $20\text{V}$ at $t=0$ with capacitor initially uncharged. Find $v_C(t)$ and $i(t)$.
> **Answer:** $\tau=RC=10^3\times10^{-5}=10^{-3}\text{s}=1\text{ms}$. $v_C(t)=20(1-e^{-1000t})\text{V}$. $i(t)=0.2e^{-1000t}\text{A}$.

**Q18.** `[P]` Find the impedance of a series RLC circuit with $R=50\Omega$, $L=0.1\text{H}$, $C=100\mu\text{F}$ at $f=60\text{Hz}$.
> **Answer:** $\omega=2\pi(60)=376.99\text{rad/s}$. $Z_L=j\omega L=j37.7\Omega$. $Z_C=1/(j\omega C)=-j26.5\Omega$. $Z=50+j37.7-j26.5=50+j11.2\Omega$. $|Z|=\sqrt{50^2+11.2^2}=51.2\Omega$.

**Q19.** `[P]` At what frequency does the series RLC circuit of Q18 resonate? What is the impedance at resonance?
> **Answer:** $f_r=1/(2\pi\sqrt{LC})=1/(2\pi\sqrt{0.1\times10^{-4}})=1/(2\pi\times0.00316)=50.3\text{Hz}$. At resonance, $Z_L=Z_C$ (cancel), so $Z=R=50\Omega$.

**Q20.** `[CT]` Derive the expression for the quality factor $Q$ of a series RLC resonant circuit and explain its physical meaning.
> **Answer:** $Q=\omega_r L/R=1/(\omega_r RC)=\frac{1}{R}\sqrt{L/C}$. Physically, $Q$ is the ratio of energy stored to energy dissipated per cycle. High $Q$ means a sharp, narrow resonance peak and selective frequency response.

**Q21.** `[CT]` For the circuit in Q16, find the energy stored in the inductor at $t=\tau$.
> **Answer:** $i(\tau)=0.5(1-e^{-1})=0.5\times0.632=0.316\text{A}$. $U_L=\frac{1}{2}Li^2=\frac{1}{2}(0.5)(0.1)=0.025\text{J}$.

**Q22.** `[N]` A phasor is a complex number representation of a sinusoidal signal. If $v(t)=10\cos(1000t+30°)\text{V}$, write its phasor representation and find the current phasor through a $j50\Omega$ inductor.
> **Answer:** $\tilde{V}=10\angle30°\text{V}$. $\tilde{I}=\tilde{V}/Z_L=10\angle30°/50\angle90°=0.2\angle-60°\text{A}$.

**Q23.** `[N]` What is the power factor of a purely capacitive load? What happens to the average power consumed?
> **Answer:** Power factor $\cos\theta=0$ (since $\theta=-90°$ for pure capacitor). Average power consumed is $P=V_{rms}I_{rms}\cos(-90°)=0$. Capacitors store and release energy but consume no average power.

---

## Digital Signal Processing (DSP)

### Topic 3: Discrete Signals and Z-Transforms

**Q24.** `[C]` Explain the Nyquist-Shannon Sampling Theorem and what aliasing is.
> **Answer:** A continuous signal with maximum frequency $f_{max}$ must be sampled at rate $f_s \ge 2f_{max}$ to be perfectly reconstructed. If $f_s < 2f_{max}$, aliasing occurs — high frequency components appear as lower frequencies in the sampled signal, causing distortion.

**Q25.** `[C]` What is the difference between an FIR and an IIR filter? Give one advantage and one disadvantage of each.
> **Answer:** FIR (Finite Impulse Response): uses only current and past inputs. Always stable. Advantage: guaranteed stability, linear phase. Disadvantage: requires many taps for sharp selectivity. IIR: uses past outputs (feedback). Advantage: sharper response with fewer coefficients. Disadvantage: can be unstable; non-linear phase.

**Q26.** `[P]` Find the Z-transform of $x[n]=\delta[n]-\delta[n-1]$.
> **Answer:** $X(z)=1-z^{-1}=\frac{z-1}{z}$, ROC: all $z$ except $z=0$.

**Q27.** `[P]** Find the Z-transform of $x[n]=a^n u[n]$.
> **Answer:** $X(z)=\sum_{n=0}^\infty a^n z^{-n}=\frac{1}{1-az^{-1}}=\frac{z}{z-a}$, ROC: $|z|>|a|$.

**Q28.** `[P]` Find the inverse Z-transform of $X(z)=\frac{z}{z-0.5}$, assuming a causal (right-sided) signal.
> **Answer:** Recognizing the standard form, $x[n]=(0.5)^n u[n]$.

**Q29.** `[P]` A system has transfer function $H(z)=\frac{1+z^{-1}}{1-0.8z^{-1}}$. Write the difference equation.
> **Answer:** $Y(z)(1-0.8z^{-1})=X(z)(1+z^{-1}) \implies y[n]-0.8y[n-1]=x[n]+x[n-1]$.

**Q30.** `[P]` Determine whether the system $H(z)=\frac{z}{z-1.2}$ is stable.
> **Answer:** Pole at $z=1.2$. For a causal system to be stable (BIBO), all poles must be inside the unit circle ($|z|<1$). Since $|1.2|>1$, the system is **unstable**.

**Q31.** `[CT]` Find the steady-state output of the stable system $H(z)=\frac{0.2z}{z-0.8}$ in response to a unit step input $x[n]=u[n]$.
> **Answer:** By the Final Value Theorem: $y[\infty]=\lim_{z\to1}(1-z^{-1})H(z)X(z)$ where $X(z)=z/(z-1)$. $y[\infty]=\lim_{z\to1}(1-z^{-1})\frac{0.2z}{z-0.8}\frac{z}{z-1}$. Simplifying: $\lim_{z\to1}\frac{0.2z^2}{(z-0.8)z}=\frac{0.2}{0.2}=1$.

**Q32.** `[CT]` A system has $H(z)=\frac{z^2}{(z-0.5)(z+0.5)}$. (a) Find the poles and zeros. (b) Is it stable? (c) Sketch the pole-zero plot.
> **Answer:** Zeros: $z=0$ (double). Poles: $z=0.5$ and $z=-0.5$. All poles inside unit circle → stable. Pole-zero plot: two zeros at origin, poles at $\pm0.5$ on real axis.

**Q33.** `[N]` Convolution in the time domain corresponds to multiplication in what domain? What is the dual of this property?
> **Answer:** Convolution in time $\leftrightarrow$ multiplication in Z (or frequency) domain. Dual: multiplication in time $\leftrightarrow$ convolution in the Z/frequency domain.

**Q34.** `[N]` Explain why the ROC of a causal system is the exterior of a circle, while for an anti-causal system it is the interior.
> **Answer:** For a causal (right-sided) sequence, the Z-transform sum converges for $|z|$ large enough to dominate $|a|^n$, giving an exterior region. For anti-causal (left-sided), the sum converges for $|z|$ small enough, giving an interior region.

---

### Topic 4: Frequency Domain and Filters

**Q35.** `[C]` Explain what the Discrete-Time Fourier Transform (DTFT) represents and how it relates to the Z-transform.
> **Answer:** The DTFT is the frequency response of a discrete-time signal: $X(e^{j\omega})=\sum x[n]e^{-j\omega n}$. It is the Z-transform evaluated on the unit circle ($z=e^{j\omega}$). It gives the spectrum of the signal.

**Q36.** `[P]` Find the frequency response $H(e^{j\omega})$ of the system described by $y[n]=x[n]+x[n-1]$.
> **Answer:** $H(z)=1+z^{-1}$. On unit circle: $H(e^{j\omega})=1+e^{-j\omega}=e^{-j\omega/2}(e^{j\omega/2}+e^{-j\omega/2})=2\cos(\omega/2)e^{-j\omega/2}$. Magnitude: $|H|=2|\cos(\omega/2)|$.

**Q37.** `[P]` What type of filter (low-pass, high-pass, band-pass) does the system in Q36 implement? Justify.
> **Answer:** Low-pass filter. At $\omega=0$: $|H|=2$ (maximum). At $\omega=\pi$ (Nyquist): $|H|=2|\cos(\pi/2)|=0$. The filter passes low frequencies and blocks high frequencies.

**Q38.** `[CT]` Design a simple first-order high-pass FIR filter (difference equation and $H$) that has a zero at DC ($\omega=0$).
> **Answer:** $y[n]=x[n]-x[n-1]$. $H(z)=1-z^{-1}$. At $\omega=0$: $H=1-1=0$. At $\omega=\pi$: $H=1-e^{-j\pi}=1-(-1)=2$. This is indeed a high-pass filter with zero at DC.

**Q39.** `[CT]` A system's magnitude response is $|H(e^{j\omega})|=1$ for all $\omega$ and phase response is $\angle H=-N\omega$. What type of filter is this? What does it do to a signal?
> **Answer:** All-pass filter with linear phase. The magnitude is flat (passes all frequencies equally), but it delays all frequencies by $N$ samples. It does not change spectral content — only time-shifts the signal.

**Q40.** `[N]` What is the Gibbs phenomenon and how does it affect FIR filter design?
> **Answer:** When truncating an ideal brick-wall filter's infinite impulse response to a finite window, Gibbs phenomenon causes oscillatory ripples near the cutoff frequency and an overshoot of about 8.9% that does not decrease with more taps. Windowing functions (Hamming, Blackman, Kaiser) are applied to reduce this effect at the cost of a wider transition band.

---

## Computer Hardware & Architecture

### Topic 5: Boolean Logic and Combinational Circuits

**Q41.** `[C]` State De Morgan's Laws and demonstrate both forms by constructing a truth table for $\overline{A+B}$.
> **Answer:** $\overline{A+B}=\bar{A}\bar{B}$ and $\overline{AB}=\bar{A}+\bar{B}$. Truth table for $\overline{A+B}$: Only row $A=0,B=0$ gives $\overline{0+0}=\overline{0}=1$. Same as $\bar{A}\bar{B}$. ✓

**Q42.** `[P]` Simplify: $F=\overline{(\bar{A}+B)(A+\bar{B})}$ using Boolean algebra.
> **Answer:** Expand: $\bar{A}\bar{B}+\bar{A}A+B\bar{B}+BA$ (using distribution). Wait—use De Morgan directly: $\bar{A}+B=0$ AND $A+\bar{B}=0$ simultaneously is impossible unless both factors are 1. Use De Morgan: $F=\overline{(\bar{A}+B)}\cdot\overline{(A+\bar{B})}=(A\bar{B})(\bar{A}B)=A\bar{A}\bar{B}B=0$. Hmm, $F=0$ always? Actually: $(A\bar{B})$ AND $(\bar{A}B)$: first requires $A=1, B=0$; second requires $A=0, B=1$. Can't both be true. So $F=0$.

**Q43.** `[P]` Minimize $F(A,B,C)=\sum m(0,1,4,5)$ using a K-map.
> **Answer:** K-map groups minterms 0,1,4,5 (where $C=0$ and any $A,B$). Wait: minterms 0,1 have $A=0,B=0$ (C varies); minterms 4,5 have $A=1,B=0$ (C varies). Group all four: $\bar{B}$. Simplified: $F=\bar{B}$.

**Q44.** `[P]` Design a 2-to-1 multiplexer using basic gates.
> **Answer:** A 2:1 MUX selects between inputs $D_0$ (when $S=0$) and $D_1$ (when $S=1$). $F=\bar{S}D_0+SD_1$. Implementation: two AND gates (one inverts $S$), then an OR gate.

**Q45.** `[P]` Write the truth table and sum-of-products (SOP) expression for a full adder (inputs $A, B, C_{in}$; outputs $S, C_{out}$).
> **Answer:** $S=A\oplus B\oplus C_{in}=\sum m(1,2,4,7)$. $C_{out}=AB+BC_{in}+AC_{in}=\sum m(3,5,6,7)$.

**Q46.** `[CT]` Design a 4-bit ripple carry adder. Explain why it's called "ripple carry" and what its main performance limitation is.
> **Answer:** Four full adders chained: $C_{out}$ of each feeds as $C_{in}$ to the next. Called ripple carry because the carry signal must propagate (ripple) from the LSB to MSB. This creates a linear delay of $O(n)$ full-adder delays. For large $n$, carry lookahead adders are preferred ($O(\log n)$ delay).

**Q47.** `[CT]` Explain what a priority encoder is and design a 4-to-2 priority encoder (inputs $I_0-I_3$, $I_3$ highest priority; outputs $A_1, A_0$).
> **Answer:** A priority encoder outputs the binary code for the highest-priority active input. Truth table: $I_3=1\to$ output $11$; $I_3=0, I_2=1\to11$ Wait: 4-to-2 encodes which of 4 inputs is highest. $I_3=1\to A_1A_0=11$; $I_3=0,I_2=1\to10$; $I_3=0,I_2=0,I_1=1\to01$; others $\to00$. Boolean: $A_1=I_3+I_2$, $A_0=I_3+\bar{I_2}I_1$.

**Q48.** `[N]` How would you implement a NOT gate using only NAND gates? An AND gate? An OR gate?
> **Answer:** NOT: $\overline{A}=\overline{AA}$ (NAND with both inputs tied). AND: $AB=\overline{\overline{AB}}$ — two NANDs (one for $\overline{AB}$, one to invert). OR: $A+B=\overline{\overline{A}\cdot\overline{B}}$ — three NANDs (invert each input, then NAND).

---

### Topic 6: Sequential Logic, CPU, and Memory

**Q49.** `[C]` Explain the difference between combinational and sequential logic circuits. Give one example of each.
> **Answer:** Combinational: output depends only on current inputs (no memory). Example: adder, MUX. Sequential: output depends on current inputs AND past state (has memory). Example: flip-flop, counter, register.

**Q50.** `[C]` Explain the difference between a latch and a flip-flop.
> **Answer:** A latch is level-sensitive — it responds to input changes whenever the enable/clock is high. A flip-flop is edge-triggered — it only samples input and updates output on the rising (or falling) edge of the clock.

**Q51.** `[P]` Draw the truth table for a D flip-flop (inputs: $D$, $CLK$; output: $Q$).
> **Answer:** On the rising edge of CLK: $Q_{next}=D$ (output follows $D$). Between clock edges: $Q$ retains its previous value.

**Q52.** `[P]` A 3-bit binary ripple counter is built from T flip-flops. After 6 clock cycles starting from 000, what is the output?
> **Answer:** Count sequence: 000→001→010→011→100→101→110. After 6 cycles: $110_2=6$.

**Q53.** `[CT]` Design a finite state machine (FSM) that detects the sequence $101$ in a serial bit stream (non-overlapping). Draw the state diagram.
> **Answer:** States: $S_0$ (initial), $S_1$ (saw 1), $S_2$ (saw 10), $S_3$ (saw 101, output 1→reset to $S_0$). Transitions: $S_0\xrightarrow{1}S_1\xrightarrow{0}S_2\xrightarrow{1}S_3/\text{output}$. On any unexpected bit, return to appropriate state.

**Q54.** `[CT]` In a 5-stage pipeline (IF, ID, EX, MEM, WB), how many cycles does it take to complete 10 instructions? How does this compare to a non-pipelined processor?
> **Answer:** Pipelined: $5 + (10-1) = 14$ cycles (5 to fill pipe + 1 per instruction thereafter). Non-pipelined: $10\times5=50$ cycles. Speedup: $50/14\approx3.57\times$.

**Q55.** `[CT]` Explain the three types of hazards in a pipelined processor and give one hardware solution for each.
> **Answer:** (1) Structural hazard: two instructions need same resource simultaneously. Solution: add hardware (duplicate units) or stall. (2) Data hazard (RAW): instruction needs result of previous instruction. Solution: forwarding/bypassing. (3) Control hazard (branch hazard): branch target unknown. Solution: branch prediction (predict not-taken, BTB, BHT).

**Q56.** `[P]` A cache has block size of 64 bytes, 8 sets, and is 4-way set-associative. How many total cache lines are there and what is the total cache size?
> **Answer:** Total lines = $8\text{ sets}\times4\text{ ways}=32$ lines. Total size = $32\times64=2048$ bytes = $2\text{KB}$.

**Q57.** `[P]` Calculate the average memory access time (AMAT) for a two-level cache hierarchy: L1 hit time $=2$ cycles, L1 miss rate $=5\%$, L2 hit time $=8$ cycles, L2 miss rate (of L1 misses) $=20\%$, main memory access time $=100$ cycles.
> **Answer:** $\text{AMAT}=t_{L1}+m_{L1}(t_{L2}+m_{L2}\times t_{mem})=2+0.05(8+0.20\times100)=2+0.05(8+20)=2+0.05(28)=2+1.4=3.4$ cycles.

**Q58.** `[N]` Explain the difference between write-through and write-back cache policies. What is a dirty bit and where is it used?
> **Answer:** Write-through: every write to cache also updates main memory immediately. Simple but uses memory bandwidth. Write-back: writes go only to cache; main memory is updated only when the block is evicted. A dirty bit tracks whether a cached block differs from memory (1 = dirty = needs writeback). Used in write-back caches.

**Q59.** `[CT]` Explain Amdahl's Law and use it to find the maximum speedup for a program where 60% of execution time can be parallelized on $N=\infty$ processors.
> **Answer:** Amdahl's Law: $S=\frac{1}{(1-p)+p/N}$ where $p$ is the parallelizable fraction. As $N\to\infty$: $S_{max}=\frac{1}{1-p}=\frac{1}{1-0.6}=\frac{1}{0.4}=2.5\times$.

**Q60.** `[N]` Explain the von Neumann bottleneck and describe one architectural approach to mitigating it.
> **Answer:** The von Neumann bottleneck is the rate limitation caused by a single bus between CPU and memory — the processor must wait for memory fetches, limiting throughput. Mitigations: (1) Cache hierarchy (reduces average memory latency), (2) Prefetching (hide latency), (3) Harvard architecture (separate instruction/data buses), (4) Memory-level parallelism (multiple outstanding memory requests).
