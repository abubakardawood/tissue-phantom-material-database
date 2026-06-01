import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Organ Browser — Phantom Material Database",
    page_icon="🫀",
    layout="wide",
)

st.markdown("""
<style>
    .block-container { padding-top: 1.5rem; }
</style>
""", unsafe_allow_html=True)

st.markdown("## Organ Browser")
st.markdown("Select an organ to view its literature stiffness range and matching phantom compositions.")
st.divider()

HTML = r"""
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { font-family: 'Segoe UI', system-ui, sans-serif; background: #fff; color: #1a1a1a; font-size: 13px; }

  .app { display: grid; grid-template-columns: 300px 1fr; gap: 0; border: 1px solid #e5e5e5; border-radius: 10px; overflow: hidden; min-height: 720px; }

  .left { background: #f9f9f8; border-right: 1px solid #e5e5e5; padding: 16px; display: flex; flex-direction: column; align-items: center; }
  .left-label { font-size: 10px; letter-spacing: 0.1em; text-transform: uppercase; color: #aaa; margin-bottom: 14px; align-self: flex-start; }
  .body-svg { width: 240px; }
  .organ-btn { cursor: pointer; }
  .organ-btn .hit { opacity: 0; transition: opacity 0.15s; }
  .organ-btn:hover .hit { opacity: 0.2; }
  .organ-btn.active .hit { opacity: 0.3; }

  .right { padding: 20px; overflow-y: auto; }
  .empty { display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100%; color: #ccc; gap: 8px; }
  .empty p { font-size: 12px; }

  .organ-header { display: flex; align-items: center; gap: 14px; margin-bottom: 18px; padding-bottom: 16px; border-bottom: 1px solid #f0f0f0; }
  .organ-illus { width: 72px; height: 72px; flex-shrink: 0; }
  .organ-name { font-size: 18px; font-weight: 600; }
  .organ-sub { font-size: 11px; color: #888; margin-top: 3px; }

  .sec-label { font-size: 10px; letter-spacing: 0.08em; text-transform: uppercase; color: #aaa; margin-bottom: 8px; }

  .legend { display: flex; gap: 12px; margin-bottom: 10px; flex-wrap: wrap; }
  .legend-item { display: flex; align-items: center; gap: 5px; font-size: 11px; color: #666; }
  .legend-dot { width: 10px; height: 10px; border-radius: 2px; flex-shrink: 0; }

  .scale-labels { display: flex; justify-content: space-between; font-size: 10px; color: #bbb; margin-bottom: 4px; font-family: monospace; }
  .bar-row { display: grid; grid-template-columns: 1fr; gap: 3px; margin-bottom: 10px; }
  .bar-label { font-size: 11px; color: #555; white-space: normal; word-break: break-word; }
  .bar-meta { display: grid; grid-template-columns: 1fr 70px; gap: 8px; align-items: center; }
  .bar-track { height: 8px; background: #f0f0f0; border-radius: 4px; position: relative; overflow: visible; }
  .bar-fill-h { position: absolute; top: 0; bottom: 0; border-radius: 4px; background: #16a34a; opacity: 0.7; }
  .bar-fill-p { position: absolute; top: 0; bottom: 0; border-radius: 4px; background: #dc2626; opacity: 0.65; }
  .bar-val { font-size: 10px; color: #888; text-align: right; font-family: monospace; }
  .pline { position: absolute; top: -5px; bottom: -5px; width: 2px; border-radius: 1px; cursor: pointer; }
  .pline:hover { opacity: 1 !important; }
  .axis-note { font-size: 10px; color: #bbb; text-align: right; margin-top: 2px; margin-bottom: 6px; }

  .note { font-size: 11px; color: #888; font-style: italic; margin-top: 8px; }

  /* Reference block */
  .refs { margin-top: 10px; border-top: 1px solid #f0f0f0; padding-top: 8px; }
  .refs-label { font-size: 9px; letter-spacing: 0.08em; text-transform: uppercase; color: #bbb; margin-bottom: 5px; }
  .ref-item { font-size: 10px; color: #999; margin-bottom: 4px; line-height: 1.5; }
  .ref-item strong { color: #666; font-weight: 600; }

  .divider { height: 1px; background: #f0f0f0; margin: 14px 0; }

  .phantom-legend { display: flex; flex-wrap: wrap; gap: 5px 12px; margin-bottom: 10px; }
  .pl-item { display: flex; align-items: center; gap: 4px; font-size: 10px; color: #555; cursor: pointer; padding: 2px 6px; border-radius: 4px; border: 1px solid transparent; font-family: monospace; }
  .pl-item:hover { background: #f5f5f5; border-color: #ddd; }
  .pl-item.sel { background: #eff6ff; border-color: #93c5fd; }
  .pl-swatch { width: 3px; height: 13px; border-radius: 1px; flex-shrink: 0; }

  .phantom-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 7px; }
  .pc { border: 1px solid #e5e5e5; border-radius: 7px; padding: 9px 11px; cursor: pointer; transition: background 0.1s, border-color 0.1s; }
  .pc:hover { background: #f5f5f5; border-color: #d0d0d0; }
  .pc.sel { background: #eff6ff; border-color: #93c5fd; }
  .pc-label { font-size: 11px; font-weight: 600; font-family: monospace; margin-bottom: 2px; }
  .pc-mod { font-size: 10px; color: #888; }
  .pc-stripe { width: 3px; height: 13px; border-radius: 1px; display: inline-block; margin-right: 5px; vertical-align: middle; }

  .recipe { border: 1px solid #bfdbfe; border-radius: 7px; padding: 12px 14px; background: #eff6ff; margin-top: 10px; display: none; }
  .recipe.vis { display: block; }
  .recipe-title { font-size: 10px; letter-spacing: 0.08em; text-transform: uppercase; color: #1d4ed8; margin-bottom: 8px; }
  .rrow { display: flex; justify-content: space-between; padding: 4px 0; border-bottom: 1px solid #bfdbfe; font-size: 12px; }
  .rrow:last-child { border-bottom: none; }
  .rkey { color: #555; }
  .rval { font-family: monospace; font-weight: 600; font-size: 11px; }
  .no-match { font-size: 12px; color: #aaa; grid-column: span 2; padding: 6px 0; }
</style>

<div class="app">
  <div class="left">
    <div class="left-label">Select an organ</div>
    <svg class="body-svg" viewBox="0 0 200 500" xmlns="http://www.w3.org/2000/svg">
      <ellipse cx="100" cy="38" rx="30" ry="34" fill="none" stroke="#ccc" stroke-width="0.8"/>
      <rect x="88" y="68" width="24" height="16" rx="4" fill="none" stroke="#ccc" stroke-width="0.8"/>
      <path d="M52 84 Q42 92 40 120 L36 268 Q36 278 48 280 L152 280 Q164 278 164 268 L160 120 Q158 92 148 84 Z" fill="none" stroke="#ccc" stroke-width="0.8"/>
      <path d="M52 90 Q36 98 30 136 L22 228 Q20 240 28 242 L44 242 Q52 240 50 228 L54 136 Z" fill="none" stroke="#ccc" stroke-width="0.8"/>
      <path d="M148 90 Q164 98 170 136 L178 228 Q180 240 172 242 L156 242 Q148 240 150 228 L146 136 Z" fill="none" stroke="#ccc" stroke-width="0.8"/>
      <path d="M48 280 L44 366 Q42 382 50 384 L78 384 Q86 382 86 366 L88 280 Z" fill="none" stroke="#ccc" stroke-width="0.8"/>
      <path d="M152 280 L156 366 Q158 382 150 384 L122 384 Q114 382 114 366 L112 280 Z" fill="none" stroke="#ccc" stroke-width="0.8"/>
      <ellipse cx="64" cy="390" rx="14" ry="8" fill="none" stroke="#ccc" stroke-width="0.8"/>
      <ellipse cx="136" cy="390" rx="14" ry="8" fill="none" stroke="#ccc" stroke-width="0.8"/>

      <g class="organ-btn" id="btn-brain" data-organ="brain">
        <rect class="hit" x="78" y="8" width="44" height="44" rx="6" fill="#9FE1CB"/>
        <path d="M82 40 Q80 26 88 18 Q96 12 106 14 Q118 16 120 28 Q122 40 114 48 Q106 54 96 52 Q86 50 82 40Z" fill="#9FE1CB" stroke="#1D9E75" stroke-width="0.8"/>
        <path d="M86 32 Q92 26 100 28" fill="none" stroke="#0F6E56" stroke-width="0.6"/>
        <path d="M88 40 Q96 36 104 40" fill="none" stroke="#0F6E56" stroke-width="0.6"/>
        <text x="100" y="66" text-anchor="middle" font-size="7" fill="#aaa">Brain</text>
      </g>
      <!-- Lung buttons -->
      <g class="organ-btn" id="btn-lung" data-organ="lung">
        <rect class="hit" x="56" y="130" width="28" height="44" rx="5" fill="#A8D4E8"/>
        <path d="M60 134 Q58 134 58 148 Q58 166 63 171 Q68 175 76 173 Q82 170 82 158 Q82 146 79 139 Q76 132 68 132 Z" fill="#A8D4E8" stroke="#2E86B0" stroke-width="0.8"/>
        <path d="M63 147 Q68 144 75 147" fill="none" stroke="#1A5E7A" stroke-width="0.5"/>
        <path d="M62 158 Q68 155 76 158" fill="none" stroke="#1A5E7A" stroke-width="0.5"/>
        <rect class="hit" x="136" y="130" width="28" height="44" rx="5" fill="#A8D4E8"/>
        <path d="M140 132 Q132 132 129 139 Q126 146 126 158 Q126 170 132 173 Q140 175 145 171 Q150 166 150 148 Q150 134 148 134 Z" fill="#A8D4E8" stroke="#2E86B0" stroke-width="0.8"/>
        <path d="M133 147 Q140 144 145 147" fill="none" stroke="#1A5E7A" stroke-width="0.5"/>
        <path d="M132 158 Q140 155 146 158" fill="none" stroke="#1A5E7A" stroke-width="0.5"/>
        <text x="100" y="184" text-anchor="middle" font-size="7" fill="#aaa">Lungs</text>
      </g>
      <!-- Breast buttons -->
      <g class="organ-btn" id="btn-breast" data-organ="breast">
        <rect class="hit" x="52" y="110" width="30" height="26" rx="5" fill="#F9C8D8"/>
        <ellipse cx="67" cy="123" rx="13" ry="10" fill="#F9C8D8" stroke="#D4537E" stroke-width="0.8"/>
        <circle cx="67" cy="125" r="2.5" fill="#D4537E" opacity="0.7"/>
        <rect class="hit" x="118" y="110" width="30" height="26" rx="5" fill="#F9C8D8"/>
        <ellipse cx="133" cy="123" rx="13" ry="10" fill="#F9C8D8" stroke="#D4537E" stroke-width="0.8"/>
        <circle cx="133" cy="125" r="2.5" fill="#D4537E" opacity="0.7"/>
        <text x="100" y="144" text-anchor="middle" font-size="7" fill="#aaa">Breast</text>
      </g>
      <g class="organ-btn" id="btn-heart" data-organ="heart">
        <rect class="hit" x="81" y="99" width="38" height="38" rx="6" fill="#F4C0D1"/>
        <path d="M100 133 Q87 123 87 113 Q87 105 93 104 Q98 102 100 107 Q102 102 108 104 Q114 105 114 113 Q114 123 100 133Z" fill="#F4C0D1" stroke="#D4537E" stroke-width="0.8"/>
        <text x="100" y="145" text-anchor="middle" font-size="7" fill="#aaa">Heart</text>
      </g>
      <g class="organ-btn" id="btn-liver" data-organ="liver">
        <rect class="hit" x="48" y="159" width="56" height="30" rx="6" fill="#B5D4F4"/>
        <path d="M52 185 Q52 169 66 167 Q78 165 86 170 Q94 173 98 168 Q106 165 102 179 Q100 189 84 191 Q70 193 60 187Z" fill="#B5D4F4" stroke="#378ADD" stroke-width="0.8"/>
        <text x="72" y="199" text-anchor="middle" font-size="7" fill="#aaa">Liver</text>
      </g>
      <g class="organ-btn" id="btn-stomach" data-organ="stomach">
        <rect class="hit" x="114" y="162" width="34" height="34" rx="6" fill="#FAC775"/>
        <path d="M122 166 Q116 166 116 178 Q116 190 124 192 Q134 194 138 186 Q140 180 138 173 Q136 165 130 165Z" fill="#FAC775" stroke="#BA7517" stroke-width="0.8"/>
        <text x="134" y="202" text-anchor="middle" font-size="7" fill="#aaa">Stomach</text>
      </g>
      <!-- Pancreas button -->
      <g class="organ-btn" id="btn-pancreas" data-organ="pancreas">
        <rect class="hit" x="60" y="196" width="48" height="22" rx="5" fill="#E8C4F5"/>
        <path d="M64 200 Q62 200 62 208 Q62 214 68 216 Q80 218 94 214 Q102 212 104 208 Q104 202 98 200 Q86 198 74 200 Z" fill="#E8C4F5" stroke="#A855C8" stroke-width="0.8"/>
        <path d="M68 208 Q78 206 90 208" fill="none" stroke="#7E22A7" stroke-width="0.5"/>
        <text x="83" y="226" text-anchor="middle" font-size="7" fill="#aaa">Pancreas</text>
      </g>
      <g class="organ-btn" id="btn-kidney" data-organ="kidney">
        <rect class="hit" x="56" y="200" width="26" height="34" rx="6" fill="#CECBF6"/>
        <rect class="hit" x="118" y="200" width="26" height="34" rx="6" fill="#CECBF6"/>
        <path d="M61 205 Q57 205 57 217 Q57 229 61 229 Q69 229 75 223 Q79 217 75 211 Q71 205 61 205Z" fill="#CECBF6" stroke="#7F77DD" stroke-width="0.7"/>
        <path d="M123 205 Q119 205 119 217 Q119 229 123 229 Q131 229 137 223 Q141 217 137 211 Q133 205 123 205Z" fill="#CECBF6" stroke="#7F77DD" stroke-width="0.7"/>
        <text x="100" y="242" text-anchor="middle" font-size="7" fill="#aaa">Kidney</text>
      </g>
      <g class="organ-btn" id="btn-prostate" data-organ="prostate">
        <rect class="hit" x="84" y="244" width="32" height="24" rx="6" fill="#F4C0D1"/>
        <ellipse cx="100" cy="256" rx="13" ry="10" fill="#F4C0D1" stroke="#D4537E" stroke-width="0.8"/>
        <ellipse cx="100" cy="256" rx="4" ry="6" fill="#FBEAF0" stroke="#D4537E" stroke-width="0.5"/>
        <text x="100" y="276" text-anchor="middle" font-size="7" fill="#aaa">Prostate</text>
      </g>
      <g class="organ-btn" id="btn-muscle" data-organ="muscle">
        <rect class="hit" x="20" y="156" width="24" height="44" rx="6" fill="#C0DD97"/>
        <ellipse cx="32" cy="178" rx="9" ry="18" fill="#C0DD97" stroke="#639922" stroke-width="0.8"/>
        <line x1="28" y1="165" x2="28" y2="190" stroke="#3B6D11" stroke-width="0.5" opacity="0.7"/>
        <line x1="32" y1="162" x2="32" y2="193" stroke="#3B6D11" stroke-width="0.5" opacity="0.7"/>
        <line x1="36" y1="165" x2="36" y2="190" stroke="#3B6D11" stroke-width="0.5" opacity="0.7"/>
        <text x="32" y="204" text-anchor="middle" font-size="7" fill="#aaa">Muscle</text>
      </g>
      <g class="organ-btn" id="btn-adipose" data-organ="adipose">
        <rect class="hit" x="138" y="192" width="28" height="36" rx="6" fill="#F5C4B3"/>
        <circle cx="152" cy="204" r="7" fill="#F5C4B3" stroke="#F0997B" stroke-width="0.6"/>
        <circle cx="147" cy="216" r="6" fill="#F5C4B3" stroke="#F0997B" stroke-width="0.6"/>
        <circle cx="158" cy="217" r="5" fill="#FAECE7" stroke="#F0997B" stroke-width="0.6"/>
        <text x="152" y="236" text-anchor="middle" font-size="7" fill="#aaa">Fat</text>
      </g>
    </svg>
  </div>

  <div class="right">
    <div class="empty" id="empty">
      <svg width="40" height="40" viewBox="0 0 40 40"><circle cx="20" cy="20" r="19" fill="none" stroke="#ddd" stroke-width="1"/><path d="M12 20 L18 26 L28 14" fill="none" stroke="#ddd" stroke-width="1.5" stroke-linecap="round"/></svg>
      <p>Click an organ to explore tissue data</p>
      <p style="font-size:11px;color:#ccc">and matching phantom compositions</p>
    </div>
    <div id="panel" style="display:none"></div>
  </div>
</div>

<script>
var SCALE_MAX = 180;

function linPos(val) {
  return (Math.min(val, SCALE_MAX) / SCALE_MAX * 100).toFixed(1);
}
var PHANTOM_COLORS = [
  '#6366f1','#f59e0b','#10b981','#ef4444','#3b82f6',
  '#ec4899','#14b8a6','#f97316','#8b5cf6','#84cc16',
  '#06b6d4','#e11d48','#a16207','#0284c7','#15803d',
  '#7c3aed','#b45309','#0f766e','#be123c'
];

var PHANTOMS = [
  { label:'EF10_100T',  material:'EcoFlex 00-10', thinner:'100%',  modulus:6.19,   sd:0.77 },
  { label:'EF10_87.5T', material:'EcoFlex 00-10', thinner:'87.5%', modulus:8.68,   sd:0.26 },
  { label:'EF10_75T',   material:'EcoFlex 00-10', thinner:'75%',   modulus:9.58,   sd:0.12 },
  { label:'EF10_62.5T', material:'EcoFlex 00-10', thinner:'62.5%', modulus:12.94,  sd:0.52 },
  { label:'EF10_50T',   material:'EcoFlex 00-10', thinner:'50%',   modulus:16.29,  sd:0.40 },
  { label:'EF10_37.5T', material:'EcoFlex 00-10', thinner:'37.5%', modulus:20.14,  sd:0.83 },
  { label:'EF10_25T',   material:'EcoFlex 00-10', thinner:'25%',   modulus:28.16,  sd:0.79 },
  { label:'EF10_12.5T', material:'EcoFlex 00-10', thinner:'12.5%', modulus:38.06,  sd:1.28 },
  { label:'EF10_0T',    material:'EcoFlex 00-10', thinner:'0%',    modulus:56.27,  sd:2.12 },
  { label:'EF30_50T',   material:'EcoFlex 00-30', thinner:'50%',   modulus:31.85,  sd:0.62 },
  { label:'EF30_37.5T', material:'EcoFlex 00-30', thinner:'37.5%', modulus:37.16,  sd:0.72 },
  { label:'EF30_25T',   material:'EcoFlex 00-30', thinner:'25%',   modulus:50.21,  sd:1.50 },
  { label:'EF30_12.5T', material:'EcoFlex 00-30', thinner:'12.5%', modulus:72.58,  sd:2.64 },
  { label:'EF30_0T',    material:'EcoFlex 00-30', thinner:'0%',    modulus:103.46, sd:2.32 },
  { label:'EF50_50T',   material:'EcoFlex 00-50', thinner:'50%',   modulus:59.25,  sd:1.88 },
  { label:'EF50_37.5T', material:'EcoFlex 00-50', thinner:'37.5%', modulus:72.76,  sd:3.07 },
  { label:'EF50_25T',   material:'EcoFlex 00-50', thinner:'25%',   modulus:86.80,  sd:3.93 },
  { label:'EF50_12.5T', material:'EcoFlex 00-50', thinner:'12.5%', modulus:111.86, sd:6.44 },
  { label:'EF50_0T',    material:'EcoFlex 00-50', thinner:'0%',    modulus:158.80, sd:3.01 }
];

var ORGANS = {
  breast: {
    name: 'Breast', sub: 'Parenchymal tissue and masses — MRE and shear-wave elastography, in vivo',
    eMin: 1, eMax: 160,
    rows: [
      { k: 'Normal parenchyma (fatty to fibroglandular) — MRE', v: '1.3 \u2013 3.8 kPa', type: 'h', rMin: 1.3, rMax: 3.8 },
      { k: 'Benign masses (fibroadenoma, fibrosis, fibrocystic) — SWE', v: '22 \u2013 102 kPa', type: 'h', rMin: 22, rMax: 102 },
      { k: 'Malignant masses (DCIS to invasive carcinoma) — SWE', v: '71 \u2013 180 kPa', type: 'p', rMin: 71, rMax: 180 }
    ],
    note: 'Normal parenchyma values (1.3\u20133.8 kPa) are from 3T MRE: fatty 1.3\u20132.4 kPa, fibroglandular 2.2\u20133.8 kPa. Benign and malignant mass values are maximum stiffness (Emax) from shear-wave elastography (SWE) of 1562 masses. Note the overlap between benign and malignant ranges (71\u2013102 kPa), which reflects the biological continuum between tissue types and is consistent with clinical observations.',
    refs: [
      { authors: 'Karakas L & Pocan S.', title: 'Correlation between breast parenchymal stiffness measured by 3T magnetic resonance elastography and CT-derived Hounsfield units', journal: 'Med Sci Monit', year: '2026', detail: 'n=48 women (ages 29\u201356); 3T MRE with 19-cm pneumatic driver at 60 Hz; fatty parenchyma 1.85 \u00b1 0.32 kPa (range 1.30\u20132.44 kPa), fibroglandular 2.95 \u00b1 0.43 kPa (range 2.17\u20133.77 kPa). DOI: 10.12659/MSM.952112' },
      { authors: 'Berg WA et al.', title: 'Quantitative maximum shear wave stiffness of breast masses as a predictor of histopathologic severity', journal: 'AJR', year: '2015', detail: 'n=1562 sonographically visible breast masses from 16 centres; SWE Emax: benign median 43 kPa (IQR 24\u201383), fibroadenoma median 45 kPa (IQR 30\u201379), DCIS median 126 kPa (IQR 71\u2013180), invasive carcinoma median 180 kPa (IQR 138\u2013180). DOI: 10.2214/AJR.14.13448' }
    ]
  },
  lung: {
    name: 'Lung', sub: 'Parenchymal tissue \u2014 healthy and fibrotic (IPF), multiple testing methods',
    eMin: 0.5, eMax: 20,
    rows: [
      { k: 'Normal lung parenchyma (indentation, SAOS, uniaxial, AFM, cavitation)', v: '1.0 \u2013 7.7 kPa', type: 'h', rMin: 1.0, rMax: 7.7 },
      { k: 'Fibrotic lung (IPF) \u2014 AFM (native human)', v: '14.3 \u2013 18.8 kPa', type: 'p', rMin: 14.3, rMax: 18.8 }
    ],
    note: 'The wide healthy range (1.0\u20137.7 kPa) reflects technique dependence rather than true tissue heterogeneity: micro-indentation ~1.4 kPa, SAOS ~3.3 kPa, uniaxial tension ~3.4 kPa, human AFM ~1.96 kPa, and cavitation rheology ~6.1 kPa (highest, due to sensitivity to local microstructural features). IPF fibrotic lung is roughly 8x stiffer than healthy tissue.',
    refs: [
      { authors: 'Polio SR et al.', title: 'Cross-platform mechanical characterization of lung tissue', journal: 'PLoS ONE', year: '2018', detail: 'Porcine lung parenchyma (Yorkshire Cross, 3\u20135 months, n=12 animals); micro-indentation 1.4 \u00b1 0.4 kPa, SAOS 3.3 \u00b1 0.5 kPa, uniaxial tension 3.4 \u00b1 0.4 kPa, cavitation rheology 6.1 \u00b1 1.6 kPa. DOI: 10.1371/journal.pone.0204765' },
      { authors: 'Booth AJ et al.', title: 'Acellular normal and fibrotic human lung matrices as a culture system for in vitro investigation', journal: 'Am J Respir Crit Care Med', year: '2012', detail: 'Human lung AFM (n=2 donors per condition); native normal 1.96 \u00b1 0.13 kPa; native IPF 16.52 \u00b1 2.25 kPa; decellularised normal 1.61 \u00b1 0.08 kPa; decellularised IPF 7.34 \u00b1 0.6 kPa. DOI: 10.1164/rccm.201204-0754OC' }
    ]
  },
  brain: {
    name:'Brain', sub:'Central nervous system \u2014 grey and white matter',
    eMin:1, eMax:20,
    rows:[
      { k:'Grey matter \u2014 indentation',  v:'1.10 \u2013 1.68 kPa', type:'h', rMin:1.10, rMax:1.68 },
      { k:'White matter \u2014 indentation', v:'1.30 \u2013 2.49 kPa', type:'h', rMin:1.30, rMax:2.49 },
      { k:'Grey matter \u2014 MRE (40\u201360 Hz)',  v:'2.24 \u2013 3.33 kPa', type:'h', rMin:2.24, rMax:3.33 },
      { k:'White matter \u2014 MRE (40\u201360 Hz)', v:'3.36 \u2013 3.85 kPa', type:'h', rMin:3.36, rMax:3.85 },
      { k:'Brain \u2014 dynamic compression (30\u201390 /s)', v:'8.83 \u2013 16.0 kPa', type:'h', rMin:8.83, rMax:16.0 }
    ],
    refs:[
      { authors:'Budday S et al.', title:'Mechanical properties of gray and white matter brain tissue by indentation', journal:'J. Mech. Behav. Biomed. Mater.', year:'2015', detail:'White matter 1.895 \u00b1 0.592 kPa, grey matter 1.389 \u00b1 0.289 kPa; bovine brain, flat-punch indentation' },
      { authors:'Huang X et al.', title:'Magnetic resonance elastography of the brain: feasibility and reproducibility', journal:'Magn. Reson. Imaging', year:'2019', detail:'White matter 3.36\u20133.85 kPa; grey matter 2.24\u20133.33 kPa at 40\u201360 Hz in vivo' },
      { authors:'Rashid B et al.', title:'Mechanical characterization of brain tissue in compression at dynamic strain rates', journal:'J. Mech. Behav. Biomed. Mater.', year:'2012', detail:'Compressive nominal stress 8.83\u201316.0 kPa at 30\u201390 s\u207b\u00b9; porcine brain, unconfined compression' }
    ]
  },
  heart: {
    name:'Heart', sub:'Left ventricular myocardium \u2014 passive mechanical properties',
    eMin:1, eMax:20,
    rows:[
      { k:'Left ventricle \u2014 MRE (140 Hz, early systole)', v:'7.2 \u2013 11.8 kPa', type:'h', rMin:7.2, rMax:11.8 }
    ],
    refs:[
      { authors:'Arani A et al.', title:'Cardiac MR elastography for quantitative assessment of elevated myocardial stiffness in cardiac amyloidosis', journal:'J. Magn. Reson. Imaging', year:'2017', detail:'Healthy volunteers (n=11); median 8.2 kPa, range 7.2\u201311.8 kPa; 3D MRE at 140 Hz, early systole, in vivo' }
    ]
  },
  liver: {
    name: 'Liver', sub: 'Parenchymal tissue \u2014 healthy, fibrotic, and neoplastic states',
    eMin: 1, eMax: 80,
    rows: [
      { k: 'Healthy parenchyma \u2014 MRE / transient elastography', v: '2.06 \u2013 5.0 kPa', type: 'h', rMin: 2.06, rMax: 5.0 },
      { k: 'Fibrotic parenchyma \u2014 MRE (F2\u2013F3, in vivo)', v: '2.56 \u2013 4.68 kPa', type: 'p', rMin: 2.56, rMax: 4.68 },
      { k: 'Hepatocellular carcinoma \u2014 transient elastography', v: '20.4 \u2013 75 kPa', type: 'p', rMin: 20.4, rMax: 75 },
      { k: 'Metastatic tumour \u2014 transient elastography', v: '23.6 \u2013 75 kPa', type: 'p', rMin: 23.6, rMax: 75 },
      { k: 'Cholangiocellular carcinoma \u2014 transient elastography', v: '69 \u2013 75 kPa', type: 'p', rMin: 69, rMax: 75 }
    ],
    note: 'Healthy parenchyma lower bound (2.06 kPa) from MRE healthy volunteers (Huwart et al.); upper bound (5.0 kPa) from transient elastography consensus across multiple studies (Masuzaki et al., corroborated by Leal-Ega\u00f1a et al.). The 75 kPa upper limit for tumour rows reflects the FibroScan device ceiling; true CCC stiffness is likely higher as five of six cases reached this ceiling.',
    refs: [
      { authors: 'Huwart L et al.', title: 'Liver fibrosis: non-invasive assessment with MR elastography', journal: 'NMR Biomed.', year: '2006', detail: 'Healthy volunteers (n=5) 2.06 \u00b1 0.26 kPa; F0\u2013F1 2.24 \u00b1 0.23 kPa; F2\u2013F3 2.56 \u00b1 0.24 kPa; cirrhosis 4.68 \u00b1 1.61 kPa; 65 Hz MRE in vivo. Provides healthy lower bound.' },
      { authors: 'Masuzaki R et al.', title: 'Assessing liver tumor stiffness by transient elastography', journal: 'Hepatol. Int.', year: '2007', detail: 'Normal parenchyma 2.5\u20135.0 kPa (stated in discussion); HCC median 55 kPa (range 20.4\u201375 kPa, n=17); CCC median 73.9 kPa (range 69\u201375 kPa, n=6); metastatic tumour median 66.5 kPa (range 23.6\u201375 kPa, n=16); FibroScan transient elastography in vivo. Provides healthy upper bound and tumour ranges.' },
      { authors: 'Leal-Ega\u00f1a A et al.', title: 'Tuning liver stiffness against tumours: an in vitro study using entrapped cells in tumour-like microcapsules', journal: 'J. Mech. Behav. Biomed. Mater.', year: '2012', detail: 'Healthy liver consensus range 1.5\u20135.0 kPa cited from Masuzaki 2007, Yeh 2002, Sandrin 2003; corroborates upper bound. DOI: 10.1016/j.jmbbm.2012.01.013' }
    ]
  },
  stomach: {
    name: 'Stomach', sub: 'Gastric wall \u2014 in situ indentation, fresh human cadaver',
    eMin: 0.5, eMax: 7,
    rows: [
      { k: 'Gastric wall \u2014 in situ indentation (1\u20138 mm depth)', v: '1.08 \u2013 3.01 kPa', type: 'h', rMin: 1.08, rMax: 3.01 }
    ],
    refs: [
      { authors: 'Lim YJ et al.', title: 'In situ measurement and modeling of biomechanical response of human cadaveric soft tissues for physics-based surgical simulation', journal: 'Surg. Endosc.', year: '2009', detail: 'Effective elastic modulus 1.08\u20133.01 kPa across indentation depths of 1\u20138 mm; mean 1.91 kPa; fresh unfrozen human cadavers (n=10), in situ ramp-and-hold indentation, stomach not insufflated' }
    ]
  },
  pancreas: {
    name: 'Pancreas', sub: 'Human pancreatic parenchyma \u2014 ex vivo compression OCE, freshly excised surgical specimens',
    eMin: 50, eMax: 170,
    rows: [
      { k: 'Acinar tissue (healthy parenchyma)', v: '54 \u2013 94 kPa', type: 'h', rMin: 54, rMax: 94 },
      { k: 'Pancreatic fibrotic stroma (chronic pancreatitis / peritumoral)', v: '106 \u2013 166 kPa', type: 'p', rMin: 106, rMax: 166 }
    ],
    note: 'Acinar tissue: 74 \u00b1 20 kPa (mean \u00b1 SD). Pancreatic fibrotic stroma: 136 \u00b1 30 kPa \u2014 localised fibrous connective tissue in chronic pancreatitis and peritumoral regions, distinct from general connective tissue. Measured using compression OCE at standardised stress of 2 \u00b1 1 kPa. POPF prediction cutoff: <84 kPa (AUC 0.94, sensitivity 85%, specificity 95%).',
    refs: [
      { authors: 'Gubarkova E et al.', title: 'Identifying intact and fibrotic parenchyma in pancreatic ductal adenocarcinomas using compression optical coherence elastography', journal: 'Scientific Reports', year: '2026', detail: 'n=35 freshly excised human PDAC specimens from 27 patients (ages 38\u201383); C-OCE at 1.3 \u03bcm wavelength, ~40\u201350 \u03bcm resolution, tangent Young\'s modulus at 2 \u00b1 1 kPa applied stress; validated against H&E and Van Gieson histology. DOI: 10.1038/s41598-026-40746-6' }
    ]
  },
  kidney: {
    name: 'Kidney', sub: 'Renal parenchyma \u2014 in vivo elastography',
    eMin: 1, eMax: 25,
    rows: [
      { k: 'Renal cortex \u2014 MRE (60 Hz, in vivo)', v: '4.12 \u2013 4.35 kPa', type: 'h', rMin: 4.12, rMax: 4.35 },
      { k: 'Renal medulla \u2014 MRE (60 Hz, in vivo)', v: '5.46 kPa', type: 'h', rMin: 5.46, rMax: 5.46 },
      { k: 'Renal sinus \u2014 MRE (60 Hz, in vivo)', v: '6.78 kPa', type: 'h', rMin: 6.78, rMax: 6.78 },
      { k: 'Chronic kidney disease \u2014 shear wave elastography', v: '5.55 \u2013 22.35 kPa', type: 'p', rMin: 5.55, rMax: 22.35 }
    ],
    refs: [
      { authors: 'Bensamoun SF et al.', title: 'Stiffness imaging of the kidney and adjacent abdominal tissues measured simultaneously using magnetic resonance elastography', journal: 'Clin. Imaging', year: '2011', detail: 'Healthy volunteers (n=11); cortex 4.35 \u00b1 0.32 kPa, medulla 5.46 \u00b1 0.48 kPa, renal sinus 6.78 \u00b1 0.10 kPa; whole kidney 4.12 \u00b1 0.24 kPa (axial), 4.32 \u00b1 0.59 kPa (coronal oblique); 60 Hz MRE in vivo' },
      { authors: 'Samir AE et al.', title: 'Shear wave elastography in chronic kidney disease: a pilot experience in native kidneys', journal: 'BMC Nephrol.', year: '2015', detail: 'Healthy controls (n=20) median 4.40 kPa (IQR 3.68\u20135.70); CKD patients (n=25) median 9.40 kPa (IQR 5.55\u201322.35); shear wave elastography in vivo, renal cortex' }
    ]
  },
  prostate: {
    name: 'Prostate', sub: 'Glandular tissue \u2014 ex vivo robotic indentation',
    eMin: 5, eMax: 45,
    rows: [
      { k: 'Normal prostate tissue \u2014 ex vivo indentation', v: '9.82 \u2013 21.40 kPa', type: 'h', rMin: 9.82, rMax: 21.40 },
      { k: 'Prostate cancer \u2014 ex vivo indentation', v: '15.85 \u2013 36.47 kPa', type: 'p', rMin: 15.85, rMax: 36.47 }
    ],
    refs: [
      { authors: 'Ahn B et al.', title: 'Robotic palpation-based mechanical property mapping for diagnosis of prostate cancer', journal: 'J. Endourol.', year: '2011', detail: 'Normal prostate mean 15.25 \u00b1 5.88 kPa (range 9.82\u201321.40 kPa across regions); prostate cancer mean 28.80 \u00b1 11.20 kPa (range 15.85\u201336.47 kPa across regions); ex vivo robotic indentation on 35 radical prostatectomy specimens, 735 sites, Hertz-Sneddon equation' }
    ]
  },
  muscle: {
    name: 'Skeletal muscle', sub: 'Passive relaxed muscle \u2014 in vivo MRE and shear wave elastography',
    eMin: 20, eMax: 60,
    rows: [
      { k: 'Biceps brachii \u2014 passive relaxed (MRE)', v: '49.1 \u2013 53.7 kPa', type: 'h', rMin: 49.1, rMax: 53.7 },
      { k: 'Soleus \u2014 passive relaxed (MRE)', v: '34.5 \u2013 37.5 kPa', type: 'h', rMin: 34.5, rMax: 37.5 },
      { k: 'Gastrocnemius \u2014 passive relaxed (MRE)', v: '22.7 \u2013 29.7 kPa', type: 'h', rMin: 22.7, rMax: 29.7 },
      { k: 'Flexor digitorum profundus \u2014 passive relaxed (MRE)', v: '22.5 \u2013 26.1 kPa', type: 'h', rMin: 22.5, rMax: 26.1 }
    ],
    refs: [
      { authors: 'Uffmann K et al.', title: 'In vivo elasticity measurements of extremity skeletal muscle with MR elastography', journal: 'NMR Biomed.', year: '2004', detail: 'Shear moduli G: biceps brachii 17.9 \u00b1 5.5 kPa, flexor digitorum profundus 8.7 \u00b1 2.8 kPa, soleus 12.5 \u00b1 7.3 kPa, gastrocnemius 9.9 \u00b1 6.8 kPa; in vivo MRE, 12 healthy volunteers, unloaded muscle; Young\'s modulus E \u2248 3G assuming Poisson\'s ratio 0.493' },
      { authors: 'Eby SF et al.', title: 'Shear wave elastography of passive skeletal muscle stiffness: influences of sex and age throughout adulthood', journal: 'Clin. Biomech.', year: '2015', detail: 'Biceps brachii shear modulus G: 5.23 \u00b1 1.86 kPa at 90\u00b0 flexion, 16.13 \u00b1 4.51 kPa at full extension; in vivo SWE, 133 healthy adults aged 21\u201394 years; Young\'s modulus E \u2248 3G assuming Poisson\'s ratio 0.493' }
    ]
  },
  adipose: {
    name:'Adipose tissue', sub:'Subcutaneous and glandular fat',
    eMin:2, eMax:25,
    rows:[
      { k:'Subcutaneous fat (MRE)',   v:'0.5 \u2013 25 kPa', type:'h', rMin:0.5, rMax:25 },
      { k:'Normal fat (compression)', v:'18 \u2013 24 kPa',  type:'h', rMin:18,  rMax:24 }
    ],
    note:'MRE shear modulus spans a very wide range (0.5\u201325 kPa); compression testing gives more consistent values around 18\u201324 kPa.',
    refs:[
      { authors:'van Houten EEW et al.', title:'Initial in vivo experience with steady-state subzone-based MR elastography of the human breast', journal:'J. Magn. Reson. Imaging', year:'2003', detail:'Adipose tissue shear modulus 0.5\u201325 kPa range' },
      { authors:'Krouskop TA et al.', title:'Elastic moduli of breast and prostate tissues under compression', journal:'Ultrason. Imaging', year:'1998', detail:'Normal fat 18 \u00b1 7 kPa (5% precompression), 20 \u00b1 8 kPa (20% precompression)' }
    ]
  }
};

var ILLUS = {
  breast: '<ellipse cx="30" cy="60" rx="26" ry="22" fill="#F9C8D8" stroke="#D4537E" stroke-width="1.2"/><ellipse cx="70" cy="60" rx="26" ry="22" fill="#F9C8D8" stroke="#D4537E" stroke-width="1.2"/><circle cx="30" cy="62" r="4" fill="#D4537E" opacity="0.6"/><circle cx="70" cy="62" r="4" fill="#D4537E" opacity="0.6"/>',
  lung: '<path d="M10 55 Q10 25 22 14 Q34 4 46 8 Q56 12 60 26 Q64 40 58 56 Q52 70 38 74 Q22 76 10 55Z" fill="#A8D4E8" stroke="#2E86B0" stroke-width="1.2"/><path d="M34 8 Q34 74 34 74" fill="none" stroke="#1A5E7A" stroke-width="0.8"/><path d="M14 30 Q24 24 34 28" fill="none" stroke="#1A5E7A" stroke-width="0.9"/><path d="M12 46 Q24 40 34 44" fill="none" stroke="#1A5E7A" stroke-width="0.9"/><path d="M90 55 Q90 25 78 14 Q66 4 54 8 Q44 12 40 26 Q36 40 42 56 Q48 70 62 74 Q78 76 90 55Z" fill="#A8D4E8" stroke="#2E86B0" stroke-width="1.2"/><path d="M66 8 Q66 74 66 74" fill="none" stroke="#1A5E7A" stroke-width="0.8"/><path d="M86 30 Q76 24 66 28" fill="none" stroke="#1A5E7A" stroke-width="0.9"/><path d="M88 46 Q76 40 66 44" fill="none" stroke="#1A5E7A" stroke-width="0.9"/>',
  brain: '<path d="M16 52 Q14 28 28 14 Q42 2 58 6 Q74 10 80 26 Q86 42 78 58 Q70 72 54 78 Q38 82 26 72 Q16 64 16 52Z" fill="#9FE1CB" stroke="#1D9E75" stroke-width="1.2"/><path d="M48 6 Q48 52 48 78" fill="none" stroke="#0F6E56" stroke-width="0.8"/><path d="M22 30 Q34 22 48 26 Q62 22 74 30" fill="none" stroke="#0F6E56" stroke-width="0.9"/><path d="M18 46 Q30 38 48 42 Q66 38 78 46" fill="none" stroke="#0F6E56" stroke-width="0.9"/>',
  heart: '<path d="M50 82 Q20 60 20 36 Q20 18 34 16 Q44 14 50 26 Q56 14 66 16 Q80 18 80 36 Q80 60 50 82Z" fill="#F4C0D1" stroke="#D4537E" stroke-width="1.2"/><line x1="50" y1="26" x2="50" y2="74" stroke="#D4537E" stroke-width="1"/><line x1="24" y1="46" x2="76" y2="46" stroke="#D4537E" stroke-width="1"/>',
  liver: '<path d="M14 55 Q14 24 34 18 Q50 12 62 18 Q76 24 80 36 Q84 48 76 58 Q66 68 44 70 Q24 72 14 55Z" fill="#B5D4F4" stroke="#378ADD" stroke-width="1.2"/><path d="M48 18 Q50 44 50 70" fill="none" stroke="#185FA5" stroke-width="1"/>',
  stomach: '<path d="M30 18 Q18 18 16 34 Q14 52 20 64 Q28 76 42 76 Q56 74 60 60 Q64 46 58 30 Q52 16 42 18Z" fill="#FAC775" stroke="#BA7517" stroke-width="1.2"/><path d="M58 30 Q72 28 74 38 Q76 50 60 60" fill="none" stroke="#BA7517" stroke-width="1.5" stroke-linecap="round"/>',
  pancreas: '<path d="M8 52 Q8 44 18 40 Q32 36 50 38 Q68 36 80 42 Q90 48 88 56 Q86 64 72 66 Q54 68 34 64 Q14 60 8 52Z" fill="#E8C4F5" stroke="#A855C8" stroke-width="1.2"/><path d="M20 52 Q34 48 50 50 Q66 48 78 52" fill="none" stroke="#7E22A7" stroke-width="0.8"/><circle cx="26" cy="52" r="4" fill="#D8A4EF" stroke="#A855C8" stroke-width="0.6"/><circle cx="50" cy="50" r="4" fill="#D8A4EF" stroke="#A855C8" stroke-width="0.6"/><circle cx="72" cy="52" r="3" fill="#D8A4EF" stroke="#A855C8" stroke-width="0.6"/>',
  kidney: '<path d="M24 10 Q10 10 10 50 Q10 88 24 88 Q42 88 56 70 Q66 54 56 32 Q44 10 24 10Z" fill="#CECBF6" stroke="#7F77DD" stroke-width="1.2"/><ellipse cx="30" cy="50" rx="16" ry="28" fill="#AFA9EC" fill-opacity="0.6"/><ellipse cx="30" cy="50" rx="8" ry="16" fill="#EEEDFE" stroke="#7F77DD" stroke-width="0.8"/>',
  prostate: '<ellipse cx="50" cy="50" rx="38" ry="32" fill="#F4C0D1" stroke="#D4537E" stroke-width="1.2"/><ellipse cx="50" cy="50" rx="14" ry="20" fill="#FBEAF0" stroke="#D4537E" stroke-width="0.8"/><ellipse cx="50" cy="50" rx="5" ry="10" fill="#F4C0D1" stroke="#D4537E" stroke-width="0.6"/>',
  muscle: '<ellipse cx="50" cy="50" rx="28" ry="44" fill="#C0DD97" stroke="#639922" stroke-width="1.2"/><line x1="36" y1="16" x2="36" y2="84" stroke="#3B6D11" stroke-width="0.8" opacity="0.8"/><line x1="50" y1="8" x2="50" y2="92" stroke="#3B6D11" stroke-width="0.8" opacity="0.8"/><line x1="64" y1="16" x2="64" y2="84" stroke="#3B6D11" stroke-width="0.8" opacity="0.8"/>',
  adipose: '<circle cx="42" cy="38" r="20" fill="#F5C4B3" stroke="#F0997B" stroke-width="1"/><circle cx="64" cy="32" r="16" fill="#FAECE7" stroke="#F0997B" stroke-width="1"/><circle cx="38" cy="64" r="18" fill="#F5C4B3" stroke="#F0997B" stroke-width="1"/><circle cx="64" cy="60" r="14" fill="#FAECE7" stroke="#F0997B" stroke-width="1"/>'
};

var currentOrgan = null;

function selectOrgan(key) {
  if (currentOrgan) {
    var old = document.getElementById('btn-' + currentOrgan);
    if (old) old.classList.remove('active');
  }
  currentOrgan = key;
  var btn = document.getElementById('btn-' + key);
  if (btn) btn.classList.add('active');

  document.getElementById('empty').style.display = 'none';
  var panel = document.getElementById('panel');
  panel.style.display = 'block';

  var organ = ORGANS[key];
  var matching = PHANTOMS.filter(function(p) { return p.modulus >= organ.eMin && p.modulus <= organ.eMax; });
  var colorMap = {};
  matching.forEach(function(p, i) { colorMap[p.label] = PHANTOM_COLORS[i % PHANTOM_COLORS.length]; });

  var barsHTML = organ.rows.map(function(r) {
    var left  = linPos(r.rMin);
    var right = linPos(r.rMax);
    var width = Math.max(1, (linPos(r.rMax) - linPos(r.rMin))).toFixed(1);
    var fc    = r.type === 'h' ? 'bar-fill-h' : 'bar-fill-p';
    var lines = PHANTOMS.map(function(p) {
      var pos     = linPos(p.modulus);
      var inRange = p.modulus >= organ.eMin && p.modulus <= organ.eMax;
      var color   = inRange ? colorMap[p.label] : '#ccc';
      var opacity = inRange ? '0.85' : '0.28';
      return '<div class="pline" data-phantom="' + p.label + '" style="left:' + pos + '%;background:' + color + ';opacity:' + opacity + '" title="' + p.label + ': ' + p.modulus.toFixed(2) + ' kPa"></div>';
    }).join('');
    return '<div class="bar-row"><div class="bar-label">' + r.k + '</div>' +
      '<div class="bar-meta"><div class="bar-track"><div class="' + fc + '" style="left:' + left + '%;width:' + width + '%"></div>' + lines + '</div>' +
      '<div class="bar-val">' + r.v + '</div></div></div>';
  }).join('');

  var refsHTML = '<div class="refs"><div class="refs-label">Primary sources</div>' +
    organ.refs.map(function(r) {
      return '<div class="ref-item"><strong>' + r.authors + '</strong> (' + r.year + '). ' +
        r.title + '. <em>' + r.journal + '</em>. ' +
        '<span style="color:#bbb">' + r.detail + '</span></div>';
    }).join('') + '</div>';

  var legendHTML = matching.length === 0
    ? '<p class="no-match">No phantoms fall within this stiffness range.</p>'
    : matching.map(function(p) {
        return '<div class="pl-item" data-phantom="' + p.label + '" id="pl-' + p.label + '">' +
          '<div class="pl-swatch" style="background:' + colorMap[p.label] + '"></div>' + p.label + '</div>';
      }).join('');

  var gridHTML = matching.length === 0
    ? '<p class="no-match">No phantoms fall within this range.</p>'
    : matching.map(function(p) {
        return '<div class="pc" data-phantom="' + p.label + '" id="pc-' + p.label + '">' +
          '<div class="pc-label"><span class="pc-stripe" style="background:' + colorMap[p.label] + '"></span>' + p.label + '</div>' +
          '<div class="pc-mod">' + p.modulus.toFixed(2) + ' \u00b1 ' + p.sd + ' kPa</div></div>';
      }).join('');

  panel.innerHTML =
    '<div class="organ-header"><svg class="organ-illus" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">' + (ILLUS[key]||'') + '</svg>' +
    '<div><div class="organ-name">' + organ.name + '</div><div class="organ-sub">' + organ.sub + '</div></div></div>' +
    '<div class="sec-label">Stiffness range (literature)</div>' +
    '<div class="legend"><div class="legend-item"><div class="legend-dot" style="background:#16a34a;opacity:0.75"></div>Healthy</div>' +
    '<div class="legend-item"><div class="legend-dot" style="background:#dc2626;opacity:0.7"></div>Pathological</div>' +
    '<div class="legend-item"><div style="width:3px;height:11px;border-radius:1px;background:#6366f1;opacity:0.85"></div>&nbsp;Phantom</div></div>' +
    '<div class="scale-labels"><span>0 kPa</span><span>60 kPa</span><span>120 kPa</span><span>180 kPa</span></div>' +
    barsHTML +
    '<div class="axis-note">Scale: 0 \u2013 180 kPa</div>' +
    (organ.note ? '<p class="note">' + organ.note + '</p>' : '') +
    refsHTML +
    '<div class="phantom-legend">' + legendHTML + '</div>' +
    '<div class="divider"></div>' +
    '<div class="sec-label">Select a phantom for fabrication recipe</div>' +
    '<div class="phantom-grid">' + gridHTML + '</div>' +
    '<div class="recipe" id="recipe"><div class="recipe-title" id="recipe-title"></div><div id="recipe-rows"></div></div>';

  panel.querySelectorAll('[data-phantom]').forEach(function(el) {
    el.addEventListener('click', function() { selectPhantom(el.getAttribute('data-phantom')); });
  });
}

function selectPhantom(label) {
  document.querySelectorAll('.pc').forEach(function(el) { el.classList.remove('sel'); });
  document.querySelectorAll('.pl-item').forEach(function(el) { el.classList.remove('sel'); });
  var pc = document.getElementById('pc-' + label);
  var pl = document.getElementById('pl-' + label);
  if (pc) pc.classList.add('sel');
  if (pl) pl.classList.add('sel');

  var p = null;
  for (var i = 0; i < PHANTOMS.length; i++) { if (PHANTOMS[i].label === label) { p = PHANTOMS[i]; break; } }
  if (!p) return;

  var rows = [
    ['Silicone family', p.material],
    ['Part A', '50 parts by weight'],
    ['Part B', '50 parts by weight'],
    ['Thinner', p.thinner + ' of total A+B weight'],
    ['Target modulus', p.modulus.toFixed(2) + ' \u00b1 ' + p.sd + ' kPa'],
    ['Mould geometry', '\u00d850 mm \u00d7 30 mm cylinder'],
    ['Cure condition', 'Room temperature']
  ];

  document.getElementById('recipe-title').textContent = 'Fabrication recipe \u2014 ' + label;
  document.getElementById('recipe-rows').innerHTML = rows.map(function(r) {
    return '<div class="rrow"><span class="rkey">' + r[0] + '</span><span class="rval">' + r[1] + '</span></div>';
  }).join('');
  document.getElementById('recipe').classList.add('vis');
  setTimeout(function() {
    var panel = document.getElementById('panel');
    if (panel) panel.scrollTop = 0;
    document.getElementById('recipe').scrollIntoView({ behavior:'smooth', block:'nearest' });
  }, 50);
}

document.querySelectorAll('.organ-btn').forEach(function(btn) {
  btn.addEventListener('click', function() {
    var organ = btn.getAttribute('data-organ');
    if (organ) selectOrgan(organ);
  });
});
</script>
"""

components.html(HTML, height=760, scrolling=True)
