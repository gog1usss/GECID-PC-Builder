<template>
  <div class="bg-slate-100 font-sans text-slate-800 min-h-screen pb-20">
    <header class="bg-blue-600 text-white p-4 shadow-lg sticky top-0 z-50">
      <div class="container mx-auto max-w-6xl flex justify-between items-center">
        <!-- Кликабельный логотип -->
        <h1 @click="currentView = 'builder'" class="text-2xl font-bold flex items-center gap-2 cursor-pointer hover:text-slate-200 transition-colors" :title="$t('header.logoTitle')">
          <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path></svg>
          GECID PC Builder
        </h1>
        
        <div class="flex items-center gap-4">
          <!-- Переключатель языков -->
          <div class="flex items-center gap-2 bg-blue-800/50 px-3 py-1.5 rounded-full">
            <button @click="changeLanguage('uk')" :class="{'text-white font-bold': locale === 'uk', 'text-blue-300': locale !== 'uk'}" class="text-xs hover:text-white transition-colors uppercase tracking-wider">UK</button>
            <span class="text-blue-400 text-xs opacity-50">|</span>
            <button @click="changeLanguage('en')" :class="{'text-white font-bold': locale === 'en', 'text-blue-300': locale !== 'en'}" class="text-xs hover:text-white transition-colors uppercase tracking-wider">EN</button>
            <span class="text-blue-400 text-xs opacity-50">|</span>
            <button @click="changeLanguage('ru')" :class="{'text-white font-bold': locale === 'ru', 'text-blue-300': locale !== 'ru'}" class="text-xs hover:text-white transition-colors uppercase tracking-wider">RU</button>
          </div>

          <div class="text-sm font-medium bg-blue-700 px-3 py-1 rounded-full hidden sm:block">Vue.js Edition</div>
          
          <template v-if="auth.isAuthenticated">
            <span class="font-medium text-sm text-blue-200">{{ $t('header.greeting') }}, {{ auth.username }}!</span>
            
            <button v-if="currentView !== 'builder'" @click="currentView = 'builder'" class="text-sm bg-blue-700 hover:bg-blue-800 px-3 py-1 rounded transition-colors font-semibold shadow-sm">
              {{ $t('header.builderBtn') }}
            </button>
            <button v-if="currentView !== 'profile'" @click="openProfile" class="text-sm bg-emerald-500 hover:bg-emerald-600 px-3 py-1 rounded transition-colors font-semibold shadow-sm">
              {{ $t('header.profileBtn') }}
            </button>
            
            <button @click="logout" class="text-sm bg-red-500 hover:bg-red-600 px-3 py-1 rounded transition-colors font-semibold shadow-sm">
              {{ $t('header.logoutBtn') }}
            </button>
          </template>
          <template v-else>
            <button @click="showAuthModal = true" class="text-sm bg-white text-blue-600 hover:bg-blue-50 px-4 py-1.5 rounded transition-colors font-bold shadow-sm">
              {{ $t('header.loginBtn') }}
            </button>
          </template>
        </div>
      </div>
    </header>

    <main class="container mx-auto max-w-6xl p-4 mt-6">
      
      <!-- === ЭКРАН 1: КОНСТРУКТОР === -->
      <div v-if="currentView === 'builder'" class="grid grid-cols-1 lg:grid-cols-3 gap-6 animate-[fadeIn_0.3s_ease-out]">
        
        <div class="lg:col-span-2 space-y-6">
          <div class="bg-white p-6 rounded-2xl shadow-sm border border-slate-200">
            <h2 class="text-xl font-bold mb-6 border-b pb-3 text-slate-800">{{ $t('builder.step1_title') }}</h2>
            
            <div class="mb-5">
              <div class="flex justify-between items-center mb-1.5">
                <label class="text-sm font-semibold text-slate-700">{{ $t('builder.labels.cpu') }}</label>
                <div class="flex gap-2">
                  <select v-model="filters.cpu.brand" class="px-2 py-1 border border-slate-300 rounded text-xs w-28 outline-none focus:ring-1 focus:ring-blue-500 bg-white">
                    <option value="">{{ $t('builder.filters.allBrands') }}</option>
                    <option v-for="brand in availableBrands.cpu" :key="brand" :value="brand">{{ brand }}</option>
                  </select>
                  <input v-model.number="filters.cpu.minPrice" type="number" :placeholder="$t('builder.filters.minPrice')" class="px-2 py-1 border border-slate-300 rounded text-xs w-20 outline-none focus:ring-1 focus:ring-blue-500">
                  <input v-model.number="filters.cpu.maxPrice" type="number" :placeholder="$t('builder.filters.maxPrice')" class="px-2 py-1 border border-slate-300 rounded text-xs w-20 outline-none focus:ring-1 focus:ring-blue-500">
                </div>
              </div>
              <select v-model="selected.cpu" class="w-full p-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none transition-all bg-white">
                <option :value="null">{{ $t('builder.placeholders.selectCpu') }}</option>
                <option v-for="item in filteredOptions.cpus" :key="item.id" :value="item">
                  {{ getField(item, 'cpu', 'name') }} ({{ item.socket_cpu }}) — {{ getField(item, 'cpu', 'price') }} ₴
                </option>
              </select>
            </div>

            <div class="mb-5">
              <div class="flex justify-between items-center mb-1.5">
                <label class="text-sm font-semibold text-slate-700">{{ $t('builder.labels.mb') }}</label>
                <div v-if="selected.cpu" class="flex gap-2">
                  <select v-model="filters.mb.brand" class="px-2 py-1 border border-slate-300 rounded text-xs w-28 outline-none focus:ring-1 focus:ring-blue-500 bg-white">
                    <option value="">{{ $t('builder.filters.allBrands') }}</option>
                    <option v-for="brand in availableBrands.mb" :key="brand" :value="brand">{{ brand }}</option>
                  </select>
                  <input v-model.number="filters.mb.minPrice" type="number" :placeholder="$t('builder.filters.minPrice')" class="px-2 py-1 border border-slate-300 rounded text-xs w-20 outline-none focus:ring-1 focus:ring-blue-500">
                  <input v-model.number="filters.mb.maxPrice" type="number" :placeholder="$t('builder.filters.maxPrice')" class="px-2 py-1 border border-slate-300 rounded text-xs w-20 outline-none focus:ring-1 focus:ring-blue-500">
                </div>
              </div>
              <select v-model="selected.mb" :disabled="!selected.cpu" class="w-full p-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none transition-all disabled:bg-slate-100 disabled:opacity-70 bg-white">
                <option :value="null">{{ selected.cpu ? $t('builder.placeholders.selectMb') : $t('builder.placeholders.needCpuFirst') }}</option>
                <option v-for="item in filteredOptions.mbs" :key="item.id" :value="item">
                  {{ getField(item, 'mb', 'name') }} ({{ item.ram_type }}) — {{ getField(item, 'mb', 'price') }} ₴
                </option>
              </select>
              <p class="text-xs text-slate-500 mt-1">{{ $t('builder.hints.mbHint') }}</p>
            </div>

            <div class="mb-2">
              <div class="flex justify-between items-center mb-1.5">
                <label class="text-sm font-semibold text-slate-700">{{ $t('builder.labels.cooler') }}</label>
                <div v-if="selected.cpu" class="flex gap-2">
                  <select v-model="filters.cooler.brand" class="px-2 py-1 border border-slate-300 rounded text-xs w-28 outline-none focus:ring-1 focus:ring-blue-500 bg-white">
                    <option value="">{{ $t('builder.filters.allBrands') }}</option>
                    <option v-for="brand in availableBrands.cooler" :key="brand" :value="brand">{{ brand }}</option>
                  </select>
                  <input v-model.number="filters.cooler.minPrice" type="number" :placeholder="$t('builder.filters.minPrice')" class="px-2 py-1 border border-slate-300 rounded text-xs w-20 outline-none focus:ring-1 focus:ring-blue-500">
                  <input v-model.number="filters.cooler.maxPrice" type="number" :placeholder="$t('builder.filters.maxPrice')" class="px-2 py-1 border border-slate-300 rounded text-xs w-20 outline-none focus:ring-1 focus:ring-blue-500">
                </div>
              </div>
              <select v-model="selected.cooler" :disabled="!selected.cpu" class="w-full p-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none transition-all disabled:bg-slate-100 disabled:opacity-70 bg-white">
                <option :value="null">{{ selected.cpu ? $t('builder.placeholders.selectCooler') : $t('builder.placeholders.needCpuFirst') }}</option>
                <option v-for="item in filteredOptions.coolers" :key="item.id" :value="item">
                  {{ getField(item, 'cooler', 'name') }} (TDP: {{ item.max_tdp }}W) — {{ getField(item, 'cooler', 'price') }} ₴
                </option>
              </select>
            </div>
          </div>

          <div class="bg-white p-6 rounded-2xl shadow-sm border border-slate-200">
            <h2 class="text-xl font-bold mb-6 border-b pb-3 text-slate-800">{{ $t('builder.step2_title') }}</h2>
            
            <div class="mb-5">
              <div class="flex justify-between items-center mb-1.5">
                <label class="text-sm font-semibold text-slate-700">{{ $t('builder.labels.ram') }}</label>
                <div v-if="selected.mb" class="flex gap-2">
                  <select v-model="filters.ram.brand" class="px-2 py-1 border border-slate-300 rounded text-xs w-28 outline-none focus:ring-1 focus:ring-blue-500 bg-white">
                    <option value="">{{ $t('builder.filters.allBrands') }}</option>
                    <option v-for="brand in availableBrands.ram" :key="brand" :value="brand">{{ brand }}</option>
                  </select>
                  <input v-model.number="filters.ram.minPrice" type="number" :placeholder="$t('builder.filters.minPrice')" class="px-2 py-1 border border-slate-300 rounded text-xs w-20 outline-none focus:ring-1 focus:ring-blue-500">
                  <input v-model.number="filters.ram.maxPrice" type="number" :placeholder="$t('builder.filters.maxPrice')" class="px-2 py-1 border border-slate-300 rounded text-xs w-20 outline-none focus:ring-1 focus:ring-blue-500">
                </div>
              </div>
              <select v-model="selected.ram" :disabled="!selected.mb" class="w-full p-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none transition-all disabled:bg-slate-100 disabled:opacity-70 bg-white">
                <option :value="null">{{ selected.mb ? $t('builder.placeholders.selectRam') : $t('builder.placeholders.needMbFirst') }}</option>
                <option v-for="item in filteredOptions.rams" :key="item.id" :value="item">
                  {{ getField(item, 'ram', 'name') }} ({{ item.frequency_mhz }} MHz) — {{ getField(item, 'ram', 'price') }} ₴
                </option>
              </select>
            </div>

            <div class="mb-2">
              <div class="flex justify-between items-center mb-1.5">
                <label class="text-sm font-semibold text-slate-700">{{ $t('builder.labels.gpu') }}</label>
                <div class="flex gap-2">
                  <select v-model="filters.gpu.brand" class="px-2 py-1 border border-slate-300 rounded text-xs w-28 outline-none focus:ring-1 focus:ring-blue-500 bg-white">
                    <option value="">{{ $t('builder.filters.allBrands') }}</option>
                    <option v-for="brand in availableBrands.gpu" :key="brand" :value="brand">{{ brand }}</option>
                  </select>
                  <input v-model.number="filters.gpu.minPrice" type="number" :placeholder="$t('builder.filters.minPrice')" class="px-2 py-1 border border-slate-300 rounded text-xs w-20 outline-none focus:ring-1 focus:ring-blue-500">
                  <input v-model.number="filters.gpu.maxPrice" type="number" :placeholder="$t('builder.filters.maxPrice')" class="px-2 py-1 border border-slate-300 rounded text-xs w-20 outline-none focus:ring-1 focus:ring-blue-500">
                </div>
              </div>
              <select v-model="selected.gpu" class="w-full p-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none transition-all bg-white">
                <option :value="null">{{ $t('builder.placeholders.selectGpu') }}</option>
                <option v-for="item in filteredOptions.gpus" :key="item.id" :value="item">
                  {{ getField(item, 'gpu', 'name') }} — {{ getField(item, 'gpu', 'price') }} ₴
                </option>
              </select>
            </div>
          </div>

          <div class="bg-white p-6 rounded-2xl shadow-sm border border-slate-200">
            <h2 class="text-xl font-bold mb-6 border-b pb-3 text-slate-800">{{ $t('builder.step3_title') }}</h2>
            
            <div class="mb-5">
              <div class="flex justify-between items-center mb-1.5">
                <label class="text-sm font-semibold text-slate-700">{{ $t('builder.labels.psu') }}</label>
                <div class="flex gap-2">
                  <select v-model="filters.psu.brand" class="px-2 py-1 border border-slate-300 rounded text-xs w-28 outline-none focus:ring-1 focus:ring-blue-500 bg-white">
                    <option value="">{{ $t('builder.filters.allBrands') }}</option>
                    <option v-for="brand in availableBrands.psu" :key="brand" :value="brand">{{ brand }}</option>
                  </select>
                  <input v-model.number="filters.psu.minWatt" type="number" :placeholder="$t('builder.filters.minWatt')" class="px-2 py-1 border border-slate-300 rounded text-xs w-16 outline-none focus:ring-1 focus:ring-blue-500">
                  <input v-model.number="filters.psu.minPrice" type="number" :placeholder="$t('builder.filters.minPrice')" class="px-2 py-1 border border-slate-300 rounded text-xs w-16 outline-none focus:ring-1 focus:ring-blue-500">
                  <input v-model.number="filters.psu.maxPrice" type="number" :placeholder="$t('builder.filters.maxPrice')" class="px-2 py-1 border border-slate-300 rounded text-xs w-16 outline-none focus:ring-1 focus:ring-blue-500">
                </div>
              </div>
              <select v-model="selected.psu" class="w-full p-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none transition-all bg-white">
                <option :value="null">{{ $t('builder.placeholders.selectPsu') }}</option>
                <option v-for="item in filteredOptions.psus" :key="item.id" :value="item">
                  {{ getField(item, 'psu', 'name') }} ({{ item.wattage }}W) — {{ getField(item, 'psu', 'price') }} ₴
                </option>
              </select>
              <p v-if="systemTdp > 0" class="text-xs text-blue-600 font-semibold mt-1">
                {{ $t('builder.hints.tdpHint', { tdp: systemTdp, psu: recommendedPsu }) }}
              </p>
            </div>

            <div class="mb-2">
              <div class="flex justify-between items-center mb-1.5">
                <label class="text-sm font-semibold text-slate-700">{{ $t('builder.labels.case') }}</label>
                <div v-if="selected.mb" class="flex gap-2">
                  <select v-model="filters.case.brand" class="px-2 py-1 border border-slate-300 rounded text-xs w-28 outline-none focus:ring-1 focus:ring-blue-500 bg-white">
                    <option value="">{{ $t('builder.filters.allBrands') }}</option>
                    <option v-for="brand in availableBrands.case" :key="brand" :value="brand">{{ brand }}</option>
                  </select>
                  <input v-model.number="filters.case.minPrice" type="number" :placeholder="$t('builder.filters.minPrice')" class="px-2 py-1 border border-slate-300 rounded text-xs w-20 outline-none focus:ring-1 focus:ring-blue-500">
                  <input v-model.number="filters.case.maxPrice" type="number" :placeholder="$t('builder.filters.maxPrice')" class="px-2 py-1 border border-slate-300 rounded text-xs w-20 outline-none focus:ring-1 focus:ring-blue-500">
                </div>
              </div>
              <select v-model="selected.case" :disabled="!selected.mb" class="w-full p-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none transition-all disabled:bg-slate-100 disabled:opacity-70 bg-white">
                <option :value="null">{{ selected.mb ? $t('builder.placeholders.selectCase') : $t('builder.placeholders.needMbFirst') }}</option>
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
            {{ $t('builder.summary_title') }}
          </h2>
          
          <ul class="space-y-4 mb-6 min-h-[150px]">
            <li v-if="!hasItemsInCart" class="text-slate-400 text-sm italic text-center mt-10">
              {{ $t('builder.summary.empty') }}
            </li>
            
            <template v-for="row in cartItems" :key="row.id">
              <li v-if="row.item" class="flex items-center gap-3 border-b pb-3 animate-[fadeIn_0.3s_ease-out] group">
                <div class="w-12 h-12 flex-shrink-0 bg-white border rounded p-1 flex items-center justify-center">
                  <img v-if="row.img" :src="row.img" class="max-w-full max-h-full object-contain" />
                  <span v-else class="text-[10px] text-slate-400 text-center leading-tight" v-html="$t('builder.summary.noPhoto')"></span>
                </div>
                
                <div class="flex-grow pr-1">
                  <!-- Для label компонентов лучше тоже использовать ключи перевода в JS -->
                  <span class="text-[11px] uppercase tracking-wider font-bold text-blue-500 block mb-1">{{ row.label }}</span> 
                  <span class="text-sm font-medium text-slate-700 leading-snug block">{{ row.name }}</span>
                </div>
                
                <div class="flex items-center gap-2">
                  <div class="font-bold text-slate-800 whitespace-nowrap">{{ row.price }} ₴</div>
                  
                  <button @click="removeComponent(row.id)" class="text-slate-400 hover:text-red-500 transition-colors p-1" :title="$t('builder.summary.remove')">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" /></svg>
                  </button>
                </div>
              </li>
            </template>
          </ul>

          <div class="border-t pt-4 bg-slate-50 p-4 rounded-xl">
            <div class="flex justify-between items-center text-xl font-black text-slate-800">
              <span>{{ $t('builder.summary.total') }}</span>
              <span class="text-blue-600">{{ totalPrice }} ₴</span>
            </div>
            <div class="flex justify-between items-center text-sm font-medium text-slate-500 mt-3">
              <span>{{ $t('builder.summary.tdp') }}</span>
              <span class="text-orange-500">{{ totalTdpCalc }} W</span>
            </div>
            
            <button @click="saveBuild" class="w-full mt-6 bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-4 rounded-lg transition-colors shadow-lg flex justify-center items-center gap-2">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7H5a2 2 0 00-2 2v9a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-3m-1 4l-3 3m0 0l-3-3m3 3V4"></path></svg>
              {{ $t('builder.summary.saveBtn') }}
            </button>
          </div>
        </div>

      </div>

      <!-- === ЭКРАН 2: ЛИЧНЫЙ КАБИНЕТ === -->
      <div v-else-if="currentView === 'profile'" class="space-y-6 animate-[fadeIn_0.3s_ease-out]">
        
        <div class="bg-white p-8 rounded-2xl shadow-sm border border-slate-200">
          <h2 class="text-2xl font-bold mb-6 border-b pb-3 text-slate-800">{{ $t('profile.settingsTitle') }}</h2>
          
          <form @submit.prevent="updateProfile" class="max-w-md space-y-4">
            <div>
              <label class="block text-sm font-semibold text-slate-700 mb-1">{{ $t('profile.newUsername') }}</label>
              <input v-model="profileForm.username" type="text" :placeholder="$t('profile.leaveEmpty')" class="w-full p-2.5 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none">
            </div>
            <div>
              <label class="block text-sm font-semibold text-slate-700 mb-1">{{ $t('profile.newPassword') }}</label>
              <input v-model="profileForm.password" type="password" :placeholder="$t('profile.leaveEmpty')" class="w-full p-2.5 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none">
            </div>
            <button type="submit" class="bg-slate-800 hover:bg-slate-900 text-white font-bold py-2.5 px-6 rounded-lg transition-colors shadow-md">
              {{ $t('profile.saveChanges') }}
            </button>
            <p class="text-xs text-slate-500 mt-2">{{ $t('profile.passwordWarning') }}</p>
          </form>
        </div>

        <div class="bg-white p-8 rounded-2xl shadow-sm border border-slate-200">
          <h2 class="text-2xl font-bold mb-6 border-b pb-3 text-slate-800">{{ $t('profile.buildsTitle') }}</h2>
          
          <div v-if="userBuilds.length === 0" class="text-slate-500 italic">
            {{ $t('profile.noBuilds') }}
          </div>
          
          <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div v-for="b in userBuilds" :key="b.id" 
                 @click="loadBuild(b)" 
                 class="border border-slate-200 rounded-xl p-4 hover:border-blue-500 hover:shadow-lg transition-all bg-slate-50 cursor-pointer relative group">
              
              <div class="flex justify-between items-start mb-3">
                <h3 class="font-bold text-lg text-blue-600 group-hover:text-blue-700 transition-colors">{{ b.build_name }}</h3>
                <button @click.stop="deleteBuild(b.id)" class="text-slate-400 hover:text-red-500 bg-white p-1.5 rounded-md shadow-sm border border-slate-200" :title="$t('profile.deleteHint')">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path></svg>
                </button>
              </div>
              
              <div class="text-sm text-slate-600 space-y-1.5">
                <p class="flex justify-between"><strong class="text-slate-500 text-xs uppercase tracking-wider">CPU:</strong> <span class="text-right ml-2 truncate">{{ getComponentName('cpus', b.cpu_id) }}</span></p>
                <p class="flex justify-between"><strong class="text-slate-500 text-xs uppercase tracking-wider">MB:</strong> <span class="text-right ml-2 truncate">{{ getComponentName('mbs', b.motherboard_id) }}</span></p>
                <p v-if="b.cooler_id" class="flex justify-between"><strong class="text-slate-500 text-xs uppercase tracking-wider">COOL:</strong> <span class="text-right ml-2 truncate">{{ getComponentName('coolers', b.cooler_id) }}</span></p>
                <p class="flex justify-between"><strong class="text-slate-500 text-xs uppercase tracking-wider">RAM:</strong> <span class="text-right ml-2 truncate">{{ getComponentName('rams', b.ram_id) }}</span></p>
                <p v-if="b.gpu_id" class="flex justify-between"><strong class="text-slate-500 text-xs uppercase tracking-wider">GPU:</strong> <span class="text-right ml-2 truncate">{{ getComponentName('gpus', b.gpu_id) }}</span></p>
                <p class="flex justify-between"><strong class="text-slate-500 text-xs uppercase tracking-wider">PSU:</strong> <span class="text-right ml-2 truncate">{{ getComponentName('psus', b.psu_id) }}</span></p>
                <p class="flex justify-between"><strong class="text-slate-500 text-xs uppercase tracking-wider">CASE:</strong> <span class="text-right ml-2 truncate">{{ getComponentName('cases', b.case_id) }}</span></p>
              </div>
              
              <div class="mt-4 pt-3 border-t border-slate-200 flex justify-between items-center">
                <span class="text-[11px] font-bold text-blue-500 uppercase tracking-wide opacity-0 group-hover:opacity-100 transition-opacity">{{ $t('profile.openBuilder') }}</span>
                <span class="text-xs text-slate-400">{{ $t('profile.createdAt') }} {{ b.created_at ? new Date(b.created_at).toLocaleDateString() : $t('profile.recently') }}</span>
              </div>
            </div>
          </div>
        </div>

      </div>
    </main>

    <!-- Модальное окно авторизации/регистрации -->
    <div v-if="showAuthModal" class="fixed inset-0 bg-slate-900/50 backdrop-blur-sm z-[100] flex items-center justify-center p-4 animate-[fadeIn_0.2s_ease-out]">
      <div class="bg-white rounded-2xl shadow-xl w-full max-w-md overflow-hidden relative">
        <button @click="showAuthModal = false" class="absolute top-4 right-4 text-slate-400 hover:text-slate-700">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
        </button>

        <div class="p-8">
          <h2 class="text-2xl font-bold text-slate-800 mb-6 text-center">
            {{ isLoginMode ? $t('auth.loginTitle') : $t('auth.registerTitle') }}
          </h2>

          <form @submit.prevent="submitAuth" class="space-y-4">
            <div>
              <label class="block text-sm font-semibold text-slate-700 mb-1">{{ $t('auth.username') }}</label>
              <input v-model="authForm.username" type="text" required class="w-full p-2.5 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none">
            </div>

            <div v-if="!isLoginMode">
              <label class="block text-sm font-semibold text-slate-700 mb-1">{{ $t('auth.email') }}</label>
              <input v-model="authForm.email" type="email" required class="w-full p-2.5 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none">
            </div>

            <div>
              <label class="block text-sm font-semibold text-slate-700 mb-1">{{ $t('auth.password') }}</label>
              <input v-model="authForm.password" type="password" required class="w-full p-2.5 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none">
            </div>

            <p v-if="authError" class="text-red-500 text-sm text-center font-medium">{{ authError }}</p>

            <button type="submit" class="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-4 rounded-lg transition-colors shadow-md mt-2">
              {{ isLoginMode ? $t('auth.loginBtn') : $t('auth.registerBtn') }}
            </button>
          </form>

          <div class="mt-6 text-center text-sm text-slate-500">
            {{ isLoginMode ? $t('auth.noAccount') : $t('auth.hasAccount') }}
            <button @click="toggleAuthMode" class="text-blue-600 font-bold hover:underline ml-1">
              {{ isLoginMode ? $t('auth.createBtn') : $t('auth.loginBtn') }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>

import { reactive, computed, onMounted, watch, ref } from 'vue';
import { useI18n } from 'vue-i18n';

const API = 'http://127.0.0.1:8000/api/v1';

// --- ЗАЩИТА ПРИ ЗАГРУЗКЕ ГОТОВОЙ СБОРКИ ---
const isRestoring = ref(false); 

const {t, locale} = useI18n(); 
const changeLanguage = (lang) => { 
  locale.value = lang; 
  localStorage.setItem('lang',lang);
}

// --- СОСТОЯНИЕ ДАННЫХ И КОНСТРУКТОРА ---
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

// --- СОСТОЯНИЕ АВТОРИЗАЦИИ ---
const auth = reactive({
  isAuthenticated: !!localStorage.getItem('token'),
  username: localStorage.getItem('username') || '',
  token: localStorage.getItem('token') || null
});

const showAuthModal = ref(false);
const isLoginMode = ref(true);
const authError = ref('');
const authForm = reactive({ username: '', email: '', password: '' });

// --- УПРАВЛЕНИЕ ВИДАМИ И ПРОФИЛЕМ ---
const currentView = ref('builder'); // 'builder' или 'profile'
const userBuilds = ref([]);
const profileForm = reactive({ username: '', password: '' });

// --- ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ---
const getUserIdFromToken = () => {
  if (!auth.token) return null;
  try {
    const payload = JSON.parse(atob(auth.token.split('.')[1]));
    return payload.sub;
  } catch (e) {
    return null;
  }
};

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

const getComponentName = (categoryListStr, id) => {
  if (!id) return 'Не выбрано';
  // Используем нестрогое равенство (==) для защиты от строковых ID из БД
  const item = options[categoryListStr]?.find(x => x.id == id);
  if (item) {
    const catMap = { 
      'cpus': 'cpu', 'mbs': 'mb', 'coolers': 'cooler', 
      'rams': 'ram', 'gpus': 'gpu', 'psus': 'psu', 'cases': 'case' 
    };
    return getField(item, catMap[categoryListStr], 'name') || 'ID: ' + id;
  }
  return 'ID: ' + id;
};

const removeComponent = (key) => {
  selected[key] = null;
};

// --- ЛОГИКА АВТОРИЗАЦИИ ---
const toggleAuthMode = () => {
  isLoginMode.value = !isLoginMode.value;
  authError.value = '';
};

const submitAuth = async () => {
  authError.value = '';
  try {
    let res;
    if (isLoginMode.value) {
      const formData = new URLSearchParams();
      formData.append('username', authForm.username);
      formData.append('password', authForm.password);

      res = await fetch(`${API}/pass/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: formData
      });
    } else {
      res = await fetch(`${API}/pass/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          username: authForm.username,
          email: authForm.email,
          password: authForm.password
        })
      });
    }

    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || 'Произошла ошибка');

    if (isLoginMode.value) {
      localStorage.setItem('token', data.access_token);
      localStorage.setItem('username', authForm.username);
      auth.token = data.access_token;
      auth.username = authForm.username;
      auth.isAuthenticated = true;
      showAuthModal.value = false;
      authForm.password = '';
    } else {
      alert("Регистрация успешна! Теперь вы можете войти.");
      isLoginMode.value = true;
      authForm.password = '';
    }
  } catch (e) {
    authError.value = e.message;
  }
};

const logout = async () => {
  if (auth.token) {
    try {
      await fetch(`${API}/pass/logout`, {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${auth.token}` }
      });
    } catch (e) {
      console.error(e);
    }
  }
  localStorage.removeItem('token');
  localStorage.removeItem('username');
  auth.isAuthenticated = false;
  auth.token = null;
  auth.username = '';
  currentView.value = 'builder';
};

// --- ЛОГИКА ПРОФИЛЯ ---
const openProfile = () => {
  currentView.value = 'profile';
  fetchUserBuilds();
};

const fetchUserBuilds = async () => {
  const userId = getUserIdFromToken();
  if (!userId) return;

  try {
    const res = await fetch(`${API}/build/${userId}`, {
      headers: { 'Authorization': `Bearer ${auth.token}` }
    });
    
    const data = await res.json();
    
    if (res.ok) {
      // Умная проверка: понимает и массив напрямую, и объект с полем data
      if (Array.isArray(data)) {
        userBuilds.value = data;
      } else if (data && Array.isArray(data.data)) {
        userBuilds.value = data.data;
      } else {
        userBuilds.value = [];
      }
    }
  } catch (e) {
    console.error("Ошибка загрузки сборок:", e);
  }
};

const deleteBuild = async (buildId) => {
  if (!confirm("Точно удалить эту сборку?")) return;
  try {
    const res = await fetch(`${API}/build/${buildId}`, {
      method: 'DELETE',
      headers: { 'Authorization': `Bearer ${auth.token}` }
    });
    if (res.ok) {
      userBuilds.value = userBuilds.value.filter(b => b.id !== buildId);
    }
  } catch (e) {
    alert("Ошибка удаления");
  }
};

const updateProfile = async () => {
  const payload = {};
  if (profileForm.username) payload.updated_username = profileForm.username;
  if (profileForm.password) payload.updated_password = profileForm.password;

  if (Object.keys(payload).length === 0) return;

  try {
    const res = await fetch(`${API}/pass/profile`, {
      method: 'PATCH',
      headers: { 
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${auth.token}`
      },
      body: JSON.stringify(payload)
    });

    const data = await res.json();
    if (!res.ok) throw new Error(data.detail);

    alert(data.message);
    
    if (payload.updated_username) {
      auth.username = payload.updated_username;
      localStorage.setItem('username', payload.updated_username);
    }

    if (payload.updated_password) {
      alert("Пароль изменен. Пожалуйста, войдите с новым паролем.");
      logout();
    }

    profileForm.username = '';
    profileForm.password = '';
  } catch (e) {
    alert("Ошибка: " + e.message);
  }
};

const saveBuild = async () => {
  if (!auth.isAuthenticated) {
    alert("Пожалуйста, войдите в аккаунт, чтобы сохранить сборку!");
    showAuthModal.value = true;
    return;
  }

  if (!selected.cpu || !selected.mb || !selected.ram || !selected.psu || !selected.case) {
    alert("Пожалуйста, соберите базовую конфигурацию (CPU, Плата, ОЗУ, Корпус, БП)!");
    return;
  }

  const buildName = prompt("Введите название для вашей сборки:", "Моя сборка");
  if (!buildName) return;

  const payload = {
    build_name: buildName,
    cpu_id: selected.cpu.id,
    motherboard_id: selected.mb.id,
    ram_id: selected.ram.id,
    gpu_id: selected.gpu?.id || null,
    psu_id: selected.psu.id,
    case_id: selected.case.id,
    cooler_id: selected.cooler?.id || null
  };

  try {
    const res = await fetch(`${API}/build/`, {
      method: 'POST',
      headers: { 
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${auth.token}`
      },
      body: JSON.stringify(payload)
    });

    const data = await res.json();
    
    if (!res.ok) {
      const errorMsg = Array.isArray(data.detail) 
        ? JSON.stringify(data.detail) 
        : (data.detail || "Неизвестная ошибка сервера");
      throw new Error(errorMsg);
    }
    
    alert(data.message || "Сборка успешно сохранена!");
    fetchUserBuilds(); // Подтягиваем свежий список сборок
    
  } catch (e) {
    console.error("Подробная ошибка при сохранении:", e);
    alert("Ошибка: " + e.message);
  }
};

const loadBuild = async (build) => {
  isRestoring.value = true;
  currentView.value = 'builder'; 

  try {
    await Promise.all([
      fetchMBs(build.cpu_id),
      fetchCoolers(build.cpu_id),
      fetchRAMs(build.motherboard_id),
      fetchCases(build.motherboard_id),
      fetchPSUs(build.cpu_id, build.gpu_id)
    ]);

    // Нестрогое равенство (==) для корректного поиска ID
    selected.cpu = options.cpus.find(c => c.id == build.cpu_id) || null;
    selected.mb = options.mbs.find(m => m.id == build.motherboard_id) || null;
    selected.cooler = options.coolers.find(c => c.id == build.cooler_id) || null;
    selected.ram = options.rams.find(r => r.id == build.ram_id) || null;
    selected.gpu = options.gpus.find(g => g.id == build.gpu_id) || null;
    selected.psu = options.psus.find(p => p.id == build.psu_id) || null;
    selected.case = options.cases.find(c => c.id == build.case_id) || null;
    
    Object.keys(filters).forEach(key => { filters[key].brand = ''; });

  } catch (e) {
    console.error("Ошибка загрузки данных сборки", e);
    alert("Не удалось загрузить все комплектующие для этой сборки.");
  } finally {
    setTimeout(() => { isRestoring.value = false; }, 100);
  }
};

// --- ВЫЧИСЛЯЕМЫЕ СВОЙСТВА КОНСТРУКТОРА ---
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

// --- ЗАГРУЗКА ДАННЫХ КОМПОНЕНТОВ ---
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
const fetchMBs = async (cpuId) => { options.mbs = await fetchData('motherboard', cpuId ? `cpu_id=${cpuId}` : ''); };
const fetchCoolers = async (cpuId) => { options.coolers = await fetchData('coolers', cpuId ? `cpu_id=${cpuId}` : ''); };
const fetchRAMs = async (mbId) => { options.rams = await fetchData('ram', mbId ? `motherboard_id=${mbId}` : ''); };
const fetchCases = async (mbId) => { options.cases = await fetchData('cases', mbId ? `motherboard_id=${mbId}` : ''); };

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
  if (isRestoring.value) return; 

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
  if (isRestoring.value) return;

  selected.ram = null; selected.case = null;
  options.rams = []; options.cases = [];
  filters.ram.brand = ''; filters.ram.minPrice = null; filters.ram.maxPrice = null;
  filters.case.brand = ''; filters.case.minPrice = null; filters.case.maxPrice = null;
  
  if (newMb) {
    fetchRAMs(newMb.id); fetchCases(newMb.id);
  }
});

watch(() => selected.gpu, (newGpu) => {
  if (isRestoring.value) return;
  fetchPSUs(selected.cpu?.id, newGpu?.id);
});

onMounted(() => {
  fetchCPUs();
  fetchGPUs();
  fetchPSUs(null, null);
  
  // ФОНОВАЯ ЗАГРУЗКА БЕЗ ФИЛЬТРОВ
  fetchMBs('');
  fetchRAMs('');
  fetchCases('');
  fetchCoolers('');
});
</script>