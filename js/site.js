"use strict";

const WHATSAPP = "5567992379876";
const fotos = Array.isArray(window.FOTOS) ? window.FOTOS : [];

function linkWhatsApp(servico) {
  const texto = servico
    ? `Oi Karina! Vim pelo site e queria um orçamento de ${servico}.`
    : "Oi Karina! Vim pelo site e queria um orçamento.";
  return `https://wa.me/${WHATSAPP}?text=${encodeURIComponent(texto)}`;
}

function prepararLinksWhatsApp() {
  document.querySelectorAll("[data-servico]").forEach((link) => {
    link.href = linkWhatsApp(link.dataset.servico);
    link.target = "_blank";
    link.rel = "noopener";
  });
}

const mosaico = document.getElementById("mosaico");
const abas = document.querySelectorAll(".abas button");
const telaCheia = document.getElementById("tela-cheia");
const telaCheiaImg = document.getElementById("tela-cheia-img");
const contador = document.getElementById("tela-cheia-contador");
let fotosAtuais = [];
let indiceAtual = 0;

function miniatura(foto, indice) {
  const botao = document.createElement("button");
  botao.type = "button";
  botao.setAttribute("aria-label", `Abrir foto ${indice + 1} em tela cheia`);
  const img = document.createElement("img");
  img.src = foto.mini;
  img.width = foto.w;
  img.height = foto.h;
  img.loading = "lazy";
  img.decoding = "async";
  img.alt = "";
  botao.append(img);
  botao.addEventListener("click", () => abrir(indice));
  return botao;
}

function avisoSemFotos() {
  const aviso = document.createElement("p");
  aviso.className = "aviso";
  aviso.innerHTML = 'Não foi possível carregar as fotos agora. Veja o trabalho no Instagram <a href="https://instagram.com/fractalume">@fractalume</a>.';
  return aviso;
}

function mostrarCategoria(categoria) {
  fotosAtuais = fotos.filter((foto) => foto.categoria === categoria);
  mosaico.replaceChildren(...(fotosAtuais.length ? fotosAtuais.map(miniatura) : [avisoSemFotos()]));
  abas.forEach((aba) => {
    const ativa = aba.dataset.categoria === categoria;
    aba.setAttribute("aria-selected", String(ativa));
    aba.tabIndex = ativa ? 0 : -1;
    if (ativa) mosaico.setAttribute("aria-labelledby", aba.id);
  });
}

function prepararAbas() {
  const lista = [...abas];
  lista.forEach((aba, i) => {
    aba.addEventListener("click", () => mostrarCategoria(aba.dataset.categoria));
    aba.addEventListener("keydown", (evento) => {
      const passo = { ArrowRight: 1, ArrowLeft: -1 }[evento.key];
      if (!passo) return;
      const proxima = lista[(i + passo + lista.length) % lista.length];
      proxima.focus();
      mostrarCategoria(proxima.dataset.categoria);
    });
  });
}

function exibir(indice) {
  if (!fotosAtuais.length) return;
  indiceAtual = (indice + fotosAtuais.length) % fotosAtuais.length;
  const foto = fotosAtuais[indiceAtual];
  telaCheiaImg.src = foto.grande;
  contador.textContent = `${indiceAtual + 1} / ${fotosAtuais.length}`;
}

function abrir(indice) {
  if (!fotosAtuais.length) return;
  exibir(indice);
  telaCheia.showModal();
}

function prepararTelaCheia() {
  telaCheia.querySelector(".tc-fechar").addEventListener("click", () => telaCheia.close());
  telaCheia.querySelector(".tc-anterior").addEventListener("click", () => exibir(indiceAtual - 1));
  telaCheia.querySelector(".tc-proxima").addEventListener("click", () => exibir(indiceAtual + 1));
  telaCheia.addEventListener("click", (evento) => {
    if (evento.target === telaCheia) telaCheia.close();
  });
  document.addEventListener("keydown", (evento) => {
    if (!telaCheia.open) return;
    if (evento.key === "ArrowLeft") exibir(indiceAtual - 1);
    if (evento.key === "ArrowRight") exibir(indiceAtual + 1);
  });
  telaCheia.addEventListener("close", () => telaCheiaImg.removeAttribute("src"));

  let inicioX = null;
  telaCheia.addEventListener("touchstart", (evento) => { inicioX = evento.touches[0].clientX; }, { passive: true });
  telaCheia.addEventListener("touchend", (evento) => {
    if (inicioX === null) return;
    const deslocamento = evento.changedTouches[0].clientX - inicioX;
    if (Math.abs(deslocamento) > 50) exibir(indiceAtual + (deslocamento < 0 ? 1 : -1));
    inicioX = null;
  });
}

prepararLinksWhatsApp();
prepararAbas();
prepararTelaCheia();
mostrarCategoria("ensaios");
