// Quiz educativo: perguntas interativas com feedback e pontuação.

(function () {
  "use strict";

  const dataEl = document.getElementById("quiz-data");
  if (!dataEl) return;
  const questions = JSON.parse(dataEl.textContent);

  const progressLabel = document.getElementById("quiz-progress-label");
  const correctLabel = document.getElementById("quiz-correct-label");
  const progressBar = document.getElementById("quiz-progress-bar");
  const area = document.getElementById("quiz-area");
  const questionEl = document.getElementById("quiz-question");
  const optionsEl = document.getElementById("quiz-options");
  const feedbackEl = document.getElementById("quiz-feedback");
  const nextBtn = document.getElementById("quiz-next-btn");
  const finalEl = document.getElementById("quiz-final");

  let indice = 0;
  let acertos = 0;
  let respondida = false;
  let currentQ = null; // pergunta atual já com alternativas embaralhadas

  function shuffle(arr) {
    for (let i = arr.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [arr[i], arr[j]] = [arr[j], arr[i]];
    }
    return arr;
  }

  // Embaralha as alternativas e recalcula o índice da correta.
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

  function atualizarHUD() {
    progressLabel.textContent = "Pergunta " + (indice + 1) + " de " + questions.length;
    correctLabel.textContent = String(acertos);
    progressBar.style.width = (indice / questions.length) * 100 + "%";
  }

  function render() {
    respondida = false;
    currentQ = shuffleOptions(questions[indice]);
    const q = currentQ;
    questionEl.textContent = q.pergunta;
    feedbackEl.classList.add("hidden");
    nextBtn.classList.add("hidden");
    optionsEl.innerHTML = "";

    q.alternativas.forEach(function (texto, idx) {
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
        responder(idx);
      });
      optionsEl.appendChild(btn);
    });

    atualizarHUD();
  }

  function responder(escolhido) {
    if (respondida) return;
    respondida = true;
    const q = currentQ;
    const correto = escolhido === q.correta;
    const botoes = optionsEl.querySelectorAll("button");

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
      acertos += 1;
      correctLabel.textContent = String(acertos);
    }

    feedbackEl.classList.remove("hidden", "bg-green-50", "bg-amber-50", "text-green-800", "text-amber-800");
    if (correto) {
      feedbackEl.classList.add("bg-green-50", "text-green-800");
      feedbackEl.innerHTML = "<strong>✅ Correto!</strong><br>" + q.explicacao;
    } else {
      feedbackEl.classList.add("bg-amber-50", "text-amber-800");
      feedbackEl.innerHTML = "<strong>🤔 Não foi dessa vez.</strong> A resposta certa está em verde.<br>" + q.explicacao;
    }
    feedbackEl.classList.add("animar-entrada");

    nextBtn.textContent =
      indice === questions.length - 1 ? "Ver resultado 🏁" : "Próxima ➡️";
    nextBtn.classList.remove("hidden");
  }

  function avancar() {
    if (indice < questions.length - 1) {
      indice += 1;
      render();
    } else {
      finalizar();
    }
  }

  async function finalizar() {
    progressBar.style.width = "100%";
    progressLabel.textContent = "Concluído!";
    area.classList.add("hidden");

    const total = questions.length;
    const percent = Math.round((acertos / total) * 100);
    document.getElementById("quiz-final-correct").textContent = String(acertos);

    let emoji = "🚀";
    let msg = "Tudo bem! Explore as páginas e refaça o quiz para aprender mais.";
    if (percent >= 90) {
      emoji = "🧠";
      msg = "Uau! Você é um expert em Inteligência Artificial!";
    } else if (percent >= 70) {
      emoji = "🌟";
      msg = "Muito bom! Você entende bastante sobre IA!";
    } else if (percent >= 50) {
      emoji = "💪";
      msg = "Boa! Você está no caminho certo. Revise e tente de novo!";
    }
    document.getElementById("quiz-final-emoji").textContent = emoji;
    document.getElementById("quiz-final-message").textContent = msg;

    finalEl.classList.remove("hidden");
    finalEl.classList.add("animar-entrada");

    try {
      await fetch("/quiz/resultado", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ correct: acertos }),
      });
    } catch (e) {
      // Silencioso: não atrapalha a experiência.
    }
  }

  function reiniciar() {
    indice = 0;
    acertos = 0;
    finalEl.classList.add("hidden");
    area.classList.remove("hidden");
    render();
    area.scrollIntoView({ behavior: "smooth", block: "start" });
  }

  nextBtn.addEventListener("click", avancar);
  document.getElementById("quiz-restart-btn").addEventListener("click", reiniciar);

  render();
})();
