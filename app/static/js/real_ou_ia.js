// Real ou IA?: adivinhe se o conteúdo foi feito por um humano ou por uma IA.

(function () {
  "use strict";

  const dataEl = document.getElementById("ra-data");
  if (!dataEl) return;
  const ITENS = JSON.parse(dataEl.textContent);
  const XP = window.RA_XP || 30;

  const progress = document.getElementById("ra-progress");
  const acertosLabel = document.getElementById("ra-acertos");
  const xpLabel = document.getElementById("ra-xp");
  const bar = document.getElementById("ra-bar");
  const card = document.getElementById("ra-card");
  const conteudo = document.getElementById("ra-conteudo");
  const humanoBtn = document.getElementById("ra-humano-btn");
  const iaBtn = document.getElementById("ra-ia-btn");
  const feedback = document.getElementById("ra-feedback");
  const nextBtn = document.getElementById("ra-next-btn");
  const finalEl = document.getElementById("ra-final");

  let indice = 0;
  let acertos = 0;
  let xpTotal = 0;
  let respondida = false;

  function shuffle(arr) {
    for (let i = arr.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [arr[i], arr[j]] = [arr[j], arr[i]];
    }
    return arr;
  }

  const ordem = shuffle(ITENS.slice());

  function updateHUD() {
    progress.textContent = "Item " + (indice + 1) + " de " + ordem.length;
    acertosLabel.textContent = String(acertos);
    xpLabel.textContent = String(xpTotal);
    bar.style.width = (indice / ordem.length) * 100 + "%";
  }

  function render() {
    respondida = false;
    const item = ordem[indice];
    conteudo.textContent = item.conteudo;
    feedback.classList.add("hidden");
    nextBtn.classList.add("hidden");
    [humanoBtn, iaBtn].forEach(function (b) {
      b.disabled = false;
      b.classList.remove("border-green-500", "bg-green-50", "border-red-400", "bg-red-50");
      b.classList.add("border-slate-200");
    });
    updateHUD();
  }

  function responder(escolha) {
    if (respondida) return;
    respondida = true;
    const item = ordem[indice];
    const correto = escolha === item.resposta;
    const corretaBtn = item.resposta === "ia" ? iaBtn : humanoBtn;
    const escolhaBtn = escolha === "ia" ? iaBtn : humanoBtn;

    [humanoBtn, iaBtn].forEach(function (b) {
      b.disabled = true;
    });
    corretaBtn.classList.remove("border-slate-200");
    corretaBtn.classList.add("border-green-500", "bg-green-50");
    if (!correto) {
      escolhaBtn.classList.remove("border-slate-200");
      escolhaBtn.classList.add("border-red-400", "bg-red-50");
    }

    if (correto) {
      acertos += 1;
      xpTotal += XP;
    }
    updateHUD();

    const rotulo = item.resposta === "ia" ? "🤖 IA" : "👤 Humano";
    feedback.classList.remove("hidden", "bg-green-50", "bg-amber-50", "text-green-800", "text-amber-800");
    if (correto) {
      feedback.classList.add("bg-green-50", "text-green-800");
      feedback.innerHTML = "<strong>✅ Acertou! Era " + rotulo + ".</strong><br>" + item.explicacao + "<br><span class='text-slate-500'>💡 " + item.dica + "</span>";
    } else {
      feedback.classList.add("bg-amber-50", "text-amber-800");
      feedback.innerHTML = "<strong>🤔 Era " + rotulo + ".</strong><br>" + item.explicacao + "<br><span class='text-slate-500'>💡 " + item.dica + "</span>";
    }
    feedback.classList.add("animar-entrada");

    nextBtn.textContent = indice === ordem.length - 1 ? "Ver resultado 🏁" : "Próximo ➡️";
    nextBtn.classList.remove("hidden");
  }

  function avancar() {
    if (indice < ordem.length - 1) {
      indice += 1;
      render();
    } else {
      finalizar();
    }
  }

  function finalizar() {
    card.classList.add("hidden");
    finalEl.classList.remove("hidden");
    finalEl.classList.add("animar-entrada");
    document.getElementById("ra-final-correct").textContent = String(acertos);
    document.getElementById("ra-final-total").textContent = String(ordem.length);
    const pct = Math.round((acertos / ordem.length) * 100);
    let emoji = "🌱";
    let msg = "Continue praticando seu olhar de detetive!";
    if (pct >= 90) { emoji = "🏆"; msg = "Incrível! Você é um verdadeiro detetive digital!"; }
    else if (pct >= 70) { emoji = "🕵️"; msg = "Muito bom! Você sabe diferenciar humano de IA!"; }
    else if (pct >= 50) { emoji = "💪"; msg = "Boa! Já está pegando o jeito."; }
    document.getElementById("ra-final-emoji").textContent = emoji;
    document.getElementById("ra-final-msg").textContent = msg;
  }

  humanoBtn.addEventListener("click", function () { responder("humano"); });
  iaBtn.addEventListener("click", function () { responder("ia"); });
  nextBtn.addEventListener("click", avancar);
  document.getElementById("ra-restart").addEventListener("click", function () {
    indice = 0; acertos = 0; xpTotal = 0; respondida = false;
    shuffle(ordem);
    finalEl.classList.add("hidden");
    card.classList.remove("hidden");
    render();
  });

  render();
})();
