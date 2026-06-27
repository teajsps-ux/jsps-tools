#!/usr/bin/env python3
"""Generate index.html for 八陣圖 poem deck."""
import os

HTML = r'''<!doctype html>
<html lang="zh-Hant">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>八陣圖 - 古詩互動 HTML 簡報</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Bpmf+Iansui&family=Bpmf+Zihi+Kai+Std&display=swap" rel="stylesheet">
  <style>
    :root {
      --ink:#25211d;--paper:rgba(255,253,248,.88);--soft:rgba(255,253,248,.72);
      --line:rgba(55,42,26,.16);--verb:#d85045;--noun:#248067;--person:#2f6fbd;
      --time:#a36600;--place:#6b58b8;--feeling:#c04382;
      --shadow:0 20px 70px rgba(29,24,17,.2);
    }
    *{box-sizing:border-box}
    body{margin:0;overflow:auto;color:var(--ink);font-family:system-ui,"Microsoft JhengHei",sans-serif;background:#f8f4ec}
    body.font-iansui{font-family:"Bpmf Iansui",system-ui,sans-serif}
    body.font-kai{font-family:"Bpmf Zihi Kai Std","Bpmf Iansui",serif}
    button,select{border:0;border-radius:999px;min-height:40px;padding:9px 15px;font:inherit;font-weight:800;color:var(--ink);background:rgba(255,255,255,.8);box-shadow:0 8px 24px rgba(38,29,18,.12);cursor:pointer}
    button:hover,select:hover{background:#fff}
    button.primary{color:white;background:#315f53}
    .deck,.slide{width:100vw;height:100vh;position:relative}
    .slide{position:absolute;inset:0;display:none;overflow-x:hidden;overflow-y:auto;background:white}
    .slide.active{display:block}
    .slide.active .art,.slide.active .shade{position:fixed}
    .art{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
    .shade{position:absolute;inset:0;background:linear-gradient(90deg,rgba(255,255,255,.9),rgba(255,255,255,.58) 48%,rgba(255,255,255,.16)),radial-gradient(circle at 76% 22%,rgba(255,255,255,.24),transparent 42%);pointer-events:none}
    body.clean-view .shade,body.clean-view .stage,body.clean-view .audio-note,body.clean-view dialog{display:none}
    body.clean-view .tools button:not(.view-toggle),body.clean-view .tools select,body.clean-view .pager{display:none}
    .topbar{position:fixed;z-index:30;pointer-events:none}
    .tools,.pager{position:fixed;top:14px;display:flex;align-items:center;gap:7px;padding:7px;border:1px solid rgba(44,35,24,.12);border-radius:999px;background:rgba(255,253,248,.74);backdrop-filter:blur(14px);pointer-events:auto;touch-action:none;cursor:move;user-select:none}
    .tools{right:16px;left:auto}.pager{right:16px;top:auto;bottom:16px}
    .tools button,.tools select,.pager button{cursor:pointer;touch-action:manipulation}
    .drag-handle{width:30px;height:30px;display:grid;place-items:center;border-radius:999px;color:#315f53;background:rgba(255,255,255,.62);font-weight:900;cursor:move}
    .stage{position:relative;z-index:2;min-height:100%;padding:clamp(78px,9vh,106px) clamp(24px,5vw,70px) clamp(56px,7vh,86px);display:grid;align-items:center}
    .home-copy{width:min(980px,94vw);display:grid;gap:18px}
    h1{margin:0;font-size:clamp(42px,7vw,94px);line-height:1.04;letter-spacing:0;color:#2e3832}
    .author{font-size:clamp(22px,2.7vw,36px);font-weight:800;color:#64574a}
    .num-cover{position:absolute;top:18px;right:18px;width:56px;height:56px;border-radius:999px;background:rgba(49,95,83,.88);color:white;font-size:28px;font-weight:900;display:grid;place-items:center;z-index:10}
    .prompt{width:max-content;max-width:min(1120px,94vw);padding:18px 24px;border:1px solid var(--line);border-radius:8px;background:var(--paper);box-shadow:var(--shadow);font-size:clamp(22px,2.5vw,34px);line-height:1.42;font-weight:850}
    .poem-vertical{writing-mode:horizontal-tb;display:flex;flex-direction:row-reverse;align-items:flex-start;gap:clamp(14px,2vw,28px);min-height:420px;font-size:clamp(32px,4.5vw,66px);line-height:1.62;font-weight:850;color:#2c332e}
    .poem-vertical .home-line{writing-mode:vertical-rl;text-orientation:upright;display:inline-block;min-height:7.8em;padding:.18em .12em;border-radius:10px;transition:background .2s,box-shadow .2s,transform .2s}
    .home-line.active-line,.compare-row.active-line{background:rgba(255,236,161,.78);box-shadow:0 0 0 5px rgba(255,236,161,.32);transform:translateY(-2px)}
    .line-stage{grid-template-columns:minmax(260px,.9fr) minmax(320px,1.1fr);gap:clamp(20px,4vw,62px)}
    .line-stage>*{min-width:0}
    .line-poem{display:grid;gap:18px;align-content:center}
    .line-title{font-size:clamp(23px,2.6vw,34px);font-weight:900;color:#66594b}
    .token-line{writing-mode:vertical-rl;text-orientation:upright;display:inline-block;min-height:min(58vh,520px);font-size:clamp(38px,5.4vw,74px);line-height:1.38;font-weight:900}
    .token{writing-mode:vertical-rl;text-orientation:upright;display:inline-block;border-radius:8px;padding:.1em .08em;background:rgba(255,255,255,.58);box-shadow:0 8px 24px rgba(42,31,19,.08)}
    button.token{min-height:0;border-radius:8px;font:inherit;box-shadow:0 8px 24px rgba(42,31,19,.08)}
    .token[data-kind="verb"]{color:var(--verb)}.token[data-kind="noun"]{color:var(--noun)}
    .token[data-kind="person"]{color:var(--person)}.token[data-kind="time"]{color:var(--time)}
    .token[data-kind="place"]{color:var(--place)}.token[data-kind="feeling"]{color:var(--feeling)}
    .plain{width:min(760px,100%);max-width:min(760px,calc(100vw - 48px));padding:20px 28px;border:1px solid var(--line);border-radius:8px;background:var(--paper);box-shadow:var(--shadow);font-size:clamp(22px,2.6vw,34px);line-height:1.45;font-weight:800;overflow-wrap:anywhere;word-break:normal;white-space:normal}
    .legend{display:flex;flex-wrap:wrap;gap:8px;font-size:16px;font-weight:800;color:#53493f}
    .legend span{padding:6px 10px;border-radius:999px;background:rgba(255,255,255,.68)}
    .compare-grid{width:min(1220px,96vw);display:grid;grid-template-columns:minmax(360px,.92fr) minmax(520px,1.2fr);gap:12px 18px;align-items:stretch}
    .compare-head{font-size:clamp(24px,3vw,38px);font-weight:900;padding:8px 18px;justify-self:start;background:rgba(255,255,255,.78)}
    .compare-row{min-height:84px;display:grid;align-items:center;cursor:pointer;border:1px solid var(--line);border-radius:8px;background:var(--paper);box-shadow:0 10px 26px rgba(29,24,17,.08);padding:14px 18px;font-size:clamp(21px,2.4vw,32px);line-height:1.36;font-weight:850;transition:background .2s,box-shadow .2s,transform .2s}
    .poem-row{writing-mode:horizontal-tb;text-orientation:mixed;display:flex;flex-wrap:wrap;gap:8px;min-height:84px}
    .poem-row .token{writing-mode:horizontal-tb;text-orientation:mixed;background:transparent;box-shadow:none;padding:0 .04em;font-size:1em}
    .panel{border:1px solid var(--line);border-radius:8px;background:var(--paper);box-shadow:var(--shadow);padding:clamp(18px,3vw,34px)}
    .panel h2{margin:0 0 14px;font-size:clamp(24px,3vw,38px)}
    .panel p{margin:0;font-size:clamp(21px,2.4vw,31px);line-height:1.55;font-weight:750}
    .home-action-tray{position:fixed;z-index:34;left:14px;bottom:14px;display:flex;align-items:center;gap:8px;padding:8px;border-radius:999px;border:1px solid rgba(44,35,24,.12);background:rgba(255,253,248,.78);backdrop-filter:blur(14px);box-shadow:0 12px 34px rgba(38,29,18,.12)}
    .home-action-tray.hidden{display:none}
    .home-tray-restore{position:fixed;z-index:34;left:14px;bottom:14px;display:none;min-width:54px;height:54px;padding:0 14px;border-radius:999px;background:rgba(255,253,248,.9);color:#315f53;box-shadow:0 12px 34px rgba(38,29,18,.14)}
    .home-tray-restore.visible{display:inline-grid;place-items:center}
    .home-action-tray .round{width:42px;min-width:42px;height:42px;min-height:42px;padding:0;display:grid;place-items:center;font-size:22px}
    .home-action-tray .primary{padding-inline:clamp(16px,2.2vw,28px)}
    body.clean-view .home-action-tray{display:none}
    .game{width:min(1240px,96vw);display:grid;gap:16px}
    .game-head{width:max-content;max-width:100%;padding:16px 24px;border-radius:8px;background:var(--paper);border:1px solid var(--line);box-shadow:var(--shadow);font-size:clamp(24px,3vw,42px);line-height:1.25;font-weight:900}
    .game-rule{width:fit-content;max-width:100%;padding:12px 18px;border-radius:999px;background:rgba(255,253,248,.84);font-size:clamp(18px,2vw,28px);font-weight:850;white-space:normal;overflow-wrap:anywhere}
    .fill-layout{display:grid;grid-template-columns:minmax(360px,1fr) minmax(360px,1fr);gap:18px;align-items:stretch}
    .fill-poem{border:1px solid var(--line);border-radius:8px;background:rgba(255,253,248,.78);padding:18px;display:grid;gap:14px;align-content:start}
    .fill-target{width:max-content;max-width:100%;justify-self:center;padding:14px 24px;border-radius:999px;background:rgba(49,95,83,.92);color:white;font-size:clamp(22px,2.6vw,34px);font-weight:900;white-space:nowrap}
    .fill-line{display:flex;flex-wrap:nowrap;gap:10px;align-items:center;justify-content:center;padding:10px;border-radius:8px;transition:background .2s,box-shadow .2s,transform .2s;font-size:clamp(26px,3.4vw,46px);font-weight:900}
    .fill-line.active-line{background:rgba(255,236,161,.82);box-shadow:0 0 0 5px rgba(255,236,161,.32);transform:translateY(-2px)}
    .fill-slot{min-width:80px;min-height:62px;display:inline-grid;place-items:center;border-radius:8px;border:3px dashed rgba(49,95,83,.38);background:rgba(255,255,255,.64);padding:6px 14px}
    .fill-slot.filled{border-style:solid;color:white;background:#315f53}
    .fill-arena{position:relative;min-height:clamp(380px,56vh,620px);border-radius:8px;border:2px solid rgba(91,127,168,.22);background:rgba(235,244,255,.42);overflow:hidden;container-type:inline-size}
    .arena-title{position:absolute;top:12px;left:50%;transform:translateX(-50%);padding:8px 18px;border-radius:999px;background:rgba(49,95,83,.88);color:white;font-size:clamp(18px,2vw,26px);font-weight:900;white-space:nowrap;z-index:2}
    .progress-bar{display:flex;flex-wrap:wrap;gap:4px;justify-content:center;padding:8px}
    .progress-dot{width:14px;height:14px;border-radius:999px;background:rgba(91,127,168,.28)}
    .progress-dot.reached{background:#315f53}
    .game-timer{font-size:15px;font-weight:700;color:#315f53;text-align:center;min-height:22px;line-height:22px}
    .boat-card,.stone-card{position:absolute;border:0;background:transparent;box-shadow:none;padding:0;cursor:pointer;transition:transform .18s}
    .boat-card:hover,.stone-card:hover{transform:scale(1.06)}
    .boat-card svg,.stone-card svg{width:100%;height:100%;display:block;pointer-events:none}
    .boat-card .boat-label,.stone-card .stone-label{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%) scale(.6);font-size:clamp(26px,3.2vw,38px);font-weight:900;color:#fff;text-shadow:0 1px 4px rgba(0,0,0,.45),0 0 6px rgba(0,0,0,.3);pointer-events:none;opacity:0;transition:opacity .4s ease .18s,transform .5s cubic-bezier(.34,1.4,.64,1) .18s;z-index:1;white-space:nowrap}
    .boat-card.revealed .boat-label,.stone-card.revealed .stone-label{opacity:1;transform:translate(-50%,-50%) scale(1)}
    .boat-card.taken,.stone-card.taken{pointer-events:none;opacity:0}
    .boat-card{width:150px;height:100px;animation:boatFloat var(--speed,6s) ease-in-out infinite alternate}
    @keyframes boatFloat{0%{translate:var(--bx1,0px) var(--by1,-4px)}25%{translate:var(--bx2,8px) var(--by2,6px)}50%{translate:var(--bx3,-10px) var(--by3,-8px)}75%{translate:var(--bx4,6px) var(--by4,4px)}100%{translate:var(--bx5,-4px) var(--by5,-6px)}}
    .stone-card{width:140px;height:110px;animation:stoneFloat var(--speed,5s) ease-in-out infinite alternate}
    @keyframes stoneFloat{0%{translate:var(--sx1,0px) var(--sy1,-3px)}33%{translate:var(--sx2,5px) var(--sy2,3px)}66%{translate:var(--sx3,-3px) var(--sy3,-5px)}100%{translate:var(--sx4,4px) var(--sy4,2px)}}
    .formation-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;padding:18px;border:2px solid rgba(49,95,83,.3);border-radius:12px;background:rgba(255,253,248,.78)}
    .formation-slot{min-height:70px;display:grid;place-items:center;border:3px dashed rgba(49,95,83,.38);border-radius:8px;background:rgba(255,255,255,.64);font-size:clamp(26px,3.4vw,46px);font-weight:900;transition:all .2s}
    .formation-slot.filled{border-style:solid;color:white;background:#315f53}
    .formation-slot.active-target{border-color:#d85045;background:rgba(216,80,69,.15);box-shadow:0 0 0 3px rgba(216,80,69,.3)}
    .word-bank{display:flex;flex-wrap:wrap;gap:10px;justify-content:center;padding:14px;border:1px solid var(--line);border-radius:8px;background:var(--paper)}
    .word-bank button{min-width:70px;min-height:56px;font-size:clamp(24px,3vw,38px);font-weight:900;padding:8px 16px}
    .word-bank button.used{opacity:.3;pointer-events:none}
    .wall-layout{display:grid;grid-template-columns:1fr 1fr;gap:18px;align-items:stretch}
    .wall-fortress{position:relative;min-height:clamp(380px,56vh,620px);border-radius:8px;border:2px solid rgba(100,100,100,.22);background:rgba(200,200,200,.22);overflow:hidden}
    .wall-slot{position:absolute;width:90px;height:70px;display:grid;place-items:center;border:3px dashed rgba(100,100,100,.4);border-radius:8px;background:rgba(255,255,255,.5);font-size:clamp(24px,3vw,36px);font-weight:900;transition:all .2s}
    .wall-slot.filled{border-style:solid;color:white;background:#5a5a5a}
    .wall-slot.active-target{border-color:#d85045;background:rgba(216,80,69,.15);box-shadow:0 0 0 3px rgba(216,80,69,.3)}
    .wall-stone{position:absolute;opacity:.15;pointer-events:none}
    .feedback{min-height:56px;padding:4px 8px;color:#315f53;font-size:clamp(22px,2.6vw,34px);font-weight:900}
    .correct-mark{position:fixed;inset:0;z-index:82;display:grid;place-items:center;pointer-events:none;font-size:clamp(210px,32vw,420px);font-family:Arial,sans-serif;font-weight:900;color:#23a45a;text-shadow:0 0 18px rgba(35,164,90,.9),0 0 46px rgba(35,164,90,.65);animation:markPop .72s ease-out both}
    @keyframes markPop{0%{transform:scale(.55);opacity:0}20%{transform:scale(1.08);opacity:1}70%{transform:scale(1);opacity:1}100%{transform:scale(.92);opacity:0}}
    .confetti{position:fixed;inset:0;z-index:81;pointer-events:none}
    .confetti i{position:absolute;width:12px;height:12px;border-radius:2px;animation:fall 3s linear forwards}
    @keyframes fall{0%{transform:translateY(-20px) rotate(0);opacity:1}100%{transform:translateY(110vh) rotate(540deg);opacity:.4}}
    .audio-note{position:fixed;z-index:31;left:16px;bottom:14px;max-width:min(46px,calc(100vw - 32px));min-height:32px;padding:8px 12px;border-radius:999px;border:1px solid rgba(163,102,0,.2);background:rgba(255,244,218,.9);color:#654400;font-size:15px;font-weight:800;white-space:nowrap;overflow:hidden;cursor:help;opacity:.72;transition:max-width .18s ease,opacity .18s ease,background .18s ease}
    .audio-note::before{content:"音";display:inline-grid;place-items:center;width:22px;height:22px;margin-right:8px;border-radius:999px;background:#fff7df;color:#654400}
    .audio-note:hover,.audio-note:focus{max-width:min(920px,calc(100vw - 32px));opacity:1;background:rgba(255,244,218,.96)}
    .fullscreen-toggle{position:fixed;z-index:31;left:18px;bottom:64px;width:42px;height:42px;min-height:42px;padding:0;display:grid;place-items:center;border-radius:999px;border:1px solid rgba(49,95,83,.18);background:rgba(255,253,248,.9);color:#315f53;font-size:21px;font-weight:900;box-shadow:0 10px 26px rgba(29,24,17,.1)}
    dialog{width:min(560px,90vw);border:0;border-radius:10px;padding:0;background:transparent}
    dialog::backdrop{background:rgba(30,24,17,.28)}
    .pop{padding:24px;border:1px solid rgba(44,35,24,.15);border-radius:10px;background:rgba(255,253,248,.96);box-shadow:var(--shadow)}
    .pop h3{margin:0 0 8px;font-size:34px}
    .pop p{margin:0 0 18px;font-size:24px;line-height:1.42;font-weight:760}
    @media(max-width:980px){body{overflow:auto}.deck,.slide{min-height:100vh;height:auto}.slide{position:relative}.line-stage,.compare-grid,.fill-layout,.wall-layout{grid-template-columns:1fr}.fill-line{flex-wrap:wrap}.stage{min-height:100vh}.topbar{position:fixed}.prompt,.plain{width:auto}}
  </style>
</head>
<body>
  <div class="topbar">
    <div class="tools" data-draggable-control="tools">
      <span class="drag-handle" title="拖曳移動">↕</span>
      <select id="fontSelect" aria-label="字體">
        <option value="normal">一般字體</option>
        <option value="iansui">Bpmf Iansui</option>
        <option value="kai">Bpmf Zihi Kai Std</option>
      </select>
      <button class="view-toggle" onclick="toggleCleanView()">只看底圖</button>
    </div>
    <div class="pager" data-draggable-control="pager">
      <span class="drag-handle" title="拖曳移動">↕</span>
      <button onclick="prevSlide()">←</button>
      <button class="primary" onclick="nextSlide()">→</button>
    </div>
  </div>

  <main class="deck">
    <!-- 首頁 -->
    <section class="slide active" data-auto="home-guide">
      <img class="art" src="generated/bazhentu-home.png" alt="八陣圖首頁插圖">
      <div class="shade"></div>
      <div class="num-cover">6</div>
      <div class="stage">
        <div class="home-copy">
          <h1>八陣圖</h1>
          <div class="author">唐・杜甫</div>
          <div class="prompt">小朋友們，你們聽過諸葛亮嗎？他是三國時代最聰明的軍師！他設計了一個超厲害的陣法，叫做八陣圖。今天我們要來學杜甫寫的這首詩，看看諸葛亮有多厲害，也聽聽他有什麼遺憾。準備好了嗎？讓我們一起來聽！</div>
          <div class="poem-vertical" id="homePoem">
            <span class="home-line" data-line="0"><span class="token" data-kind="verb">功蓋</span><span class="token" data-kind="time">三分</span><span class="token" data-kind="place">國</span></span>
            <span class="home-line" data-line="1"><span class="token" data-kind="feeling">名成</span><span class="token" data-kind="noun">八陣</span><span class="token" data-kind="noun">圖</span></span>
            <span class="home-line" data-line="2"><span class="token" data-kind="place">江流</span><span class="token" data-kind="noun">石</span><span class="token" data-kind="verb">不轉</span></span>
            <span class="home-line" data-line="3"><span class="token" data-kind="feeling">遺恨</span><span class="token" data-kind="verb">失</span><span class="token" data-kind="verb">吞吳</span></span>
          </div>
          <div class="legend">
            <span style="color:var(--verb)">● 動作/狀態</span>
            <span style="color:var(--noun)">● 名詞/事物</span>
            <span style="color:var(--place)">● 地方</span>
            <span style="color:var(--time)">● 時間/數字</span>
            <span style="color:var(--feeling)">● 感受</span>
          </div>
        </div>
      </div>
      <div class="home-action-tray" id="homeActionTray">
        <button class="round" onclick="hideHomeTray()" title="收起">×</button>
        <button class="round" onclick="playSegment('home-guide')" title="聽引導">音</button>
        <button class="primary" onclick="playHomePoem()">帶讀整首詩</button>
        <button onclick="nextSlide()">開始一句一句看</button>
      </div>
      <button class="home-tray-restore" id="homeTrayRestore" onclick="showHomeTray()">朗讀</button>
    </section>

    <!-- 第一句：功蓋三分國 -->
    <section class="slide" data-auto="line1-meaning">
      <img class="art" src="generated/bazhentu-line1.png" alt="功蓋三分國插圖">
      <div class="shade"></div>
      <div class="stage line-stage">
        <div class="line-poem">
          <div class="line-title">第一句</div>
          <div class="token-line">
            <button class="token" data-kind="verb" onclick="showWord(this,'功蓋','功勞最大、最厲害。')">功蓋</button>
            <button class="token" data-kind="time" onclick="showWord(this,'三分','三個國家。')">三分</button>
            <button class="token" data-kind="place" onclick="showWord(this,'國','國家。')">國</button>
          </div>
        </div>
        <div class="plain" id="line1Plain">諸葛亮的功勞蓋過三國時期的所有人。</div>
      </div>
    </section>

    <!-- 第二句：名成八陣圖 -->
    <section class="slide" data-auto="line2-meaning">
      <img class="art" src="generated/bazhentu-line2.png" alt="名成八陣圖插圖">
      <div class="shade"></div>
      <div class="stage line-stage">
        <div class="line-poem">
          <div class="line-title">第二句</div>
          <div class="token-line">
            <button class="token" data-kind="feeling" onclick="showWord(this,'名成','名聲最大、最有名。')">名成</button>
            <button class="token" data-kind="noun" onclick="showWord(this,'八陣','八種陣法。')">八陣</button>
            <button class="token" data-kind="noun" onclick="showWord(this,'圖','陣法的圖形。')">圖</button>
          </div>
        </div>
        <div class="plain" id="line2Plain">他因為設計八陣圖而聞名天下。</div>
      </div>
    </section>

    <!-- 第三句：江流石不轉 -->
    <section class="slide" data-auto="line3-meaning">
      <img class="art" src="generated/bazhentu-line3.png" alt="江流石不轉插圖">
      <div class="shade"></div>
      <div class="stage line-stage">
        <div class="line-poem">
          <div class="line-title">第三句</div>
          <div class="token-line">
            <button class="token" data-kind="place" onclick="showWord(this,'江流','江水一直流。')">江流</button>
            <button class="token" data-kind="noun" onclick="showWord(this,'石','石頭。')">石</button>
            <button class="token" data-kind="verb" onclick="showWord(this,'不轉','不動、不改變。')">不轉</button>
          </div>
        </div>
        <div class="plain" id="line3Plain">江水日夜奔流，但八陣圖的石頭從來不動。</div>
      </div>
    </section>

    <!-- 第四句：遺恨失吞吳 -->
    <section class="slide" data-auto="line4-meaning">
      <img class="art" src="generated/bazhentu-line4.png" alt="遺恨失吞吳插圖">
      <div class="shade"></div>
      <div class="stage line-stage">
        <div class="line-poem">
          <div class="line-title">第四句</div>
          <div class="token-line">
            <button class="token" data-kind="feeling" onclick="showWord(this,'遺恨','很可惜、很遺憾。')">遺恨</button>
            <button class="token" data-kind="verb" onclick="showWord(this,'失','失去、沒能成功。')">失</button>
            <button class="token" data-kind="verb" onclick="showWord(this,'吞吳','打敗吳國。')">吞吳</button>
          </div>
        </div>
        <div class="plain" id="line4Plain">最遺憾的是沒能成功阻止先主去攻打吳國。</div>
      </div>
    </section>

    <!-- 對照頁 -->
    <section class="slide" data-auto="compare-read">
      <img class="art" src="generated/bazhentu-compare.png" alt="對照頁插圖">
      <div class="shade"></div>
      <div class="stage">
        <div class="compare-grid">
          <div class="compare-head">原詩</div>
          <div class="compare-head">白話</div>
          <div class="poem-row compare-row" data-pair="0" onclick="playComparePair(0)">
            <span class="token" data-kind="verb">功蓋</span><span class="token" data-kind="time">三分</span><span class="token" data-kind="place">國</span>
          </div>
          <div class="compare-row plain-row" data-pair="0" onclick="playComparePair(0)">諸葛亮的功勞蓋過三國時期的所有人。</div>
          <div class="poem-row compare-row" data-pair="1" onclick="playComparePair(1)">
            <span class="token" data-kind="feeling">名成</span><span class="token" data-kind="noun">八陣</span><span class="token" data-kind="noun">圖</span>
          </div>
          <div class="compare-row plain-row" data-pair="1" onclick="playComparePair(1)">他因為設計八陣圖而聞名天下。</div>
          <div class="poem-row compare-row" data-pair="2" onclick="playComparePair(2)">
            <span class="token" data-kind="place">江流</span><span class="token" data-kind="noun">石</span><span class="token" data-kind="verb">不轉</span>
          </div>
          <div class="compare-row plain-row" data-pair="2" onclick="playComparePair(2)">江水日夜奔流，但八陣圖的石頭從來不動。</div>
          <div class="poem-row compare-row" data-pair="3" onclick="playComparePair(3)">
            <span class="token" data-kind="feeling">遺恨</span><span class="token" data-kind="verb">失</span><span class="token" data-kind="verb">吞吳</span>
          </div>
          <div class="compare-row plain-row" data-pair="3" onclick="playComparePair(3)">最遺憾的是沒能成功阻止先主去攻打吳國。</div>
        </div>
        <div style="display:flex;gap:10px;margin-top:18px;justify-content:center;flex-wrap:wrap">
          <button onclick="playPoemOnly()">原詩</button>
          <button onclick="playPlainOnly()">白話</button>
          <button class="primary" onclick="playCompareAll()">對照朗讀</button>
        </div>
      </div>
    </section>

    <!-- 背景啟示 -->
    <section class="slide" data-auto="heart-read">
      <img class="art" src="generated/bazhentu-heart.png" alt="背景啟示插圖">
      <div class="shade"></div>
      <div class="stage">
        <div class="panel" style="max-width:min(860px,92vw)">
          <h2>詩人的感受</h2>
          <p>諸葛亮是三國時代最有智慧的人。他發明的八陣圖非常厲害，連江水都沖不走。</p>
          <p style="margin-top:14px">但是，他也有做不到的事——沒能阻止劉備去打吳國。</p>
          <p style="margin-top:14px">這首詩告訴我們，再厲害的人也會有遺憾，所以我們要珍惜每個機會。</p>
        </div>
      </div>
    </section>

    <!-- 遊戲一：排兵布陣版 -->
    <section class="slide" data-auto="game1-guide">
      <img class="art" src="generated/bazhentu-game1.png" alt="排兵布陣版插圖">
      <div class="shade"></div>
      <div class="stage">
        <div class="game">
          <div class="game-head">遊戲一：排兵布陣</div>
          <div class="game-rule">把打亂的字排入正確位置，完成八陣圖！</div>
          <div class="fill-layout">
            <div class="fill-poem" id="formationBuild"></div>
            <div>
              <div class="fill-target" id="formationTarget">下一個要點：____</div>
              <div class="word-bank" id="formationBank"></div>
            </div>
          </div>
          <div class="progress-bar" id="formationProgress"></div>
          <div class="game-timer" id="formationTimer"></div>
          <div class="feedback" id="formationFeedback"></div>
        </div>
      </div>
    </section>

    <!-- 遊戲二：江水流字版 -->
    <section class="slide" data-auto="game2-guide">
      <img class="art" src="generated/bazhentu-game2.png" alt="江水流字版插圖">
      <div class="shade"></div>
      <div class="stage">
        <div class="game">
          <div class="game-head">遊戲二：江水流字</div>
          <div class="game-rule">小船在江上漂流，按順序點擊正確的字！</div>
          <div class="fill-layout">
            <div class="fill-poem" id="boatBuild"></div>
            <div>
              <div class="fill-target" id="boatTarget">下一個要點：____</div>
              <div class="fill-arena" id="boatArena">
                <div class="arena-title">長江區　點船收字</div>
              </div>
            </div>
          </div>
          <div class="progress-bar" id="boatProgress"></div>
          <div class="game-timer" id="boatTimer"></div>
          <div class="feedback" id="boatFeedback"></div>
        </div>
      </div>
    </section>

    <!-- 遊戲三：石壘守城版 -->
    <section class="slide" data-auto="game3-guide">
      <img class="art" src="generated/bazhentu-game3.png" alt="石壘守城版插圖">
      <div class="shade"></div>
      <div class="stage">
        <div class="game">
          <div class="game-head">遊戲三：石壘守城</div>
          <div class="game-rule">點擊石壘找出隱藏的字，補上城牆缺口！</div>
          <div class="fill-layout">
            <div class="fill-poem" id="wallBuild"></div>
            <div>
              <div class="fill-target" id="wallTarget">下一個要點：____</div>
              <div class="fill-arena" id="wallArena">
                <div class="arena-title">石壘區　點石尋字</div>
              </div>
            </div>
          </div>
          <div class="progress-bar" id="wallProgress"></div>
          <div class="game-timer" id="wallTimer"></div>
          <div class="feedback" id="wallFeedback"></div>
        </div>
      </div>
    </section>
  </main>

  <!-- 詞語解釋彈窗 -->
  <dialog id="wordDialog">
    <div class="pop">
      <h3 id="wordTitle">詞語</h3>
      <p id="wordText">解釋</p>
      <button class="primary" onclick="closeWord()">收起</button>
    </div>
  </dialog>

  <!-- 音訊筆記 -->
  <div class="audio-note" id="audioNote">預覽中，音檔待生成</div>
  <button class="fullscreen-toggle" onclick="toggleFullscreen()" title="全螢幕">⛶</button>

  <script>
    /* ===== 幻燈片導航 ===== */
    const slides = document.querySelectorAll('.slide');
    let current = 0;
    function showSlide(n) {
      if (n < 0 || n >= slides.length) return;
      slides[current].classList.remove('active');
      current = n;
      slides[current].classList.add('active');
      const autoAction = slides[current].dataset.auto;
      if (autoAction === 'line1-meaning') playSegment('line1-meaning');
      else if (autoAction === 'line2-meaning') playSegment('line2-meaning');
      else if (autoAction === 'line3-meaning') playSegment('line3-meaning');
      else if (autoAction === 'line4-meaning') playSegment('line4-meaning');
      else if (autoAction === 'game1-guide') { initFormationGame(); playSegment('game1-guide'); }
      else if (autoAction === 'game2-guide') { initBoatGame(); playSegment('game2-guide'); }
      else if (autoAction === 'game3-guide') { initWallGame(); playSegment('game3-guide'); }
      else if (autoAction === 'compare-read') resetTimer('compare');
      else if (autoAction === 'heart-read') playSegment('heart-read');
      resetTimer('formation'); resetTimer('boat'); resetTimer('wall');
    }
    function nextSlide() { showSlide(current + 1); }
    function prevSlide() { showSlide(current - 1); }

    /* ===== 語音系統 ===== */
    let currentAudio = null;
    const poemLines = ['功蓋三分國','名成八陣圖','江流石不轉','遺恨失吞吳'];
    const plainLines = ['諸葛亮的功勞蓋過三國時期的所有人。','他因為設計八陣圖而聞名天下。','江水日夜奔流，但八陣圖的石頭從來不動。','最遺憾的是沒能成功阻止先主去攻打吳國。'];
    const audioFiles = {};
    const poemAudioIds = ['line1-poem','line2-poem','line3-poem','line4-poem'];
    const plainAudioIds = ['line1-plain','line2-plain','line3-plain','line4-plain'];
    const wordAudioIds = {};

    function stopAudio() {
      if (currentAudio) { try { currentAudio.pause(); } catch(e){} currentAudio = null; }
      window.speechSynthesis && window.speechSynthesis.cancel();
    }
    function speak(text) {
      return new Promise(resolve => {
        stopAudio();
        if (!window.speechSynthesis) { resolve(); return; }
        const u = new SpeechSynthesisUtterance(text);
        u.lang = 'zh-TW'; u.rate = 0.85;
        const voices = window.speechSynthesis.getVoices();
        const yating = voices.find(v => v.name.includes('Yating') || v.name.includes('雅婷'));
        if (yating) u.voice = yating;
        u.onend = resolve; u.onerror = resolve;
        window.speechSynthesis.speak(u);
      });
    }
    function playAudioFileOnly(id) {
      const src = audioFiles[id];
      if (!src) return Promise.resolve();
      stopAudio();
      return new Promise(resolve => {
        const audio = new Audio(src);
        currentAudio = audio;
        audio.onended = () => { if (currentAudio === audio) currentAudio = null; resolve(); };
        audio.onerror = () => { if (currentAudio === audio) currentAudio = null; resolve(); };
        audio.play().catch(() => { if (currentAudio === audio) currentAudio = null; resolve(); });
      });
    }
    async function playAudioOrSpeak(id, fallback) {
      if (id && audioFiles[id]) return playAudioFileOnly(id);
      return speak(fallback);
    }
    function playSegment(id) { speak(getSegmentText(id)); }
    function getSegmentText(id) {
      const map = {
        'home-guide': '小朋友們，你們聽過諸葛亮嗎？他是三國時代最聰明的軍師！他設計了一個超厲害的陣法，叫做八陣圖。今天我們要來學杜甫寫的這首詩，看看諸葛亮有多厲害，也聽聽他有什麼遺憾。準備好了嗎？讓我們一起來聽！',
        'line1-meaning': '功蓋三分國。諸葛亮的功勞蓋過三國時期的所有人。',
        'line2-meaning': '名成八陣圖。他因為設計八陣圖而聞名天下。',
        'line3-meaning': '江流石不轉。江水日夜奔流，但八陣圖的石頭從來不動。',
        'line4-meaning': '遺恨失吞吳。最遺憾的是沒能成功阻止先主去攻打吳國。',
        'heart-read': '諸葛亮是三國時代最有智慧的人。他發明的八陣圖非常厲害，連江水都沖不走。但是，他也有做不到的事。這首詩告訴我們，再厲害的人也會有遺憾，所以我們要珍惜每個機會。',
        'game1-guide': '遊戲一：排兵布陣。把打亂的字排入正確位置，完成八陣圖！',
        'game2-guide': '遊戲二：江水流字。小船在江上漂流，按順序點擊正確的字！',
        'game3-guide': '遊戲三：石壘守城。點擊石壘找出隱藏的字，補上城牆缺口！',
      };
      return map[id] || '';
    }
    async function playHomePoem() {
      stopAudio();
      const lines = document.querySelectorAll('#homePoem .home-line');
      for (let i = 0; i < poemLines.length; i++) {
        lines.forEach(l => l.classList.remove('active-line'));
        lines[i].classList.add('active-line');
        await playAudioOrSpeak(poemAudioIds[i], poemLines[i]);
        await delay(450);
      }
      lines.forEach(l => l.classList.remove('active-line'));
    }

    /* ===== 詞語彈窗 ===== */
    function showWord(source, word, meaning) {
      const title = document.getElementById('wordTitle');
      title.textContent = word;
      title.style.color = getComputedStyle(source).color;
      document.getElementById('wordText').textContent = meaning;
      document.getElementById('wordDialog').showModal();
      const id = wordAudioIds[word];
      if (id && audioFiles[id]) playAudioFileOnly(id);
      else speak(word + '。' + meaning);
    }
    function closeWord() { document.getElementById('wordDialog').close(); stopAudio(); }
    document.getElementById('wordDialog').addEventListener('click', function(e) { if (e.target === this) closeWord(); });

    /* ===== 對照朗讀 ===== */
    async function playComparePair(i) {
      stopAudio();
      document.querySelectorAll('.compare-row').forEach(r => r.classList.remove('active-line'));
      document.querySelector(`.poem-row[data-pair="${i}"]`)?.classList.add('active-line');
      document.querySelector(`.plain-row[data-pair="${i}"]`)?.classList.add('active-line');
      await playAudioOrSpeak(poemAudioIds[i], poemLines[i]);
      await delay(450);
      await playAudioOrSpeak(plainAudioIds[i], plainLines[i]);
      document.querySelectorAll('.compare-row').forEach(r => r.classList.remove('active-line'));
    }
    async function playPoemOnly() {
      stopAudio();
      for (let i = 0; i < poemLines.length; i++) {
        document.querySelectorAll('.compare-row').forEach(r => r.classList.remove('active-line'));
        document.querySelector(`.poem-row[data-pair="${i}"]`)?.classList.add('active-line');
        await playAudioOrSpeak(poemAudioIds[i], poemLines[i]);
        await delay(450);
      }
      document.querySelectorAll('.compare-row').forEach(r => r.classList.remove('active-line'));
    }
    async function playPlainOnly() {
      stopAudio();
      for (let i = 0; i < plainLines.length; i++) {
        document.querySelectorAll('.compare-row').forEach(r => r.classList.remove('active-line'));
        document.querySelector(`.plain-row[data-pair="${i}"]`)?.classList.add('active-line');
        await playAudioOrSpeak(plainAudioIds[i], plainLines[i]);
        await delay(450);
      }
      document.querySelectorAll('.compare-row').forEach(r => r.classList.remove('active-line'));
    }
    async function playCompareAll() {
      stopAudio();
      for (let i = 0; i < poemLines.length; i++) {
        document.querySelectorAll('.compare-row').forEach(r => r.classList.remove('active-line'));
        document.querySelector(`.poem-row[data-pair="${i}"]`)?.classList.add('active-line');
        await playAudioOrSpeak(poemAudioIds[i], poemLines[i]);
        await delay(450);
        document.querySelectorAll('.compare-row').forEach(r => r.classList.remove('active-line'));
        document.querySelector(`.plain-row[data-pair="${i}"]`)?.classList.add('active-line');
        await playAudioOrSpeak(plainAudioIds[i], plainLines[i]);
        await delay(450);
      }
      document.querySelectorAll('.compare-row').forEach(r => r.classList.remove('active-line'));
    }

    /* ===== UI 控制 ===== */
    function hideHomeTray() { document.getElementById('homeActionTray')?.classList.add('hidden'); document.getElementById('homeTrayRestore')?.classList.add('visible'); }
    function showHomeTray() { document.getElementById('homeActionTray')?.classList.remove('hidden'); document.getElementById('homeTrayRestore')?.classList.remove('visible'); }
    function toggleCleanView() { document.body.classList.toggle('clean-view'); document.querySelector('.view-toggle').textContent = document.body.classList.contains('clean-view') ? '恢復文字' : '只看底圖'; }
    function setFont(v) { document.body.classList.remove('font-iansui','font-kai'); if (v==='iansui') document.body.classList.add('font-iansui'); if (v==='kai') document.body.classList.add('font-kai'); }
    document.getElementById('fontSelect').addEventListener('change', e => setFont(e.target.value));
    async function toggleFullscreen() { try { if (document.fullscreenElement) await document.exitFullscreen(); else await document.documentElement.requestFullscreen(); } catch(e){} }
    window.addEventListener('keydown', e => { if (e.key==='ArrowRight') nextSlide(); if (e.key==='ArrowLeft') prevSlide(); });

    /* ===== 計時器 ===== */
    const timers = {};
    function startTimer(id) {
      const el = document.getElementById(id+'Timer'); if (!el) return; stopTimer(id);
      timers[id] = { start: Date.now(), el, interval: setInterval(() => { const s=Math.floor((Date.now()-timers[id].start)/1000); el.textContent=`⏱ ${s}秒`; },200) };
      el.textContent='⏱ 0秒';
    }
    function stopTimer(id) { const t=timers[id]; if(!t) return; clearInterval(t.interval); const s=Math.floor((Date.now()-t.start)/1000); t.el.textContent=`⏱ ${s}秒 ✓`; delete timers[id]; }
    function resetTimer(id) { const t=timers[id]; if(t) clearInterval(t.interval); const el=document.getElementById(id+'Timer'); if(el) el.textContent=''; delete timers[id]; }

    /* ===== 共用遊戲函數 ===== */
    function shuffle(items) { return [...items].sort(() => Math.random() - .5); }
    function showCorrectMark() {
      document.querySelectorAll('.correct-mark').forEach(m => m.remove());
      const m = document.createElement('div'); m.className='correct-mark'; m.textContent='○';
      document.body.appendChild(m); window.setTimeout(() => m.remove(), 750);
    }
    function launchConfetti() {
      const box = document.createElement('div'); box.className='confetti';
      const colors=['#d85045','#248067','#2f6fbd','#a36600','#6b58b8','#c04382','#e86a82'];
      for(let i=0;i<80;i++){const p=document.createElement('i');p.style.left=`${Math.random()*100}%`;p.style.background=colors[Math.floor(Math.random()*colors.length)];p.style.animationDelay=`${Math.random()*1.5}s`;p.style.animationDuration=`${2.5+Math.random()*2}s`;box.appendChild(p);}
      document.body.appendChild(box); window.setTimeout(() => box.remove(), 5500);
    }
    function renderProgress(id, current, total) {
      const bar = document.getElementById(id); if (!bar) return; bar.innerHTML='';
      for(let i=0;i<=total;i++){const d=document.createElement('span');d.className='progress-dot'+(i<=current?' reached':'');bar.appendChild(d);}
    }
    function delay(ms) { return new Promise(r => setTimeout(r, ms)); }

    /* ===== 遊戲一：排兵布陣版 ===== */
    const allWords = ['功蓋','三分','國','名成','八陣','圖','江流','石','不轉','遺恨','失','吞吳'];
    let formIndex = 0, formLocked = false;
    function initFormationGame() {
      if (document.getElementById('formationBuild').children.length) return;
      formIndex = 0; formLocked = false;
      resetTimer('formation');
      // 建立陣法格子
      const build = document.getElementById('formationBuild');
      build.innerHTML = '<div class="formation-grid" id="formationGrid"></div>';
      const grid = document.getElementById('formationGrid');
      allWords.forEach((w, i) => {
        const slot = document.createElement('div');
        slot.className = 'formation-slot';
        slot.dataset.idx = i;
        slot.dataset.word = w;
        grid.appendChild(slot);
      });
      renderProgress('formationProgress', 0, allWords.length);
      spawnFormationWords();
    }
    function spawnFormationWords() {
      const bank = document.getElementById('formationBank');
      bank.innerHTML = '';
      if (formIndex >= allWords.length) {
        document.getElementById('formationTarget').textContent = '整首詩完成';
        document.getElementById('formationFeedback').textContent = '○ 全部完成！';
        launchConfetti(); return;
      }
      const target = allWords[formIndex];
      document.getElementById('formationTarget').textContent = `下一個要點：${target}`;
      const pool = shuffle([target, ...allWords.filter(w => w !== target).slice(0, 11)]);
      pool.forEach(w => {
        const btn = document.createElement('button');
        btn.textContent = w;
        btn.onclick = () => tryFormationWord(w, btn);
        bank.appendChild(btn);
      });
      // 高亮目標格子
      document.querySelectorAll('.formation-slot').forEach(s => {
        s.classList.toggle('active-target', parseInt(s.dataset.idx) === formIndex);
      });
    }
    function tryFormationWord(word, btn) {
      if (formLocked) return;
      const target = allWords[formIndex];
      const fb = document.getElementById('formationFeedback');
      if (word !== target) {
        formLocked = true;
        fb.textContent = '再想想，換一個試試。';
        speak('再想想，換一個試試。').then(() => { formLocked = false; });
        return;
      }
      formLocked = false;
      showCorrectMark();
      if (formIndex === 0) startTimer('formation');
      if (formIndex === allWords.length - 1) stopTimer('formation');
      btn.classList.add('used');
      const slot = document.querySelector(`.formation-slot[data-idx="${formIndex}"]`);
      if (slot) { slot.textContent = word; slot.classList.add('filled'); slot.classList.remove('active-target'); }
      formIndex++;
      renderProgress('formationProgress', formIndex, allWords.length);
      spawnFormationWords();
    }

    /* ===== 遊戲二：江水流字版 ===== */
    let boatIndex = 0, boatLocked = false;
    function initBoatGame() {
      if (document.getElementById('boatBuild').children.length) return;
      boatIndex = 0; boatLocked = false;
      resetTimer('boat');
      let slotIdx = 0;
      document.getElementById('boatBuild').innerHTML = [
        {words:['功蓋','三分','國']},
        {words:['名成','八陣','圖']},
        {words:['江流','石','不轉']},
        {words:['遺恨','失','吞吳']}
      ].map((line, li) => {
        const slots = line.words.map(() => `<span class="fill-slot" data-boat-slot="${slotIdx++}"></span>`).join('');
        return `<div class="fill-line" data-line-index="${li}">${slots}</div>`;
      }).join('');
      renderProgress('boatProgress', 0, allWords.length);
      spawnBoats();
    }
    function spawnBoats() {
      const arena = document.getElementById('boatArena');
      arena.innerHTML = '<div class="arena-title">長江區　點船收字</div>';
      if (boatIndex >= allWords.length) {
        document.getElementById('boatTarget').textContent = '整首詩完成';
        document.getElementById('boatFeedback').textContent = '○ 全部完成！';
        readAllFillLines('boatBuild'); launchConfetti(); return;
      }
      const target = allWords[boatIndex];
      document.getElementById('boatTarget').textContent = `下一個要點：${target}`;
      const pool = shuffle([target, ...allWords.filter(w => w !== target)].slice(0, 6));
      const lanes = [8, 22, 36, 50, 64, 78];
      const lanePool = shuffle([...lanes]);
      pool.forEach((word, i) => {
        const btn = document.createElement('button');
        btn.className = 'boat-card';
        btn.innerHTML = boatSvg() + `<span class="boat-label">${word}</span>`;
        btn.style.left = `${lanePool[i % lanes.length]}%`;
        btn.style.top = '15%';
        const speed = 5 + Math.random() * 6;
        btn.style.setProperty('--speed', `${speed}s`);
        btn.style.setProperty('--bx1', `${(Math.random()-.5)*40}px`);
        btn.style.setProperty('--by1', `${-4-Math.random()*8}px`);
        btn.style.setProperty('--bx2', `${8+Math.random()*16}px`);
        btn.style.setProperty('--by2', `${4+Math.random()*10}px`);
        btn.style.setProperty('--bx3', `${-8-Math.random()*14}px`);
        btn.style.setProperty('--by3', `${-6-Math.random()*8}px`);
        btn.style.setProperty('--bx4', `${6+Math.random()*12}px`);
        btn.style.setProperty('--by4', `${4+Math.random()*8}px`);
        btn.style.setProperty('--bx5', `${(Math.random()-.5)*30}px`);
        btn.style.setProperty('--by5', `${-4-Math.random()*6}px`);
        btn.style.animationDelay = `${-Math.random()*speed*0.3}s`;
        btn.onclick = () => tryBoatWord(word, btn);
        arena.appendChild(btn);
      });
    }
    function tryBoatWord(word, boat) {
      if (boatLocked || boat.classList.contains('taken')) return;
      const target = allWords[boatIndex];
      const fb = document.getElementById('boatFeedback');
      boatLocked = true;
      boat.classList.add('revealed');
      setTimeout(() => {
        boatLocked = false;
        if (word === target) {
          if (boatIndex === 0) startTimer('boat');
          if (boatIndex === allWords.length - 1) stopTimer('boat');
          fb.textContent = `○ 找到「${word}」了！`;
          showCorrectMark();
          setTimeout(() => {
            boat.classList.add('taken');
            const slot = document.querySelector(`#boatBuild .fill-slot[data-boat-slot="${boatIndex}"]`);
            if (slot) { slot.textContent = word; slot.classList.add('filled'); }
            boatIndex++;
            renderProgress('boatProgress', boatIndex, allWords.length);
            const completedLine = boatLineEnds.find(l => l.end === boatIndex);
            if (completedLine) setTimeout(async () => { await readCompletedFillLine(completedLine, 'boatBuild'); spawnBoats(); }, 260);
            else spawnBoats();
          }, 360);
        } else {
          fb.textContent = `這是「${word}」，再找「${target}」。`;
          boat.classList.remove('revealed');
        }
      }, 720);
    }

    /* ===== 遊戲三：石壘守城版 ===== */
    let wallIndex = 0, wallLocked = false;
    function initWallGame() {
      if (document.getElementById('wallBuild').children.length) return;
      wallIndex = 0; wallLocked = false;
      resetTimer('wall');
      let slotIdx = 0;
      document.getElementById('wallBuild').innerHTML = [
        {words:['功蓋','三分','國']},
        {words:['名成','八陣','圖']},
        {words:['江流','石','不轉']},
        {words:['遺恨','失','吞吳']}
      ].map((line, li) => {
        const slots = line.words.map(() => `<span class="fill-slot" data-wall-slot="${slotIdx++}"></span>`).join('');
        return `<div class="fill-line" data-line-index="${li}">${slots}</div>`;
      }).join('');
      renderProgress('wallProgress', 0, allWords.length);
      spawnStones();
    }
    function spawnStones() {
      const arena = document.getElementById('wallArena');
      arena.innerHTML = '<div class="arena-title">石壘區　點石尋字</div>';
      arena.style.background = 'linear-gradient(180deg, #2a2a2a 0%, #3a3a3a 40%, #4a4a4a 80%, #2a2a2a 100%)';
      if (wallIndex >= allWords.length) {
        document.getElementById('wallTarget').textContent = '整首詩完成';
        document.getElementById('wallFeedback').textContent = '○ 全部完成！';
        readAllFillLines('wallBuild'); launchConfetti(); return;
      }
      const target = allWords[wallIndex];
      document.getElementById('wallTarget').textContent = `下一個要點：${target}`;
      const pool = shuffle([target, ...allWords.filter(w => w !== target)].slice(0, 6));
      const positions = generatePositions(7, 18);
      pool.forEach((word, i) => {
        const btn = document.createElement('button');
        btn.className = 'stone-card';
        btn.dataset.word = word;
        btn.innerHTML = stoneSvg() + `<span class="stone-label">${word}</span>`;
        const pos = positions[i % positions.length];
        btn.style.left = `${pos.x}%`;
        btn.style.top = `${pos.y}%`;
        const speed = 4 + Math.random() * 4;
        btn.style.setProperty('--speed', `${speed}s`);
        btn.style.setProperty('--sx1', `${(Math.random()-.5)*16}px`);
        btn.style.setProperty('--sy1', `${-3-Math.random()*6}px`);
        btn.style.setProperty('--sx2', `${4+Math.random()*8}px`);
        btn.style.setProperty('--sy2', `${3+Math.random()*6}px`);
        btn.style.setProperty('--sx3', `${-3-Math.random()*6}px`);
        btn.style.setProperty('--sy3', `${-4-Math.random()*5}px`);
        btn.style.setProperty('--sx4', `${3+Math.random()*6}px`);
        btn.style.setProperty('--sy4', `${2+Math.random()*5}px`);
        btn.style.animationDelay = `${-Math.random()*speed*0.6}s`;
        btn.onclick = () => tryWallWord(word, btn);
        arena.appendChild(btn);
      });
    }
    function tryWallWord(word, stone) {
      if (wallLocked || stone.classList.contains('revealed') || stone.classList.contains('taken')) return;
      const target = allWords[wallIndex];
      const fb = document.getElementById('wallFeedback');
      wallLocked = true;
      stone.classList.add('revealed');
      const pop = document.createElement('span');
      pop.className = 'stone-pop'; pop.innerHTML = stonePopSvg();
      stone.appendChild(pop);
      setTimeout(() => pop.remove(), 850);
      setTimeout(() => {
        wallLocked = false;
        if (word === target) {
          if (wallIndex === 0) startTimer('wall');
          if (wallIndex === allWords.length - 1) stopTimer('wall');
          fb.textContent = `○ 找到「${word}」了！`;
          showCorrectMark();
          setTimeout(() => {
            stone.classList.add('taken');
            const slot = document.querySelector(`#wallBuild .fill-slot[data-wall-slot="${wallIndex}"]`);
            if (slot) { slot.textContent = word; slot.classList.add('filled'); }
            wallIndex++;
            renderProgress('wallProgress', wallIndex, allWords.length);
            const completedLine = wallLineEnds.find(l => l.end === wallIndex);
            if (completedLine) setTimeout(async () => { await readCompletedFillLine(completedLine, 'wallBuild'); spawnStones(); }, 260);
            else spawnStones();
          }, 360);
        } else {
          fb.textContent = `這是「${word}」，再找「${target}」。`;
          stone.classList.remove('revealed');
        }
      }, 820);
    }

    /* ===== 填字遊戲共用 ===== */
    const fillLines = [
      { text: '功蓋三分國', words: ['功蓋','三分','國'] },
      { text: '名成八陣圖', words: ['名成','八陣','圖'] },
      { text: '江流石不轉', words: ['江流','石','不轉'] },
      { text: '遺恨失吞吳', words: ['遺恨','失','吞吳'] }
    ];
    const allFillWords = fillLines.flatMap(l => l.words);
    const boatLineEnds = [], wallLineEnds = [];
    let acc = 0;
    fillLines.forEach(l => { acc += l.words.length; boatLineEnds.push({ end: acc, text: l.text }); wallLineEnds.push({ end: acc, text: l.text }); });
    function generatePositions(count, minDist) {
      const positions = [];
      for (let attempt = 0; attempt < 200 && positions.length < count; attempt++) {
        const x = 4 + Math.random() * 76;
        const y = 8 + Math.random() * 65;
        const ok = positions.every(p => Math.hypot(p.x - x, p.y - y) >= minDist);
        if (ok) positions.push({x, y});
      }
      while (positions.length < count) positions.push({x: 4+Math.random()*76, y: 8+Math.random()*65});
      return shuffle(positions);
    }
    async function readCompletedFillLine(completedLine, buildId) {
      const lineIndex = boatLineEnds.indexOf(completedLine);
      const row = document.querySelector(`#${buildId} .fill-line[data-line-index="${lineIndex}"]`);
      document.querySelectorAll(`#${buildId} .fill-line`).forEach(l => l.classList.remove('active-line'));
      row?.classList.add('active-line');
      await playAudioOrSpeak(poemAudioIds[lineIndex], completedLine.text);
      row?.classList.remove('active-line');
    }
    async function readAllFillLines(buildId) {
      document.querySelectorAll(`#${buildId} .fill-line`).forEach(l => l.classList.remove('active-line'));
      await delay(300);
      for (let i = 0; i < fillLines.length; i++) {
        const row = document.querySelector(`#${buildId} .fill-line[data-line-index="${i}"]`);
        row?.classList.add('active-line');
        await playAudioOrSpeak(poemAudioIds[i], fillLines[i].text);
        await delay(350);
        row?.classList.remove('active-line');
      }
    }

    /* ===== SVG 素材 ===== */
    function boatSvg() {
      const gid = 'bg' + Math.random().toString(36).slice(2,7);
      return `<svg viewBox="0 0 150 100" xmlns="http://www.w3.org/2000/svg">
        <defs><linearGradient id="${gid}" x1="0%" y1="100%" x2="100%" y2="0%">
          <stop offset="0%" stop-color="#5a3d28"/><stop offset="100%" stop-color="#8b6f3c"/>
        </linearGradient></defs>
        <g transform="translate(75,50)">
          <path d="M-40,10 Q-30,20 0,22 Q30,20 40,10 Q30,16 0,18 Q-30,16 -40,10 Z" fill="#5a3d28"/>
          <path d="M-35,8 Q-25,16 0,18 Q25,16 35,8 Q25,14 0,16 Q-25,14 -35,8 Z" fill="url(#${gid})"/>
          <line x1="0" y1="-30" x2="0" y2="10" stroke="#5a3d28" stroke-width="2"/>
          <path d="M2,-28 Q20,-20 2,-8" fill="none" stroke="#8b6f3c" stroke-width="1.5"/>
          <path d="M0,-28 L24,-18 L0,-8 Z" fill="rgba(200,180,140,.6)" stroke="#8b6f3c" stroke-width=".8"/>
        </g>
      </svg>`;
    }
    function stoneSvg() {
      const gid = 'st' + Math.random().toString(36).slice(2,7);
      return `<svg viewBox="0 0 140 110" xmlns="http://www.w3.org/2000/svg">
        <defs><radialGradient id="${gid}" cx="50%" cy="40%" r="55%">
          <stop offset="0%" stop-color="#e8e0d0"/><stop offset="50%" stop-color="#a09478"/><stop offset="100%" stop-color="#7a7058"/>
        </radialGradient></defs>
        <g transform="translate(70,55)">
          <ellipse cx="0" cy="8" rx="36" ry="12" fill="rgba(0,0,0,.15)"/>
          <path d="M-34,4 Q-36,-6 -20,-18 Q-4,-28 10,-24 Q28,-20 34,-6 Q36,6 28,14 Q16,22 2,20 Q-14,18 -28,14 Q-34,10 -34,4 Z" fill="url(#${gid})" stroke="#8a7e64" stroke-width="1"/>
          <path d="M-18,-6 Q-8,-14 6,-12 Q16,-10 20,-2 Q16,-4 6,-6 Q-6,-8 -18,-6 Z" fill="rgba(255,255,255,.12)"/>
        </g>
      </svg>`;
    }
    function stonePopSvg() {
      return `<svg viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg">
        <circle cx="40" cy="40" r="28" fill="#d4e8ff" opacity=".4"/>
        <circle cx="40" cy="40" r="18" fill="#c8dff0" opacity=".3"/>
        <circle cx="40" cy="40" r="8" fill="#ffffff" opacity=".25"/>
      </svg>`;
    }

    /* ===== 拖曳控制項 ===== */
    (function() {
      document.querySelectorAll('[data-draggable-control]').forEach(control => {
        let dragging = false, offsetX = 0, offsetY = 0;
        control.addEventListener('pointerdown', e => {
          if (e.target.closest('button, select, option')) return;
          dragging = true;
          const rect = control.getBoundingClientRect();
          offsetX = e.clientX - rect.left; offsetY = e.clientY - rect.top;
          control.setPointerCapture(e.pointerId);
        });
        control.addEventListener('pointermove', e => {
          if (!dragging) return;
          const maxX = window.innerWidth - control.offsetWidth - 8;
          const maxY = window.innerHeight - control.offsetHeight - 8;
          const x = Math.max(8, Math.min(maxX, e.clientX - offsetX));
          const y = Math.max(8, Math.min(maxY, e.clientY - offsetY));
          control.style.left = `${x}px`; control.style.top = `${y}px`; control.style.right = 'auto';
        });
        control.addEventListener('pointerup', e => {
          dragging = false;
          try { control.releasePointerCapture(e.pointerId); } catch(err) {}
        });
      });
    })();
    speechSynthesis.onvoiceschanged = () => {};
    showSlide(0);
  </script>
</body>
</html>'''

out = r'G:\我的雲端硬碟\jsps-tools\tools\classical-poems\06-bazhentu\index.html'
with open(out, 'w', encoding='utf-8') as f:
    f.write(HTML)
print(f'Written {len(HTML)} bytes to {out}')
