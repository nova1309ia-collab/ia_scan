import streamlit as st
from PIL import Image, ImageEnhance
import io
import numpy as np
import base64
import json
import img2pdf

st.set_page_config(
    page_title="Nova Scan",
    page_icon="📄",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;0,600;1,300&display=swap');

:root{
  --bg:#1e3058;
  --bg2:#243868;
  --bg3:#162544;
  --blue:#5b96ff;
  --blue2:#3a7bff;
  --blue-dim:rgba(91,150,255,.16);
  --blue-glow:rgba(91,150,255,.4);
  --cyan:#38d9f5;
  --green:#2ecc8a;
  --amber:#f5c842;
  --text:#eef2ff;
  --muted:#7a9acc;
  --border:rgba(91,150,255,.2);
  --radius:18px;
  --radius-sm:12px;
}

/* ── Reset & base ── */
*{-webkit-font-smoothing:antialiased}
html,body,[data-testid="stAppViewContainer"],[data-testid="stMain"]{
  background:var(--bg)!important;
  color:var(--text);
  font-family:'DM Sans',sans-serif;
}
/* Fond avec texture subtile */
[data-testid="stAppViewContainer"]::before{
  content:'';
  position:fixed;inset:0;
  background:
    radial-gradient(ellipse 80% 50% at 50% -10%, rgba(91,150,255,.18) 0%, transparent 60%),
    radial-gradient(ellipse 40% 30% at 90% 80%, rgba(56,217,245,.08) 0%, transparent 50%);
  pointer-events:none;z-index:0;
}
[data-testid="stHeader"],[data-testid="stToolbar"],[data-testid="stDecoration"]{display:none!important}
div[data-testid="stTextInput"]{display:none!important}
[data-testid="stFileUploader"]{display:none!important}
.block-container{
  padding:1.5rem 1rem 3rem!important;
  max-width:460px!important;
  position:relative;z-index:1;
}
@media(max-width:460px){.block-container{padding:1rem .7rem 2.5rem!important}}

/* ── Header ── */
.nova-header{
  text-align:center;
  padding:1.2rem 0 .2rem;
  margin-bottom:.2rem;
}
.nova-icon{
  font-size:2.4rem;
  display:block;
  margin-bottom:.3rem;
  filter:drop-shadow(0 0 12px rgba(56,217,245,.5));
  animation:float 3s ease-in-out infinite;
}
@keyframes float{0%,100%{transform:translateY(0)}50%{transform:translateY(-5px)}}
.nova-title{
  font-family:'Syne',sans-serif;
  font-size:2rem;
  font-weight:800;
  background:linear-gradient(120deg,#a8c8ff 0%,#5b96ff 40%,#38d9f5 100%);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
  letter-spacing:4px;
  line-height:1.1;
  filter:drop-shadow(0 2px 12px rgba(91,150,255,.3));
}
.nova-subtitle{
  font-size:.72rem;color:var(--muted);
  letter-spacing:3px;text-transform:uppercase;font-weight:400;
  margin-top:.4rem;margin-bottom:1.8rem;
  font-style:italic;
}
.nova-divider{
  height:1px;
  background:linear-gradient(90deg,transparent,rgba(91,150,255,.4),rgba(56,217,245,.3),transparent);
  margin-bottom:1.6rem;
  border:none;
}

/* ── Bouton téléchargement ── */
[data-testid="stDownloadButton"]>button{
  background:linear-gradient(135deg,#5b96ff 0%,#2563eb 100%)!important;
  color:#fff!important;border:none!important;
  border-radius:var(--radius)!important;
  font-family:'Syne',sans-serif!important;font-weight:700!important;
  font-size:1rem!important;padding:1rem 1.5rem!important;
  width:100%!important;letter-spacing:2px!important;
  box-shadow:0 6px 28px rgba(91,150,255,.45),0 1px 0 rgba(255,255,255,.15) inset!important;
  min-height:58px!important;
  -webkit-tap-highlight-color:transparent!important;
  transition:transform .15s,box-shadow .15s!important;
  position:relative;overflow:hidden;
}
[data-testid="stDownloadButton"]>button::after{
  content:'';position:absolute;inset:0;
  background:linear-gradient(180deg,rgba(255,255,255,.08) 0%,transparent 60%);
  pointer-events:none;
}
[data-testid="stDownloadButton"]>button:active{
  transform:scale(.97)!important;
  box-shadow:0 2px 12px rgba(91,150,255,.3)!important;
}

/* ── Bouton reset ── */
[data-testid="stButton"]>button{
  background:rgba(255,255,255,.04)!important;
  border:1px solid rgba(91,150,255,.25)!important;
  color:var(--muted)!important;border-radius:var(--radius-sm)!important;
  width:100%!important;margin-top:.7rem!important;
  font-family:'DM Sans',sans-serif!important;font-size:.88rem!important;
  min-height:48px!important;letter-spacing:.5px!important;
  -webkit-tap-highlight-color:transparent!important;
  transition:all .15s!important;
}
[data-testid="stButton"]>button:hover{
  border-color:var(--blue)!important;color:#b8d0ff!important;
  background:rgba(91,150,255,.06)!important;
}

/* ── Radio mode rendu ── */
[data-testid="stRadio"]>div{
  display:flex!important;flex-direction:row!important;
  gap:6px!important;flex-wrap:nowrap!important;
}
[data-testid="stRadio"] label{
  flex:1!important;
  background:rgba(91,150,255,.05)!important;
  border:1.5px solid rgba(91,150,255,.18)!important;
  border-radius:var(--radius-sm)!important;
  padding:10px 4px!important;text-align:center!important;
  cursor:pointer!important;font-size:.75rem!important;
  font-weight:600!important;color:var(--muted)!important;
  transition:all .18s!important;min-height:46px!important;
  display:flex!important;align-items:center!important;justify-content:center!important;
  -webkit-tap-highlight-color:transparent!important;
}
[data-testid="stRadio"] label:has(input:checked){
  background:linear-gradient(135deg,rgba(91,150,255,.25),rgba(56,217,245,.12))!important;
  border-color:var(--blue)!important;color:#fff!important;
  box-shadow:0 0 14px rgba(91,150,255,.2)!important;
}
[data-testid="stRadio"] input{display:none!important}

/* ── Steps ── */
.steps-row{
  display:flex;justify-content:center;gap:.35rem;
  margin-bottom:1.2rem;flex-wrap:wrap;
}
.step-badge{
  background:rgba(91,150,255,.07);
  border:1px solid rgba(91,150,255,.18);
  border-radius:30px;padding:5px 14px;
  font-size:.7rem;color:var(--muted);white-space:nowrap;font-weight:500;
}
.step-active{
  background:linear-gradient(135deg,rgba(91,150,255,.28),rgba(56,217,245,.15));
  border-color:var(--blue);color:#fff;font-weight:700;
  box-shadow:0 0 12px rgba(91,150,255,.25);
}

/* ── Card PDF info ── */
.pdf-info{
  background:linear-gradient(135deg,rgba(56,217,245,.05),rgba(91,150,255,.04));
  border:1px solid rgba(56,217,245,.2);
  border-radius:var(--radius);
  padding:1rem 1.2rem;margin:1rem 0;
  font-size:.83rem;line-height:1.8;
}
.pdf-info span{color:var(--cyan);font-weight:600}

/* ── Tip box ── */
.tip-box{
  background:rgba(245,200,66,.05);
  border-left:3px solid var(--amber);
  border-radius:0 var(--radius-sm) var(--radius-sm) 0;
  padding:.75rem 1rem;font-size:.8rem;color:#d4aa2a;margin-bottom:1rem;
}

/* ── Badges ── */
.badge-crop,.badge-manual,.badge-no-crop{
  display:inline-flex;align-items:center;gap:4px;
  border-radius:20px;padding:3px 12px;font-size:.71rem;font-weight:600;margin-left:6px;
}
.badge-crop{background:rgba(46,204,138,.1);border:1px solid var(--green);color:var(--green)}
.badge-manual{background:rgba(91,150,255,.12);border:1px solid var(--blue);color:#9ab8ff}
.badge-no-crop{background:rgba(245,200,66,.1);border:1px solid var(--amber);color:var(--amber)}

/* ── Preview label ── */
.preview-label{
  font-size:.68rem;color:var(--muted);text-align:center;
  margin-bottom:.5rem;letter-spacing:2.5px;text-transform:uppercase;font-weight:500;
  opacity:.8;
}
[data-testid="stImage"]{
  border-radius:var(--radius)!important;overflow:hidden!important;
  box-shadow:0 8px 32px rgba(0,0,0,.25)!important;
}

/* ── Separator ── */
.sep{
  border:none;
  height:1px;
  background:linear-gradient(90deg,transparent,rgba(91,150,255,.25),transparent);
  margin:1.5rem 0;
}

/* ── Spinner ── */
[data-testid="stSpinner"] p{color:var(--muted)!important;font-size:.85rem!important}

/* ── Scrollbar ── */
::-webkit-scrollbar{width:4px}
::-webkit-scrollbar-thumb{background:var(--border);border-radius:4px}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="nova-header">
  <span class="nova-icon">🔍</span>
  <div class="nova-title">NOVA SCAN</div>
  <div class="nova-subtitle">Numérisation instantanée · Zéro installation</div>
</div>
<hr class="nova-divider">
""", unsafe_allow_html=True)

# ── Session state ──────────────────────────────────────────────────────────────
if st.session_state.get("reset_requested"):
    st.session_state["reset_requested"] = False
    st.session_state["scan_key"] = st.session_state.get("scan_key", 0) + 1

if "scan_key" not in st.session_state:
    st.session_state["scan_key"] = 0
sk = st.session_state["scan_key"]


# ── Helpers ───────────────────────────────────────────────────────────────────
def corriger_orientation(img):
    try:
        from PIL import ExifTags
        exif = img._getexif()
        if exif:
            for tag, val in exif.items():
                if ExifTags.TAGS.get(tag) == "Orientation":
                    rotations = {3: 180, 6: 270, 8: 90}
                    if val in rotations:
                        img = img.rotate(rotations[val], expand=True)
                    break
    except Exception:
        pass
    return img

def img_to_b64(img_pil):
    buf = io.BytesIO()
    img_pil.convert("RGB").save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode()

def b64_to_img(s):
    return Image.open(io.BytesIO(base64.b64decode(s)))

def detecter_contour_auto(img_pil):
    try:
        import cv2
        img_np = np.array(img_pil.convert("RGB"))
        h, w = img_np.shape[:2]
        sc = 800 / max(h, w)
        small = cv2.resize(img_np, (int(w * sc), int(h * sc)))
        gray = cv2.cvtColor(small, cv2.COLOR_RGB2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        edges = cv2.Canny(blur, 50, 150)
        edges = cv2.dilate(edges, np.ones((3, 3), np.uint8), iterations=2)
        cnts, _ = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:10]
        for c in cnts:
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.02 * peri, True)
            if len(approx) == 4 and cv2.contourArea(c) > (small.shape[0] * small.shape[1] * 0.2):
                pts = (approx.reshape(4, 2) / sc).astype(np.float32)
                s = pts.sum(axis=1); diff = np.diff(pts, axis=1)
                o = np.zeros((4, 2), dtype=np.float32)
                o[0] = pts[np.argmin(s)]; o[1] = pts[np.argmin(diff)]
                o[2] = pts[np.argmax(s)]; o[3] = pts[np.argmax(diff)]
                return o.tolist()
        return None
    except Exception:
        return None

def recadrer_depuis_coins(img_pil, coins, mode="couleur"):
    import cv2
    img_np = np.array(img_pil.convert("RGB"))
    pts = np.array(coins, dtype=np.float32)
    wA = np.linalg.norm(pts[2] - pts[3]); wB = np.linalg.norm(pts[1] - pts[0])
    hA = np.linalg.norm(pts[1] - pts[2]); hB = np.linalg.norm(pts[0] - pts[3])
    mW = int(max(wA, wB)); mH = int(max(hA, hB))
    if mW < 10 or mH < 10:
        return img_pil
    dst = np.array([[0, 0], [mW - 1, 0], [mW - 1, mH - 1], [0, mH - 1]], dtype=np.float32)
    M = cv2.getPerspectiveTransform(pts, dst)
    warped = cv2.warpPerspective(img_np, M, (mW, mH))
    if mode == "nb":
        gray = cv2.cvtColor(warped, cv2.COLOR_RGB2GRAY)
        clean = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 21, 10)
        return Image.fromarray(clean).convert("RGB")
    elif mode == "gris":
        gray = cv2.cvtColor(warped, cv2.COLOR_RGB2GRAY)
        return ImageEnhance.Contrast(Image.fromarray(gray)).enhance(1.4).convert("RGB")
    else:
        pil_color = Image.fromarray(warped)
        pil_color = ImageEnhance.Contrast(pil_color).enhance(1.2)
        return ImageEnhance.Sharpness(pil_color).enhance(1.3)

def image_vers_pdf(img):
    if img.mode != "RGB":
        img = img.convert("RGB")
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=92, optimize=True)
    pdf_bytes = img2pdf.convert(buf.getvalue())
    return pdf_bytes, img


# ── Canvas interactif ─────────────────────────────────────────────────────────
def canvas_et_relay(img_pil, coins_initiales, relay_key):
    import streamlit.components.v1 as components

    max_dim = 1200
    img_d = img_pil.copy()
    w_o, h_o = img_d.size
    if max(w_o, h_o) > max_dim:
        sc = max_dim / max(w_o, h_o)
        img_d = img_d.resize((int(w_o * sc), int(h_o * sc)), Image.LANCZOS)

    wd, hd = img_d.size
    sx, sy = w_o / wd, h_o / hd

    buf = io.BytesIO()
    img_d.save(buf, format="JPEG", quality=80)
    b64 = base64.b64encode(buf.getvalue()).decode()

    if coins_initiales:
        cd = [[c[0] / sx, c[1] / sy] for c in coins_initiales]
    else:
        mx, my = wd * .08, hd * .08
        cd = [[mx, my], [wd - mx, my], [wd - mx, hd - my], [mx, hd - my]]

    relay_val = st.text_input("_relay_", key=relay_key, label_visibility="collapsed")

    html = f"""<!DOCTYPE html><html><head>
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:#2a3d6b;font-family:'Segoe UI',sans-serif;padding:2px}}
#wrap{{width:100%;max-width:600px;margin:0 auto}}
canvas{{display:block;width:100%;border-radius:12px;touch-action:none;cursor:crosshair}}
.toolbar{{display:flex;gap:8px;margin-top:10px}}
.btn{{flex:1;padding:14px 8px;border-radius:14px;font-size:.95rem;font-weight:700;
      cursor:pointer;border:none;font-family:'Segoe UI',sans-serif;
      -webkit-tap-highlight-color:transparent;transition:transform .1s,opacity .1s}}
.btn:active{{transform:scale(.97);opacity:.85}}
.btn-ok{{background:linear-gradient(135deg,#4d8aff,#1565c0);color:#fff;box-shadow:0 4px 18px rgba(77,138,255,.5)}}
.btn-skip{{background:rgba(255,255,255,.08);border:1px solid rgba(77,138,255,.3)!important;color:#8ba4cc}}
.hint{{text-align:center;font-size:.75rem;color:#6a82a8;margin-top:7px}}
#status{{text-align:center;font-size:.82rem;color:#00e676;margin-top:6px;min-height:1.4em;font-weight:600}}
</style></head><body>
<div id="wrap">
  <canvas id="cv"></canvas>
  <div class="toolbar">
    <button class="btn btn-skip" onclick="doSkip()">⏭ Sans recadrage</button>
    <button class="btn btn-ok"   onclick="doConfirm()">✓ Confirmer</button>
  </div>
  <div class="hint">Glissez les 4 coins 🔵 sur les bords du document</div>
  <div id="status"></div>
</div>
<script>
const IW={wd},IH={hd},SX={sx},SY={sy};
const COINS_INIT={json.dumps(cd)};
const cv=document.getElementById('cv');
const ctx=cv.getContext('2d');
cv.width=IW; cv.height=IH;
const img=new Image(); img.src='data:image/jpeg;base64,{b64}';
let coins=COINS_INIT.map(c=>({{x:c[0],y:c[1]}}));
let drag=null;
const R=Math.max(20,Math.min(IW,IH)*.042);
img.onload=()=>draw();

function draw(){{
  ctx.clearRect(0,0,IW,IH); ctx.drawImage(img,0,0);
  const off=new OffscreenCanvas(IW,IH),oc=off.getContext('2d');
  oc.fillStyle='rgba(0,0,0,.55)'; oc.fillRect(0,0,IW,IH);
  oc.globalCompositeOperation='destination-out';
  oc.beginPath(); oc.moveTo(coins[0].x,coins[0].y);
  coins.forEach((c,i)=>{{if(i)oc.lineTo(c.x,c.y)}}); oc.closePath();
  oc.fillStyle='rgba(0,0,0,1)'; oc.fill();
  ctx.drawImage(off,0,0);
  ctx.beginPath(); ctx.moveTo(coins[0].x,coins[0].y);
  coins.forEach((c,i)=>{{if(i)ctx.lineTo(c.x,c.y)}}); ctx.closePath();
  ctx.strokeStyle='#4d8aff'; ctx.lineWidth=Math.max(2.5,R*.12); ctx.stroke();
  const lbl=['↖','↗','↘','↙'];
  coins.forEach((c,i)=>{{
    ctx.beginPath(); ctx.arc(c.x,c.y,R+6,0,Math.PI*2);
    ctx.fillStyle='rgba(0,0,0,.25)'; ctx.fill();
    ctx.beginPath(); ctx.arc(c.x,c.y,R,0,Math.PI*2);
    ctx.fillStyle=drag===i?'#82b1ff':'#4d8aff'; ctx.fill();
    ctx.strokeStyle='#fff'; ctx.lineWidth=Math.max(2,R*.1); ctx.stroke();
    const s=R*.38;
    ctx.strokeStyle='rgba(255,255,255,.85)'; ctx.lineWidth=Math.max(1.5,R*.08);
    ctx.beginPath(); ctx.moveTo(c.x-s,c.y); ctx.lineTo(c.x+s,c.y); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(c.x,c.y-s); ctx.lineTo(c.x,c.y+s); ctx.stroke();
    ctx.fillStyle='rgba(255,255,255,.7)';
    ctx.font=`bold ${{Math.max(11,R*.45)}}px Segoe UI`;
    ctx.textAlign='center'; ctx.textBaseline='middle';
    ctx.fillText(lbl[i],c.x,c.y);
  }});
}}
function gp(e){{
  const r=cv.getBoundingClientRect(),sx2=IW/r.width,sy2=IH/r.height;
  const s=e.touches?e.touches[0]:e;
  return{{x:Math.max(0,Math.min(IW,(s.clientX-r.left)*sx2)),
          y:Math.max(0,Math.min(IH,(s.clientY-r.top)*sy2))}};
}}
function hit(p){{
  for(let i=0;i<4;i++){{const dx=p.x-coins[i].x,dy=p.y-coins[i].y;if(Math.sqrt(dx*dx+dy*dy)<R*2.2)return i;}}
  return null;
}}
cv.addEventListener('mousedown',e=>{{e.preventDefault();drag=hit(gp(e));draw();}});
cv.addEventListener('touchstart',e=>{{e.preventDefault();drag=hit(gp(e));draw();}},{{passive:false}});
cv.addEventListener('mousemove',e=>{{if(drag===null)return;coins[drag]=gp(e);draw();}});
cv.addEventListener('touchmove',e=>{{e.preventDefault();if(drag===null)return;coins[drag]=gp(e);draw();}},{{passive:false}});
cv.addEventListener('mouseup',()=>{{drag=null;draw();}});
cv.addEventListener('touchend',()=>{{drag=null;draw();}});

function sendRelay(value){{
  document.getElementById('status').textContent='⏳ Traitement en cours...';
  try{{
    const doc=window.parent.document;
    let inp=null;
    for(const el of doc.querySelectorAll('input[type="text"]')){{
      if(el.getAttribute('aria-label')==='_relay_'){{inp=el;break;}}
    }}
    if(!inp){{
      const all=[...doc.querySelectorAll('input[type="text"]')];
      inp=all[all.length-1];
    }}
    if(!inp){{document.getElementById('status').textContent='⚠ Champ introuvable';return;}}
    const setter=Object.getOwnPropertyDescriptor(window.parent.HTMLInputElement.prototype,'value').set;
    setter.call(inp,value);
    inp.dispatchEvent(new Event('input',{{bubbles:true}}));
    inp.dispatchEvent(new KeyboardEvent('keydown',{{key:'Enter',code:'Enter',keyCode:13,which:13,bubbles:true}}));
    inp.dispatchEvent(new KeyboardEvent('keypress',{{key:'Enter',code:'Enter',keyCode:13,which:13,bubbles:true}}));
    inp.dispatchEvent(new KeyboardEvent('keyup',{{key:'Enter',code:'Enter',keyCode:13,which:13,bubbles:true}}));
  }}catch(err){{
    document.getElementById('status').textContent='Erreur: '+err.message;
  }}
}}
function doConfirm(){{
  const result=coins.map(c=>[Math.round(c.x*SX),Math.round(c.y*SY)]);
  sendRelay('CONFIRM:'+JSON.stringify(result));
}}
function doSkip(){{sendRelay('SKIP');}}
</script></body></html>"""

    components.html(html, height=680, scrolling=False)
    return relay_val


# ── Flux image avec rognage ───────────────────────────────────────────────────
def flux_image(img_pil, nom_pdf, prefix):
    sk_local    = st.session_state["scan_key"]
    state_key   = f"state_{prefix}"
    corners_key = f"corners_{prefix}"
    badge_key   = f"badge_{prefix}"
    img_b64_key = f"img_b64_{prefix}"
    nom_key     = f"nom_pdf_{prefix}"
    mode_key    = f"mode_{prefix}"
    relay_key   = f"_relay_{prefix}_{sk_local}"

    if img_b64_key not in st.session_state:
        st.session_state[img_b64_key] = img_to_b64(img_pil)
        st.session_state[nom_key] = nom_pdf

    if state_key not in st.session_state:
        st.session_state[state_key] = "detecting"

    img_pil = b64_to_img(st.session_state[img_b64_key])
    nom_pdf = st.session_state[nom_key]
    state   = st.session_state[state_key]

    # ── DÉTECTION ──
    if state == "detecting":
        with st.spinner("🔍 Détection du document..."):
            coins = detecter_contour_auto(img_pil)
        st.session_state[corners_key] = coins
        st.session_state[badge_key]   = "auto" if coins else "none"
        st.session_state[state_key]   = "canvas"
        st.rerun()

    # ── CANVAS ──
    elif state == "canvas":
        st.markdown('<div class="steps-row">'
                    '<div class="step-badge">① ✓ Photo chargée</div>'
                    '<div class="step-badge step-active">② Ajuster le recadrage</div>'
                    '<div class="step-badge">③ PDF</div>'
                    '</div>', unsafe_allow_html=True)

        coins = st.session_state.get(corners_key)
        if coins:
            st.markdown("""<div style="background:rgba(0,230,118,.07);border:1px solid #00e67644;
                border-radius:10px;padding:.55rem 1rem;font-size:.78rem;color:#00e676;
                margin-bottom:.7rem;text-align:center;">
                ✂️ Document détecté — ajustez les coins si besoin</div>""", unsafe_allow_html=True)
        else:
            st.markdown('<div class="tip-box">💡 Document non détecté. Placez les coins manuellement.</div>',
                        unsafe_allow_html=True)

        st.markdown("<div style='font-size:.78rem;color:#8ba4cc;margin-bottom:.4rem;'>Mode de rendu :</div>",
                    unsafe_allow_html=True)
        mode = st.radio("Mode", ["🎨 Couleur", "🌫️ Niveaux de gris", "📄 Noir & Blanc"],
                        horizontal=True, key=f"mode_radio_{prefix}_{sk_local}",
                        label_visibility="collapsed")
        mode_map = {"🎨 Couleur": "couleur", "🌫️ Niveaux de gris": "gris", "📄 Noir & Blanc": "nb"}
        st.session_state[mode_key] = mode_map[mode]

        relay_val = canvas_et_relay(img_pil, coins, relay_key)

        if relay_val:
            if relay_val.startswith("CONFIRM:"):
                try:
                    corners_js = json.loads(relay_val[8:])
                    st.session_state[corners_key] = corners_js
                    st.session_state[badge_key]   = "manual"
                    st.session_state[state_key]   = "result"
                    st.rerun()
                except Exception as e:
                    st.error(f"Erreur recadrage : {e}")
            elif relay_val == "SKIP":
                st.session_state[badge_key] = "none"
                st.session_state[state_key] = "result"
                st.rerun()

    # ── RÉSULTAT ──
    elif state == "result":
        badge   = st.session_state.get(badge_key, "none")
        corners = st.session_state.get(corners_key)
        mode    = st.session_state.get(mode_key, "couleur")

        if badge == "none" or not corners:
            img_finale = img_pil
        else:
            try:
                img_finale = recadrer_depuis_coins(img_pil, corners, mode)
            except Exception as e:
                img_finale = img_pil
                st.warning(f"Recadrage impossible, image originale utilisée. ({e})")

        # Affichage résultat
        st.markdown('<div class="steps-row">'
                    '<div class="step-badge">① ✓ Photo chargée</div>'
                    '<div class="step-badge">② ✓ Recadrage</div>'
                    '<div class="step-badge step-active">③ Télécharger</div>'
                    '</div>', unsafe_allow_html=True)

        try:
            pdf_bytes, img_rgb = image_vers_pdf(img_finale)
            w, h = img_rgb.size
            ko = len(pdf_bytes) / 1024
            taille = f"{ko/1024:.1f} Mo" if ko >= 1024 else f"{ko:.0f} Ko"

            badges = {
                "auto":   '<span class="badge-crop">✂️ Recadré auto</span>',
                "manual": '<span class="badge-manual">✋ Recadrage manuel</span>',
                "none":   '<span class="badge-no-crop">⚠️ Sans recadrage</span>',
            }
            st.markdown('<div class="preview-label">APERÇU DU DOCUMENT</div>', unsafe_allow_html=True)
            st.image(img_rgb, use_container_width=True)
            st.markdown(f"""<div class="pdf-info">📄 PDF prêt&nbsp;! {badges.get(badge, '')}
                <br>Taille : <span>{taille}</span> &nbsp;|&nbsp; Résolution : <span>{w} × {h} px</span>
                </div>""", unsafe_allow_html=True)
            st.download_button(label="⬇️  TÉLÉCHARGER LE PDF", data=pdf_bytes,
                               file_name=nom_pdf, mime="application/pdf",
                               key=f"dl_{prefix}_{sk_local}")
        except Exception as e:
            st.error(f"Erreur PDF : {e}")

        st.markdown('<hr class="sep">', unsafe_allow_html=True)
        if st.button("🔄  Scanner un autre document", key=f"reset_{prefix}_{sk_local}"):
            st.session_state["reset_requested"] = True
            st.rerun()


# ══ IMPORT ════════════════════════════════════════════════════════════════════
fichier = st.file_uploader(
    label="Choisir une image",
    type=["jpg", "jpeg", "png", "webp", "bmp"],
    label_visibility="collapsed",
    key=f"upload_{sk}",
)
if fichier is None:
    import streamlit.components.v1 as components
    components.html("""<style>
    *{box-sizing:border-box;margin:0;padding:0}
    body{background:transparent;font-family:'Segoe UI',sans-serif}
    .card{
      background:linear-gradient(145deg,rgba(91,150,255,.09),rgba(56,217,245,.04));
      border:1.5px dashed rgba(91,150,255,.4);
      border-radius:20px;padding:2rem 1.2rem 1.5rem;
      margin-bottom:1rem;text-align:center;
      box-shadow:0 4px 24px rgba(0,0,0,.15);
      position:relative;overflow:hidden;
    }
    .card::before{
      content:'';position:absolute;top:-40px;right:-40px;
      width:120px;height:120px;border-radius:50%;
      background:radial-gradient(circle,rgba(56,217,245,.12),transparent 70%);
      pointer-events:none;
    }
    .icon{font-size:3.4rem;display:block;margin-bottom:.7rem;
      animation:float 3s ease-in-out infinite;
      filter:drop-shadow(0 4px 12px rgba(91,150,255,.4));
    }
    @keyframes float{0%,100%{transform:translateY(0)}50%{transform:translateY(-6px)}}
    .title{font-size:1.05rem;font-weight:700;color:#eef2ff;margin-bottom:.8rem;letter-spacing:.3px}
    .formats{display:flex;justify-content:center;gap:.4rem;flex-wrap:wrap;margin-bottom:.8rem}
    .fmt{
      background:rgba(91,150,255,.14);
      border:1px solid rgba(91,150,255,.28);
      border-radius:8px;padding:3px 11px;
      font-size:.7rem;color:#9ab8ff;font-weight:700;letter-spacing:.5px;
    }
    .tips{
      display:flex;flex-direction:column;gap:.3rem;margin-top:.2rem;
    }
    .tip-item{
      font-size:.75rem;color:#6a8ab8;
      display:flex;align-items:center;justify-content:center;gap:.35rem;
    }
    .big-btn{
      display:block;width:100%;
      background:linear-gradient(135deg,#5b96ff 0%,#2563eb 100%);
      color:#fff;border:none;border-radius:18px;
      padding:1.15rem;font-size:1.05rem;font-weight:700;
      cursor:pointer;
      box-shadow:0 6px 28px rgba(91,150,255,.5),0 1px 0 rgba(255,255,255,.15) inset;
      font-family:'Segoe UI',sans-serif;
      -webkit-tap-highlight-color:transparent;
      letter-spacing:.8px;
      transition:transform .12s,box-shadow .12s;
      position:relative;overflow:hidden;
    }
    .big-btn::after{
      content:'';position:absolute;inset:0;
      background:linear-gradient(180deg,rgba(255,255,255,.1) 0%,transparent 60%);
      pointer-events:none;
    }
    .big-btn:active{transform:scale(.97);box-shadow:0 2px 12px rgba(91,150,255,.35)}
    </style>
    <div class="card">
      <span class="icon">🖼️</span>
      <div class="title">Importez votre document</div>
      <div class="formats">
        <span class="fmt">JPG</span>
        <span class="fmt">PNG</span>
        <span class="fmt">WEBP</span>
        <span class="fmt">BMP</span>
      </div>
      <div class="tips">
        <div class="tip-item">💡 Photo nette et bien éclairée</div>
        <div class="tip-item">📐 4 coins du document visibles</div>
        <div class="tip-item">🎨 Fond contrasté recommandé</div>
      </div>
    </div>
    <button class="big-btn" onclick="openFile()">🖼️ &nbsp; Choisir une image</button>
    <script>
    function openFile(){
      try{
        const inp=window.parent.document.querySelector('input[type="file"]');
        if(inp){inp.removeAttribute('capture');inp.setAttribute('accept','image/*');inp.click();return;}
      }catch(e){}
      const inp=document.createElement('input');
      inp.type='file';inp.accept='image/*';inp.click();
    }
    </script>""", height=360, scrolling=False)
else:
    img_imp = corriger_orientation(Image.open(fichier))
    flux_image(img_imp, fichier.name.rsplit(".", 1)[0] + ".pdf", "imp")


# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""<hr class="sep">
<div style="text-align:center;font-size:.68rem;color:#3d5a80;letter-spacing:1px;">
Nova Scan · Traitement 100 % en mémoire · Aucun fichier stocké</div>
""", unsafe_allow_html=True)
