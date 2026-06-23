// Jogo dos Prompts: missões interativas com XP, progresso e badges.

(function () {
  "use strict";

  const dataEl = document.getElementById("missions-data");
  if (!dataEl) return;
  const missions = JSON.parse(dataEl.textContent);
  const XP_POR_ACERTO = 100;

  // Elementos do DOM.
  const progressLabel = document.getElementById("progress-label");
  const xpLabel = document.getElementById("xp-label");
  const progressBar = document.getElementById("progress-bar");
  const missionArea = document.getElementById("mission-area");
  const missionTitle = document.getElementById("mission-title");
  const missionDesc = document.getElementById("mission-desc");
  const missionOptions = document.getElementById("mission-options");
  const missionFeedback = document.getElementById("mission-feedback");
  const nextBtn = document.getElementById("next-btn");
  const finalArea = document.getElementById("final-area");

  let indiceAtual = 0;
  let acertos = 0;
  let xp = 0;
  let respondida = false;

  function atualizarHUD() {
    progressLabel.textContent = "Missão " + (indiceAtual + 1) + " de " + missions.length;
    xpLabel.textContent = String(xp);
    const pct = (indiceAtual / missions.length) * 100;
    progressBar.style.width = pct + "%";
  }

  function renderMissao() {
    respondida = false;
    const m = missions[indiceAtual];
    missionTitle.textContent = m.titulo;
    missionDesc.textContent = m.descricao;
    missionFeedback.classList.add("hidden");
    nextBtn.classList.add("hidden");
    missionOptions.innerHTML = "";

    m.prompts.forEach(function (texto, idx) {
      const btn = document.createElement("button");
      btn.className =
        "w-full text-left p-4 rounded-xl border-2 border-slate-200 hover:border-marca-roxoclaro hover:bg-slate-50 transition-colors font-medium text-slate-700";
      btn.innerHTML =
        '<span class="font-bold text-marca-roxo mr-2">' +
        String.fromCharCode(65 + idx) +
        ")</span>";
      const span = document.createElement("span");
      span.textContent = texto;
      btn.appendChild(span);
      btn.addEventListener("click", function () {
        responder(idx, btn);
      });
      missionOptions.appendChild(btn);
    });

    atualizarHUD();
  }

  function responder(escolhido, btn) {
    if (respondida) return;
    respondida = true;
    const m = missions[indiceAtual];
    const correto = escolhido === m.correta;
    const botoes = missionOptions.querySelectorAll("button");

    botoes.forEach(function (b, idx) {
      b.disabled = true;
      if (idx === m.correta) {
        b.classList.remove("border-slate-200");
        b.classList.add("border-green-500", "bg-green-50");
      } else if (idx === escolhido) {
        b.classList.remove("border-slate-200");
        b.classList.add("border-red-400", "bg-red-50");
      }
    });

    if (correto) {
      acertos += 1;
      xp += XP_POR_ACERTO;
      xpLabel.textContent = String(xp);
      xpLabel.parentElement.classList.add("animar-pulo");
      setTimeout(function () {
        xpLabel.parentElement.classList.remove("animar-pulo");
      }, 400);
    }

    missionFeedback.classList.remove("hidden", "bg-green-50", "bg-amber-50", "text-green-800", "text-amber-800");
    if (correto) {
      missionFeedback.classList.add("bg-green-50", "text-green-800");
      missionFeedback.innerHTML = "<strong>✅ Acertou! +" + XP_POR_ACERTO + " XP</strong><br>" + m.explicacao;
    } else {
      missionFeedback.classList.add("bg-amber-50", "text-amber-800");
      missionFeedback.innerHTML = "<strong>🤔 Quase!</strong> A melhor opção era a destacada em verde.<br>" + m.explicacao;
    }
    missionFeedback.classList.add("animar-entrada");

    nextBtn.textContent =
      indiceAtual === missions.length - 1 ? "Ver resultado 🏁" : "Próxima missão ➡️";
    nextBtn.classList.remove("hidden");
  }

  function avancar() {
    if (indiceAtual < missions.length - 1) {
      indiceAtual += 1;
      renderMissao();
    } else {
      finalizar();
    }
  }

  async function finalizar() {
    progressBar.style.width = "100%";
    progressLabel.textContent = "Concluído!";
    missionArea.classList.add("hidden");

    const total = missions.length;
    const percent = Math.round((acertos / total) * 100);

    document.getElementById("final-correct").textContent = acertos + "/" + total;
    document.getElementById("final-xp").textContent = String(xp);

    let emoji = "🚀";
    let msg = "Você começou a jornada! Revise o Guia de Prompts e tente de novo.";
    if (percent >= 100) {
      emoji = "🏆";
      msg = "Incrível! Você é um verdadeiro Mestre dos Prompts!";
    } else if (percent >= 70) {
      emoji = "🌟";
      msg = "Muito bem! Você já cria prompts ótimos!";
    } else if (percent >= 40) {
      emoji = "💪";
      msg = "Bom trabalho! Continue praticando para evoluir.";
    }
    document.getElementById("final-emoji").textContent = emoji;
    document.getElementById("final-message").textContent = msg;

    renderBadges(acertos, percent);

    finalArea.classList.remove("hidden");
    finalArea.classList.add("animar-entrada");

    // Persiste o resultado no backend.
    try {
      await fetch("/jogo/resultado", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ correct: acertos }),
      });
    } catch (e) {
      // Falha de rede não deve atrapalhar a experiência do usuário.
    }
  }

  function renderBadges(acertos, percent) {
    const badgesEl = document.getElementById("badges");
    badgesEl.innerHTML = "";
    const conquistas = [];
    if (acertos >= 1) conquistas.push("🎯 Primeiro acerto");
    if (acertos >= 3) conquistas.push("⭐ Meio caminho");
    if (percent >= 100) conquistas.push("🏆 Tudo certo!");
    if (percent >= 70) conquistas.push("🧠 Bom de prompt");
    if (conquistas.length === 0) conquistas.push("🌱 Aprendiz");

    conquistas.forEach(function (txt) {
      const span = document.createElement("span");
      span.className =
        "bg-marca-roxo/10 text-marca-roxo font-bold text-sm px-3 py-1 rounded-full";
      span.textContent = txt;
      badgesEl.appendChild(span);
    });
  }

  function reiniciar() {
    indiceAtual = 0;
    acertos = 0;
    xp = 0;
    finalArea.classList.add("hidden");
    missionArea.classList.remove("hidden");
    renderMissao();
    missionArea.scrollIntoView({ behavior: "smooth", block: "start" });
  }

  nextBtn.addEventListener("click", avancar);
  document.getElementById("restart-btn").addEventListener("click", reiniciar);

  renderMissao();
})();
