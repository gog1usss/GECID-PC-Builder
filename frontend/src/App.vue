<template>
  <div class="bg-slate-100 font-sans text-slate-800 min-h-screen pb-20">
    <header class="bg-blue-600 text-white p-4 shadow-lg sticky top-0 z-50">
      <div class="container mx-auto max-w-6xl flex justify-between items-center">
        <h1 class="text-2xl font-bold flex items-center gap-2">
          <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path></svg>
          GECID PC Builder
        </h1>
        <div class="text-sm font-medium bg-blue-700 px-3 py-1 rounded-full">Vue.js Edition</div>
      </div>
    </header>

    <main class="container mx-auto max-w-6xl p-4 mt-6 grid grid-cols-1 lg:grid-cols-3 gap-6">
      
      <div class="lg:col-span-2 space-y-6">
        
        <div class="bg-white p-6 rounded-2xl shadow-sm border border-slate-200">
          <h2 class="text-xl font-bold mb-6 border-b pb-3 text-slate-800">Шаг 1: Основа системы</h2>
          
          <div class="mb-5">
            <div class="flex justify-between items-center mb-1.5">
              <label class="text-sm font-semibold text-slate-700">Процессор (CPU)</label>
              <div class="flex gap-2">
                <select v-model="filters.cpu.brand" class="px-2 py-1 border border-slate-300 rounded text-xs w-28 outline-none focus:ring-1 focus:ring-blue-500 bg-white">
                  <option value="">Все бренды</option>
                  <option v-for="brand in availableBrands.cpu" :key="brand" :value="brand">{{ brand }}</option>
                </select>
                <input v-model.number="filters.cpu.minPrice" type="number" placeholder="Мин. ₴" class="px-2 py-1 border border-slate-300 rounded text-xs w-20 outline-none focus:ring-1 focus:ring-blue-500">
                <input v-model.number="filters.cpu.maxPrice" type="number" placeholder="Макс. ₴" class="px-2 py-1 border border-slate-300 rounded text-xs w-20 outline-none focus:ring-1 focus:ring-blue-500">
              </div>
            </div>
            <select v-model="selected.cpu" class="w-full p-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none transition-all bg-white">
              <option :value="null">-- Выберите процессор --</option>
              <option v-for="item in filteredOptions.cpus" :key="item.id" :value="item">
                {{ getField(item, 'cpu', 'name') }} ({{ item.socket_cpu }}) — {{ getField(item, 'cpu', 'price') }} ₴
              </option>
            </select>
          </div>

          <div class="mb-5">
            <div class="flex justify-between items-center mb-1.5">
              <label class="text-sm font-semibold text-slate-700">Материнская плата (Motherboard)</label>
              <div v-if="selected.cpu" class="flex gap-2">
                <select v-model="filters.mb.brand" class="px-2 py-1 border border-slate-300 rounded text-xs w-28 outline-none focus:ring-1 focus:ring-blue-500 bg-white">
                  <option value="">Все бренды</option>
                  <option v-for="brand in availableBrands.mb" :key="brand" :value="brand">{{ brand }}</option>
                </select>
                <input v-model.number="filters.mb.minPrice" type="number" placeholder="Мин. ₴" class="px-2 py-1 border border-slate-300 rounded text-xs w-20 outline-none focus:ring-1 focus:ring-blue-500">
                <input v-model.number="filters.mb.maxPrice" type="number" placeholder="Макс. ₴" class="px-2 py-1 border border-slate-300 rounded text-xs w-20 outline-none focus:ring-1 focus:ring-blue-500">
              </div>
            </div>
            <select v-model="selected.mb" :disabled="!selected.cpu" class="w-full p-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none transition-all disabled:bg-slate-100 disabled:opacity-70 bg-white">
              <option :value="null">{{ selected.cpu ? '-- Выберите материнскую плату --' : 'Сначала выберите процессор' }}</option>
              <option v-for="item in filteredOptions.mbs" :key="item.id" :value="item">
                {{ getField(item, 'mb', 'name') }} ({{ item.ram_type }}) — {{ getField(item, 'mb', 'price') }} ₴
              </option>
            </select>
            <p class="text-xs text-slate-500 mt-1">Отображаются только платы с подходящим сокетом</p>
          </div>

          <div class="mb-2">
            <div class="flex justify-between items-center mb-1.5">
              <label class="text-sm font-semibold text-slate-700">Охлаждение (Cooler)</label>
              <div v-if="selected.cpu" class="flex gap-2">
                <select v-model="filters.cooler.brand" class="px-2 py-1 border border-slate-300 rounded text-xs w-28 outline-none focus:ring-1 focus:ring-blue-500 bg-white">
                  <option value="">Все бренды</option>
                  <option v-for="brand in availableBrands.cooler" :key="brand" :value="brand">{{ brand }}</option>
                </select>
                <input v-model.number="filters.cooler.minPrice" type="number" placeholder="Мин. ₴" class="px-2 py-1 border border-slate-300 rounded text-xs w-20 outline-none focus:ring-1 focus:ring-blue-500">
                <input v-model.number="filters.cooler.maxPrice" type="number" placeholder="Макс. ₴" class="px-2 py-1 border border-slate-300 rounded text-xs w-20 outline-none focus:ring-1 focus:ring-blue-500">
              </div>
            </div>
            <select v-model="selected.cooler" :disabled="!selected.cpu" class="w-full p-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none transition-all disabled:bg-slate-100 disabled:opacity-70 bg-white">
              <option :value="null">{{ selected.cpu ? '-- Выберите охлаждение --' : 'Сначала выберите процессор' }}</option>
              <option v-for="item in filteredOptions.coolers" :key="item.id" :value="item">
                {{ getField(item, 'cooler', 'name') }} (TDP: {{ item.max_tdp }}W) — {{ getField(item, 'cooler', 'price') }} ₴
              </option>
            </select>
          </div>
        </div>

        <div class="bg-white p-6 rounded-2xl shadow-sm border border-slate-200">
          <h2 class="text-xl font-bold mb-6 border-b pb-3 text-slate-800">Шаг 2: Память и Видео</h2>
          
          <div class="mb-5">
            <div class="flex justify-between items-center mb-1.5">
              <label class="text-sm font-semibold text-slate-700">Оперативная память (RAM)</label>
              <div v-if="selected.mb" class="flex gap-2">
                <select v-model="filters.ram.brand" class="px-2 py-1 border border-slate-300 rounded text-xs w-28 outline-none focus:ring-1 focus:ring-blue-500 bg-white">
                  <option value="">Все бренды</option>
                  <option v-for="brand in availableBrands.ram" :key="brand" :value="brand">{{ brand }}</option>
                </select>
                <input v-model.number="filters.ram.minPrice" type="number" placeholder="Мин. ₴" class="px-2 py-1 border border-slate-300 rounded text-xs w-20 outline-none focus:ring-1 focus:ring-blue-500">
                <input v-model.number="filters.ram.maxPrice" type="number" placeholder="Макс. ₴" class="px-2 py-1 border border-slate-300 rounded text-xs w-20 outline-none focus:ring-1 focus:ring-blue-500">
              </div>
            </div>
            <select v-model="selected.ram" :disabled="!selected.mb" class="w-full p-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none transition-all disabled:bg-slate-100 disabled:opacity-70 bg-white">
              <option :value="null">{{ selected.mb ? '-- Выберите оперативную память --' : 'Сначала выберите материнскую плату' }}</option>
              <option v-for="item in filteredOptions.rams" :key="item.id" :value="item">
                {{ getField(item, 'ram', 'name') }} ({{ item.frequency_mhz }} MHz) — {{ getField(item, 'ram', 'price') }} ₴
              </option>
            </select>
          </div>

          <div class="mb-2">
            <div class="flex justify-between items-center mb-1.5">
              <label class="text-sm font-semibold text-slate-700">Видеокарта (GPU)</label>
              <div class="flex gap-2">
                <select v-model="filters.gpu.brand" class="px-2 py-1 border border-slate-300 rounded text-xs w-28 outline-none focus:ring-1 focus:ring-blue-500 bg-white">
                  <option value="">Все бренды</option>
                  <option v-for="brand in availableBrands.gpu" :key="brand" :value="brand">{{ brand }}</option>
                </select>
                <input v-model.number="filters.gpu.minPrice" type="number" placeholder="Мин. ₴" class="px-2 py-1 border border-slate-300 rounded text-xs w-20 outline-none focus:ring-1 focus:ring-blue-500">
                <input v-model.number="filters.gpu.maxPrice" type="number" placeholder="Макс. ₴" class="px-2 py-1 border border-slate-300 rounded text-xs w-20 outline-none focus:ring-1 focus:ring-blue-500">
              </div>
            </div>
            <select v-model="selected.gpu" class="w-full p-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none transition-all bg-white">
              <option :value="null">-- Выберите видеокарту --</option>
                {{ getField(item, 'gpu', 'name') }} — {{ getField(item, 'gpu', 'price') }} ₴
              </option>
            </select>
          </div>
        </div>

        <div class="bg-white p-6 rounded-2xl shadow-sm border border-slate-200">
          <h2 class="text-xl font-bold mb-6 border-b pb-3 text-slate-800">Шаг 3: Корпус и Питание</h2>
          
          <div class="mb-5">
            <div class="flex justify-between items-center mb-1.5">
              <label class="text-sm font-semibold text-slate-700">Блок питания (PSU)</label>
              <div class="flex gap-2">
                <select v-model="filters.psu.brand" class="px-2 py-1 border border-slate-300 rounded text-xs w-28 outline-none focus:ring-1 focus:ring-blue-500 bg-white">
                  <option value="">Все бренды</option>
                  <option v-for="brand in availableBrands.psu" :key="brand" :value="brand">{{ brand }}</option>
                </select>
                <input v-model.number="filters.psu.minWatt" type="number" placeholder="Мин. W" class="px-2 py-1 border border-slate-300 rounded text-xs w-16 outline-none focus:ring-1 focus:ring-blue-500">
                <input v-model.number="filters.psu.minPrice" type="number" placeholder="Мин. ₴" class="px-2 py-1 border border-slate-300 rounded text-xs w-16 outline-none focus:ring-1 focus:ring-blue-500">
                <input v-model.number="filters.psu.maxPrice" type="number" placeholder="Макс. ₴" class="px-2 py-1 border border-slate-300 rounded text-xs w-16 outline-none focus:ring-1 focus:ring-blue-500">
              </div>
            </div>
            <select v-model="selected.psu" class="w-full p-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none transition-all bg-white">
              <option :value="null">-- Выберите блок питания --</option>
              <option v-for="item in filteredOptions.psus" :key="item.id" :value="item">
                {{ getField(item, 'psu', 'name') }} ({{ item.wattage }}W) — {{ getField(item, 'psu', 'price') }} ₴
              </option>
            </select>
            <p v-if="systemTdp > 0" class="text-xs text-blue-600 font-semibold mt-1">
              TDP Сборки: {{ systemTdp }} Вт. Рекомендуем БП от {{ recommendedPsu }} Вт.
            </p>
          </div>

          <div class="mb-2">
            <div class="flex justify-between items-center mb-1.5">
              <label class="text-sm font-semibold text-slate-700">Корпус (Case)</label>
              <div v-if="selected.mb" class="flex gap-2">
                <select v-model="filters.case.brand" class="px-2 py-1 border border-slate-300 rounded text-xs w-28 outline-none focus:ring-1 focus:ring-blue-500 bg-white">
                  <option value="">Все бренды</option>
                  <option v-for="brand in availableBrands.case" :key="brand" :value="brand">{{ brand }}</option>
                </select>
                <input v-model.number="filters.case.minPrice" type="number" placeholder="Мин. ₴" class="px-2 py-1 border border-slate-300 rounded text-xs w-20 outline-none focus:ring-1 focus:ring-blue-500">
                <input v-model.number="filters.case.maxPrice" type="number" placeholder="Макс. ₴" class="px-2 py-1 border border-slate-300 rounded text-xs w-20 outline-none focus:ring-1 focus:ring-blue-500">
              </div>
            </div>
            <select v-model="selected.case" :disabled="!selected.mb" class="w-full p-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none transition-all disabled:bg-slate-100 disabled:opacity-70 bg-white">
              <option :value="null">{{ selected.mb ? '-- Выберите корпус --' : 'Сначала выберите материнскую плату' }}</option>
              <option v-for="item in filteredOptions.cases" :key="item.id" :value="item">
                {{ getField(item, 'case', 'name') }} — {{ getField(item, 'case', 'price') }} ₴
              </option>
            </select>
          </div>
        </div>

      </div>

      <div class="bg-white p-6 rounded-2xl shadow-sm border border-blue-200 h-fit sticky top-24">
        <h2 class="text-xl font-bold mb-4 border-b pb-2 flex items-center gap-2">
          <svg class="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z"></path></svg>
          Итоговая сборка
        </h2>
        
        <ul class="space-y-4 mb-6 min-h-[150px]">
          <li v-if="!hasItemsInCart" class="text-slate-400 text-sm italic text-center mt-10">
            Сборка пуста. Выберите комплектующие слева.
          </li>
          
          <template v-for="row in cartItems" :key="row.id">
            <li v-if="row.item" class="flex items-center gap-3 border-b pb-3 animate-[fadeIn_0.3s_ease-out] group">
              <div class="w-12 h-12 flex-shrink-0 bg-white border rounded p-1 flex items-center justify-center">
                <img v-if="row.img" :src="row.img" class="max-w-full max-h-full object-contain" />
                <span v-else class="text-[10px] text-slate-400 text-center leading-tight">Нет<br>фото</span>
              </div>
              
              <div class="flex-grow pr-1">
                <span class="text-[11px] uppercase tracking-wider font-bold text-blue-500 block mb-1">{{ row.label }}</span> 
                <span class="text-sm font-medium text-slate-700 leading-snug block">{{ row.name }}</span>
              </div>
              
              <div class="flex items-center gap-2">
                <div class="font-bold text-slate-800 whitespace-nowrap">{{ row.price }} ₴</div>
                
                <button @click="removeComponent(row.id)" class="text-slate-400 hover:text-red-500 transition-colors p-1" title="Убрать из сборки">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>
            </li>
          </template>
        </ul>

        <div class="border-t pt-4 bg-slate-50 p-4 rounded-xl">
          <div class="flex justify-between items-center text-xl font-black text-slate-800">
            <span>Итого:</span>
            <span class="text-blue-600">{{ totalPrice }} ₴</span>
          </div>
          <div class="flex justify-between items-center text-sm font-medium text-slate-500 mt-3">
            <span>Потребление (TDP):</span>
            <span class="text-orange-500">{{ totalTdpCalc }} Вт</span>
          </div>
          
          <button @click="saveBuild" class="w-full mt-6 bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-4 rounded-lg transition-colors shadow-lg flex justify-center items-center gap-2">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7H5a2 2 0 00-2 2v9a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-3m-1 4l-3 3m0 0l-3-3m3 3V4"></path></svg>
            Сохранить сборку
          </button>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { reactive, computed, onMounted, watch, ref } from 'vue';

const API = 'http://127.0.0.1:8000/api/v1';

const options = reactive({ cpus: [], mbs: [], coolers: [], rams: [], gpus: [], psus: [], cases: [] });
const selected = reactive({ cpu: null, mb: null, cooler: null, ram: null, gpu: null, psu: null, case: null });

const systemTdp = ref(0);
const recommendedPsu = ref(0);

const filters = reactive({
  cpu: { brand: '', minPrice: null, maxPrice: null },
  mb: { brand: '', minPrice: null, maxPrice: null },
  cooler: { brand: '', minPrice: null, maxPrice: null },
  ram: { brand: '', minPrice: null, maxPrice: null },
  gpu: { brand: '', minPrice: null, maxPrice: null },
  psu: { brand: '', minWatt: null, minPrice: null, maxPrice: null },
  case: { brand: '', minPrice: null, maxPrice: null }
});

const getField = (item, category, field) => {
  if (!item) return field === 'price' ? 0 : '';
  
  const map = {
    cpu: { name: 'name_cpu', price: 'price', brand: 'brand_cpu' },
    mb: { name: 'name_mother', price: 'price_mother', brand: 'brand_mother' },
    cooler: { name: 'name_cooler', price: 'price', brand: 'brand_cooler' },
    ram: { name: 'name_ram', price: 'price_ram', brand: 'brand_ram' },
    gpu: { name: 'name_gpu', price: 'price_gpu', brand: 'brand_gpu' },
    psu: { name: 'name_psu', price: 'price_psu', brand: 'brand_psu' },
    case: { name: 'name_case', price: 'price', brand: 'brand_case' }
  };
  
  return item[map[category][field]] || (field === 'price' ? 0 : '');
};

// --- АВТОМАТИЧЕСКИЙ СБОР БРЕНДОВ ---
const availableBrands = computed(() => {
  const getUniqueBrands = (list, category) => {
    const brands = list.map(item => getField(item, category, 'brand'));
    return [...new Set(brands)].filter(Boolean).sort();
  };

  return {
    cpu: getUniqueBrands(options.cpus, 'cpu'),
    mb: getUniqueBrands(options.mbs, 'mb'),
    cooler: getUniqueBrands(options.coolers, 'cooler'),
    ram: getUniqueBrands(options.rams, 'ram'),
    gpu: getUniqueBrands(options.gpus, 'gpu'),
    psu: getUniqueBrands(options.psus, 'psu'),
    case: getUniqueBrands(options.cases, 'case')
  };
});

const removeComponent = (key) => {
  selected[key] = null;
};

const filteredOptions = computed(() => {
  return {
    cpus: options.cpus.filter(item => {
      if (filters.cpu.brand && getField(item, 'cpu', 'brand') !== filters.cpu.brand) return false;
      if (filters.cpu.minPrice && getField(item, 'cpu', 'price') < Number(filters.cpu.minPrice)) return false;
      if (filters.cpu.maxPrice && getField(item, 'cpu', 'price') > Number(filters.cpu.maxPrice)) return false;
      return true;
    }),
    mbs: options.mbs.filter(item => {
      if (filters.mb.brand && getField(item, 'mb', 'brand') !== filters.mb.brand) return false;
      if (filters.mb.minPrice && getField(item, 'mb', 'price') < Number(filters.mb.minPrice)) return false;
      if (filters.mb.maxPrice && getField(item, 'mb', 'price') > Number(filters.mb.maxPrice)) return false;
      return true;
    }),
    coolers: options.coolers.filter(item => {
      if (filters.cooler.brand && getField(item, 'cooler', 'brand') !== filters.cooler.brand) return false;
      if (filters.cooler.minPrice && getField(item, 'cooler', 'price') < Number(filters.cooler.minPrice)) return false;
      if (filters.cooler.maxPrice && getField(item, 'cooler', 'price') > Number(filters.cooler.maxPrice)) return false;
      return true;
    }),
    rams: options.rams.filter(item => {
      if (filters.ram.brand && getField(item, 'ram', 'brand') !== filters.ram.brand) return false;
      if (filters.ram.minPrice && getField(item, 'ram', 'price') < Number(filters.ram.minPrice)) return false;
      if (filters.ram.maxPrice && getField(item, 'ram', 'price') > Number(filters.ram.maxPrice)) return false;
      return true;
    }),
    gpus: options.gpus.filter(item => {
      if (filters.gpu.brand && getField(item, 'gpu', 'brand') !== filters.gpu.brand) return false;
      if (filters.gpu.minPrice && getField(item, 'gpu', 'price') < Number(filters.gpu.minPrice)) return false;
      if (filters.gpu.maxPrice && getField(item, 'gpu', 'price') > Number(filters.gpu.maxPrice)) return false;
      return true;
    }),
    psus: options.psus.filter(item => {
      if (filters.psu.brand && getField(item, 'psu', 'brand') !== filters.psu.brand) return false;
      if (filters.psu.minWatt && (item?.wattage || 0) < Number(filters.psu.minWatt)) return false;
      if (filters.psu.minPrice && getField(item, 'psu', 'price') < Number(filters.psu.minPrice)) return false;
      if (filters.psu.maxPrice && getField(item, 'psu', 'price') > Number(filters.psu.maxPrice)) return false;
      return true;
    }),
    cases: options.cases.filter(item => {
      if (filters.case.brand && getField(item, 'case', 'brand') !== filters.case.brand) return false;
      if (filters.case.minPrice && getField(item, 'case', 'price') < Number(filters.case.minPrice)) return false;
      if (filters.case.maxPrice && getField(item, 'case', 'price') > Number(filters.case.maxPrice)) return false;
      return true;
    })
  };
});

const fetchData = async (endpoint, params = '') => {
  try {
    const res = await fetch(`${API}/${endpoint}/${params ? '?' + params : ''}`);
    if (!res.ok) throw new Error(`Ошибка бэкенда! Код: ${res.status}`);
    const json = await res.json();
    const dataArray = Object.values(json).find(val => Array.isArray(val));
    return dataArray || [];
  } catch (e) {
    console.error(`Сбой загрузки /${endpoint}/:`, e.message);
    return [];
  }
};

const fetchCPUs = async () => { options.cpus = await fetchData('cpu'); };
const fetchGPUs = async () => { options.gpus = await fetchData('gpu'); };
const fetchMBs = async (cpuId) => { options.mbs = await fetchData('motherboard', `cpu_id=${cpuId}`); };
const fetchCoolers = async (cpuId) => { options.coolers = await fetchData('coolers', `cpu_id=${cpuId}`); };
const fetchRAMs = async (mbId) => { options.rams = await fetchData('ram', `motherboard_id=${mbId}`); };
const fetchCases = async (mbId) => { options.cases = await fetchData('cases', `motherboard_id=${mbId}`); };

const fetchPSUs = async (cpuId, gpuId) => {
  try {
    let url = `${API}/psu/?`;
    if (cpuId) url += `cpu_id=${cpuId}&`;
    if (gpuId) url += `gpu_id=${gpuId}`;
    
    const res = await fetch(url);
    if (!res.ok) throw new Error(`Ошибка бэкенда! Код: ${res.status}`);
    const data = await res.json();
    options.psus = data.data || [];
    systemTdp.value = data.system_tdp || 0;
    recommendedPsu.value = data.recommended_wattage || 0;
  } catch (e) { console.error(`Сбой загрузки /psu/:`, e.message); }
};

watch(() => selected.cpu, (newCpu) => {
  selected.mb = null; selected.cooler = null;
  options.mbs = []; options.coolers = [];
  filters.mb.brand = ''; filters.mb.minPrice = null; filters.mb.maxPrice = null;
  filters.cooler.brand = ''; filters.cooler.minPrice = null; filters.cooler.maxPrice = null;
  
  if (newCpu) {
    fetchMBs(newCpu.id); fetchCoolers(newCpu.id);
  }
  fetchPSUs(newCpu?.id, selected.gpu?.id);
});

watch(() => selected.mb, (newMb) => {
  selected.ram = null; selected.case = null;
  options.rams = []; options.cases = [];
  filters.ram.brand = ''; filters.ram.minPrice = null; filters.ram.maxPrice = null;
  filters.case.brand = ''; filters.case.minPrice = null; filters.case.maxPrice = null;
  
  if (newMb) {
    fetchRAMs(newMb.id); fetchCases(newMb.id);
  }
});

watch(() => selected.gpu, (newGpu) => {
  fetchPSUs(selected.cpu?.id, newGpu?.id);
});

const cartItems = computed(() => {
  return [
    { id: 'cpu', label: 'Процессор', item: selected.cpu, name: selected.cpu ? getField(selected.cpu, 'cpu', 'name') : '', price: getField(selected.cpu, 'cpu', 'price'), img: selected.cpu?.image_url },
    { id: 'mb', label: 'Мат. плата', item: selected.mb, name: selected.mb ? getField(selected.mb, 'mb', 'name') : '', price: getField(selected.mb, 'mb', 'price'), img: selected.mb?.image_url },
    { id: 'cooler', label: 'Охлаждение', item: selected.cooler, name: selected.cooler ? getField(selected.cooler, 'cooler', 'name') : '', price: getField(selected.cooler, 'cooler', 'price'), img: selected.cooler?.image_url },
    { id: 'ram', label: 'ОЗУ', item: selected.ram, name: selected.ram ? getField(selected.ram, 'ram', 'name') : '', price: getField(selected.ram, 'ram', 'price'), img: selected.ram?.image_url },
    { id: 'gpu', label: 'Видеокарта', item: selected.gpu, name: selected.gpu ? getField(selected.gpu, 'gpu', 'name') : '', price: getField(selected.gpu, 'gpu', 'price'), img: selected.gpu?.image_url },
    { id: 'psu', label: 'Блок питания', item: selected.psu, name: selected.psu ? getField(selected.psu, 'psu', 'name') : '', price: getField(selected.psu, 'psu', 'price'), img: selected.psu?.image_url },
    { id: 'case', label: 'Корпус', item: selected.case, name: selected.case ? getField(selected.case, 'case', 'name') : '', price: getField(selected.case, 'case', 'price'), img: selected.case?.image_url }
  ];
});

const hasItemsInCart = computed(() => cartItems.value.some(row => row.item !== null));
const totalPrice = computed(() => cartItems.value.reduce((sum, row) => sum + (row.price || 0), 0));
const totalTdpCalc = computed(() => (selected.cpu?.tdp || 0) + (selected.gpu?.tdp || 0));

const saveBuild = () => {
  if (!selected.cpu || !selected.mb || !selected.ram || !selected.psu || !selected.case) {
    alert("Пожалуйста, соберите хотя бы базовую конфигурацию (CPU, Плата, ОЗУ, Корпус, БП)!");
    return;
  }
  alert("Конфигурация готова! Скоро мы подключим сюда базу данных для сохранения.");
};

onMounted(() => {
  fetchCPUs();
  fetchGPUs();
  fetchPSUs(null, null);
});
</script>