// Jogo dos Prompts: 6 missões com dificuldade, XP e estrelas (estilo Angry Birds).

(function () {
  "use strict";

  const dataEl = document.getElementById("missions-data");
  if (!dataEl) return;
  const MISSIONS = JSON.parse(dataEl.textContent);
  const CFG = window.JOGO_CONFIG;

  // Telas
  const startScreen = document.getElementById("start-screen");
  const gameScreen = document.getElementById("game-screen");
  const finalScreen = document.getElementById("final-screen");

  // HUD
  const missionLabel = document.getElementById("mission-label");
  const xpLabel = document.getElementById("xp-label");
  const xpBar = document.getElementById("xp-bar");
  const starsTrack = document.getElementById("stars-track");

  // Banner da missão
  const banner = document.getElementById("mission-banner");
  const bannerIcon = document.getElementById("mission-banner-icon");
  const bannerTitle = document.getElementById("mission-banner-title");
  const bannerDesc = document.getElementById("mission-banner-desc");
  const startMissionBtn = document.getElementById("start-mission-btn");

  // Pergunta
  const questionCard = document.getElementById("question-card");
  const qMissionTag = document.getElementById("q-mission-tag");
  const qCounter = document.getElementById("q-counter");
  const qText = document.getElementById("q-text");
  const qOptions = document.getElementById("q-options");
  const qFeedback = document.getElementById("q-feedback");
  const qNextBtn = document.getElementById("q-next-btn");

  // Resumo da missão
  const missionSummary = document.getElementById("mission-summary");
  const summaryStars = document.getElementById("summary-stars");
  const summaryCorrect = document.getElementById("summary-correct");
  const summaryXp = document.getElementById("summary-xp");
  const continueBtn = document.getElementById("continue-btn");

  // Estado
  let dificuldade = "facil";
  let partida = []; // missões com 5 questões cada
  let mIndex = 0;
  let qIndex = 0;
  let acertosMissao = 0;
  let xpTotal = 0;
  let estrelasTotal = 0;
  let respondida = false;
  let currentQ = null; // questão atual já com alternativas embaralhadas
  const acertosPorMissao = [];
  const estrelasPorMissao = [];

  function shuffle(arr) {
    for (let i = arr.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [arr[i], arr[j]] = [arr[j], arr[i]];
    }
    return arr;
  }

  // Embaralha as alternativas e recalcula o índice da resposta correta,
  // para que a posição da resposta certa mude a cada exibição.
  function shuffleOptions(q) {
    const itens = q.alternativas.map(function (texto, i) {
      return { texto: texto, correta: i === q.correta };
    });
    shuffle(itens);
    return {
      pergunta: q.pergunta,
      explicacao: q.explicacao,
      alternativas: itens.map(function (x) { return x.texto; }),
      correta: itens.findIndex(function (x) { return x.correta; }),
    };
  }

  function pickQuestions(mission, dif, k) {
    const pool = shuffle(mission.questoes.filter((q) => q.dificuldade === dif));
    const outras = shuffle(mission.questoes.filter((q) => q.dificuldade !== dif));
    let sel = pool.slice(0, k);
    if (sel.length < k) sel = sel.concat(outras.slice(0, k - sel.length));
    return sel;
  }

  function starsForCorrect(c) {
    if (c >= 5) return 3;
    if (c >= 3) return 2;
    if (c >= 1) return 1;
    return 0;
  }

  function starString(n, max) {
    let s = "";
    for (let i = 0; i < max; i++) s += i < n ? "⭐" : "☆";
    return s;
  }

  function startGame(dif) {
    dificuldade = dif;
    partida = MISSIONS.map((m) => ({
      meta: m,
      questoes: pickQuestions(m, dif, CFG.questoesPorMissao),
    }));
    mIndex = 0;
    xpTotal = 0;
    estrelasTotal = 0;
    acertosPorMissao.length = 0;
    estrelasPorMissao.length = 0;
    startScreen.classList.add("hidden");
    finalScreen.classList.add("hidden");
    gameScreen.classList.remove("hidden");
    renderStarsTrack();
    updateHUD();
    showBanner();
  }

  function renderStarsTrack() {
    starsTrack.innerHTML = "";
    partida.forEach(function (m, i) {
      const span = document.createElement("span");
      if (i < estrelasPorMissao.length) {
        span.textContent = estrelasPorMissao[i] > 0 ? "⭐".repeat(estrelasPorMissao[i]) : "✖";
        span.className = "px-1 font-bold";
        span.style.color = estrelasPorMissao[i] > 0 ? "#f59e0b" : "#cbd5e1";
      } else if (i === mIndex) {
        span.textContent = "▶";
        span.className = "px-1 text-marca-roxo";
      } else {
        span.textContent = "•";
        span.className = "px-1 text-slate-300";
      }
      starsTrack.appendChild(span);
    });
  }

  function updateHUD() {
    missionLabel.textContent = "Missão " + (mIndex + 1) + " de " + partida.length;
    xpLabel.textContent = String(xpTotal);
    xpBar.style.width = Math.min(100, (xpTotal / CFG.maxXp) * 100) + "%";
  }

  function showBanner() {
    const m = partida[mIndex].meta;
    bannerIcon.textContent = m.icone;
    bannerTitle.textContent = m.titulo;
    bannerDesc.textContent = m.descricao;
    banner.classList.remove("hidden");
    questionCard.classList.add("hidden");
    missionSummary.classList.add("hidden");
    renderStarsTrack();
    updateHUD();
  }

  function startMission() {
    qIndex = 0;
    acertosMissao = 0;
    banner.classList.add("hidden");
    missionSummary.classList.add("hidden");
    questionCard.classList.remove("hidden");
    renderQuestion();
  }

  function renderQuestion() {
    respondida = false;
    const m = partida[mIndex];
    currentQ = shuffleOptions(m.questoes[qIndex]);
    const q = currentQ;
    qMissionTag.textContent = "Missão " + (mIndex + 1) + " • " + m.meta.tema;
    qCounter.textContent = "Pergunta " + (qIndex + 1) + "/" + m.questoes.length;
    qText.textContent = q.pergunta;
    qFeedback.classList.add("hidden");
    qNextBtn.classList.add("hidden");
    qOptions.innerHTML = "";

    q.alternativas.forEach(function (texto, idx) {
      const btn = document.createElement("button");
      btn.className =
        "w-full text-left p-4 rounded-xl border-2 border-slate-200 hover:border-marca-roxoclaro hover:bg-slate-50 transition-colors font-medium text-slate-700";
      btn.innerHTML = '<span class="font-bold text-marca-roxo mr-2">' + String.fromCharCode(65 + idx) + ")</span>";
      const span = document.createElement("span");
      span.textContent = texto;
      btn.appendChild(span);
      btn.addEventListener("click", function () {
        answer(idx);
      });
      qOptions.appendChild(btn);
    });
  }

  function answer(escolhido) {
    if (respondida) return;
    respondida = true;
    const m = partida[mIndex];
    const q = currentQ;
    const correto = escolhido === q.correta;
    const botoes = qOptions.querySelectorAll("button");

    botoes.forEach(function (b, idx) {
      b.disabled = true;
      if (idx === q.correta) {
        b.classList.remove("border-slate-200");
        b.classList.add("border-green-500", "bg-green-50");
      } else if (idx === escolhido) {
        b.classList.remove("border-slate-200");
        b.classList.add("border-red-400", "bg-red-50");
      }
    });

    if (correto) {
      acertosMissao += 1;
      xpTotal += m.meta.xp_por_acerto;
      updateHUD();
      xpLabel.parentElement.classList.add("animar-pulo");
      setTimeout(function () {
        xpLabel.parentElement.classList.remove("animar-pulo");
      }, 400);
    }

    qFeedback.classList.remove("hidden", "bg-green-50", "bg-amber-50", "text-green-800", "text-amber-800");
    if (correto) {
      qFeedback.classList.add("bg-green-50", "text-green-800");
      qFeedback.innerHTML = "<strong>✅ Acertou! +" + m.meta.xp_por_acerto + " XP</strong><br>" + q.explicacao;
    } else {
      qFeedback.classList.add("bg-amber-50", "text-amber-800");
      qFeedback.innerHTML = "<strong>🤔 Quase!</strong> A resposta certa está em verde.<br>" + q.explicacao;
    }
    qFeedback.classList.add("animar-entrada");

    qNextBtn.textContent = qIndex === m.questoes.length - 1 ? "Concluir missão 🏁" : "Próxima ➡️";
    qNextBtn.classList.remove("hidden");
  }

  function nextQuestion() {
    const m = partida[mIndex];
    if (qIndex < m.questoes.length - 1) {
      qIndex += 1;
      renderQuestion();
    } else {
      finishMission();
    }
  }

  function finishMission() {
    const estrelas = starsForCorrect(acertosMissao);
    acertosPorMissao[mIndex] = acertosMissao;
    estrelasPorMissao[mIndex] = estrelas;
    estrelasTotal += estrelas;

    questionCard.classList.add("hidden");
    summaryStars.textContent = starString(estrelas, 3);
    summaryCorrect.textContent = String(acertosMissao);
    summaryXp.textContent = String(acertosMissao * partida[mIndex].meta.xp_por_acerto);
    missionSummary.classList.remove("hidden");
    renderStarsTrack();
  }

  function continueGame() {
    if (mIndex < partida.length - 1) {
      mIndex += 1;
      showBanner();
    } else {
      finishGame();
    }
  }

  async function finishGame() {
    gameScreen.classList.add("hidden");
    finalScreen.classList.remove("hidden");
    finalScreen.classList.add("animar-entrada");

    document.getElementById("final-xp").textContent = String(xpTotal);
    document.getElementById("final-stars").textContent = estrelasTotal + "/" + CFG.maxEstrelas;

    let emoji = "🌱";
    let msg = "Quase lá! Você precisa de " + CFG.meta + " XP para vencer. Tente de novo!";
    if (xpTotal >= CFG.maxXp) {
      emoji = "🏆";
      msg = "PERFEITO! " + CFG.maxXp + " XP! Você é a lenda dos prompts!";
    } else if (xpTotal >= 1500) {
      emoji = "🌟";
      msg = "Incrível! Você dominou a Inteligência Artificial!";
    } else if (xpTotal >= 1000) {
      emoji = "💪";
      msg = "Muito bom! Você manda bem em IA!";
    } else if (xpTotal >= CFG.meta) {
      emoji = "🚀";
      msg = "Boa! Você bateu a meta de " + CFG.meta + " XP! Continue evoluindo.";
    }
    document.getElementById("final-emoji").textContent = emoji;
    document.getElementById("final-message").textContent = msg;

    const breakdown = document.getElementById("final-breakdown");
    breakdown.innerHTML = "";
    partida.forEach(function (m, i) {
      const row = document.createElement("div");
      row.className = "flex items-center justify-between bg-slate-50 rounded-lg px-3 py-2 text-sm";
      const nome = document.createElement("span");
      nome.className = "text-slate-700 font-semibold";
      nome.textContent = "Missão " + (i + 1) + " • " + m.meta.tema;
      const est = document.createElement("span");
      est.textContent = starString(estrelasPorMissao[i] || 0, 3);
      row.appendChild(nome);
      row.appendChild(est);
      breakdown.appendChild(row);
    });

    try {
      await fetch("/jogo/resultado", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ acertos_por_missao: acertosPorMissao, dificuldade: dificuldade }),
      });
    } catch (e) {
      // Falha de rede não atrapalha a experiência.
    }
  }

  // Eventos
  document.querySelectorAll(".dif-btn").forEach(function (btn) {
    btn.addEventListener("click", function () {
      startGame(btn.getAttribute("data-dif"));
    });
  });
  startMissionBtn.addEventListener("click", startMission);
  qNextBtn.addEventListener("click", nextQuestion);
  continueBtn.addEventListener("click", continueGame);
  document.getElementById("restart-btn").addEventListener("click", function () {
    finalScreen.classList.add("hidden");
    startScreen.classList.remove("hidden");
    startScreen.scrollIntoView({ behavior: "smooth", block: "start" });
  });
})();
