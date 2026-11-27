const DATA_URL = "./data/transferegov/financial_sp645.json";
const MAP_URL = "./data/maps/municipalities.geojson";
const state = { data: null, map: null, selectedCode: null };

const $ = (selector) => document.querySelector(selector);
const number = new Intl.NumberFormat("pt-BR");
const currency = new Intl.NumberFormat("pt-BR", {
  style: "currency", currency: "BRL", maximumFractionDigits: 0
});

function safeText(value) {
  return String(value ?? "").replace(/[&<>"']/g, (char) => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;"
  })[char]);
}

async function json(url) {
  const response = await fetch(url);
  if (!response.ok) throw new Error(`Falha ao carregar ${url}: ${response.status}`);
  return response.json();
}

function selectedRecords() {
  const stage = $("#stage-select").value;
  const year = Number($("#year-select").value);
  return state.data.records.filter(item => item.stage === stage && item.year === year);
}

function currentRecordMap() {
  return new Map(selectedRecords().map(item => [item.codigo_ibge, item]));
}

function fillBreaks(values, bins = 5) {
  const sorted = values.filter(Number.isFinite).sort((a, b) => a - b);
  if (!sorted.length) return [];
  const cuts = [];
  for (let i = 1; i < bins; i++) {
    cuts.push(sorted[Math.min(sorted.length - 1, Math.floor(i * sorted.length / bins))]);
  }
  return [...new Set(cuts)];
}

function color(value, cuts) {
  if (!Number.isFinite(value)) return "#dfe4e9";
  const palette = ["#e7f0f5", "#c5dae6", "#99bfd3", "#659bb8", "#2f6f95"];
  const index = cuts.findIndex(cut => value <= cut);
  return palette[Math.min(index < 0 ? cuts.length : index, palette.length - 1)];
}

function rings(geometry) {
  if (geometry?.type === "Polygon") return geometry.coordinates;
  if (geometry?.type === "MultiPolygon") return geometry.coordinates.flat();
  return [];
}

function renderMap() {
  const svg = $("#finance-map");
  const features = state.map?.features || [];
  if (!features.length) {
    svg.replaceChildren();
    $("#map-note").textContent = "Cartografia municipal indisponível.";
    return;
  }
  const points = features.flatMap(feature => rings(feature.geometry).flat());
  const bounds = {
    minX: Math.min(...points.map(point => point[0])),
    maxX: Math.max(...points.map(point => point[0])),
    minY: Math.min(...points.map(point => point[1])),
    maxY: Math.max(...points.map(point => point[1])),
  };
  const width = 960, height = 620, pad = 22;
  const scale = Math.min(
    (width - 2 * pad) / Math.max(1e-9, bounds.maxX - bounds.minX),
    (height - 2 * pad) / Math.max(1e-9, bounds.maxY - bounds.minY)
  );
  const offsetX = (width - (bounds.maxX - bounds.minX) * scale) / 2;
  const offsetY = (height - (bounds.maxY - bounds.minY) * scale) / 2;
  const project = ([lon, lat]) => [
    offsetX + (lon - bounds.minX) * scale,
    height - (offsetY + (lat - bounds.minY) * scale),
  ];
  const byCode = currentRecordMap();
  const cuts = fillBreaks([...byCode.values()].map(row => row.net_amount_brl));
  svg.replaceChildren();

  for (const feature of features) {
    const code = String(feature.properties?.codigo_ibge || feature.id || "");
    const row = byCode.get(code);
    const commands = [];
    for (const ring of rings(feature.geometry)) {
      ring.forEach((point, index) => {
        const [x, y] = project(point);
        commands.push(`${index === 0 ? "M" : "L"} ${x.toFixed(2)} ${y.toFixed(2)}`);
      });
      commands.push("Z");
    }
    const path = document.createElementNS("http://www.w3.org/2000/svg", "path");
    path.setAttribute("d", commands.join(" "));
    path.setAttribute("class", "finance-feature");
    path.setAttribute("fill", color(row?.net_amount_brl, cuts));
    path.setAttribute("tabindex", "0");
    const municipality = state.data.municipalities.find(item => item.codigo_ibge === code);
    const title = document.createElementNS("http://www.w3.org/2000/svg", "title");
    title.textContent = row
      ? `${municipality?.municipio || code}: ${currency.format(row.net_amount_brl)} · ${number.format(row.event_count)} eventos`
      : `${municipality?.municipio || code}: sem registro selecionado`;
    path.appendChild(title);
    path.addEventListener("click", () => selectMunicipality(code));
    path.addEventListener("keydown", event => {
      if (event.key === "Enter" || event.key === " ") {
        event.preventDefault();
        selectMunicipality(code);
      }
    });
    svg.appendChild(path);
  }

  const legend = [];
  let lower = -Infinity;
  for (const upper of [...cuts, Infinity]) {
    legend.push(lower === -Infinity
      ? `≤ ${currency.format(upper)}`
      : upper === Infinity
        ? `> ${currency.format(lower)}`
        : `${currency.format(lower)} – ${currency.format(upper)}`);
    lower = upper;
  }
  $("#map-legend").innerHTML = legend.map((label, index) =>
    `<span><i style="background:${color(index < cuts.length ? cuts[index] : Number.MAX_SAFE_INTEGER, cuts)}"></i>${safeText(label)}</span>`
  ).join("") + '<span><i style="background:#dfe4e9"></i>Sem registro</span>';
  $("#map-note").textContent = "As classes representam valores nominais agregados por município proponente, exercício e etapa.";
}

function renderDetails() {
  const code = state.selectedCode;
  const municipality = state.data.municipalities.find(item => item.codigo_ibge === code);
  if (!municipality) {
    $("#municipality-title").textContent = "Selecione um município";
    $("#municipality-summary").textContent = "Clique no mapa ou em uma linha da tabela.";
    $("#municipality-detail").replaceChildren();
    return;
  }
  $("#municipality-title").textContent = municipality.municipio;
  const current = currentRecordMap().get(code);
  $("#municipality-summary").textContent = current
    ? `${number.format(current.event_count)} eventos em ${current.year} · ${number.format(current.instrument_count)} convênios`
    : "Sem registro selecionado nessa etapa e exercício; isso não equivale a valor zero.";

  const rows = state.data.records.filter(item => item.codigo_ibge === code)
    .sort((a, b) => a.year - b.year || a.stage.localeCompare(b.stage));
  $("#municipality-detail").innerHTML = rows.length
    ? `<div class="finance-table-wrap"><table class="finance-table"><thead><tr><th>Ano</th><th>Etapa</th><th>Valor nominal</th></tr></thead><tbody>${rows.map(item =>
      `<tr><td>${item.year}</td><td>${item.stage === "desembolso" ? "Desembolso" : "Pagamento"}</td><td class="num">${currency.format(item.net_amount_brl)}</td></tr>`
    ).join("")}</tbody></table></div>`
    : '<p class="muted">Nenhum evento selecionado para este município.</p>';
}

function renderTable() {
  const stage = $("#stage-select").value;
  const year = Number($("#year-select").value);
  const rowsByCode = currentRecordMap();
  const query = $("#municipality-search").value.trim().toLocaleLowerCase("pt-BR");
  const all = state.data.municipalities.map(municipality => ({
    ...municipality, record: rowsByCode.get(municipality.codigo_ibge) || null
  })).filter(item => item.municipio.toLocaleLowerCase("pt-BR").includes(query));
  all.sort((a, b) =>
    (b.record?.net_amount_brl ?? -Infinity) - (a.record?.net_amount_brl ?? -Infinity)
    || a.municipio.localeCompare(b.municipio, "pt-BR")
  );
  $("#municipality-rows").innerHTML = all.map(item => {
    const r = item.record;
    return `<tr data-code="${safeText(item.codigo_ibge)}" class="${item.codigo_ibge === state.selectedCode ? "selected" : ""}">
      <td>${safeText(item.municipio)}</td>
      <td class="num">${r ? number.format(r.event_count) : "—"}</td>
      <td class="num">${r ? number.format(r.instrument_count) : "—"}</td>
      <td class="num">${r ? currency.format(r.net_amount_brl) : "Sem registro"}</td>
      <td class="num">${r ? number.format(r.negative_events) : "—"}</td>
      <td class="num">${r ? number.format(r.zero_events) : "—"}</td>
    </tr>`;
  }).join("");
  $("#table-empty").hidden = all.length > 0;
  document.querySelectorAll("#municipality-rows tr[data-code]").forEach(row =>
    row.addEventListener("click", () => selectMunicipality(row.dataset.code))
  );

  const records = selectedRecords();
  const events = records.reduce((sum, item) => sum + item.event_count, 0);
  const amount = records.reduce((sum, item) => sum + item.net_amount_brl, 0);
  $("#kpi-amount").textContent = currency.format(amount);
  $("#kpi-events").textContent = number.format(events);
  $("#kpi-coverage").textContent = `${number.format(new Set(records.map(item => item.codigo_ibge)).size)} / 645`;
  $("#map-title").textContent = `${stage === "desembolso" ? "Desembolsos" : "Pagamentos"} · ${year}`;
  $("#load-status").textContent = `Fonte oficial Transferegov · ${number.format(records.length)} agregações municipais registradas nesta seleção.`;
}

function selectMunicipality(code) {
  state.selectedCode = code;
  renderTable();
  renderDetails();
}

function csvExport() {
  const year = Number($("#year-select").value);
  const stage = $("#stage-select").value;
  const rowsByCode = currentRecordMap();
  const header = ["codigo_ibge", "municipio", "ano", "etapa", "status", "eventos", "convenios", "valor_nominal_brl", "eventos_negativos", "eventos_zerados"];
  const lines = [header.join(";")];
  for (const municipality of state.data.municipalities) {
    const row = rowsByCode.get(municipality.codigo_ibge);
    lines.push([
      municipality.codigo_ibge,
      municipality.municipio,
      year,
      stage,
      row ? "observado" : "sem_registro",
      row?.event_count ?? "",
      row?.instrument_count ?? "",
      row ? row.net_amount_brl.toFixed(2).replace(".", ",") : "",
      row?.negative_events ?? "",
      row?.zero_events ?? "",
    ].map(value => `"${String(value).replaceAll('"', '""')}"`).join(";"));
  }
  const blob = new Blob(["\ufeff" + lines.join("\r\n")], {type:"text/csv;charset=utf-8"});
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = `transferegov_sp645_${stage}_${year}.csv`;
  link.click();
  URL.revokeObjectURL(url);
}

async function init() {
  try {
    const [data, map] = await Promise.all([json(DATA_URL), json(MAP_URL)]);
    state.data = data;
    state.map = map;
    const years = [...data.years].sort((a, b) => b - a);
    $("#year-select").innerHTML = years.map(year => `<option value="${year}">${year}</option>`).join("");
    $("#source-note").textContent =
      `Fonte: ${data.source.name}. Recorte pelo município proponente; atualização vinculada ao staging ${data.source.staging_run}. Valores nominais e agregados por ano e etapa.`;
    const defaultYear = years[0];
    $("#year-select").value = String(defaultYear);
    $("#stage-select").addEventListener("change", () => {
      renderTable(); renderMap(); renderDetails();
    });
    $("#year-select").addEventListener("change", () => {
      renderTable(); renderMap(); renderDetails();
    });
    $("#municipality-search").addEventListener("input", renderTable);
    $("#export-csv").addEventListener("click", csvExport);
    const initial = selectedRecords().sort((a, b) => b.net_amount_brl - a.net_amount_brl)[0];
    if (initial) state.selectedCode = initial.codigo_ibge;
    renderTable(); renderMap(); renderDetails();
  } catch (error) {
    $("#load-status").textContent = error.message;
    $("#load-status").classList.add("error");
  }
}

init();
