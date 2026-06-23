// Monte o Prompt: o jogador escolhe um bloco por categoria e monta o prompt.

(function () {
  "use strict";

  const dataEl = document.getElementById("mp-data");
  if (!dataEl) return;
  const DESAFIOS = JSON.parse(dataEl.textContent);
  const XP = window.MP_XP || 25;

  const progress = document.getElementById("mp-progress");
  const xpLabel = document.getElementById("mp-xp");
  const bar = document.getElementById("mp-bar");
  const card = document.getElementById("mp-card");
  const cenario = document.getElementById("mp-cenario");
  const categoriasEl = document.getElementById("mp-categorias");
  const montarBtn = document.getElementById("mp-montar-btn");
  const resultado = document.getElementById("mp-resultado");
  const promptFinal = document.getElementById("mp-prompt-final");
  const feedback = document.getElementById("mp-feedback");
  const nextBtn = document.getElementById("mp-next-btn");
  const finalEl = document.getElementById("mp-final");

  let indice = 0;
  let xpTotal = 0;
  let escolhas = {}; // categoriaIndex -> opcaoIndex
  const maxXp = DESAFIOS.reduce((acc, d) => acc + d.categorias.length * XP, 0);

  function updateHUD() {
    progress.textContent = "Desafio " + (indice + 1) + " de " + DESAFIOS.length;
    xpLabel.textContent = String(xpTotal);
    bar.style.width = Math.min(100, (xpTotal / maxXp) * 100) + "%";
  }

  function render() {
    escolhas = {};
    const d = DESAFIOS[indice];
    cenario.textContent = " " + d.cenario;
    resultado.classList.add("hidden");
    montarBtn.classList.remove("hidden");
    montarBtn.disabled = true;
    categoriasEl.innerHTML = "";

    d.categorias.forEach(function (cat, ci) {
      const wrap = document.createElement("div");
      const titulo = document.createElement("div");
      titulo.className = "font-bold text-slate-700 mb-2 flex items-center gap-2";
      titulo.innerHTML = "<span>" + cat.icone + "</span><span></span>";
      titulo.querySelector("span:last-child").textContent = cat.nome;
      wrap.appendChild(titulo);

      const opts = document.createElement("div");
      opts.className = "grid gap-2";
      cat.opcoes.forEach(function (op, oi) {
        const btn = document.createElement("button");
        btn.className =
          "opt-btn text-left p-3 rounded-xl border-2 border-slate-200 hover:border-marca-roxoclaro hover:bg-slate-50 transition-colors text-sm text-slate-700";
        btn.textContent = op.texto;
        btn.dataset.cat = ci;
        btn.dataset.opt = oi;
        btn.addEventListener("click", function () {
          selecionar(ci, oi, opts, btn);
        });
        opts.appendChild(btn);
      });
      wrap.appendChild(opts);
      categoriasEl.appendChild(wrap);
    });

    updateHUD();
  }

  function selecionar(ci, oi, container, btn) {
    escolhas[ci] = oi;
    container.querySelectorAll(".opt-btn").forEach(function (b) {
      b.classList.remove("border-marca-roxo", "bg-marca-roxo/10", "font-bold");
      b.classList.add("border-slate-200");
    });
    btn.classList.remove("border-slate-200");
    btn.classList.add("border-marca-roxo", "bg-marca-roxo/10", "font-bold");
    // Habilita o botão quando todas as categorias têm escolha.
    const total = DESAFIOS[indice].categorias.length;
    montarBtn.disabled = Object.keys(escolhas).length < total;
  }

  function montar() {
    const d = DESAFIOS[indice];
    let acertos = 0;
    const partes = [];
    const botoes = categoriasEl.querySelectorAll(".opt-btn");

    d.categorias.forEach(function (cat, ci) {
      const escolhida = escolhas[ci];
      partes.push(cat.opcoes[escolhida].texto);
      if (cat.opcoes[escolhida].bom) acertos += 1;
      // Marca visualmente o melhor e o escolhido.
      botoes.forEach(function (b) {
        if (Number(b.dataset.cat) === ci) {
          b.disabled = true;
          const oi = Number(b.dataset.opt);
          if (cat.opcoes[oi].bom) {
            b.classList.remove("border-slate-200", "bg-marca-roxo/10", "border-marca-roxo");
            b.classList.add("border-green-500", "bg-green-50");
          } else if (oi === escolhida) {
            b.classList.remove("border-marca-roxo", "bg-marca-roxo/10");
            b.classList.add("border-red-400", "bg-red-50");
          }
        }
      });
    });

    const ganho = acertos * XP;
    xpTotal += ganho;
    updateHUD();

    promptFinal.textContent = '"' + partes.join(" ") + '"';
    feedback.classList.remove("text-green-700", "text-amber-600");
    if (acertos === d.categorias.length) {
      feedback.classList.add("text-green-700");
      feedback.textContent = "✅ Perfeito! Todos os blocos certos! +" + ganho + " XP";
    } else {
      feedback.classList.add("text-amber-600");
      feedback.textContent =
        "👍 Você acertou " + acertos + " de " + d.categorias.length + " blocos. +" + ganho + " XP. Os melhores estão em verde!";
    }

    montarBtn.classList.add("hidden");
    resultado.classList.remove("hidden");
    resultado.classList.add("animar-entrada");
    nextBtn.textContent = indice === DESAFIOS.length - 1 ? "Ver resultado 🏁" : "Próximo desafio ➡️";
  }

  function avancar() {
    if (indice < DESAFIOS.length - 1) {
      indice += 1;
      render();
      card.scrollIntoView({ behavior: "smooth", block: "start" });
    } else {
      finalizar();
    }
  }

  function finalizar() {
    card.classList.add("hidden");
    finalEl.classList.remove("hidden");
    finalEl.classList.add("animar-entrada");
    document.getElementById("mp-final-xp").textContent = String(xpTotal);
    const pct = Math.round((xpTotal / maxXp) * 100);
    let msg = "Continue praticando para montar prompts ainda melhores!";
    if (pct === 100) msg = "Você montou todos os prompts perfeitamente! 🏆";
    else if (pct >= 70) msg = "Mandou muito bem! Seus prompts estão ótimos! 🌟";
    else if (pct >= 40) msg = "Bom trabalho! Já dá para ver a evolução. 💪";
    document.getElementById("mp-final-msg").textContent = msg;
  }

  montarBtn.addEventListener("click", montar);
  nextBtn.addEventListener("click", avancar);
  document.getElementById("mp-restart").addEventListener("click", function () {
    indice = 0;
    xpTotal = 0;
    finalEl.classList.add("hidden");
    card.classList.remove("hidden");
    render();
  });

  render();
})();
