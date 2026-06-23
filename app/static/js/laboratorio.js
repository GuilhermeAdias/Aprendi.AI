// Laboratório de Prompts: envia o prompt ao backend e exibe a análise.

(function () {
  "use strict";

  const input = document.getElementById("prompt-input");
  const analisarBtn = document.getElementById("analisar-btn");
  const exemploBtn = document.getElementById("exemplo-btn");
  const resultado = document.getElementById("resultado");

  const scoreNum = document.getElementById("score-num");
  const levelBadge = document.getElementById("level-badge");
  const scoreBar = document.getElementById("score-bar");
  const strengthsEl = document.getElementById("strengths");
  const improvementsEl = document.getElementById("improvements");
  const suggestedEl = document.getElementById("suggested");

  const EXEMPLOS = [
    "Explique o que é fotossíntese para um aluno de 11 anos, em 4 tópicos simples e com um exemplo.",
    "Sou estudante do 8º ano. Crie um resumo divertido sobre o ciclo da água, em 5 frases curtas.",
    "me fala sobre dinossauros",
    "Crie uma lista de 5 dicas para estudar matemática, com linguagem simples para um jovem de 13 anos.",
  ];

  function corDaNota(score) {
    if (score >= 70) return "#16a34a"; // verde
    if (score >= 40) return "#f59e0b"; // amarelo
    return "#dc2626"; // vermelho
  }

  function corDoBadge(score) {
    if (score >= 70) return "#7c3aed";
    if (score >= 40) return "#2563eb";
    return "#64748b";
  }

  function preencherLista(el, itens, vazio) {
    el.innerHTML = "";
    if (!itens || itens.length === 0) {
      const li = document.createElement("li");
      li.textContent = vazio;
      li.className = "text-slate-400";
      el.appendChild(li);
      return;
    }
    itens.forEach(function (texto) {
      const li = document.createElement("li");
      li.className = "flex gap-2";
      li.innerHTML = "<span>•</span><span></span>";
      li.querySelector("span:last-child").textContent = texto;
      el.appendChild(li);
    });
  }

  function animarNota(alvo) {
    let atual = 0;
    scoreNum.textContent = "0";
    const passo = Math.max(1, Math.round(alvo / 25));
    const timer = setInterval(function () {
      atual += passo;
      if (atual >= alvo) {
        atual = alvo;
        clearInterval(timer);
      }
      scoreNum.textContent = String(atual);
    }, 25);
  }

  function mostrarResultado(data) {
    scoreNum.style.color = corDaNota(data.score);
    levelBadge.textContent = data.level;
    levelBadge.style.backgroundColor = corDoBadge(data.score);

    scoreBar.style.backgroundColor = corDaNota(data.score);
    scoreBar.style.width = "0%";

    preencherLista(strengthsEl, data.strengths, "—");
    preencherLista(improvementsEl, data.improvements, "Nada a melhorar, seu prompt está ótimo! 🎉");
    suggestedEl.textContent = data.suggested_prompt;

    resultado.classList.remove("hidden");
    resultado.classList.add("animar-entrada");

    animarNota(data.score);
    // Pequeno atraso para a barra animar após ficar visível.
    setTimeout(function () {
      scoreBar.style.width = data.score + "%";
    }, 100);

    resultado.scrollIntoView({ behavior: "smooth", block: "start" });
  }

  async function analisar() {
    const prompt = input.value.trim();
    analisarBtn.disabled = true;
    analisarBtn.textContent = "Analisando...";
    try {
      const resp = await fetch("/laboratorio/analisar", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt: prompt }),
      });
      if (!resp.ok) throw new Error("Falha na análise");
      const data = await resp.json();
      mostrarResultado(data);
    } catch (e) {
      alert("Não foi possível analisar o prompt agora. Tente novamente.");
    } finally {
      analisarBtn.disabled = false;
      analisarBtn.textContent = "🔍 Analisar meu prompt";
    }
  }

  if (analisarBtn) {
    analisarBtn.addEventListener("click", analisar);
  }

  if (exemploBtn) {
    exemploBtn.addEventListener("click", function () {
      const idx = Math.floor(Math.random() * EXEMPLOS.length);
      input.value = EXEMPLOS[idx];
      input.focus();
    });
  }
})();
