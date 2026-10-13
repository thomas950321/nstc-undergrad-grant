#!/usr/bin/env python3
"""Create a self-contained HTML/SVG chart from JSON data.

The browser performs the visual rendering from the supplied numeric values;
this script never asks an image model to draw quantitative geometry.
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path
from html import escape


def load_data(path: Path) -> dict:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"無法讀取 JSON 數據：{exc}") from exc
    if not isinstance(data, dict):
        raise ValueError("JSON 根節點必須是物件")
    labels = data.get("labels")
    values = data.get("values")
    if not isinstance(labels, list) or not labels or not all(isinstance(x, str) for x in labels):
        raise ValueError("labels 必須是非空字串陣列")
    if not isinstance(values, list) or len(values) != len(labels):
        raise ValueError("values 必須與 labels 等長")
    if not all(isinstance(x, (int, float)) and math.isfinite(x) for x in values):
        raise ValueError("values 必須全部是有限數值")
    chart_type = data.get("type", "bar")
    if chart_type not in {"bar", "line", "pie"}:
        raise ValueError("type 只支援 bar、line 或 pie")
    if chart_type == "pie" and any(x < 0 for x in values):
        raise ValueError("pie 圖的 values 不可為負數")
    if chart_type == "pie" and sum(values) <= 0:
        raise ValueError("pie 圖的 values 總和必須大於 0")
    return data


def build_html(data: dict, source_name: str) -> str:
    payload = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    title = escape(str(data.get("title", "研究數據圖表")))
    unit = escape(str(data.get("unit", "")))
    return f'''<!doctype html>
<html lang="zh-Hant">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<style>
  * {{ box-sizing: border-box; }}
  body {{ margin: 0; background: white; color: #172033; font-family: Arial, "Noto Sans CJK TC", sans-serif; }}
  main {{ width: 1200px; padding: 42px 52px 34px; }}
  h1 {{ margin: 0 0 8px; font-size: 30px; font-weight: 700; }}
  .meta {{ color: #5b6578; font-size: 16px; margin-bottom: 18px; }}
  svg {{ display: block; width: 1096px; height: 620px; overflow: visible; }}
  .source {{ margin-top: 12px; font-size: 12px; color: #657084; }}
  .grid {{ stroke: #dce2eb; stroke-width: 1; }}
  .axis {{ stroke: #354052; stroke-width: 2; }}
  .label {{ fill: #354052; font-size: 15px; }}
  .value {{ fill: #172033; font-size: 14px; font-weight: 700; }}
  .series {{ fill: #2764d8; stroke: #2764d8; }}
  .line {{ fill: none; stroke: #2764d8; stroke-width: 4; }}
  .point {{ fill: #2764d8; stroke: white; stroke-width: 2; }}
</style>
</head>
<body><main>
<h1 id="title"></h1><div class="meta" id="meta"></div><svg id="chart" viewBox="0 0 1096 620" role="img" aria-label="{title}"></svg>
<div class="source">數據來源：{escape(source_name)}</div>
<script>
const DATA = {payload};
const svg = document.getElementById('chart');
const NS = 'http://www.w3.org/2000/svg';
const W = 1096, H = 620, left = 88, right = 28, plotTop = 24, bottom = 82;
const plotW = W-left-right, plotH = H-plotTop-bottom;
const labels = DATA.labels, values = DATA.values;
document.getElementById('title').textContent = DATA.title || '研究數據圖表';
document.getElementById('meta').textContent = DATA.unit ? `單位：${{DATA.unit}}｜圖表類型：${{DATA.type || 'bar'}}` : `圖表類型：${{DATA.type || 'bar'}}`;
function el(tag, attrs={{}}) {{ const n=document.createElementNS(NS,tag); for(const [k,v] of Object.entries(attrs)) n.setAttribute(k,v); svg.appendChild(n); return n; }}
function text(x,y,s,cls='label',anchor='middle') {{ const n=el('text',{{x,y,class:cls,'text-anchor':anchor}}); n.textContent=s; return n; }}
function niceMax(max) {{ if(max<=0)return 1; const p=10**Math.floor(Math.log10(max)); const n=max/p; return (n<=1?1:n<=2?2:n<=5?5:10)*p; }}
function axis(max) {{ const m=niceMax(max); for(let i=0;i<=5;i++) {{ const v=m*i/5, y=plotTop+plotH-(v/m)*plotH; el('line',{{x1:left,y1:y,x2:W-right,y2:y,class:'grid'}}); text(left-12,y+5,String(Number(v.toFixed(2))), 'label','end'); }} el('line',{{x1:left,y1:plotTop,x2:left,y2:plotTop+plotH,class:'axis'}}); el('line',{{x1:left,y1:plotTop+plotH,x2:W-right,y2:plotTop+plotH,class:'axis'}}); return m; }}
function xLabel(x,s) {{ text(x,plotTop+plotH+28,s,'label','middle'); }}
function bar() {{ const max=axis(Math.max(...values)); const gap=plotW/labels.length, bw=Math.min(90,gap*0.62); values.forEach((v,i)=>{{const x=left+gap*i+(gap-bw)/2, h=Math.max(0,v/max*plotH), y=plotTop+plotH-h; el('rect',{{x,y,width:bw,height:h,rx:5,class:'series'}}); text(x+bw/2,y-10,String(v),'value'); xLabel(x+bw/2,labels[i]);}}); }}
function line() {{ const max=axis(Math.max(...values)); const gap=labels.length===1?plotW:plotW/(labels.length-1); const pts=values.map((v,i)=>[left+gap*i,plotTop+plotH-v/max*plotH]); el('polyline',{{points:pts.map(p=>p.join(',')).join(' '),class:'line'}}); pts.forEach((p,i)=>{{el('circle',{{cx:p[0],cy:p[1],r:7,class:'point'}}); text(p[0],p[1]-14,String(values[i]),'value'); xLabel(p[0],labels[i]);}}); }}
function pie() {{ const total=values.reduce((a,b)=>a+b,0), cx=548, cy=300, r=205; let angle=-Math.PI/2; const colors=['#2764d8','#ef8a35','#32a66a','#9b59b6','#d64d63','#00a6a6']; values.forEach((v,i)=>{{const a=v/total*Math.PI*2, x1=cx+r*Math.cos(angle), y1=cy+r*Math.sin(angle), x2=cx+r*Math.cos(angle+a), y2=cy+r*Math.sin(angle+a), large=a>Math.PI?1:0; const d=`M ${{cx}} ${{cy}} L ${{x1}} ${{y1}} A ${{r}} ${{r}} 0 ${{large}} 1 ${{x2}} ${{y2}} Z`; el('path',{{d,fill:colors[i%colors.length],stroke:'white','stroke-width':3}}); const mid=angle+a/2; text(cx+(r+36)*Math.cos(mid),cy+(r+36)*Math.sin(mid),`${{labels[i]}} ${{(v/total*100).toFixed(1)}}%`,'label'); angle+=a;}}); }}
if(DATA.type==='line') line(); else if(DATA.type==='pie') pie(); else bar();
</script></main></body></html>'''


def main() -> int:
    parser = argparse.ArgumentParser(description="將 JSON 數據轉成可渲染的 HTML/SVG 圖表")
    parser.add_argument("data_json")
    parser.add_argument("output_html")
    args = parser.parse_args()
    try:
        data_path = Path(args.data_json)
        data = load_data(data_path)
        Path(args.output_html).write_text(build_html(data, data_path.name), encoding="utf-8")
        print(f"[OK] 已產生 HTML 圖表：{args.output_html}")
    except Exception as exc:
        print(f"[FAIL] 圖表生成失敗：{exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
