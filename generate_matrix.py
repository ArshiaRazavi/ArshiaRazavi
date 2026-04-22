#!/usr/bin/env python3
"""
Matrix Rain SVG Generator
=========================
Generates a Matrix-style falling characters SVG for your GitHub profile.
Each character falls independently from the top to the bottom.
Profile text is overlaid on top of the faded matrix rain.
Tweak the config below and re-run: python3 generate_matrix.py
"""

import random
import html

# ─── MATRIX CONFIG ───────────────────────────────────────────────────────
WIDTH = 850           # SVG width
HEIGHT = 400          # SVG height (taller to fit profile info)
BG_COLOR = "#0d1117"  # Background (GitHub dark)
TEXT_COLOR = "#0f0"   # Normal green
BRIGHT_COLOR = "#5f5" # Bright/glow green
FONT_SIZE_MIN = 10    # Smallest character size
FONT_SIZE_MAX = 14    # Largest character size
NUM_CHARS = 60        # Total number of falling snippets (less = cleaner)
RAIN_OPACITY = 0.18   # Overall opacity of the rain (lower = more faded)
CLEAR_ZONE = False    # Keep the center clear so profile text is readable
CLEAR_X = (200, 650)  # Horizontal clear zone (pixels from left)
CLEAR_Y = (130, 310)  # Vertical clear zone (pixels from top)
BRIGHT_CHANCE = 0.2   # Chance a character is bright (0.0 - 1.0)
MIN_SPEED = 2.0       # Fastest fall (seconds)
MAX_SPEED = 5.0       # Slowest fall (seconds)
MAX_DELAY = 4.0       # Max animation delay (seconds)
OUTPUT_FILE = "matrix.svg"
SEED = None           # Set to a number to lock in a layout, None for random

# ─── PROFILE TEXT CONFIG ─────────────────────────────────────────────────
PROFILE_NAME = "Hey, I'm Arshia"
PROFILE_EMOJI = "👋"
PROFILE_LINES = [
    "🎓  BSc Physics  ·  MSc Computational Neuroscience",
    "🚀  Software Engineer @ AltaML",
    "🛠️  Python  ·  C/C++  ·  MATLAB  ·  Git  ·  Linux",
]
NAME_FONT_SIZE = 36
NAME_COLOR = "#ffffff"
LINE_FONT_SIZE = 16
LINE_COLOR = "#c9d1d9"
LINE_SPACING = 28     # Vertical gap between profile lines

# ─── SNIPPET POOL ────────────────────────────────────────────────────────
# Each snippet falls as a whole string. Add/remove whatever you want!
SNIPPETS = [
    # ── Physics formulas ──
    "E=mc²", "F=ma", "ΔxΔp≥ℏ/2", "∇·E=ρ/ε₀", "∇×B=μ₀J",
    "iℏ∂ψ/∂t=Hψ", "p=mv", "λ=h/p", "E=hf", "PV=nRT",
    "F=-kx", "v=fλ", "τ=r×F", "W=Fd", "KE=½mv²",
    "S=k·lnΩ", "∇²φ=0", "dS≥0", "F=qE", "a=v²/r",
    "∂²ψ/∂x²", "Ĥψ=Eψ", "L=T-V", "∮B·dl=μ₀I",
    "g=9.81", "c=3×10⁸", "ℏ=h/2π", "ε₀μ₀=1/c²",

    # ── Computational Neuroscience ──
    "V=IR", "C·dV/dt=-gₗ(V-Eₗ)+I", "τₘ=RC",
    "dV/dt=-V/τ+I/C", "Iₛᵧₙ=g·(V-E)",
    "spike!", "∫PSP·dt", "STDP", "Δw∝pre·post",
    "LIF neuron", "Hodgkin-Huxley", "∂V/∂t=D∇²V",
    "firing rate", "Nernst eq.", "V=-70mV",
    "EPSP/IPSP", "Na⁺ K⁺ Ca²⁺", "gₙₐ·m³h",
    "refractory", "∂n/∂t=αₙ(1-n)-βₙn",
    "θ=threshold", "raster plot", "Poisson(λt)",
    "fMRI BOLD", "EEG signal", "neural code",
    "population vector", "tuning curve", "receptive field",
    "∇²V=f(V,w)", "FitzHugh-Nagumo", "bifurcation",
    "synaptic plasticity", "Hebbian", "∂w/∂t",

    # ── Math ──
    "∫f(x)dx", "∑n²", "lim x→∞", "dy/dx", "∂f/∂x",
    "∇·F=0", "det(A)=0", "eⁱᶿ=cosθ+isinθ", "∀x∈ℝ",
    "∃x:f(x)=0", "n!", "∏ᵢaᵢ", "√(a²+b²)", "log₂(n)",
    "P(A|B)", "σ²=E[X²]", "μ=E[X]", "∫₀^∞", "Σᵢxᵢ",
    "∂²f/∂x∂y", "||v||=1", "A⊗B", "dim(V)", "rank(A)",

    # ── Python code ──
    "def f(x):", "import numpy", "return x**2",
    "for i in range(n):", "if x > 0:", "lambda x: x+1",
    "np.array([])", "self.train()", "model.fit(X,y)",
    "pip install", "class Model:", "yield x",
    "print(loss)", "grad = ∇L", "lr = 0.001",
    "torch.tensor", "plt.plot(x,y)",

    # ── C/C++ ──
    "#include", "int main()", "malloc(n)", "free(ptr)",
    "printf()", "*ptr = &x", "sizeof(int)", "return 0;",
    "void f()", "struct Node", "std::vector",

    # ── MATLAB ──
    "A = zeros(n)", "eig(A)", "fft(x)", "plot(x,y)",
    "inv(A)", "linspace()", "ode45(@f)", "meshgrid",

    # ── Finance / Quant ──
    "dS=μSdt+σSdW", "Δ=∂V/∂S", "Θ=-∂V/∂t", "σ√t",
    "E[R]=Σwᵢrᵢ", "VaR 95%", "β=cov/var", "NPV=Σ",
    "r=ln(S/K)", "max(S-K,0)", "CAPM",

    # ── ML / Data Science ──
    "∇L(θ)", "softmax(z)", "ReLU(x)", "σ(x)=1/(1+e⁻ˣ)",
    "MSE=Σ(ŷ-y)²/n", "cross_entropy", "backprop",
    "SGD(lr=α)", "dropout=0.5", "batch_size=32",
]
# ─── END CONFIG ──────────────────────────────────────────────────────────


def generate_svg():
    if SEED is not None:
        random.seed(SEED)

    # ── Build rain snippets ──
    chars_svg = ""
    css_classes = ""

    placed = 0
    attempts = 0
    while placed < NUM_CHARS and attempts < NUM_CHARS * 10:
        attempts += 1
        snippet = random.choice(SNIPPETS)
        size = random.randint(FONT_SIZE_MIN, FONT_SIZE_MAX)
        # Estimate text width to keep it in bounds
        est_width = len(snippet) * size * 0.6
        max_x = max(5, int(WIDTH - est_width - 10))
        x = random.randint(5, max_x)

        # Skip if snippet lands in the clear zone (where profile text is)
        if CLEAR_ZONE:
            # The snippet's Y is animated, but we spread them across the height
            # by using the delay to stagger. We check a "rest" Y estimate.
            # For center-clearing, skip if x overlaps the clear zone center.
            x_end = x + est_width
            if x < CLEAR_X[1] and x_end > CLEAR_X[0]:
                # Only allow ~30% of snippets in the clear X band
                if random.random() > 0.15:
                    continue

        speed = round(random.uniform(MIN_SPEED, MAX_SPEED), 2)
        delay = round(random.uniform(0, MAX_DELAY), 2)
        is_bright = random.random() < BRIGHT_CHANCE
        i = placed

        css_classes += (
            f"    .c{i} {{ animation: drop{i} {speed}s linear {delay}s infinite; }}\n"
            f"    @keyframes drop{i} {{ "
            f"0% {{ transform: translateY(-20px); opacity: 0; }} "
            f"5% {{ opacity: 1; }} "
            f"90% {{ opacity: 1; }} "
            f"100% {{ transform: translateY({HEIGHT + 20}px); opacity: 0; }} }}\n"
        )

        cls = f"c{i}"
        if is_bright:
            cls += " bright"
        chars_svg += f'    <text x="{x}" y="0" font-size="{size}" class="{cls}">{html.escape(snippet)}</text>\n'
        placed += 1

    # ── Build profile overlay text ──
    center_x = WIDTH // 2
    name_y = HEIGHT // 2 - 40
    profile_svg = f'  <g class="profile">\n'
    profile_svg += (
        f'    <text x="{center_x}" y="{name_y}" '
        f'font-size="{NAME_FONT_SIZE}" fill="{NAME_COLOR}" '
        f'font-weight="bold" text-anchor="middle" font-family="\'Segoe UI\', Arial, sans-serif">'
        f'{html.escape(PROFILE_NAME)} {PROFILE_EMOJI}</text>\n'
    )
    for idx, line in enumerate(PROFILE_LINES):
        ly = name_y + 50 + idx * LINE_SPACING
        profile_svg += (
            f'    <text x="{center_x}" y="{ly}" '
            f'font-size="{LINE_FONT_SIZE}" fill="{LINE_COLOR}" '
            f'text-anchor="middle" font-family="\'Segoe UI\', Arial, sans-serif">'
            f'{html.escape(line)}</text>\n'
        )
    profile_svg += '  </g>\n'

    # ── Assemble CSS ──
    css = f"""
    rect.bg {{ fill: {BG_COLOR}; }}
    .rain text {{ font-family: 'Courier New', monospace; fill: {TEXT_COLOR}; }}
    .rain text.bright {{ fill: {BRIGHT_COLOR}; font-weight: bold; }}
{css_classes}"""

    # ── Assemble SVG ──
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}">
  <style>{css}  </style>
  <rect class="bg" width="{WIDTH}" height="{HEIGHT}" rx="6"/>
  <g class="rain" opacity="{RAIN_OPACITY}">
{chars_svg}  </g>
{profile_svg}</svg>
"""

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(svg)

    print(f"Generated {OUTPUT_FILE} ({NUM_CHARS} rain snippets, {WIDTH}x{HEIGHT})")
    print(f"Snippet pool: {len(SNIPPETS)} formulas/code fragments")
    print(f"Rain opacity: {RAIN_OPACITY} (lower = more faded)")
    print(f"Seed: {SEED if SEED else 'random'}")


if __name__ == "__main__":
    generate_svg()
