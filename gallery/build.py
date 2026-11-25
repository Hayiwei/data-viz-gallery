"""Build standalone charts, a contact sheet, and a static HTML gallery."""

import argparse
import html
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from .charts import RECIPES
from .data import read_data, write_data
from .style import apply_style, NAVY, TEAL, MUTED

ROOT = Path(__file__).resolve().parents[1]


def build(output: Path, data_dir: Path):
    apply_style()
    data = read_data(data_dir)
    figures = output / "figures"
    figures.mkdir(parents=True, exist_ok=True)
    for slug, title, subtitle, draw in RECIPES:
        fig, ax = plt.subplots(figsize=(8, 5), layout="constrained")
        draw(ax, data)
        ax.set_title(title, loc="left")
        fig.suptitle(subtitle, x=.02, ha="left", fontsize=9, color=MUTED)
        fig.supxlabel("SYNTHETIC DATA  /  Data Viz Gallery · Hayiwei", fontsize=8, color=MUTED)
        fig.savefig(figures / f"{slug}.png", dpi=180)
        fig.savefig(figures / f"{slug}.svg", metadata={"Date": None})
        plt.close(fig)

    fig, axes = plt.subplots(3, 2, figsize=(14, 13), layout="constrained")
    fig.suptitle("Everyday data, thoughtfully drawn.", x=.02, ha="left", fontsize=26, weight="bold", color=NAVY)
    for ax, (_, title, subtitle, draw) in zip(axes.flat, RECIPES):
        draw(ax, data)
        ax.set_title(title + "\n" + subtitle, loc="left", fontsize=11, pad=14)
    fig.supxlabel("DATA VIZ GALLERY  /  Six reproducible chart recipes  /  All observations are synthetic", fontsize=10, color=MUTED)
    fig.savefig(output / "overview.png", dpi=150)
    plt.close(fig)
    cards = "\n".join(
        f'<article><div class="card-top"><span>0{i}</span><span>{kind}</span></div>'
        f'<a href="figures/{slug}.svg"><img src="figures/{slug}.svg" alt="{html.escape(title + ": " + subtitle)}" loading="lazy"></a>'
        f'<div class="card-bottom"><h2>{html.escape(title)}</h2><p>{html.escape(subtitle)}</p>'
        f'<a href="figures/{slug}.svg" download>SVG ↗</a> <a href="figures/{slug}.png" download>PNG ↗</a></div></article>'
        for i, ((slug, title, subtitle, _), kind) in enumerate(zip(RECIPES, ["Trend", "Comparison", "Distribution", "Pattern", "Relationship", "Variation"]), 1)
    )
    document = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Data Viz Gallery · Hayiwei</title>
<style>
:root{color-scheme:light;--ink:#19334a;--teal:#117c83;--muted:#596e7c;--line:#dfe7ed}
*{box-sizing:border-box}body{margin:0;background:#f5f7f9;color:var(--ink);font:16px/1.6 system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}
header,main,footer{max-width:1160px;margin:auto;padding:0 32px}header{padding-top:64px;padding-bottom:40px}
nav{display:flex;justify-content:space-between;gap:20px;font-size:13px}a{color:var(--teal);text-underline-offset:4px}
.label{font-weight:700;letter-spacing:.16em;color:var(--teal);font-size:12px;text-transform:uppercase}
h1{font-size:clamp(32px,5vw,56px);letter-spacing:-.045em;line-height:1.12;margin:36px 0 18px;max-width:750px}
.lead{max-width:640px;color:var(--muted);font-size:18px}.tags{display:flex;gap:10px;flex-wrap:wrap;margin-top:24px}
.tags span{font-size:12px;border:1px solid var(--line);border-radius:20px;padding:4px 12px;background:white}
main{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:24px}
article{background:white;border:1px solid var(--line);border-radius:14px;overflow:hidden}
.card-top{padding:18px 22px;display:flex;justify-content:space-between;font-size:12px;color:var(--muted);border-bottom:1px solid #eef2f5}
.card-top span:first-child{color:var(--teal);font-weight:700}img{display:block;width:100%;height:auto}
.card-bottom{padding:8px 22px 24px}h2{font-size:18px;letter-spacing:-.02em;margin:0}
.card-bottom p{font-size:13px;color:var(--muted);margin:5px 0 16px}.card-bottom a{font-size:12px;margin-right:14px}
footer{padding-top:40px;padding-bottom:36px;font-size:13px;color:var(--muted)}a:focus-visible{outline:3px solid var(--teal);outline-offset:4px}
@media(max-width:700px){main{grid-template-columns:1fr}header,main,footer{padding-left:20px;padding-right:20px}header{padding-top:30px}}
</style></head><body><header>
<nav><span class="label">Hayiwei / Data Viz Gallery</span><a href="https://github.com/Hayiwei/data-viz-gallery">View source ↗</a></nav>
<h1>Everyday data,<br>thoughtfully drawn.</h1>
<p class="lead">Six small studies in making data easier to read. A consistent palette, clear labels, and Python you can run yourself.</p>
<div class="tags"><span>Python + Matplotlib</span><span>Six chart recipes</span><span>PNG + SVG</span><span>Synthetic data · fixed seed</span></div>
</header><main>""" + cards + """</main><footer>
All observations are generated examples, not measurements of real people or cities.
<br>Reproduce every chart with <code>python -m gallery.build</code>. MIT licensed.</footer></body></html>"""
    (output / "index.html").write_text(document, encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "docs")
    parser.add_argument("--data-dir", type=Path, default=ROOT / "data")
    parser.add_argument("--regenerate-data", action="store_true", help="Replace the synthetic CSVs using seed 2026.")
    args = parser.parse_args()
    if args.regenerate_data:
        write_data(args.data_dir)
    build(args.output, args.data_dir)
    print(f"Built six PNGs, six SVGs, an overview, and index.html in {args.output}")


if __name__ == "__main__":
    main()
