const state = {
  metadata: null,
  universes: [],
  currentUniverse: null,
  dataBase: "./data",
  municipalities: [],
  catalog: [],
  methodology: [],
  currentMunicipality: null,
  currentYear: null,
  currentVariable: "investimento_pct_receita_corrente",
  annual: null,
  municipal: null,
  mapGeoJSON: null,
  references: [],
  coverage: [],
  crosswalk: [],
};

const THEMES = {
  "Receitas e autonomia": [
    "dca_receita_corrente_bruta",
    "dca_receita_tributaria_bruta",
    "dca_iptu_principal",
    "dca_itbi_principal",
    "dca_iss_principal",
    "dca_fpm_cota_mensal",
    "dca_icms_cota_parte",
    "dca_ipva_cota_parte",
    "tributos_imobiliarios",
    "tributos_selecionados",
    "transferencias_selecionadas",
    "receita_tributaria_pct_receita_corrente",
    "tributos_imobiliarios_pct_receita_tributaria",
    "transferencias_selecionadas_pct_receita_corrente"
  ],
  "Despesas e investimento": [
    "dca_despesa_total_liquidada",
    "dca_despesa_corrente_liquidada",
    "dca_pessoal_encargos_liquidada",
    "dca_investimentos_liquidada",
    "dca_inversoes_financeiras_liquidada",
    "dca_amortizacao_divida_liquidada",
    "servico_divida_liquidado",
    "despesas_capital_selecionadas",
    "gasto_social_selecionado",
    "saldo_corrente_simplificado",
    "investimento_pct_receita_corrente",
    "investimento_pc"
  ],
  "Território": [
    "dca_func_urbanismo_liquidada",
    "dca_func_habitacao_liquidada",
    "dca_func_saneamento_liquidada",
    "dca_func_gestao_ambiental_liquidada",
    "dca_func_transporte_liquidada",
    "despesa_territorial",
    "despesa_territorial_pct_despesa",
    "despesa_territorial_pc",
    "urbanismo_pct_territorial",
    "habitacao_pct_territorial",
    "saneamento_pct_territorial",
    "gestao_ambiental_pct_territorial",
    "transporte_pct_territorial"
  ],
  "Dívida e liquidez": [
    "rreo_rcl_oficial",
    "rgf_despesa_total_pessoal",
    "rgf_caixa_liquida_apos_rpnp",
    "rgf02_divida_consolidada",
    "rgf02_divida_consolidada_liquida",
    "rgf02_divida_contratual",
    "rgf02_parcelamento_dividas",
    "rgf02_precatorios_vencidos_nao_pagos",
    "rgf02_deducoes_divida_consolidada",
    "rgf02_disponibilidade_caixa",
    "rgf02_demais_haveres_financeiros",
    "rgf02_restos_pagar_processados",
    "dtp_pct_rcl",
    "dc_pct_rcl",
    "dcl_pct_rcl",
    "caixa_pos_rpnp_pct_rcl"
  ],
  "CAPAG": ["capag", "indicador_1", "indicador_2", "indicador_3"]
};

const KPI_IDS = [
  "receita_tributaria_pct_receita_corrente",
  "investimento_pct_receita_corrente",
  "investimento_pc",
  "dtp_pct_rcl",
  "dc_pct_rcl",
  "dcl_pct_rcl",
  "caixa_pos_rpnp_pct_rcl",
  "capag",
];

const $ = (selector) => document.querySelector(selector);
const $$ = (selector) => [...document.querySelectorAll(selector)];

async function getJSON(url) {
  const response = await fetch(url);
  if (!response.ok) {
    throw new Error(`Falha ao carregar ${url}: ${response.status}`);
  }
  return response.json();
}

async function getOptionalJSON(url) {
  const response = await fetch(url);
  if (!response.ok) return null;
  return response.json();
}

function catalogItem(id) {
  return state.catalog.find((item) => item.variavel_id === id) || null;
}

function formatValue(value, doc) {
  if (value === null || value === undefined) return "NA";
  if (typeof value === "string") return value;

  const unit = doc?.unidade_publica || doc?.unidade_tecnica || "";
  if (unit === "pct" || unit === "percentual") {
    return new Intl.NumberFormat("pt-BR", {
      style: "percent",
      minimumFractionDigits: 1,
      maximumFractionDigits: 2,
    }).format(value);
  }
  if (unit === "brl" || unit === "BRL") {
    return new Intl.NumberFormat("pt-BR", {
      style: "currency",
      currency: "BRL",
      maximumFractionDigits: 0,
    }).format(value);
  }
  if (unit === "brlpc" || unit === "BRL_por_habitante") {
    return `${new Intl.NumberFormat("pt-BR", {
      style: "currency",
      currency: "BRL",
      maximumFractionDigits: 0,
    }).format(value)} / hab.`;
  }
  return new Intl.NumberFormat("pt-BR", {
    maximumFractionDigits: 2,
  }).format(value);
}

function statusLabel(status) {
  const map = {
    observado: "observado",
    ausente: "ausente",
    nao_aplicavel: "não aplicável",
    em_revisao: "em revisão",
    sem_classificacao: "sem classificação",
  };
  return map[status] || status || "—";
}

function currentAnnualMunicipality() {
  return state.annual?.municipalities?.find(
    (item) => item.codigo_ibge === state.currentMunicipality
  );
}

function variableValue(id) {
  const municipality = currentAnnualMunicipality();
  const entry = municipality?.values?.[id];
  return entry || { status: "ausente", value: null };
}

function renderKpis() {
  const grid = $("#kpi-grid");
  grid.innerHTML = "";
  for (const id of KPI_IDS) {
    const doc = catalogItem(id);
    if (!doc) continue;
    const entry = variableValue(id);
    const card = document.createElement("article");
    card.className = "kpi panel";
    card.innerHTML = `
      <div class="label">${doc.titulo_publico || doc.nome_tecnico}</div>
      <div class="value">${formatValue(entry.value, doc)}</div>
      <div class="muted">${statusLabel(entry.status)}</div>
      <a href="#dictionary" data-help="${id}">Como ler</a>
    `;
    grid.appendChild(card);
  }
}

function renderSelectedVariable() {
  const id = state.currentVariable;
  const doc = catalogItem(id);
  const entry = variableValue(id);
  $("#selected-variable-label").textContent =
    doc?.titulo_publico || doc?.nome_tecnico || id;
  $("#selected-variable-value").textContent = formatValue(entry.value, doc);
  $("#selected-variable-status").textContent =
    `Status: ${statusLabel(entry.status)} · ${state.currentYear}`;
}

function renderOverview() {
  const municipality = state.municipalities.find(
    (item) => item.codigo_ibge === state.currentMunicipality
  );
  $("#overview-title").textContent =
    `${municipality?.nome || "—"} · ${state.currentYear || "—"}`;
  renderKpis();
  renderSelectedVariable();
  renderProfile();
}

function renderSeries() {
  const doc = catalogItem(state.currentVariable);
  const series = state.municipal?.series?.[state.currentVariable] || [];
  $("#series-title").textContent =
    doc?.titulo_publico || doc?.nome_tecnico || state.currentVariable;

  const svg = $("#series-chart");
  svg.innerHTML = "";

  const observed = series.filter(
    (item) => item.status === "observado" && typeof item.value === "number"
  );
  if (!observed.length) {
    svg.innerHTML =
      '<text x="24" y="42" class="chart-label">Sem valores observados para esta série.</text>';
  } else {
    const width = 900, height = 320;
    const margin = { left: 66, right: 24, top: 24, bottom: 48 };
    const xs = observed.map((d) => d.year);
    const ys = observed.map((d) => d.value);
    const minX = Math.min(...xs), maxX = Math.max(...xs);
    let minY = Math.min(...ys), maxY = Math.max(...ys);
    if (minY === maxY) {
      minY -= 1;
      maxY += 1;
    }
    const x = (year) =>
      margin.left + ((year - minX) / Math.max(1, maxX - minX)) *
      (width - margin.left - margin.right);
    const y = (value) =>
      margin.top + (1 - (value - minY) / (maxY - minY)) *
      (height - margin.top - margin.bottom);

    const axis = document.createElementNS("http://www.w3.org/2000/svg", "line");
    axis.setAttribute("x1", margin.left);
    axis.setAttribute("x2", margin.left);
    axis.setAttribute("y1", margin.top);
    axis.setAttribute("y2", height - margin.bottom);
    axis.setAttribute("class", "chart-axis");
    svg.appendChild(axis);

    const baseline = axis.cloneNode();
    baseline.setAttribute("x1", margin.left);
    baseline.setAttribute("x2", width - margin.right);
    baseline.setAttribute("y1", height - margin.bottom);
    baseline.setAttribute("y2", height - margin.bottom);
    svg.appendChild(baseline);

    const poly = document.createElementNS("http://www.w3.org/2000/svg", "polyline");
    poly.setAttribute(
      "points",
      observed.map((d) => `${x(d.year)},${y(d.value)}`).join(" ")
    );
    poly.setAttribute("class", "chart-line");
    svg.appendChild(poly);

    for (const d of observed) {
      const dot = document.createElementNS("http://www.w3.org/2000/svg", "circle");
      dot.setAttribute("cx", x(d.year));
      dot.setAttribute("cy", y(d.value));
      dot.setAttribute("r", 5);
      dot.setAttribute("class", "chart-dot");
      const title = document.createElementNS("http://www.w3.org/2000/svg", "title");
      title.textContent = `${d.year}: ${formatValue(d.value, doc)}`;
      dot.appendChild(title);
      svg.appendChild(dot);
    }

    for (const year of [...new Set(xs)]) {
      const label = document.createElementNS("http://www.w3.org/2000/svg", "text");
      label.setAttribute("x", x(year));
      label.setAttribute("y", height - 18);
      label.setAttribute("text-anchor", "middle");
      label.setAttribute("class", "chart-label");
      label.textContent = year;
      svg.appendChild(label);
    }
  }

  const wrap = $("#series-table-wrap");
  wrap.innerHTML = `
    <table class="data-table">
      <thead><tr><th>Ano</th><th>Valor</th><th>Status</th></tr></thead>
      <tbody>
        ${series.map((item) => `
          <tr>
            <td>${item.year}</td>
            <td>${formatValue(item.value, doc)}</td>
            <td>${statusLabel(item.status)}</td>
          </tr>
        `).join("")}
      </tbody>
    </table>
  `;
}


function geometryRings(geometry) {
  if (!geometry) return [];
  if (geometry.type === "Polygon") return geometry.coordinates;
  if (geometry.type === "MultiPolygon") {
    return geometry.coordinates.flat();
  }
  return [];
}

function mapBounds(features) {
  const points = [];
  for (const feature of features) {
    for (const ring of geometryRings(feature.geometry)) {
      for (const point of ring) points.push(point);
    }
  }
  if (!points.length) return null;
  return {
    minX: Math.min(...points.map((p) => p[0])),
    maxX: Math.max(...points.map((p) => p[0])),
    minY: Math.min(...points.map((p) => p[1])),
    maxY: Math.max(...points.map((p) => p[1])),
  };
}

function quantileBreaks(values, bins = 5) {
  const sorted = values.slice().sort((a, b) => a - b);
  if (!sorted.length) return [];
  const breaks = [];
  for (let i = 1; i < bins; i++) {
    const index = Math.min(
      sorted.length - 1,
      Math.floor((i * sorted.length) / bins)
    );
    breaks.push(sorted[index]);
  }
  return [...new Set(breaks)];
}

function mapFill(value, breaks) {
  if (typeof value !== "number") return "#dfe4e9";
  const palette = ["#dbe8f0", "#b9d0df", "#8eb4ca", "#5e94b4", "#2e6f95"];
  let index = breaks.findIndex((cut) => value <= cut);
  if (index < 0) index = breaks.length;
  return palette[Math.min(index, palette.length - 1)];
}

function renderMap() {
  const svg = $("#municipal-map");
  const empty = $("#map-empty");
  const legend = $("#map-legend");
  const doc = catalogItem(state.currentVariable);
  $("#map-title").textContent =
    `${doc?.titulo_publico || state.currentVariable} · ${state.currentYear}`;

  if (!state.mapGeoJSON?.features?.length) {
    svg.innerHTML = "";
    legend.innerHTML = "";
    empty.hidden = false;
    return;
  }
  empty.hidden = true;

  const annualByCode = new Map(
    (state.annual?.municipalities || []).map((item) => [
      item.codigo_ibge,
      item.values?.[state.currentVariable] || { status: "ausente", value: null },
    ])
  );
  const numericValues = [...annualByCode.values()]
    .filter((entry) => entry.status === "observado" && typeof entry.value === "number")
    .map((entry) => entry.value);
  const breaks = quantileBreaks(numericValues, 5);

  const width = 960;
  const height = 620;
  const pad = 22;
  const bounds = mapBounds(state.mapGeoJSON.features);
  if (!bounds) return;

  const spanX = Math.max(1e-9, bounds.maxX - bounds.minX);
  const spanY = Math.max(1e-9, bounds.maxY - bounds.minY);
  const scale = Math.min(
    (width - pad * 2) / spanX,
    (height - pad * 2) / spanY
  );
  const offsetX = (width - spanX * scale) / 2;
  const offsetY = (height - spanY * scale) / 2;

  const project = ([lon, lat]) => [
    offsetX + (lon - bounds.minX) * scale,
    height - (offsetY + (lat - bounds.minY) * scale),
  ];

  svg.innerHTML = "";
  for (const feature of state.mapGeoJSON.features) {
    const code = String(feature.properties?.codigo_ibge || feature.id || "");
    const municipality = state.municipalities.find((m) => m.codigo_ibge === code);
    const entry = annualByCode.get(code) || { status: "ausente", value: null };

    const commands = [];
    for (const ring of geometryRings(feature.geometry)) {
      if (!ring.length) continue;
      ring.forEach((point, index) => {
        const [x, y] = project(point);
        commands.push(`${index === 0 ? "M" : "L"} ${x.toFixed(2)} ${y.toFixed(2)}`);
      });
      commands.push("Z");
    }

    const path = document.createElementNS("http://www.w3.org/2000/svg", "path");
    path.setAttribute("d", commands.join(" "));
    path.setAttribute(
      "class",
      `map-feature${entry.status !== "observado" ? " is-missing" : ""}${code === state.currentMunicipality ? " is-selected" : ""}`
    );
    path.setAttribute("fill", mapFill(entry.value, breaks));
    path.dataset.code = code;

    const title = document.createElementNS("http://www.w3.org/2000/svg", "title");
    title.textContent =
      `${municipality?.nome || code}: ${formatValue(entry.value, doc)} (${statusLabel(entry.status)})`;
    path.appendChild(title);

    path.addEventListener("click", async () => {
      state.currentMunicipality = code;
      $("#municipality-select").value = code;
      await loadMunicipal();
      renderOverview();
      renderSeries();
      renderMap();
      renderThemes();
    });

    svg.appendChild(path);
  }

  const labels = [];
  let previous = -Infinity;
  for (const cut of [...breaks, Infinity]) {
    const text = cut === Infinity
      ? `> ${formatValue(previous, doc)}`
      : previous === -Infinity
        ? `≤ ${formatValue(cut, doc)}`
        : `${formatValue(previous, doc)} – ${formatValue(cut, doc)}`;
    labels.push(text);
    previous = cut;
  }
  legend.innerHTML = labels.map((label, index) => `
    <span>
      <i class="map-swatch" style="background:${mapFill(
        index < breaks.length ? breaks[index] : Number.MAX_SAFE_INTEGER,
        breaks
      )}"></i>
      ${label}
    </span>
  `).join("") + '<span><i class="map-swatch" style="background:#dfe4e9"></i>NA</span>';
}

function renderComparison() {
  const doc = catalogItem(state.currentVariable);
  $("#compare-title").textContent =
    `${doc?.titulo_publico || state.currentVariable} · ${state.currentYear}`;

  const rows = (state.annual?.municipalities || []).map((m) => {
    const entry = m.values?.[state.currentVariable] || {
      status: "ausente",
      value: null,
    };
    return { ...m, entry };
  });

  rows.sort((a, b) => {
    const av = typeof a.entry.value === "number" ? a.entry.value : -Infinity;
    const bv = typeof b.entry.value === "number" ? b.entry.value : -Infinity;
    return bv - av || a.municipio.localeCompare(b.municipio, "pt-BR");
  });

  $("#compare-body").innerHTML = rows.map((row) => `
    <tr>
      <td>${row.municipio}</td>
      <td>${formatValue(row.entry.value, doc)}</td>
      <td>${statusLabel(row.entry.status)}</td>
    </tr>
  `).join("");
}


function renderProfile() {
  const allMarkers = state.municipal?.markers || [];
  const markers = allMarkers.filter(
    (item) => item.status === "observado" && item.valor_texto
  );
  const observedMarkerCount = markers.length;

  $("#marker-list").innerHTML = markers.length
    ? markers.map((item) =>
        `<span class="badge">${item.valor_texto}</span>`
      ).join("") +
      `<p class="muted profile-coverage">${observedMarkerCount}/6 marcadores comparáveis observados nesta janela.</p>`
    : '<span class="muted">Sem marcadores classificáveis por cobertura suficiente nesta janela.</span>';

  const pairs = (state.municipal?.pairs || []).filter(
    (item) => item.ordem_prioritaria !== null
  ).slice(0, 3);
  $("#pair-list").innerHTML = pairs.length
    ? pairs.map((item) => `
        <div class="pair-item">
          <strong>${item.ordem_prioritaria}. ${item.municipio_comparado}</strong>
          <div class="muted">
            ${item.dimensoes_coincidentes}/${item.dimensoes_comparaveis} marcadores coincidentes
            · ${new Intl.NumberFormat("pt-BR", {style:"percent", maximumFractionDigits:0}).format(item.proporcao_coincidencia)}
            ${item.reciproco ? " · recíproco" : ""}
          </div>
        </div>
      `).join("")
    : (
        observedMarkerCount < 4
          ? `<span class="muted">Sem par prioritário: ${observedMarkerCount}/6 marcadores comparáveis observados; são necessários pelo menos 4.</span>`
          : '<span class="muted">Sem pares prioritários disponíveis neste build.</span>'
      );
}

function renderThemes() {
  const municipality = state.municipalities.find(
    (item) => item.codigo_ibge === state.currentMunicipality
  );
  $("#themes-title").textContent =
    `${municipality?.nome || "—"} · ${state.currentYear || "—"}`;

  $("#theme-groups").innerHTML = Object.entries(THEMES).map(([group, ids]) => {
    const cards = ids
      .map((id) => {
        const doc = catalogItem(id);
        if (!doc) return "";
        const entry = variableValue(id);
        return `
          <article class="metric-card">
            <div class="metric-name">${doc.titulo_publico || doc.nome_tecnico || id}</div>
            <div class="metric-value">${formatValue(entry.value, doc)}</div>
            <div class="muted">${statusLabel(entry.status)}</div>
            <button class="link-button" data-help="${id}">Como ler</button>
          </article>
        `;
      })
      .join("");
    return `
      <section class="theme-section panel">
        <h3>${group}</h3>
        <div class="metric-grid">${cards}</div>
      </section>
    `;
  }).join("");
}

function renderSourcesAndCoverage() {
  $("#source-list").innerHTML = (state.references || []).map((item) => `
    <div class="source-item">
      <strong>${item.titulo}</strong>
      <div class="muted">${item.descricao || ""}</div>
      ${item.url ? `<a href="${item.url}" target="_blank" rel="noopener">Abrir fonte</a>` : ""}
    </div>
  `).join("") || '<p class="muted">Nenhuma referência carregada.</p>';

  const doc = catalogItem(state.currentVariable);
  const rows = (state.coverage || []).filter(
    (item) => item.variavel_id === state.currentVariable
  );
  $("#coverage-wrap").innerHTML = `
    <p><strong>${doc?.titulo_publico || doc?.nome_tecnico || state.currentVariable}</strong></p>
    <table class="data-table">
      <thead><tr><th>Ano</th><th>Observado</th><th>Esperado</th><th>Ausente</th><th>Não aplicável</th><th>Em revisão</th></tr></thead>
      <tbody>
        ${rows.map((item) => `
          <tr>
            <td>${item.ano}</td>
            <td>${item.observado}</td>
            <td>${item.esperado}</td>
            <td>${item.ausente}</td>
            <td>${item.nao_aplicavel}</td>
            <td>${item.em_revisao || 0}</td>
          </tr>
        `).join("")}
      </tbody>
    </table>
  `;
}

function renderCrosswalk() {
  const rows = (state.crosswalk || []).filter(
    (item) => item.variavel_id === state.currentVariable
  );
  if (!rows.length) {
    $("#crosswalk-wrap").innerHTML =
      '<p class="muted">Não há regra de crosswalk carregada para a variável selecionada neste build.</p>';
    return;
  }
  $("#crosswalk-wrap").innerHTML = `
    <table class="data-table">
      <thead>
        <tr>
          <th>Período</th><th>Fonte</th><th>Demonstrativo</th><th>Estágio</th>
          <th>Código</th><th>Descrição</th><th>Regra</th><th>Confiança</th>
        </tr>
      </thead>
      <tbody>
        ${rows.map((item) => `
          <tr>
            <td>${item.ano_inicio}–${item.ano_fim}</td>
            <td>${item.fonte_id || "—"}</td>
            <td>${item.demonstrativo || "—"}</td>
            <td>${item.estagio || "—"}</td>
            <td><code>${item.codigo_conta || "—"}</code></td>
            <td>${item.descricao_conta || "—"}</td>
            <td>${item.regra_harmonizacao || "—"}</td>
            <td>${item.confianca || "—"}</td>
          </tr>
        `).join("")}
      </tbody>
    </table>
  `;
}

function showHelp(id) {
  const doc = catalogItem(id);
  if (!doc) return;
  $("#help-content").innerHTML = `
    <p class="eyebrow">${doc.grupo_publico || doc.grupo_tecnico || ""}</p>
    <h2>${doc.titulo_publico || doc.nome_tecnico}</h2>
    <dl class="definition-grid">
      <dt>Fórmula/definição</dt><dd>${doc.formula_publica || doc.formula_tecnica || "—"}</dd>
      <dt>Componentes</dt><dd>${doc.componentes_publicos || "—"}</dd>
      <dt>Fonte</dt><dd>${doc.fonte_publica || "—"}</dd>
      <dt>Período</dt><dd>${doc.periodo_publico || "—"}</dd>
      <dt>Como ler</dt><dd>${doc.como_ler || "—"}</dd>
      <dt>Limitações</dt><dd>${doc.limitacoes || "—"}</dd>
      <dt>Regra de ausência</dt><dd>${doc.regra_ausencia || "—"}</dd>
    </dl>
    ${doc.url_fonte ? `<p><a href="${doc.url_fonte}" target="_blank" rel="noopener">Abrir fonte oficial</a></p>` : ""}
  `;
  $("#help-dialog").showModal();
}

function renderDictionary(filter = "") {
  const term = filter.trim().toLocaleLowerCase("pt-BR");
  const items = state.catalog.filter((item) => {
    if (!term) return true;
    return [
      item.variavel_id,
      item.titulo_publico,
      item.nome_tecnico,
      item.grupo_publico,
      item.grupo_tecnico,
    ].some((value) =>
      String(value || "").toLocaleLowerCase("pt-BR").includes(term)
    );
  });

  $("#dictionary-list").innerHTML = items.map((item) => `
    <article class="dictionary-item">
      <p class="eyebrow">${item.grupo_publico || item.grupo_tecnico || ""}</p>
      <h3>${item.titulo_publico || item.nome_tecnico}</h3>
      <p><code>${item.variavel_id}</code></p>
      <p>${item.como_ler || item.formula_publica || item.formula_tecnica || ""}</p>
      <button class="link-button" data-help="${item.variavel_id}">Ver definição completa</button>
    </article>
  `).join("");
}

function renderMethodology() {
  $("#methodology-list").innerHTML = state.methodology.map((item) => `
    <article class="methodology-item">
      <p class="eyebrow">${item.secao_id}</p>
      <h3>${item.titulo}</h3>
      <p class="muted">${item.resumo || ""}</p>
      <div>${String(item.corpo_markdown || "")
        .split("\n")
        .filter(Boolean)
        .map((p) => `<p>${p}</p>`)
        .join("")}</div>
    </article>
  `).join("");
}

function csvEscape(value) {
  if (value === null || value === undefined) return "";
  const text = String(value);
  if (/[",\n\r]/.test(text)) return '"' + text.replaceAll('"', '""') + '"';
  return text;
}

function exportCurrentSliceCsv() {
  const rows = state.annual?.municipalities || [];
  const variable = state.currentVariable;
  const lines = [
    ["codigo_ibge", "municipio", "ano", "variavel_id", "valor", "status"],
    ...rows.map((m) => {
      const entry = m.values?.[variable] || { status: "ausente", value: null };
      return [
        m.codigo_ibge,
        m.municipio,
        state.currentYear,
        variable,
        entry.value,
        entry.status || "ausente",
      ];
    }),
  ];
  const csv = lines.map((row) => row.map(csvEscape).join(",")).join("\r\n");
  const blob = new Blob(["\ufeff", csv], { type: "text/csv;charset=utf-8" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = `financas_municipais_sp_${state.currentUniverse}_${state.currentYear}_${variable}.csv`;
  document.body.appendChild(link);
  link.click();
  link.remove();
  URL.revokeObjectURL(url);
}

function selectedUniverse() {
  return state.universes.find(
    (item) => item.universo_id === state.currentUniverse
  ) || null;
}

function universeDataBase(universeId) {
  const item = state.universes.find((row) => row.universo_id === universeId);
  if (!item || item.data_path === ".") return "./data";
  return `./data/${item.data_path}`;
}

function updateBuildMeta() {
  const universe = selectedUniverse();
  $("#build-meta").textContent = [
    universe?.nome || state.metadata?.universe?.nome,
    state.metadata?.build?.data_version,
    state.metadata?.build?.qa_status,
  ].filter(Boolean).join(" · ");
}

function populateUniverseSelect() {
  const select = $("#universe-select");
  select.innerHTML = state.universes.map((item) =>
    `<option value="${item.universo_id}">${item.nome} (${item.municipality_count})</option>`
  ).join("");
  select.value = state.currentUniverse;
}

function populateMunicipalitySelect() {
  $("#municipality-select").innerHTML = state.municipalities.map((m) =>
    `<option value="${m.codigo_ibge}">${m.nome}</option>`
  ).join("");
  $("#municipality-select").value = state.currentMunicipality;
}

function populateYearSelect() {
  const years = state.metadata?.years || [];
  $("#year-select").innerHTML = years.map((year) =>
    `<option value="${year}">${year}</option>`
  ).join("");
  $("#year-select").value = state.currentYear;
}

async function loadAnnual() {
  state.annual = await getJSON(
    `${state.dataBase}/annual/${state.currentYear}.json`
  );
}

async function loadMunicipal() {
  state.municipal = await getJSON(
    `${state.dataBase}/municipalities/${state.currentMunicipality}.json`
  );
}

async function loadUniverse(universeId, { initial = false } = {}) {
  const previousMunicipality = state.currentMunicipality;
  const previousYear = state.currentYear;

  state.currentUniverse = universeId;
  state.dataBase = universeDataBase(universeId);

  [
    state.metadata,
    state.municipalities,
    state.coverage,
  ] = await Promise.all([
    getJSON(`${state.dataBase}/metadata.json`),
    getJSON(`${state.dataBase}/municipalities.json`),
    getJSON(`${state.dataBase}/coverage.json`),
  ]);

  state.mapGeoJSON = await getOptionalJSON(
    `${state.dataBase}/maps/municipalities.geojson`
  );

  const years = state.metadata.years || [];
  state.currentYear = years.includes(previousYear)
    ? previousYear
    : years[years.length - 1];

  const availableCodes = new Set(
    state.municipalities.map((item) => item.codigo_ibge)
  );
  state.currentMunicipality = availableCodes.has(previousMunicipality)
    ? previousMunicipality
    : state.municipalities[0]?.codigo_ibge || null;

  populateUniverseSelect();
  populateMunicipalitySelect();
  populateYearSelect();
  updateBuildMeta();

  if (!initial) {
    await refresh();
  }
}

async function refresh() {
  await Promise.all([loadAnnual(), loadMunicipal()]);
  renderOverview();
  renderSeries();
  renderComparison();
  renderMap();
  renderThemes();
  renderSourcesAndCoverage();
  renderCrosswalk();
}

function bindTabs() {
  $$(".tab").forEach((button) => {
    button.addEventListener("click", () => {
      $$(".tab").forEach((b) => b.classList.remove("is-active"));
      $$(".view").forEach((v) => v.classList.remove("is-active"));
      button.classList.add("is-active");
      $("#" + button.dataset.target).classList.add("is-active");
    });
  });
}

function bindDelegatedHelp() {
  document.addEventListener("click", (event) => {
    const target = event.target.closest("[data-help]");
    if (target) {
      event.preventDefault();
      showHelp(target.dataset.help);
    }
  });
}

async function init() {
  try {
    const universeCatalog = await getOptionalJSON("./data/universes.json");

    [
      state.catalog,
      state.methodology,
      state.references,
      state.crosswalk,
    ] = await Promise.all([
      getJSON("./data/catalog/variables.json"),
      getJSON("./data/methodology/index.json"),
      getJSON("./data/references.json"),
      getJSON("./data/crosswalk.json"),
    ]);

    const rootMetadata = await getJSON("./data/metadata.json");
    state.universes = universeCatalog?.length
      ? universeCatalog
      : [{
          ...rootMetadata.universe,
          municipality_count: rootMetadata.municipality_count,
          default: true,
          data_path: ".",
        }];
    state.currentUniverse =
      state.universes.find((item) => item.default)?.universo_id
      || rootMetadata.universe?.universo_id
      || state.universes[0]?.universo_id;

    $("#variable-select").innerHTML = state.catalog
      .filter((item) => item.titulo_publico)
      .map((item) =>
        `<option value="${item.variavel_id}">${item.titulo_publico}</option>`
      ).join("");
    if (!state.catalog.some((x) => x.variavel_id === state.currentVariable)) {
      state.currentVariable = state.catalog[0]?.variavel_id || null;
    }
    $("#variable-select").value = state.currentVariable;

    await loadUniverse(state.currentUniverse, { initial: true });

    $("#universe-select").addEventListener("change", async (event) => {
      await loadUniverse(event.target.value);
    });

    $("#municipality-select").addEventListener("change", async (event) => {
      state.currentMunicipality = event.target.value;
      await loadMunicipal();
      renderOverview();
      renderSeries();
      renderMap();
      renderThemes();
    });

    $("#year-select").addEventListener("change", async (event) => {
      state.currentYear = Number(event.target.value);
      await loadAnnual();
      renderOverview();
      renderComparison();
      renderMap();
      renderThemes();
    });

    $("#variable-select").addEventListener("change", (event) => {
      state.currentVariable = event.target.value;
      renderSelectedVariable();
      renderSeries();
      renderComparison();
      renderMap();
      renderThemes();
      renderSourcesAndCoverage();
      renderCrosswalk();
    });

    $("#export-csv").addEventListener("click", exportCurrentSliceCsv);

    $("#open-help").addEventListener("click", () =>
      showHelp(state.currentVariable)
    );
    $("#map-help").addEventListener("click", () =>
      showHelp(state.currentVariable)
    );

    $("#dictionary-search").addEventListener("input", (event) =>
      renderDictionary(event.target.value)
    );

    bindTabs();
    bindDelegatedHelp();
    renderDictionary();
    renderMethodology();
    await refresh();
  } catch (error) {
    console.error(error);
    document.body.innerHTML = `
      <main>
        <article class="panel" style="padding:24px;margin-top:24px">
          <h1>Não foi possível carregar o painel</h1>
          <p>${error.message}</p>
        </article>
      </main>
    `;
  }
}

init();
