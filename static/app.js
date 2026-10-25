/**
 * Dota 2 Draft Assistant & Heroes Encyclopedia
 * Reactive Frontend Application
 */

const tg = window.Telegram?.WebApp;
if (tg) {
  try {
    tg.ready();
    tg.expand();
    if (tg.setHeaderColor) tg.setHeaderColor('#0a0d14');
    if (tg.setBackgroundColor) tg.setBackgroundColor('#0b0e14');
  } catch (e) {
    console.warn("Telegram WebApp API init warning:", e);
  }
}

function haptic(type = 'light') {
  try {
    if (tg?.HapticFeedback) {
      tg.HapticFeedback.impactOccurred(type);
    }
  } catch (e) {}
}

// ── GLOBAL APPLICATION STATE ──
const state = {
  activeTab: 'draft', // 'draft' | 'heroes'
  heroes: [],
  heroMap: {},
  allies: [],   // Array of hero_id (up to 5)
  enemies: [],  // Array of hero_id (up to 5)
  role: null,   // null (any) or 1..5
  modalTarget: null, // { type: 'enemy'|'ally', slotIndex: number }
  attrFilter: 'all',
  searchQuery: '',

  // Recommendations
  rawRecommendations: [],
  recomTypeFilter: 'all', // 'all' | 'meta_counter' | 'situational' | 'meta'
  teamCounterItems: [],

  // Wiki tab
  wikiAttrFilter: 'all',
  wikiRoleFilter: 'all',
  wikiSearchQuery: '',

  // Active guide modal hero
  currentGuideHeroId: null,
};

// ── DOM ELEMENTS ──
// Views & Tabs
const viewDraft = document.getElementById('view-draft');
const viewHeroes = document.getElementById('view-heroes');
const tabBtnDraft = document.getElementById('tab-btn-draft');
const tabBtnHeroes = document.getElementById('tab-btn-heroes');
const bottomNavDraft = document.getElementById('bottom-nav-draft');
const bottomNavHeroes = document.getElementById('bottom-nav-heroes');
const patchBadge = document.getElementById('patch-badge');
const patchName = document.getElementById('patch-name');

// Draft Board
const enemySlotsEl = document.getElementById('enemy-slots');
const allySlotsEl = document.getElementById('ally-slots');
const enemyCountEl = document.getElementById('enemy-count');
const allyCountEl = document.getElementById('ally-count');
const roleSelector = document.getElementById('role-selector');
const activeRoleLabel = document.getElementById('active-role-label');
const btnReset = document.getElementById('btn-reset');

// Team Counter Items
const teamCounterPanel = document.getElementById('team-counter-items-panel');
const teamCounterContainer = document.getElementById('team-counter-items-container');

// Recommendations
const recomContainer = document.getElementById('recommendations-container');
const recomStatusEl = document.getElementById('recom-status');
const recomCounterEl = document.getElementById('recom-counter');
const recomTypeFilterEl = document.getElementById('recom-type-filter');

// Hero Picker Modal
const modalEl = document.getElementById('hero-modal');
const modalTitle = document.getElementById('modal-title');
const modalClose = document.getElementById('modal-close');
const heroSearch = document.getElementById('hero-search');
const searchClear = document.getElementById('search-clear');
const attrFilterEl = document.getElementById('attr-filter');
const heroGrid = document.getElementById('hero-grid');

// Wiki View Elements
const wikiSearch = document.getElementById('wiki-search');
const wikiSearchClear = document.getElementById('wiki-search-clear');
const wikiAttrFilterEl = document.getElementById('wiki-attr-filter');
const wikiRoleFilterEl = document.getElementById('wiki-role-filter');
const wikiHeroGrid = document.getElementById('wiki-hero-grid');
const wikiTotalCount = document.getElementById('wiki-total-count');

// Hero Guide Modal Elements
const guideModal = document.getElementById('guide-modal');
const guideModalClose = document.getElementById('guide-modal-close');
const guideModalCloseBtn = document.getElementById('guide-modal-close-btn');
const guideHeroIcon = document.getElementById('guide-hero-icon');
const guideHeroName = document.getElementById('guide-hero-name');
const guideHeroEnName = document.getElementById('guide-hero-en-name');
const guideHeroAttr = document.getElementById('guide-hero-attr');
const guideHeroTier = document.getElementById('guide-hero-tier');
const guideHeroWinrate = document.getElementById('guide-hero-winrate');
const guideHeroRoles = document.getElementById('guide-hero-roles');
const guideCoreItemsList = document.getElementById('guide-core-items-list');
const guideCounterItemsList = document.getElementById('guide-counter-items-list');
const guideHardCountersList = document.getElementById('guide-hard-counters-list');
const guideStrongAgainstList = document.getElementById('guide-strong-against-list');
const guideSynergiesList = document.getElementById('guide-synergies-list');
const guideTacticsStrengths = document.getElementById('guide-tactics-strengths');
const guideTacticsWeaknesses = document.getElementById('guide-tactics-weaknesses');
const guideTacticsHowTo = document.getElementById('guide-tactics-how-to');
const guideAddAlly = document.getElementById('guide-add-ally');
const guideAddEnemy = document.getElementById('guide-add-enemy');

const ROLE_LABELS = {
  1: "Поз 1 (Керри)",
  2: "Поз 2 (Мид)",
  3: "Оффлейн (Поз 3)",
  4: "Семи-саппорт (Поз 4)",
  5: "Фулл-саппорт (Поз 5)",
};

const ATTR_NAMES_RU = {
  str: "Сила",
  agi: "Ловкость",
  int: "Интеллект",
  all: "Универсал"
};

// ── INITIALIZATION ──

async function init() {
  renderEmptySlots();
  setupEventListeners();

  // Load patch info in background
  fetchPatchInfo();

  try {
    const res = await fetch('/api/heroes');
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    state.heroes = await res.json();
    state.heroes.sort((a, b) => (a.localized_name || '').localeCompare(b.localized_name || ''));
    state.heroes.forEach(h => state.heroMap[h.id] = h);

    if (wikiTotalCount) wikiTotalCount.innerText = state.heroes.length;
    renderWikiHeroes();
    
    // Initial recommendations calculation
    await updateRecommendations();
  } catch (err) {
    console.error("Failed to load heroes:", err);
    recomContainer.innerHTML = `
      <div class="p-6 text-center text-rose-400 bg-dota-card rounded-xl border border-rose-900/40">
        Ошибка загрузки базы героев. Попробуйте обновить страницу.
      </div>
    `;
  }
}

async function fetchPatchInfo() {
  try {
    const res = await fetch('/api/patch');
    if (res.ok) {
      const data = await res.json();
      if (patchName && data.patch) {
        patchName.innerText = data.patch;
        patchBadge?.classList.remove('hidden');
      }
    }
  } catch (e) {
    console.warn("Could not fetch patch:", e);
  }
}

// ── TAB SWITCHING ──

function switchTab(tab) {
  haptic();
  state.activeTab = tab;
  if (tab === 'draft') {
    if (viewDraft) viewDraft.classList.remove('hidden');
    if (viewHeroes) viewHeroes.classList.add('hidden');
    if (tabBtnDraft) tabBtnDraft.className = "px-3 py-1.5 text-xs font-bold rounded-lg transition flex items-center gap-1.5 tab-active";
    if (tabBtnHeroes) tabBtnHeroes.className = "px-3 py-1.5 text-xs font-semibold rounded-lg text-slate-400 hover:text-white transition flex items-center gap-1.5";
    if (bottomNavDraft) bottomNavDraft.className = "flex flex-col items-center gap-1 text-xs font-bold text-amber-400 transition";
    if (bottomNavHeroes) bottomNavHeroes.className = "flex flex-col items-center gap-1 text-xs font-semibold text-slate-400 hover:text-white transition";
  } else {
    if (viewDraft) viewDraft.classList.add('hidden');
    if (viewHeroes) viewHeroes.classList.remove('hidden');
    if (tabBtnHeroes) tabBtnHeroes.className = "px-3 py-1.5 text-xs font-bold rounded-lg transition flex items-center gap-1.5 tab-active";
    if (tabBtnDraft) tabBtnDraft.className = "px-3 py-1.5 text-xs font-semibold rounded-lg text-slate-400 hover:text-white transition flex items-center gap-1.5";
    if (bottomNavDraft) bottomNavDraft.className = "flex flex-col items-center gap-1 text-xs font-semibold text-slate-400 hover:text-white transition";
    if (bottomNavHeroes) bottomNavHeroes.className = "flex flex-col items-center gap-1 text-xs font-bold text-amber-400 transition";
    renderWikiHeroes();
  }
}

// ── DRAFT BOARD SLOTS ──

function renderEmptySlots() {
  // 5 Enemy Slots
  enemySlotsEl.innerHTML = '';
  for (let i = 0; i < 5; i++) {
    const heroId = state.enemies[i];
    enemySlotsEl.appendChild(createSlotElement('enemy', i, heroId));
  }
  enemyCountEl.innerText = state.enemies.length;

  // 5 Ally Slots
  allySlotsEl.innerHTML = '';
  for (let i = 0; i < 5; i++) {
    const heroId = state.allies[i];
    allySlotsEl.appendChild(createSlotElement('ally', i, heroId));
  }
  allyCountEl.innerText = state.allies.length;
}

function createSlotElement(type, index, heroId) {
  const isEnemy = type === 'enemy';
  const hero = heroId ? state.heroMap[heroId] : null;

  const div = document.createElement('div');
  
  if (hero) {
    div.className = `relative aspect-square rounded-xl overflow-hidden border-2 cursor-pointer transition-all hover:scale-105 shadow-md ${
      isEnemy ? 'border-rose-600 glow-red' : 'border-emerald-500 glow-green'
    }`;
    div.innerHTML = `
      <img src="${hero.icon_url}" alt="${hero.localized_name_ru}" onerror="this.onerror=null;this.src='https://cdn.cloudflare.steamstatic.com/apps/dota2/images/dota_react/heroes/pudge.png';" class="w-full h-full object-cover">
      <div class="absolute inset-0 bg-gradient-to-t from-black/80 via-transparent to-black/20 flex flex-col justify-between p-1">
        <span class="self-end text-[10px] text-white/90 bg-black/60 rounded px-1 leading-tight hover:text-rose-400 font-bold" title="Удалить">✕</span>
        <span class="text-[9px] font-bold text-white truncate drop-shadow leading-tight">${hero.localized_name}</span>
      </div>
    `;
    div.onclick = () => removeHeroFromSlot(type, index);
  } else {
    div.className = `relative aspect-square rounded-xl border border-dashed flex flex-col items-center justify-center cursor-pointer transition-all hover:bg-slate-800/40 ${
      isEnemy ? 'border-rose-900/60 text-rose-500/60 hover:border-rose-600' : 'border-emerald-900/60 text-emerald-500/60 hover:border-emerald-600'
    }`;
    div.innerHTML = `
      <span class="text-lg leading-none font-bold">+</span>
      <span class="text-[9px] font-semibold uppercase mt-0.5">${isEnemy ? 'Враг' : 'Союзник'}</span>
    `;
    div.onclick = () => openPickerModal(type, index);
  }
  return div;
}

function removeHeroFromSlot(type, index) {
  haptic('medium');
  if (type === 'enemy') {
    state.enemies.splice(index, 1);
  } else {
    state.allies.splice(index, 1);
  }
  renderEmptySlots();
  updateRecommendations();
}

function resetDraft() {
  haptic('medium');
  state.allies = [];
  state.enemies = [];
  state.role = null;
  activeRoleLabel.innerText = "Любая роль";
  document.querySelectorAll('.role-btn').forEach(btn => {
    btn.classList.toggle('active', btn.dataset.role === "");
    btn.className = btn.dataset.role === "" 
      ? "role-btn active px-2 py-1.5 rounded-lg text-xs font-semibold bg-amber-500/20 text-amber-400 border border-amber-500/40 flex flex-col items-center justify-center transition"
      : "role-btn px-2 py-1.5 rounded-lg text-xs font-semibold bg-dota-card text-slate-300 border border-dota-border hover:border-slate-600 flex flex-col items-center justify-center transition";
  });
  renderEmptySlots();
  updateRecommendations();
}

// ── RECOMMENDATIONS ──

let recommendReqSeq = 0;

async function updateRecommendations() {
  const reqId = ++recommendReqSeq;
  recomStatusEl.innerText = "Расчет...";
  const payload = {
    ally_ids: state.allies,
    enemy_ids: state.enemies,
    role: state.role,
    top_k: 20
  };

  for (let attempt = 1; attempt <= 2; attempt++) {
    try {
      const res = await fetch('/api/recommend', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();
      if (reqId !== recommendReqSeq) return;

      state.rawRecommendations = data.recommendations || [];
      state.teamCounterItems = data.team_counter_items || [];

      renderTeamCounterItems(state.teamCounterItems);
      filterAndRenderRecommendations();
      recomStatusEl.innerText = "";
      return;
    } catch (err) {
      if (reqId !== recommendReqSeq) return;
      if (attempt < 2) {
        await new Promise(r => setTimeout(r, 400));
        continue;
      }
      console.error("Draft recommendation error:", err);
      if (!state.rawRecommendations || state.rawRecommendations.length === 0) {
        recomStatusEl.innerText = "Ошибка";
      } else {
        recomStatusEl.innerText = "";
      }
    }
  }
}

function renderTeamCounterItems(items) {
  if (!items || items.length === 0 || state.enemies.length === 0) {
    teamCounterPanel.classList.add('hidden');
    return;
  }

  teamCounterPanel.classList.remove('hidden');
  teamCounterContainer.innerHTML = items.map(item => `
    <div class="bg-slate-950/90 border border-slate-700/60 rounded-xl p-2 flex items-center gap-2 hover:border-amber-500/50 transition shadow" title="${item.reason}">
      <img src="${item.icon_url}" alt="${item.name_ru}" onerror="this.onerror=null;this.src='https://cdn.cloudflare.steamstatic.com/apps/dota2/images/dota_react/items/branches.png';" class="w-8 h-8 rounded-lg object-cover shrink-0 border border-amber-500/40">
      <div class="min-w-0">
        <h4 class="text-[11px] font-bold text-white truncate leading-tight">${item.name_ru}</h4>
        <p class="text-[9px] text-amber-300/80 truncate leading-tight">${item.reason}</p>
      </div>
    </div>
  `).join('');
}

function filterAndRenderRecommendations() {
  let filtered = state.rawRecommendations;

  if (state.recomTypeFilter === 'situational') {
    filtered = filtered.filter(item => 
      item.category === 'situational' || item.category === 'hybrid' || 
      item.pick_type === 'situational' || item.pick_type === 'meta_counter'
    );
  } else if (state.recomTypeFilter === 'meta') {
    filtered = filtered.filter(item => 
      item.category === 'meta' || item.category === 'hybrid' || 
      item.pick_type === 'meta' || item.pick_type === 'meta_counter'
    );
  }

  renderRecommendations(filtered);
}

function renderRecommendations(items) {
  if (recomCounterEl) {
    recomCounterEl.innerText = `Показано: ${items ? items.length : 0}`;
  }

  if (!items || items.length === 0) {
    recomContainer.innerHTML = `
      <div class="p-8 text-center text-slate-400 bg-dota-card rounded-xl border border-dota-border">
        Нет доступных рекомендаций для выбранных фильтров.
      </div>
    `;
    return;
  }

  recomContainer.innerHTML = '';
  items.forEach((item, idx) => {
    const b = item.breakdown || {};
    const totalScore = typeof b.total_score === 'number' ? b.total_score : item.score;
    
    // Pick Type & Category Banner
    let pickTypeBadge = '';
    const isHybrid = item.category === 'hybrid' || item.pick_type === 'meta_counter';
    const isSituational = item.category === 'situational' || item.pick_type === 'situational';

    if (isHybrid) {
      pickTypeBadge = `<span class="text-[10px] font-bold px-2 py-0.5 rounded bg-gradient-to-r from-amber-600/30 to-red-600/30 text-amber-300 border border-amber-500/50">🔥 МЕТА + КОНТРПИК</span>`;
    } else if (isSituational) {
      pickTypeBadge = `<span class="text-[10px] font-bold px-2 py-0.5 rounded bg-gradient-to-r from-cyan-600/30 to-blue-600/30 text-cyan-300 border border-cyan-500/50">⚡ СИТУАТИВНЫЙ КОНТРПИК</span>`;
    } else {
      pickTypeBadge = `<span class="text-[10px] font-bold px-2 py-0.5 rounded bg-purple-950/40 text-purple-300 border border-purple-500/40">👑 МЕТА ПАТЧА</span>`;
    }

    // Color thresholds for 0-100 score
    const scoreColor = totalScore >= 70.0 ? 'text-emerald-400 border-emerald-500/50 bg-emerald-500/15' :
                       totalScore >= 50.0 ? 'text-amber-400 border-amber-500/50 bg-amber-500/15' :
                                            'text-rose-400 border-rose-500/50 bg-rose-500/15';

    const scoreBarWidth = Math.max(5, Math.min(100, totalScore));
    const scoreBarColor = totalScore >= 70.0 ? 'bg-emerald-500' :
                          totalScore >= 50.0 ? 'bg-amber-500' : 'bg-rose-500';

    const tierBadge = b.tier === 'S' ? 'bg-amber-500/20 text-amber-300 border-amber-500/40' :
                      b.tier === 'A' ? 'bg-purple-500/20 text-purple-300 border-purple-500/40' :
                                       'bg-slate-700/40 text-slate-400 border-slate-600/40';

    const card = document.createElement('div');
    card.className = "bg-dota-card border border-dota-border hover:border-slate-600 rounded-xl p-3 sm:p-3.5 flex flex-col gap-2.5 transition-all shadow-md";
    
    // Badges HTML
    let badgesHtml = (b.badges || []).map(badge => `
      <span class="inline-flex items-center gap-1 text-[11px] font-semibold px-2 py-0.5 rounded bg-blue-950/60 text-blue-300 border border-blue-700/40">
        ${badge}
      </span>
    `).join('');

    // Pros and Cons tags
    let prosHtml = (b.pros || []).slice(0, 3).map(p => `
      <span class="inline-flex items-center gap-1 text-[11px] px-2 py-0.5 rounded bg-emerald-950/60 text-emerald-300 border border-emerald-800/50">
        ✓ ${p}
      </span>
    `).join('');

    // Concrete Detailed Reason (minimum 15-25 words)
    const concreteReason = item.reason || b.reason || b.summary || "Отличный синергичный выбор под текущую фазу драфта";

    // Core Items row (Стандартная сборка на героя)
    let coreItemsHtml = '';
    if (item.core_items && item.core_items.length > 0) {
      const coreBadges = item.core_items.slice(0, 4).map(it => `
        <div class="flex items-center gap-1.5 bg-slate-900/90 border border-slate-700/70 rounded-lg px-2 py-1 shrink-0 shadow-sm" title="${it.reason}">
          <img src="${it.icon_url}" alt="${it.name}" onerror="this.onerror=null;this.src='https://cdn.cloudflare.steamstatic.com/apps/dota2/images/dota_react/items/branches.png';" class="w-5 h-5 rounded object-cover border border-slate-600">
          <span class="text-[11px] text-slate-200 font-medium whitespace-nowrap">${it.name}</span>
        </div>
      `).join('');

      coreItemsHtml = `
        <div class="flex flex-col gap-1 mt-0.5 pt-2 border-t border-slate-800/80">
          <span class="text-[10px] font-bold text-slate-400 uppercase tracking-wider flex items-center gap-1">
            <span>🎒</span> Стандартная сборка на героя:
          </span>
          <div class="flex flex-wrap items-center gap-1.5">
            ${coreBadges}
          </div>
        </div>
      `;
    }

    // Situational Items row (Собрать против пика врага)
    let situationalItemsHtml = '';
    if (item.situational_items && item.situational_items.length > 0 && state.enemies.length > 0) {
      const sitBadges = item.situational_items.map(it => `
        <div class="bg-amber-950/40 border border-amber-600/40 rounded-lg p-2 flex items-start gap-2 w-full">
          <img src="${it.icon_url}" alt="${it.name}" onerror="this.onerror=null;this.src='https://cdn.cloudflare.steamstatic.com/apps/dota2/images/dota_react/items/branches.png';" class="w-7 h-7 rounded object-cover border border-amber-500/60 shrink-0 mt-0.5">
          <div class="min-w-0 flex-1">
            <span class="text-xs font-bold text-amber-300 block leading-tight">${it.name}</span>
            <p class="text-[11px] text-amber-200/90 leading-tight mt-0.5">${it.reason}</p>
          </div>
        </div>
      `).join('');

      situationalItemsHtml = `
        <div class="flex flex-col gap-1 mt-0.5 pt-2 border-t border-amber-900/50">
          <span class="text-[10px] font-bold text-amber-400 uppercase tracking-wider flex items-center gap-1">
            <span>⚔️</span> Собрать против пика врага:
          </span>
          <div class="flex flex-col gap-1.5">
            ${sitBadges}
          </div>
        </div>
      `;
    }

    card.innerHTML = `
      <div class="flex items-center justify-between gap-3">
        
        <!-- Hero Details -->
        <div class="flex items-center gap-2.5 min-w-0">
          <div class="relative shrink-0 cursor-pointer" onclick="openHeroGuide(${item.hero_id})">
            <span class="absolute -top-1.5 -left-1.5 z-10 w-5 h-5 rounded-full bg-slate-900 border border-slate-700 text-slate-300 text-[10px] font-bold flex items-center justify-center">
              #${idx + 1}
            </span>
            <img src="${item.icon_url}" alt="${item.localized_name_ru}" onerror="this.onerror=null;this.src='https://cdn.cloudflare.steamstatic.com/apps/dota2/images/dota_react/heroes/pudge.png';" class="w-12 h-12 sm:w-14 sm:h-14 rounded-lg object-cover border border-slate-700 shadow hover:border-amber-400 transition">
          </div>
          <div class="min-w-0">
            <div class="flex items-center gap-1.5 flex-wrap">
              <h3 class="text-sm sm:text-base font-bold text-white tracking-wide truncate cursor-pointer hover:text-amber-400 transition" onclick="openHeroGuide(${item.hero_id})">
                ${item.localized_name}
              </h3>
              <span class="text-[11px] text-slate-400 font-normal">
                (${item.localized_name_ru})
              </span>
              <span class="text-[10px] font-bold px-1.5 py-0.2 rounded border ${tierBadge}">
                Тир ${b.tier || 'B'}
              </span>
              ${pickTypeBadge}
              <button onclick="openHeroGuide(${item.hero_id})" class="w-5 h-5 rounded-full bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white flex items-center justify-center font-bold text-[10px] transition" title="Открыть подробный гайд">
                ℹ️
              </button>
            </div>
            <div class="flex items-center gap-2 mt-0.5 text-xs text-slate-400 flex-wrap">
              <span>D2PT WR: <strong class="text-white">${b.meta_winrate?.toFixed(1) || 50.0}%</strong></span>
              <span>•</span>
              <span>Роль: <span class="text-slate-200 font-medium">${b.role_name}</span></span>
            </div>
          </div>
        </div>

        <!-- Rating 0-100 Badge -->
        <div class="flex flex-col items-end shrink-0">
          <div class="px-2.5 py-1 rounded-xl border font-gaming font-bold text-base sm:text-lg tracking-wider ${scoreColor}">
            ${totalScore.toFixed(1)}<span class="text-[11px] font-sans font-normal opacity-70">/100</span>
          </div>
          <span class="text-[10px] text-slate-500 mt-0.5">Общий рейтинг</span>
        </div>

      </div>

      <!-- Concrete 1-Line Explanation -->
      <div class="text-xs text-amber-200/95 font-medium bg-amber-500/10 border border-amber-500/20 rounded-lg px-2.5 py-1.5 flex items-center gap-2">
        <span>🎯</span>
        <span class="leading-tight">${concreteReason}</span>
      </div>

      <!-- Rating Progress Bar -->
      <div class="w-full bg-slate-800 rounded-full h-1.5 overflow-hidden">
        <div class="${scoreBarColor} h-1.5 rounded-full transition-all duration-300" style="width: ${scoreBarWidth}%"></div>
      </div>

      <!-- Badges and Advantages -->
      ${badgesHtml ? `<div class="flex flex-wrap gap-1.5">${badgesHtml}</div>` : ''}
      ${prosHtml ? `<div class="flex flex-wrap gap-1.5">${prosHtml}</div>` : ''}

      <!-- Item Builds -->
      ${coreItemsHtml}

      <!-- Bottom Card Action Buttons -->
      <div class="pt-2 border-t border-slate-800/80 flex items-center justify-between gap-2 text-xs">
        <button onclick="openHeroGuide(${item.hero_id})" class="px-2.5 py-1 rounded-lg text-slate-300 hover:text-white bg-slate-800/60 hover:bg-slate-700/80 border border-slate-700 transition flex items-center gap-1 font-medium">
          <span>📖</span>
          <span>Гайд & Контр-предметы</span>
        </button>
        <div class="flex items-center gap-1.5">
          <button onclick="quickAddHero('ally', ${item.hero_id})" class="px-2.5 py-1 rounded-lg text-emerald-300 hover:text-white bg-emerald-950/60 hover:bg-emerald-900 border border-emerald-800/60 transition font-medium">
            + Союзник
          </button>
          <button onclick="quickAddHero('enemy', ${item.hero_id})" class="px-2.5 py-1 rounded-lg text-rose-300 hover:text-white bg-rose-950/60 hover:bg-rose-900 border border-rose-800/60 transition font-medium">
            + Враг
          </button>
        </div>
      </div>
    `;

    recomContainer.appendChild(card);
  });
}

function quickAddHero(type, heroId) {
  haptic('medium');
  if (type === 'ally') {
    if (state.allies.length >= 5) {
      alert("Слоты союзников заполнены (максимум 5)");
      return;
    }
    if (!state.allies.includes(heroId) && !state.enemies.includes(heroId)) {
      state.allies.push(heroId);
      renderEmptySlots();
      updateRecommendations();
    }
  } else {
    if (state.enemies.length >= 5) {
      alert("Слоты врагов заполнены (максимум 5)");
      return;
    }
    if (!state.enemies.includes(heroId) && !state.allies.includes(heroId)) {
      state.enemies.push(heroId);
      renderEmptySlots();
      updateRecommendations();
    }
  }
}

// ── HEROES ENCYCLOPEDIA (WIKI) VIEW ──

function renderWikiHeroes() {
  if (!wikiHeroGrid) return;
  const q = state.wikiSearchQuery.toLowerCase().trim();
  const attr = state.wikiAttrFilter;
  const role = state.wikiRoleFilter;

  const filtered = state.heroes.filter(h => {
    // 1. Attribute filter
    if (attr !== 'all') {
      const targetAttr = attr === 'all_attr' ? 'all' : attr;
      if (h.primary_attr !== targetAttr) return false;
    }

    // 2. Role filter
    if (role !== 'all') {
      const roleNum = parseInt(role, 10);
      if (!Array.isArray(h.viable_roles) || !h.viable_roles.includes(roleNum)) return false;
    }

    // 3. Search query
    if (!q) return true;
    if (h.localized_name_ru.toLowerCase().includes(q)) return true;
    if (h.localized_name.toLowerCase().includes(q)) return true;
    if (h.aliases && h.aliases.some(a => a.toLowerCase().includes(q))) return true;
    return false;
  });

  if (filtered.length === 0) {
    wikiHeroGrid.innerHTML = `
      <div class="col-span-full py-12 text-center text-slate-400">
        Героев по заданным фильтрам не найдено.
      </div>
    `;
    return;
  }

  filtered.sort((a, b) => (a.localized_name || '').localeCompare(b.localized_name || ''));

  wikiHeroGrid.innerHTML = filtered.map(h => {
    const attrColor = h.primary_attr === 'str' ? 'border-red-900/60 text-red-400' :
                      h.primary_attr === 'agi' ? 'border-emerald-900/60 text-emerald-400' :
                      h.primary_attr === 'int' ? 'border-sky-900/60 text-sky-400' :
                                                 'border-purple-900/60 text-purple-400';

    const winrateDisplay = h.winrate ? `${h.winrate.toFixed(1)}%` : '50.0%';
    const wrColor = (h.winrate || 50) >= 52.0 ? 'text-emerald-400 border-emerald-500/40 bg-emerald-950/80' :
                    (h.winrate || 50) >= 49.0 ? 'text-amber-400 border-amber-500/40 bg-amber-950/80' :
                                                'text-rose-400 border-rose-500/40 bg-rose-950/80';

    return `
      <div onclick="openHeroGuide(${h.id})" class="bg-dota-card border border-dota-border hover:border-amber-500/60 rounded-xl p-2 flex flex-col items-center gap-1.5 cursor-pointer transition-all hover:scale-105 shadow relative group">
        <div class="relative w-full aspect-video rounded-lg overflow-hidden border border-slate-700">
          <img src="${h.icon_url}" alt="${h.localized_name}" onerror="this.onerror=null;this.src='https://cdn.cloudflare.steamstatic.com/apps/dota2/images/dota_react/heroes/pudge.png';" class="w-full h-full object-cover">
          <span class="absolute top-1 right-1 text-[9px] font-bold px-1.5 py-0.2 rounded border shadow ${wrColor}">
            ${winrateDisplay}
          </span>
        </div>
        <div class="w-full text-center min-w-0">
          <h4 class="text-xs font-bold text-white truncate leading-tight group-hover:text-amber-300 transition">${h.localized_name}</h4>
          <span class="text-[10px] text-slate-400 truncate block leading-tight">${h.localized_name_ru}</span>
        </div>
        <span class="text-[9px] font-semibold px-1.5 py-0.2 rounded border ${attrColor}">
          ${ATTR_NAMES_RU[h.primary_attr] || h.primary_attr}
        </span>
      </div>
    `;
  }).join('');
}

// ── RICH HERO GUIDE MODAL ──

async function openHeroGuide(heroId) {
  haptic('light');
  state.currentGuideHeroId = heroId;
  const hero = state.heroMap[heroId];
  if (!hero) return;

  // Set initial placeholders
  guideHeroIcon.src = hero.icon_url;
  guideHeroName.innerText = hero.localized_name;
  guideHeroEnName.innerText = hero.localized_name_ru ? `(${hero.localized_name_ru})` : '';
  guideHeroAttr.innerText = ATTR_NAMES_RU[hero.primary_attr] || hero.primary_attr;
  guideHeroRoles.innerText = Array.isArray(hero.roles) ? hero.roles.join(', ') : hero.roles;
  guideHeroTier.innerText = hero.tier ? `Тир ${hero.tier}` : "Тир ...";
  guideHeroWinrate.innerText = hero.winrate ? `${hero.winrate.toFixed(1)}%` : "...";

  if (guideCoreItemsList) guideCoreItemsList.innerHTML = `<div class="col-span-2 text-center text-slate-400 py-4">Загрузка данных гайда...</div>`;
  guideCounterItemsList.innerHTML = `<div class="col-span-2 text-center text-slate-400 py-4">Загрузка данных гайда...</div>`;
  guideHardCountersList.innerHTML = `<div class="text-center text-slate-400 py-2">Загрузка...</div>`;
  guideStrongAgainstList.innerHTML = `<div class="text-center text-slate-400 py-2">Загрузка...</div>`;
  guideSynergiesList.innerHTML = `<div class="text-center text-slate-400 py-2">Загрузка...</div>`;
  guideTacticsStrengths.innerText = "Загрузка...";
  guideTacticsWeaknesses.innerText = "Загрузка...";
  guideTacticsHowTo.innerText = "Загрузка...";

  guideModal.classList.remove('hidden');

  try {
    const res = await fetch(`/api/heroes/${heroId}/guide`);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();
    const g = data.guide;

    // Header info
    guideHeroTier.innerText = `Тир ${g.meta?.tier || 'B'}`;
    guideHeroWinrate.innerText = `${g.meta?.winrate?.toFixed(1) || 50.0}%`;

    // 1A. Core Items (Что обычно собирают на героя)
    if (guideCoreItemsList) {
      if (g.core_items && g.core_items.length > 0) {
        guideCoreItemsList.innerHTML = g.core_items.map(item => `
          <div class="bg-slate-950 border border-emerald-900/50 rounded-xl p-2.5 flex items-start gap-2.5 shadow hover:border-emerald-500/50 transition">
            <img src="${item.icon_url}" alt="${item.name_ru || item.name}" onerror="this.onerror=null;this.src='https://cdn.cloudflare.steamstatic.com/apps/dota2/images/dota_react/items/branches.png';" class="w-10 h-10 rounded-lg object-cover shrink-0 border border-emerald-500/50">
            <div class="min-w-0 flex-1">
              <h4 class="text-xs font-bold text-emerald-300 leading-tight">${item.name_ru || item.name} (${item.name})</h4>
              <p class="text-[11px] text-slate-300 mt-1 leading-snug break-words">${item.reason}</p>
            </div>
          </div>
        `).join('');
      } else {
        guideCoreItemsList.innerHTML = `<div class="col-span-2 text-slate-400">Стандартная сборка формируется по ходу матча.</div>`;
      }
    }

    // 1B. Counter Items (Предметы против этого героя)
    if (g.counter_items && g.counter_items.length > 0) {
      guideCounterItemsList.innerHTML = g.counter_items.map(item => `
        <div class="bg-slate-950 border border-amber-900/50 rounded-xl p-2.5 flex items-start gap-2.5 shadow hover:border-amber-500/50 transition">
          <img src="${item.icon_url}" alt="${item.name_ru || item.name}" onerror="this.onerror=null;this.src='https://cdn.cloudflare.steamstatic.com/apps/dota2/images/dota_react/items/branches.png';" class="w-10 h-10 rounded-lg object-cover shrink-0 border border-amber-500/50">
          <div class="min-w-0 flex-1">
            <h4 class="text-xs font-bold text-amber-300 leading-tight">${item.name_ru || item.name} (${item.name})</h4>
            <p class="text-[11px] text-slate-300 mt-1 leading-snug break-words">${item.reason}</p>
          </div>
        </div>
      `).join('');
    } else {
      guideCounterItemsList.innerHTML = `<div class="col-span-2 text-slate-400">Стандартные защитные предметы: BKB, Scythe of Vyse, Ghost Scepter.</div>`;
    }

    // 2. Hard Counters (Top 6)
    if (g.hard_counters && g.hard_counters.length > 0) {
      guideHardCountersList.innerHTML = g.hard_counters.map(c => `
        <div onclick="openHeroGuide(${c.hero_id})" class="bg-slate-950/80 border border-rose-900/40 rounded-xl p-2.5 flex items-start gap-2.5 hover:border-rose-500/50 transition cursor-pointer">
          <img src="${c.icon_url}" alt="${c.name_ru}" onerror="this.onerror=null;this.src='https://cdn.cloudflare.steamstatic.com/apps/dota2/images/dota_react/heroes/pudge.png';" class="w-9 h-9 rounded-lg object-cover shrink-0 border border-rose-700/60 mt-0.5">
          <div class="min-w-0 flex-1">
            <div class="flex items-center justify-between gap-1">
              <strong class="text-xs text-white font-semibold truncate">${c.name}</strong>
              <span class="text-[11px] text-rose-400 font-bold shrink-0">${c.advantage > 0 ? '+' : ''}${c.advantage}%</span>
            </div>
            <p class="text-[11px] text-slate-300 mt-1 leading-snug break-words">${c.reason}</p>
          </div>
        </div>
      `).join('');
    } else {
      guideHardCountersList.innerHTML = `<div class="text-slate-400 text-xs">Нет критических контр-пиков.</div>`;
    }

    // 3. Strong Against (Top 6)
    if (g.strong_against && g.strong_against.length > 0) {
      guideStrongAgainstList.innerHTML = g.strong_against.map(s => `
        <div onclick="openHeroGuide(${s.hero_id})" class="bg-slate-950/80 border border-emerald-900/40 rounded-xl p-2.5 flex items-start gap-2.5 hover:border-emerald-500/50 transition cursor-pointer">
          <img src="${s.icon_url}" alt="${s.name_ru}" onerror="this.onerror=null;this.src='https://cdn.cloudflare.steamstatic.com/apps/dota2/images/dota_react/heroes/pudge.png';" class="w-9 h-9 rounded-lg object-cover shrink-0 border border-emerald-700/60 mt-0.5">
          <div class="min-w-0 flex-1">
            <div class="flex items-center justify-between gap-1">
              <strong class="text-xs text-white font-semibold truncate">${s.name}</strong>
              <span class="text-[11px] text-emerald-400 font-bold shrink-0">+${s.advantage}%</span>
            </div>
            <p class="text-[11px] text-slate-300 mt-1 leading-snug break-words">${s.reason}</p>
          </div>
        </div>
      `).join('');
    } else {
      guideStrongAgainstList.innerHTML = `<div class="text-slate-400 text-xs">Нейтральный матчап против большинства героев.</div>`;
    }

    // 4. Synergies (Top 5)
    if (g.best_synergies && g.best_synergies.length > 0) {
      guideSynergiesList.innerHTML = g.best_synergies.map(syn => `
        <div onclick="openHeroGuide(${syn.hero_id})" class="bg-slate-950/80 border border-blue-900/40 rounded-xl p-2.5 flex items-start gap-2.5 hover:border-blue-500/50 transition cursor-pointer">
          <img src="${syn.icon_url}" alt="${syn.name_ru}" onerror="this.onerror=null;this.src='https://cdn.cloudflare.steamstatic.com/apps/dota2/images/dota_react/heroes/pudge.png';" class="w-9 h-9 rounded-lg object-cover shrink-0 border border-blue-700/60 mt-0.5">
          <div class="min-w-0 flex-1">
            <div class="flex items-center justify-between gap-1">
              <strong class="text-xs text-white font-semibold truncate">${syn.name}</strong>
              <span class="text-[11px] text-blue-300 font-bold shrink-0">+${syn.synergy}%</span>
            </div>
            <p class="text-[11px] text-slate-300 mt-1 leading-snug break-words">${syn.reason}</p>
          </div>
        </div>
      `).join('');
    } else {
      guideSynergiesList.innerHTML = `<div class="col-span-2 text-slate-400 text-xs">Универсальный герой, работает в любых связках.</div>`;
    }

    // 5. Tactics
    guideTacticsStrengths.innerText = g.tactics?.strengths || "Высокий потенциал в текущем патче.";
    guideTacticsWeaknesses.innerText = g.tactics?.weaknesses || "Зависит от позиционирования.";
    guideTacticsHowTo.innerText = g.tactics?.how_to_play_against || "Используйте специализированные контр-предметы и командный контроль.";

  } catch (err) {
    console.error("Failed to load hero guide:", err);
    guideCounterItemsList.innerHTML = `<div class="col-span-2 text-rose-400">Ошибка загрузки деталей гайда.</div>`;
  }
}

// ── EVENT LISTENERS SETUP ──

function setupEventListeners() {
  // Tabs (Header & Bottom Nav)
  if (tabBtnDraft) tabBtnDraft.addEventListener('click', () => switchTab('draft'));
  if (tabBtnHeroes) tabBtnHeroes.addEventListener('click', () => switchTab('heroes'));
  if (bottomNavDraft) bottomNavDraft.addEventListener('click', () => switchTab('draft'));
  if (bottomNavHeroes) bottomNavHeroes.addEventListener('click', () => switchTab('heroes'));

  // Reset
  btnReset.addEventListener('click', resetDraft);

  // Recommendation Type Filter (Все / Мета+Контр / Ситуативные / Мета)
  if (recomTypeFilterEl) {
    recomTypeFilterEl.addEventListener('click', (e) => {
      const btn = e.target.closest('.recom-filter-btn');
      if (!btn) return;
      haptic();
      state.recomTypeFilter = btn.dataset.type;
      
      document.querySelectorAll('.recom-filter-btn').forEach(b => {
        const isActive = b.dataset.type === state.recomTypeFilter;
        b.className = isActive 
          ? "recom-filter-btn px-2.5 py-1 rounded font-semibold bg-amber-500/20 text-amber-300 border border-amber-500/40 transition"
          : "recom-filter-btn px-2.5 py-1 rounded text-slate-400 hover:text-white transition";
      });

      filterAndRenderRecommendations();
    });
  }

  // Role Selector in Draft
  roleSelector.addEventListener('click', (e) => {
    const btn = e.target.closest('.role-btn');
    if (!btn) return;
    haptic();

    document.querySelectorAll('.role-btn').forEach(b => {
      b.classList.remove('active');
      b.className = "role-btn px-2 py-1.5 rounded-lg text-xs font-semibold bg-dota-card text-slate-300 border border-dota-border hover:border-slate-600 flex flex-col items-center justify-center transition";
    });

    btn.classList.add('active');
    btn.className = "role-btn active px-2 py-1.5 rounded-lg text-xs font-semibold bg-amber-500/20 text-amber-400 border border-amber-500/40 flex flex-col items-center justify-center transition";

    const roleVal = btn.dataset.role;
    state.role = roleVal ? parseInt(roleVal, 10) : null;
    activeRoleLabel.innerText = state.role ? ROLE_LABELS[state.role] : "Любая роль";

    updateRecommendations();
  });

  // Hero Picker Modal Events
  modalClose.addEventListener('click', closePickerModal);
  modalEl.addEventListener('click', (e) => {
    if (e.target === modalEl) closePickerModal();
  });

  heroSearch.addEventListener('input', (e) => {
    state.searchQuery = e.target.value;
    searchClear.classList.toggle('hidden', !state.searchQuery);
    renderHeroPickerGrid();
  });

  searchClear.addEventListener('click', () => {
    heroSearch.value = '';
    state.searchQuery = '';
    searchClear.classList.add('hidden');
    renderHeroPickerGrid();
  });

  attrFilterEl.addEventListener('click', (e) => {
    const btn = e.target.closest('.attr-btn');
    if (!btn) return;
    haptic();

    document.querySelectorAll('.attr-btn').forEach(b => {
      b.classList.remove('active');
      b.className = "attr-btn px-3 py-1 rounded-md bg-slate-800 text-slate-400 border border-slate-700 hover:border-slate-500 whitespace-nowrap";
    });

    btn.classList.add('active');
    btn.className = "attr-btn active px-3 py-1 rounded-md bg-amber-500/20 text-amber-300 border border-amber-500/30 whitespace-nowrap";

    state.attrFilter = btn.dataset.attr;
    renderHeroPickerGrid();
  });

  // Wiki Tab Search & Filters
  wikiSearch.addEventListener('input', (e) => {
    state.wikiSearchQuery = e.target.value;
    wikiSearchClear.classList.toggle('hidden', !state.wikiSearchQuery);
    renderWikiHeroes();
  });

  wikiSearchClear.addEventListener('click', () => {
    wikiSearch.value = '';
    state.wikiSearchQuery = '';
    wikiSearchClear.classList.add('hidden');
    renderWikiHeroes();
  });

  wikiAttrFilterEl.addEventListener('click', (e) => {
    const btn = e.target.closest('.wiki-attr-btn');
    if (!btn) return;
    haptic();

    document.querySelectorAll('.wiki-attr-btn').forEach(b => {
      b.classList.remove('active');
      b.className = "wiki-attr-btn px-3 py-1 rounded-md bg-slate-800 text-slate-400 border border-slate-700 hover:border-slate-500 whitespace-nowrap";
    });

    btn.classList.add('active');
    btn.className = "wiki-attr-btn active px-3 py-1 rounded-md bg-amber-500/20 text-amber-300 border border-amber-500/30 whitespace-nowrap";

    state.wikiAttrFilter = btn.dataset.attr;
    renderWikiHeroes();
  });

  if (wikiRoleFilterEl) {
    wikiRoleFilterEl.addEventListener('click', (e) => {
      const btn = e.target.closest('.wiki-role-btn');
      if (!btn) return;
      haptic();

      document.querySelectorAll('.wiki-role-btn').forEach(b => {
        b.classList.remove('active');
        b.className = "wiki-role-btn px-3 py-1 rounded-md bg-slate-800 text-slate-300 border border-slate-700 hover:border-slate-500 whitespace-nowrap";
      });

      btn.classList.add('active');
      btn.className = "wiki-role-btn active px-3 py-1 rounded-md bg-blue-500/20 text-blue-300 border border-blue-500/40 whitespace-nowrap";

      state.wikiRoleFilter = btn.dataset.role;
      renderWikiHeroes();
    });
  }

  // Guide Modal Events
  guideModalClose.addEventListener('click', closeHeroGuide);
  guideModalCloseBtn.addEventListener('click', closeHeroGuide);
  guideModal.addEventListener('click', (e) => {
    if (e.target === guideModal) closeHeroGuide();
  });

  guideAddAlly.addEventListener('click', () => {
    if (state.currentGuideHeroId) {
      quickAddHero('ally', state.currentGuideHeroId);
      closeHeroGuide();
      switchTab('draft');
    }
  });

  guideAddEnemy.addEventListener('click', () => {
    if (state.currentGuideHeroId) {
      quickAddHero('enemy', state.currentGuideHeroId);
      closeHeroGuide();
      switchTab('draft');
    }
  });
}

function openPickerModal(type, slotIndex) {
  haptic('light');
  state.modalTarget = { type, slotIndex };
  modalTitle.innerText = type === 'enemy' ? `Выберите вражеского героя (Слот ${slotIndex + 1})` : `Выберите союзника (Слот ${slotIndex + 1})`;
  heroSearch.value = '';
  state.searchQuery = '';
  searchClear.classList.add('hidden');
  modalEl.classList.remove('hidden');
  renderHeroPickerGrid();
  setTimeout(() => heroSearch.focus(), 50);
}

function closePickerModal() {
  modalEl.classList.add('hidden');
  state.modalTarget = null;
}

function closeHeroGuide() {
  guideModal.classList.add('hidden');
  state.currentGuideHeroId = null;
}

function renderHeroPickerGrid() {
  const q = state.searchQuery.toLowerCase().trim();
  const attr = state.attrFilter;
  const picked = new Set([...state.allies, ...state.enemies]);

  const filtered = state.heroes.filter(h => {
    if (picked.has(h.id)) return false;
    if (attr !== 'all') {
      const targetAttr = attr === 'all_attr' ? 'all' : attr;
      if (h.primary_attr !== targetAttr) return false;
    }
    if (!q) return true;
    if (h.localized_name_ru.toLowerCase().includes(q)) return true;
    if (h.localized_name.toLowerCase().includes(q)) return true;
    if (h.aliases && h.aliases.some(a => a.toLowerCase().includes(q))) return true;
    return false;
  });

  filtered.sort((a, b) => (a.localized_name || '').localeCompare(b.localized_name || ''));

  heroGrid.innerHTML = filtered.map(h => `
    <div onclick="selectHeroForSlot(${h.id})" class="bg-slate-900 border border-slate-700 hover:border-amber-500 rounded-xl p-1.5 flex flex-col items-center gap-1 cursor-pointer transition hover:scale-105">
      <img src="${h.icon_url}" alt="${h.localized_name}" onerror="this.onerror=null;this.src='https://cdn.cloudflare.steamstatic.com/apps/dota2/images/dota_react/heroes/pudge.png';" class="w-full aspect-square rounded-lg object-cover">
      <span class="text-[10px] font-bold text-white text-center truncate w-full leading-tight">${h.localized_name}</span>
    </div>
  `).join('');
}

function selectHeroForSlot(heroId) {
  if (!state.modalTarget) return;
  haptic('medium');
  const { type, slotIndex } = state.modalTarget;
  if (type === 'enemy') {
    state.enemies[slotIndex] = heroId;
    state.enemies = state.enemies.filter(Boolean);
  } else {
    state.allies[slotIndex] = heroId;
    state.allies = state.allies.filter(Boolean);
  }

  closePickerModal();
  renderEmptySlots();
  updateRecommendations();
}

// Global functions attached to window for HTML click handlers
window.openHeroGuide = openHeroGuide;
window.quickAddHero = quickAddHero;
window.selectHeroForSlot = selectHeroForSlot;

// Start app on DOM ready
document.addEventListener('DOMContentLoaded', init);
