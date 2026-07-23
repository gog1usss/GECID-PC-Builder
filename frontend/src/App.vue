<template>
  <div class="bg-slate-50 dark:bg-[#121212] font-sans text-slate-800 dark:text-gray-200 min-h-screen pb-20 transition-colors duration-300 selection:bg-blue-500 dark:selection:bg-orange-500 selection:text-white">
    
    <!-- Хедер -->
    <header class="bg-blue-600 dark:bg-[#1a1a1a] border-b border-transparent dark:border-[#333333] p-4 sticky top-0 z-50 shadow-md transition-colors duration-300">
      <div class="container mx-auto max-w-6xl flex flex-wrap gap-4 justify-between items-center">
        <!-- Логотип -->
        <h1 @click="currentView = 'builder'" class="text-2xl font-black flex items-center gap-2 cursor-pointer text-white dark:text-orange-500 hover:opacity-80 transition-all tracking-wide" :title="$t('header.logoTitle')">
          <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path></svg>
          GECID BUILDER
        </h1>
        
        <div class="flex flex-wrap items-center gap-3 sm:gap-4">
          <!-- Кнопка смены темы -->
          <button @click="toggleTheme" class="p-2 rounded-full bg-blue-700 dark:bg-[#222] hover:bg-blue-800 dark:hover:bg-[#333] transition-colors text-white dark:text-gray-300" :title="$t('header.themeBtn')">
            <svg v-if="!isDarkMode" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"></path></svg>
            <svg v-else class="w-5 h-5 text-orange-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"></path></svg>
          </button>

          <!-- Переключатель языков -->
          <div class="flex items-center gap-1 sm:gap-2 bg-blue-700 dark:bg-[#222222] px-3 py-1.5 rounded-full border border-transparent dark:border-[#333333] transition-colors duration-300">
            <button @click="changeLanguage('uk')" :class="{'text-white dark:text-orange-500 font-bold': locale === 'uk', 'text-blue-200 dark:text-gray-500': locale !== 'uk'}" class="text-xs hover:text-white dark:hover:text-orange-400 transition-colors uppercase tracking-wider">UK</button>
            <span class="text-blue-400 dark:text-gray-700 text-xs">|</span>
            <button @click="changeLanguage('en')" :class="{'text-white dark:text-orange-500 font-bold': locale === 'en', 'text-blue-200 dark:text-gray-500': locale !== 'en'}" class="text-xs hover:text-white dark:hover:text-orange-400 transition-colors uppercase tracking-wider">EN</button>
            <span class="text-blue-400 dark:text-gray-700 text-xs">|</span>
            <button @click="changeLanguage('ru')" :class="{'text-white dark:text-orange-500 font-bold': locale === 'ru', 'text-blue-200 dark:text-gray-500': locale !== 'ru'}" class="text-xs hover:text-white dark:hover:text-orange-400 transition-colors uppercase tracking-wider">RU</button>
          </div>

          <template v-if="auth.isAuthenticated">
            <span class="font-medium text-sm text-blue-100 dark:text-gray-400 hidden lg:block">{{ $t('header.greeting') }}, <span class="text-white dark:text-orange-500 font-bold">{{ auth.username }}</span></span>
            
            <button v-if="currentView !== 'builder'" @click="currentView = 'builder'" class="text-sm bg-blue-700 dark:bg-[#2a2a2a] hover:bg-blue-800 dark:hover:bg-[#333] text-white dark:text-gray-200 px-4 py-1.5 rounded-full transition-all font-semibold">
              {{ $t('header.builderBtn') }}
            </button>
            <button v-if="currentView !== 'profile'" @click="openProfile" class="text-sm bg-emerald-500 dark:bg-orange-600 hover:bg-emerald-600 dark:hover:bg-orange-500 text-white px-4 py-1.5 rounded-full transition-all font-semibold shadow-md dark:shadow-[0_0_10px_rgba(234,88,12,0.3)]">
              {{ $t('header.profileBtn') }}
            </button>
            <button @click="logout" class="text-sm text-blue-200 dark:text-gray-500 hover:text-red-400 dark:hover:text-red-500 px-2 py-1.5 transition-colors font-semibold">
              {{ $t('header.logoutBtn') }}
            </button>
          </template>
          <template v-else>
            <button @click="showAuthModal = true" class="text-sm border-2 border-white dark:border-orange-500 text-white dark:text-orange-500 hover:bg-white dark:hover:bg-orange-500 hover:text-blue-600 dark:hover:text-white px-5 py-1.5 rounded-full transition-all font-bold shadow-sm">
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
    
    <!-- ШАГ 1: ОСНОВА СИСТЕМЫ -->
    <div class="bg-white dark:bg-[#1e1e1e] p-6 rounded-3xl shadow-md hover:shadow-xl border border-slate-200 dark:border-[#2a2a2a] transition-all duration-300">
      <h2 class="text-xl font-bold mb-6 border-b border-slate-100 dark:border-[#333] pb-3 text-blue-600 dark:text-orange-500 transition-colors duration-300">{{ $t('builder.step1_title') }}</h2>
      
      <!-- CPU -->
      <div class="mb-6 relative">
        <div class="flex flex-wrap justify-between items-center mb-3 gap-2">
          <label class="text-sm font-semibold text-slate-700 dark:text-gray-300 transition-colors duration-300">{{ $t('builder.labels.cpu') }}</label>
          <div class="flex flex-wrap gap-2 items-center">
            <div class="w-36 z-50">
              <CustomSelect v-model="filters.cpu.brand" :options="getBrandOptions(availableBrands.cpu)" :placeholder="$t('builder.filters.allBrands')" :labelFunc="(item) => item.name" />
            </div>
            
            <select v-model="filters.cpu.sort" class="px-3 py-2 bg-slate-50 dark:bg-[#121212] border border-slate-200 dark:border-[#333] rounded-xl text-xs outline-none focus:border-blue-500 dark:focus:border-orange-500 text-slate-700 dark:text-gray-300 transition-colors duration-300 cursor-pointer">
              <option value="default">{{ $t('builder.filters.sortDefault') }}</option>
              <option value="asc">{{ $t('builder.filters.sortAsc') }}</option>
              <option value="desc">{{ $t('builder.filters.sortDesc') }}</option>
            </select>

            <input v-model.number="filters.cpu.minPrice" type="number" :placeholder="$t('builder.filters.minPrice')" class="px-3 py-2 bg-slate-50 dark:bg-[#121212] border border-slate-200 dark:border-[#333] rounded-xl text-xs w-24 outline-none focus:border-blue-500 dark:focus:border-orange-500 text-slate-700 dark:text-gray-300 transition-colors duration-300 placeholder-slate-400 dark:placeholder-gray-600">
            <input v-model.number="filters.cpu.maxPrice" type="number" :placeholder="$t('builder.filters.maxPrice')" class="px-3 py-2 bg-slate-50 dark:bg-[#121212] border border-slate-200 dark:border-[#333] rounded-xl text-xs w-24 outline-none focus:border-blue-500 dark:focus:border-orange-500 text-slate-700 dark:text-gray-300 transition-colors duration-300 placeholder-slate-400 dark:placeholder-gray-600">
          </div>
        </div>
        <div class="z-40">
          <CustomSelect v-model="selected.cpu" :options="filteredOptions.cpus" :placeholder="$t('builder.placeholders.selectCpu')" :labelFunc="(item) => formatOption(item, 'cpu')" />
        </div>
      </div>

      <!-- MB -->
      <div class="mb-6 relative">
        <div class="flex flex-wrap justify-between items-center mb-3 gap-2">
          <label class="text-sm font-semibold text-slate-700 dark:text-gray-300 transition-colors duration-300">{{ $t('builder.labels.mb') }}</label>
          <div class="flex flex-wrap gap-2 items-center" v-if="selected.cpu">
            <div class="w-36 z-30">
              <CustomSelect v-model="filters.mb.brand" :options="getBrandOptions(availableBrands.mb)" :placeholder="$t('builder.filters.allBrands')" :labelFunc="(item) => item.name" />
            </div>
            
            <select v-model="filters.mb.sort" class="px-3 py-2 bg-slate-50 dark:bg-[#121212] border border-slate-200 dark:border-[#333] rounded-xl text-xs outline-none focus:border-blue-500 dark:focus:border-orange-500 text-slate-700 dark:text-gray-300 transition-colors duration-300 cursor-pointer">
              <option value="default">{{ $t('builder.filters.sortDefault') }}</option>
              <option value="asc">{{ $t('builder.filters.sortAsc') }}</option>
              <option value="desc">{{ $t('builder.filters.sortDesc') }}</option>
            </select>

            <input v-model.number="filters.mb.minPrice" type="number" :placeholder="$t('builder.filters.minPrice')" class="px-3 py-2 bg-slate-50 dark:bg-[#121212] border border-slate-200 dark:border-[#333] rounded-xl text-xs w-24 outline-none focus:border-blue-500 dark:focus:border-orange-500 text-slate-700 dark:text-gray-300 transition-colors duration-300 placeholder-slate-400 dark:placeholder-gray-600">
            <input v-model.number="filters.mb.maxPrice" type="number" :placeholder="$t('builder.filters.maxPrice')" class="px-3 py-2 bg-slate-50 dark:bg-[#121212] border border-slate-200 dark:border-[#333] rounded-xl text-xs w-24 outline-none focus:border-blue-500 dark:focus:border-orange-500 text-slate-700 dark:text-gray-300 transition-colors duration-300 placeholder-slate-400 dark:placeholder-gray-600">
          </div>
        </div>
        <div class="z-20">
          <CustomSelect v-model="selected.mb" :options="filteredOptions.mbs" :disabled="!selected.cpu" :placeholder="selected.cpu ? $t('builder.placeholders.selectMb') : $t('builder.placeholders.needCpuFirst')" :labelFunc="(item) => formatOption(item, 'mb')" />
        </div>
        <p class="text-xs text-slate-500 dark:text-gray-500 mt-2 transition-colors duration-300">{{ $t('builder.hints.mbHint') }}</p>
      </div>

      <!-- Cooler -->
      <div class="mb-2 relative">
        <div class="flex flex-wrap justify-between items-center mb-3 gap-2">
          <label class="text-sm font-semibold text-slate-700 dark:text-gray-300 transition-colors duration-300">{{ $t('builder.labels.cooler') }}</label>
          <div class="flex flex-wrap gap-2 items-center" v-if="selected.cpu">
            <div class="w-36 z-20">
              <CustomSelect v-model="filters.cooler.brand" :options="getBrandOptions(availableBrands.cooler)" :placeholder="$t('builder.filters.allBrands')" :labelFunc="(item) => item.name" />
            </div>
            
            <select v-model="filters.cooler.sort" class="px-3 py-2 bg-slate-50 dark:bg-[#121212] border border-slate-200 dark:border-[#333] rounded-xl text-xs outline-none focus:border-blue-500 dark:focus:border-orange-500 text-slate-700 dark:text-gray-300 transition-colors duration-300 cursor-pointer">
              <option value="default">{{ $t('builder.filters.sortDefault') }}</option>
              <option value="asc">{{ $t('builder.filters.sortAsc') }}</option>
              <option value="desc">{{ $t('builder.filters.sortDesc') }}</option>
            </select>

            <input v-model.number="filters.cooler.minPrice" type="number" :placeholder="$t('builder.filters.minPrice')" class="px-3 py-2 bg-slate-50 dark:bg-[#121212] border border-slate-200 dark:border-[#333] rounded-xl text-xs w-24 outline-none focus:border-blue-500 dark:focus:border-orange-500 text-slate-700 dark:text-gray-300 transition-colors duration-300 placeholder-slate-400 dark:placeholder-gray-600">
            <input v-model.number="filters.cooler.maxPrice" type="number" :placeholder="$t('builder.filters.maxPrice')" class="px-3 py-2 bg-slate-50 dark:bg-[#121212] border border-slate-200 dark:border-[#333] rounded-xl text-xs w-24 outline-none focus:border-blue-500 dark:focus:border-orange-500 text-slate-700 dark:text-gray-300 transition-colors duration-300 placeholder-slate-400 dark:placeholder-gray-600">
          </div>
        </div>
        <div class="z-10">
          <CustomSelect v-model="selected.cooler" :options="filteredOptions.coolers" :disabled="!selected.cpu" :placeholder="selected.cpu ? $t('builder.placeholders.selectCooler') : $t('builder.placeholders.needCpuFirst')" :labelFunc="(item) => formatOption(item, 'cooler')" />
        </div>
      </div>
    </div>

    <!-- ШАГ 2: ПАМЯТЬ И ВИДЕО -->
    <div class="bg-white dark:bg-[#1e1e1e] p-6 rounded-3xl shadow-md hover:shadow-xl border border-slate-200 dark:border-[#2a2a2a] transition-all duration-300">
      <h2 class="text-xl font-bold mb-6 border-b border-slate-100 dark:border-[#333] pb-3 text-blue-600 dark:text-orange-500 transition-colors duration-300">{{ $t('builder.step2_title') }}</h2>
      
      <!-- RAM -->
      <div class="mb-6 relative">
        <div class="flex flex-wrap justify-between items-center mb-3 gap-2">
          <label class="text-sm font-semibold text-slate-700 dark:text-gray-300 transition-colors duration-300">{{ $t('builder.labels.ram') }}</label>
          <div class="flex flex-wrap gap-2 items-center" v-if="selected.mb">
            <div class="w-36 z-50">
              <CustomSelect v-model="filters.ram.brand" :options="getBrandOptions(availableBrands.ram)" :placeholder="$t('builder.filters.allBrands')" :labelFunc="(item) => item.name" />
            </div>
            
            <select v-model="filters.ram.sort" class="px-3 py-2 bg-slate-50 dark:bg-[#121212] border border-slate-200 dark:border-[#333] rounded-xl text-xs outline-none focus:border-blue-500 dark:focus:border-orange-500 text-slate-700 dark:text-gray-300 transition-colors duration-300 cursor-pointer">
              <option value="default">{{ $t('builder.filters.sortDefault') }}</option>
              <option value="asc">{{ $t('builder.filters.sortAsc') }}</option>
              <option value="desc">{{ $t('builder.filters.sortDesc') }}</option>
            </select>

            <input v-model.number="filters.ram.minPrice" type="number" :placeholder="$t('builder.filters.minPrice')" class="px-3 py-2 bg-slate-50 dark:bg-[#121212] border border-slate-200 dark:border-[#333] rounded-xl text-xs w-24 outline-none focus:border-blue-500 dark:focus:border-orange-500 text-slate-700 dark:text-gray-300 transition-colors duration-300 placeholder-slate-400 dark:placeholder-gray-600">
            <input v-model.number="filters.ram.maxPrice" type="number" :placeholder="$t('builder.filters.maxPrice')" class="px-3 py-2 bg-slate-50 dark:bg-[#121212] border border-slate-200 dark:border-[#333] rounded-xl text-xs w-24 outline-none focus:border-blue-500 dark:focus:border-orange-500 text-slate-700 dark:text-gray-300 transition-colors duration-300 placeholder-slate-400 dark:placeholder-gray-600">
          </div>
        </div>
        <div class="z-40">
          <CustomSelect v-model="selected.ram" :options="filteredOptions.rams" :disabled="!selected.mb" :placeholder="selected.mb ? $t('builder.placeholders.selectRam') : $t('builder.placeholders.needMbFirst')" :labelFunc="(item) => formatOption(item, 'ram')" />
        </div>
      </div>

      <!-- GPU -->
      <div class="mb-2 relative">
        <div class="flex flex-wrap justify-between items-center mb-3 gap-2">
          <label class="text-sm font-semibold text-slate-700 dark:text-gray-300 transition-colors duration-300">{{ $t('builder.labels.gpu') }}</label>
          <div class="flex flex-wrap gap-2 items-center">
            <div class="w-36 z-30">
              <CustomSelect v-model="filters.gpu.brand" :options="getBrandOptions(availableBrands.gpu)" :placeholder="$t('builder.filters.allBrands')" :labelFunc="(item) => item.name" />
            </div>
            
            <select v-model="filters.gpu.sort" class="px-3 py-2 bg-slate-50 dark:bg-[#121212] border border-slate-200 dark:border-[#333] rounded-xl text-xs outline-none focus:border-blue-500 dark:focus:border-orange-500 text-slate-700 dark:text-gray-300 transition-colors duration-300 cursor-pointer">
              <option value="default">{{ $t('builder.filters.sortDefault') }}</option>
              <option value="asc">{{ $t('builder.filters.sortAsc') }}</option>
              <option value="desc">{{ $t('builder.filters.sortDesc') }}</option>
            </select>

            <input v-model.number="filters.gpu.minPrice" type="number" :placeholder="$t('builder.filters.minPrice')" class="px-3 py-2 bg-slate-50 dark:bg-[#121212] border border-slate-200 dark:border-[#333] rounded-xl text-xs w-24 outline-none focus:border-blue-500 dark:focus:border-orange-500 text-slate-700 dark:text-gray-300 transition-colors duration-300 placeholder-slate-400 dark:placeholder-gray-600">
            <input v-model.number="filters.gpu.maxPrice" type="number" :placeholder="$t('builder.filters.maxPrice')" class="px-3 py-2 bg-slate-50 dark:bg-[#121212] border border-slate-200 dark:border-[#333] rounded-xl text-xs w-24 outline-none focus:border-blue-500 dark:focus:border-orange-500 text-slate-700 dark:text-gray-300 transition-colors duration-300 placeholder-slate-400 dark:placeholder-gray-600">
          </div>
        </div>
        <div class="z-20">
          <CustomSelect v-model="selected.gpu" :options="filteredOptions.gpus" :placeholder="$t('builder.placeholders.selectGpu')" :labelFunc="(item) => formatOption(item, 'gpu')" />
        </div>
      </div>
    </div>

    <!-- ШАГ 3: КОРПУС И ПИТАНИЕ -->
    <div class="bg-white dark:bg-[#1e1e1e] p-6 rounded-3xl shadow-md hover:shadow-xl border border-slate-200 dark:border-[#2a2a2a] transition-all duration-300">
      <h2 class="text-xl font-bold mb-6 border-b border-slate-100 dark:border-[#333] pb-3 text-blue-600 dark:text-orange-500 transition-colors duration-300">{{ $t('builder.step3_title') }}</h2>
      
      <!-- PSU -->
      <div class="mb-6 relative">
        <div class="flex flex-wrap justify-between items-center mb-3 gap-2">
          <label class="text-sm font-semibold text-slate-700 dark:text-gray-300 transition-colors duration-300">{{ $t('builder.labels.psu') }}</label>
          <div class="flex flex-wrap gap-2 items-center">
            <div class="w-36 z-50">
              <CustomSelect v-model="filters.psu.brand" :options="getBrandOptions(availableBrands.psu)" :placeholder="$t('builder.filters.allBrands')" :labelFunc="(item) => item.name" />
            </div>
            
            <select v-model="filters.psu.sort" class="px-3 py-2 bg-slate-50 dark:bg-[#121212] border border-slate-200 dark:border-[#333] rounded-xl text-xs outline-none focus:border-blue-500 dark:focus:border-orange-500 text-slate-700 dark:text-gray-300 transition-colors duration-300 cursor-pointer">
              <option value="default">{{ $t('builder.filters.sortDefault') }}</option>
              <option value="asc">{{ $t('builder.filters.sortAsc') }}</option>
              <option value="desc">{{ $t('builder.filters.sortDesc') }}</option>
            </select>

            <input v-model.number="filters.psu.minWatt" type="number" :placeholder="$t('builder.filters.minW')" class="px-3 py-2 bg-slate-50 dark:bg-[#121212] border border-slate-200 dark:border-[#333] rounded-xl text-xs w-20 outline-none focus:border-blue-500 dark:focus:border-orange-500 text-slate-700 dark:text-gray-300 transition-colors duration-300 placeholder-slate-400 dark:placeholder-gray-600">
            <input v-model.number="filters.psu.minPrice" type="number" :placeholder="$t('builder.filters.minPrice')" class="px-3 py-2 bg-slate-50 dark:bg-[#121212] border border-slate-200 dark:border-[#333] rounded-xl text-xs w-20 outline-none focus:border-blue-500 dark:focus:border-orange-500 text-slate-700 dark:text-gray-300 transition-colors duration-300 placeholder-slate-400 dark:placeholder-gray-600">
            <input v-model.number="filters.psu.maxPrice" type="number" :placeholder="$t('builder.filters.maxPrice')" class="px-3 py-2 bg-slate-50 dark:bg-[#121212] border border-slate-200 dark:border-[#333] rounded-xl text-xs w-20 outline-none focus:border-blue-500 dark:focus:border-orange-500 text-slate-700 dark:text-gray-300 transition-colors duration-300 placeholder-slate-400 dark:placeholder-gray-600">
          </div>
        </div>
        <div class="z-40">
          <CustomSelect v-model="selected.psu" :options="filteredOptions.psus" :placeholder="$t('builder.placeholders.selectPsu')" :labelFunc="(item) => formatOption(item, 'psu')" />
        </div>
        <p v-if="systemTdp > 0" class="text-xs text-blue-500 dark:text-orange-400 font-semibold mt-2 transition-colors duration-300">
          {{ $t('builder.hints.tdpHint', { tdp: systemTdp, psu: recommendedPsu }) }}
        </p>
      </div>

      <!-- CASE -->
      <div class="mb-2 relative">
        <div class="flex flex-wrap justify-between items-center mb-3 gap-2">
          <label class="text-sm font-semibold text-slate-700 dark:text-gray-300 transition-colors duration-300">{{ $t('builder.labels.case') }}</label>
          <div class="flex flex-wrap gap-2 items-center" v-if="selected.mb">
            <div class="w-36 z-30">
              <CustomSelect v-model="filters.case.brand" :options="getBrandOptions(availableBrands.case)" :placeholder="$t('builder.filters.allBrands')" :labelFunc="(item) => item.name" />
            </div>
            
            <select v-model="filters.case.sort" class="px-3 py-2 bg-slate-50 dark:bg-[#121212] border border-slate-200 dark:border-[#333] rounded-xl text-xs outline-none focus:border-blue-500 dark:focus:border-orange-500 text-slate-700 dark:text-gray-300 transition-colors duration-300 cursor-pointer">
              <option value="default">{{ $t('builder.filters.sortDefault') }}</option>
              <option value="asc">{{ $t('builder.filters.sortAsc') }}</option>
              <option value="desc">{{ $t('builder.filters.sortDesc') }}</option>
            </select>

            <input v-model.number="filters.case.minPrice" type="number" :placeholder="$t('builder.filters.minPrice')" class="px-3 py-2 bg-slate-50 dark:bg-[#121212] border border-slate-200 dark:border-[#333] rounded-xl text-xs w-24 outline-none focus:border-blue-500 dark:focus:border-orange-500 text-slate-700 dark:text-gray-300 transition-colors duration-300 placeholder-slate-400 dark:placeholder-gray-600">
            <input v-model.number="filters.case.maxPrice" type="number" :placeholder="$t('builder.filters.maxPrice')" class="px-3 py-2 bg-slate-50 dark:bg-[#121212] border border-slate-200 dark:border-[#333] rounded-xl text-xs w-24 outline-none focus:border-blue-500 dark:focus:border-orange-500 text-slate-700 dark:text-gray-300 transition-colors duration-300 placeholder-slate-400 dark:placeholder-gray-600">
          </div>
        </div>
        <div class="z-20">
          <CustomSelect v-model="selected.case" :options="filteredOptions.cases" :disabled="!selected.mb" :placeholder="selected.mb ? $t('builder.placeholders.selectCase') : $t('builder.placeholders.needMbFirst')" :labelFunc="(item) => formatOption(item, 'case')" />
        </div>
      </div>
    </div>
  </div>
        <!-- Итоговая сборка (Сайдбар) -->
        <div class="bg-white dark:bg-[#1a1a1a] p-6 rounded-3xl shadow-xl border border-blue-200 dark:border-orange-500/20 h-fit sticky top-24 transition-colors duration-300">
          <div class="flex justify-between items-center mb-4 border-b border-slate-100 dark:border-[#333] pb-3">
            <h2 class="text-xl font-bold flex items-center gap-2 text-slate-800 dark:text-white transition-colors duration-300">
              <svg class="w-5 h-5 text-blue-600 dark:text-orange-500 transition-colors duration-300" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 014 0z"></path></svg>
              {{ $t('builder.summary_title') }}
            </h2>
            
            <!-- Кнопка очистки сборки -->
            <button v-if="hasItemsInCart" @click="clearBuilder" class="text-xs font-semibold text-slate-400 hover:text-red-500 transition-colors bg-slate-100 dark:bg-[#222] px-2 py-1 rounded-md" :title="$t('builder.summary.reset')">
              {{ $t('builder.summary.reset') }}
            </button>
          </div>
          
          <ul class="space-y-4 mb-6 min-h-[150px]">
            <li v-if="!hasItemsInCart" class="text-slate-400 dark:text-gray-500 text-sm italic text-center mt-10 transition-colors duration-300">
              {{ $t('builder.summary.empty') }}
            </li>
            
            <template v-for="row in cartItems" :key="row.id">
              <li v-if="row.item" class="flex items-center gap-3 border-b border-slate-100 dark:border-[#333] pb-3 animate-[fadeIn_0.3s_ease-out] group transition-colors duration-300">
                <div class="w-12 h-12 flex-shrink-0 bg-slate-50 dark:bg-[#222] border border-slate-200 dark:border-[#444] rounded-lg p-1 flex items-center justify-center transition-colors duration-300">
                  <img v-if="row.img" :src="row.img" class="max-w-full max-h-full object-contain" />
                  <span v-else class="text-[10px] text-slate-400 dark:text-gray-500 text-center leading-tight transition-colors duration-300" v-html="$t('builder.summary.noPhoto')"></span>
                </div>
                
                <div class="flex-grow pr-1">
                  <span class="text-[11px] uppercase tracking-wider font-bold text-blue-500 dark:text-orange-500 block mb-0.5 transition-colors duration-300">{{ row.label }}</span> 
                  <span class="text-sm font-medium text-slate-700 dark:text-gray-200 leading-snug block transition-colors duration-300">{{ row.name }}</span>
                </div>
                
                <div class="flex items-center gap-2">
                  <div class="font-bold text-slate-800 dark:text-gray-100 whitespace-nowrap transition-colors duration-300">{{ row.price }} ₴</div>
                  
                  <button @click="removeComponent(row.id)" class="text-slate-400 dark:text-gray-500 hover:text-red-500 transition-colors p-1" :title="$t('builder.summary.remove')">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" /></svg>
                  </button>
                </div>
              </li>
            </template>
          </ul>

          <div class="border-t border-slate-200 dark:border-[#333] pt-5 mt-2 transition-colors duration-300">
            <div class="flex justify-between items-center text-xl font-black text-slate-800 dark:text-gray-100 transition-colors duration-300">
              <span>{{ $t('builder.summary.total') }}</span>
              <span class="text-blue-600 dark:text-orange-500 transition-colors duration-300">{{ totalPrice }} ₴</span>
            </div>
            <div class="flex justify-between items-center text-sm font-medium text-slate-500 dark:text-gray-400 mt-2 transition-colors duration-300">
              <span>{{ $t('builder.summary.tdp') }}</span>
              <span>{{ totalTdpCalc }} W</span>
            </div>
            
            <button @click="openSaveModal" class="w-full mt-6 bg-blue-600 dark:bg-orange-600 hover:bg-blue-700 dark:hover:bg-orange-500 text-white font-bold py-3 px-4 rounded-full transition-all shadow-lg dark:shadow-[0_0_15px_rgba(234,88,12,0.3)] flex justify-center items-center gap-2 uppercase tracking-wide">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7H5a2 2 0 00-2 2v9a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-3m-1 4l-3 3m0 0l-3-3m3 3V4"></path></svg>
              {{ currentBuildId ? $t('builder.summary.updateBtn') : $t('builder.summary.saveBtn') }}
            </button>
          </div>
        </div>

      </div>

      <!-- === ЭКРАН 2: ЛИЧНЫЙ КАБИНЕТ === -->
      <div v-else-if="currentView === 'profile'" class="space-y-6 animate-[fadeIn_0.3s_ease-out]">
        
        <div class="bg-white dark:bg-[#1e1e1e] p-8 rounded-3xl shadow-md border border-slate-200 dark:border-[#2a2a2a] transition-colors duration-300">
          <h2 class="text-2xl font-bold mb-6 border-b border-slate-100 dark:border-[#333] pb-3 text-blue-600 dark:text-orange-500 transition-colors duration-300">{{ $t('profile.settingsTitle') }}</h2>
          
          <form @submit.prevent="updateProfile" class="max-w-md space-y-4">
            <div>
              <label class="block text-sm font-semibold text-slate-700 dark:text-gray-300 mb-2 transition-colors duration-300">{{ $t('profile.newUsername') }}</label>
              <input v-model="profileForm.username" type="text" :placeholder="$t('profile.leaveEmpty')" class="w-full p-3 bg-slate-50 dark:bg-[#121212] border border-slate-200 dark:border-[#333] text-slate-800 dark:text-gray-200 rounded-xl focus:border-blue-500 dark:focus:border-orange-500 outline-none placeholder-slate-400 dark:placeholder-gray-600 transition-colors duration-300">
            </div>
            <div>
              <label class="block text-sm font-semibold text-slate-700 dark:text-gray-300 mb-2 transition-colors duration-300">{{ $t('profile.newPassword') }}</label>
              <input v-model="profileForm.password" type="password" :placeholder="$t('profile.leaveEmpty')" class="w-full p-3 bg-slate-50 dark:bg-[#121212] border border-slate-200 dark:border-[#333] text-slate-800 dark:text-gray-200 rounded-xl focus:border-blue-500 dark:focus:border-orange-500 outline-none placeholder-slate-400 dark:placeholder-gray-600 transition-colors duration-300">
            </div>
            <button type="submit" class="bg-slate-800 dark:bg-[#2a2a2a] hover:bg-slate-900 dark:hover:bg-[#333] border border-transparent dark:border-[#444] text-white font-bold py-3 px-6 rounded-full transition-all mt-2">
              {{ $t('profile.saveChanges') }}
            </button>
            <p class="text-xs text-slate-500 dark:text-orange-500/70 mt-2 transition-colors duration-300">{{ $t('profile.passwordWarning') }}</p>
          </form>
        </div>

        <div class="bg-white dark:bg-[#1e1e1e] p-8 rounded-3xl shadow-md border border-slate-200 dark:border-[#2a2a2a] transition-colors duration-300">
          <h2 class="text-2xl font-bold mb-6 border-b border-slate-100 dark:border-[#333] pb-3 text-blue-600 dark:text-orange-500 transition-colors duration-300">{{ $t('profile.buildsTitle') }}</h2>
          
          <div v-if="userBuilds.length === 0" class="text-slate-500 dark:text-gray-500 italic transition-colors duration-300">
            {{ $t('profile.noBuilds') }}
          </div>
          
          <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div v-for="b in userBuilds" :key="b.id" 
                 @click="loadBuild(b)" 
                 class="bg-slate-50 dark:bg-[#1a1a1a] border border-slate-200 dark:border-[#333] rounded-2xl p-5 hover:border-blue-500 dark:hover:border-orange-500 hover:shadow-lg dark:hover:shadow-[0_0_15px_rgba(234,88,12,0.1)] transition-all cursor-pointer relative group">
              
              <div class="flex justify-between items-start mb-4">
                <h3 class="font-bold text-lg text-slate-800 dark:text-gray-100 group-hover:text-blue-600 dark:group-hover:text-orange-500 transition-colors">{{ b.build_name }}</h3>
                <button @click.stop="buildToDelete = b.id" class="text-slate-400 dark:text-gray-500 hover:text-red-500 bg-white dark:bg-[#222] p-2 rounded-lg border border-slate-200 dark:border-[#333] transition-colors duration-300" :title="$t('profile.deleteHint')">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path></svg>
                </button>
              </div>
              
              <div class="text-sm text-slate-600 dark:text-gray-400 space-y-2 transition-colors duration-300">
                <p class="flex justify-between border-b border-slate-200 dark:border-[#222] pb-1"><strong class="text-slate-500 dark:text-gray-500 text-xs uppercase tracking-wider">CPU:</strong> <span class="text-right ml-2 truncate text-slate-700 dark:text-gray-300">{{ getComponentName('cpus', b.cpu_id) }}</span></p>
                <p class="flex justify-between border-b border-slate-200 dark:border-[#222] pb-1"><strong class="text-slate-500 dark:text-gray-500 text-xs uppercase tracking-wider">MB:</strong> <span class="text-right ml-2 truncate text-slate-700 dark:text-gray-300">{{ getComponentName('mbs', b.motherboard_id) }}</span></p>
                <p class="flex justify-between border-b border-slate-200 dark:border-[#222] pb-1"><strong class="text-slate-500 dark:text-gray-500 text-xs uppercase tracking-wider">Cooler:</strong> <span class="text-right ml-2 truncate text-slate-700 dark:text-gray-300">{{ getComponentName('coolers', b.cooler_id) }}</span></p>
                <p class="flex justify-between border-b border-slate-200 dark:border-[#222] pb-1"><strong class="text-slate-500 dark:text-gray-500 text-xs uppercase tracking-wider">RAM:</strong> <span class="text-right ml-2 truncate text-slate-700 dark:text-gray-300">{{ getComponentName('rams', b.ram_id) }}</span></p>
                <p class="flex justify-between border-b border-slate-200 dark:border-[#222] pb-1"><strong class="text-slate-500 dark:text-gray-500 text-xs uppercase tracking-wider">GPU:</strong> <span class="text-right ml-2 truncate text-slate-700 dark:text-gray-300">{{ getComponentName('gpus', b.gpu_id) }}</span></p>
                <p class="flex justify-between border-b border-slate-200 dark:border-[#222] pb-1"><strong class="text-slate-500 dark:text-gray-500 text-xs uppercase tracking-wider">PSU:</strong> <span class="text-right ml-2 truncate text-slate-700 dark:text-gray-300">{{ getComponentName('psus', b.psu_id) }}</span></p>
                <p class="flex justify-between border-b border-slate-200 dark:border-[#222] pb-1"><strong class="text-slate-500 dark:text-gray-500 text-xs uppercase tracking-wider">Case:</strong> <span class="text-right ml-2 truncate text-slate-700 dark:text-gray-300">{{ getComponentName('cases', b.case_id) }}</span></p>
              </div>
              
              <div class="mt-5 pt-4 border-t border-slate-200 dark:border-[#333] flex justify-between items-center transition-colors duration-300">
                <span class="text-[11px] font-bold text-blue-500 dark:text-orange-500 uppercase tracking-wide opacity-0 group-hover:opacity-100 transition-opacity">{{ $t('profile.openBuilder') }} ({{ $t('profile.editBuild') }})</span>
                <span class="text-xs text-slate-400 dark:text-gray-500">{{ b.created_at ? new Date(b.created_at).toLocaleDateString() : $t('profile.recently') }}</span>
              </div>
            </div>
          </div>
        </div>

      </div>
    </main>

    <!-- Модальное окно авторизации/регистрации -->
    <div v-if="showAuthModal" class="fixed inset-0 bg-slate-900/50 dark:bg-black/70 backdrop-blur-sm z-[100] flex items-center justify-center p-4 animate-[fadeIn_0.2s_ease-out] transition-colors duration-300">
      <div class="bg-white dark:bg-[#1e1e1e] border border-transparent dark:border-[#333] rounded-3xl shadow-2xl w-full max-w-md overflow-hidden relative transition-colors duration-300">
        <button @click="showAuthModal = false" class="absolute top-5 right-5 text-slate-400 dark:text-gray-500 hover:text-slate-800 dark:hover:text-white transition-colors">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
        </button>

        <div class="p-8">
          <h2 class="text-2xl font-bold text-slate-800 dark:text-white mb-6 text-center transition-colors duration-300">
            {{ isLoginMode ? $t('auth.loginTitle') : $t('auth.registerTitle') }}
          </h2>

          <form @submit.prevent="submitAuth" class="space-y-4">
            <div>
              <label class="block text-sm font-semibold text-slate-700 dark:text-gray-300 mb-2 transition-colors duration-300">{{ $t('auth.username') }}</label>
              <input v-model="authForm.username" type="text" required class="w-full p-3 bg-slate-50 dark:bg-[#121212] border border-slate-300 dark:border-[#333] text-slate-800 dark:text-white rounded-xl focus:border-blue-500 dark:focus:border-orange-500 outline-none transition-colors duration-300">
            </div>

            <div v-if="!isLoginMode">
              <label class="block text-sm font-semibold text-slate-700 dark:text-gray-300 mb-2 transition-colors duration-300">{{ $t('auth.email') }}</label>
              <input v-model="authForm.email" type="email" required class="w-full p-3 bg-slate-50 dark:bg-[#121212] border border-slate-300 dark:border-[#333] text-slate-800 dark:text-white rounded-xl focus:border-blue-500 dark:focus:border-orange-500 outline-none transition-colors duration-300">
            </div>

            <div>
              <label class="block text-sm font-semibold text-slate-700 dark:text-gray-300 mb-2 transition-colors duration-300">{{ $t('auth.password') }}</label>
              <input v-model="authForm.password" type="password" required class="w-full p-3 bg-slate-50 dark:bg-[#121212] border border-slate-300 dark:border-[#333] text-slate-800 dark:text-white rounded-xl focus:border-blue-500 dark:focus:border-orange-500 outline-none transition-colors duration-300">
            </div>

            <button type="submit" class="w-full bg-blue-600 dark:bg-orange-600 hover:bg-blue-700 dark:hover:bg-orange-500 text-white font-bold py-3 px-4 rounded-full transition-all shadow-md dark:shadow-[0_0_15px_rgba(234,88,12,0.2)] mt-4">
              {{ isLoginMode ? $t('auth.loginBtn') : $t('auth.registerBtn') }}
            </button>
          </form>

          <div class="mt-6 text-center text-sm text-slate-500 dark:text-gray-400 transition-colors duration-300">
            {{ isLoginMode ? $t('auth.noAccount') : $t('auth.hasAccount') }}
            <button @click="toggleAuthMode" class="text-blue-600 dark:text-orange-500 font-bold hover:text-blue-800 dark:hover:text-orange-400 ml-1 transition-colors">
              {{ isLoginMode ? $t('auth.createBtn') : $t('auth.loginBtn') }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Модальное окно сохранения/ОБНОВЛЕНИЯ сборки -->
    <div v-if="showSaveModal" class="fixed inset-0 bg-slate-900/50 dark:bg-black/70 backdrop-blur-sm z-[100] flex items-center justify-center p-4 animate-[fadeIn_0.2s_ease-out] transition-colors duration-300">
      <div class="bg-white dark:bg-[#1e1e1e] border border-transparent dark:border-[#333] rounded-3xl shadow-2xl w-full max-w-md overflow-hidden relative transition-colors duration-300">
        <button @click="showSaveModal = false" class="absolute top-5 right-5 text-slate-400 dark:text-gray-500 hover:text-slate-800 dark:hover:text-white transition-colors">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
        </button>

        <div class="p-8">
          <h2 class="text-2xl font-bold text-slate-800 dark:text-white mb-6 text-center transition-colors duration-300">
            {{ currentBuildId ? $t('modals.save.titleUpdate') : $t('modals.save.titleSave') }}
          </h2>

          <div class="space-y-4">
            <div>
              <label class="block text-sm font-semibold text-slate-700 dark:text-gray-300 mb-2 transition-colors duration-300">{{ $t('modals.save.buildNameLabel') }}</label>
              <input v-model="newBuildName" type="text" :placeholder="$t('modals.save.buildNamePlaceholder')" class="w-full p-3 bg-slate-50 dark:bg-[#121212] border border-slate-300 dark:border-[#333] text-slate-800 dark:text-white rounded-xl focus:border-blue-500 dark:focus:border-orange-500 outline-none transition-colors duration-300" @keyup.enter="confirmSaveBuild(false)">
            </div>

            <div v-if="currentBuildId" class="flex flex-col gap-2 pt-2">
              <button @click="confirmSaveBuild(false)" class="w-full bg-emerald-500 dark:bg-orange-600 hover:bg-emerald-600 dark:hover:bg-orange-500 text-white font-bold py-3 px-4 rounded-full transition-all shadow-md mt-2">
                {{ $t('modals.save.updateCurrent') }}
              </button>
              <button @click="confirmSaveBuild(true)" class="w-full bg-blue-100 dark:bg-[#333] text-blue-700 dark:text-gray-200 hover:bg-blue-200 dark:hover:bg-[#444] font-bold py-3 px-4 rounded-full transition-all">
                {{ $t('modals.save.saveAsNew') }}
              </button>
            </div>
            
            <button v-else @click="confirmSaveBuild(false)" class="w-full bg-blue-600 dark:bg-orange-600 hover:bg-blue-700 dark:hover:bg-orange-500 text-white font-bold py-3 px-4 rounded-full transition-all shadow-md dark:shadow-[0_0_15px_rgba(234,88,12,0.2)] mt-4">
              {{ $t('modals.save.saveBtn') }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Модальное окно подтверждения удаления (НОВОЕ) -->
    <div v-if="buildToDelete" class="fixed inset-0 bg-slate-900/50 dark:bg-black/70 backdrop-blur-sm z-[100] flex items-center justify-center p-4 animate-[fadeIn_0.2s_ease-out] transition-colors duration-300">
      <div class="bg-white dark:bg-[#1e1e1e] border border-transparent dark:border-[#333] rounded-3xl shadow-2xl w-full max-w-sm p-6 text-center transition-colors duration-300 relative overflow-hidden">
        
        <div class="w-16 h-16 bg-red-100 dark:bg-red-900/30 text-red-500 rounded-full flex items-center justify-center mx-auto mb-4">
          <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path></svg>
        </div>
        
        <h3 class="text-xl font-bold text-slate-800 dark:text-white mb-2">{{ $t('modals.delete.title') }}</h3>
        <p class="text-sm text-slate-500 dark:text-gray-400 mb-6">{{ $t('modals.delete.description') }}</p>
        
        <div class="flex gap-3">
          <button @click="buildToDelete = null" class="flex-1 bg-slate-100 dark:bg-[#333] hover:bg-slate-200 dark:hover:bg-[#444] text-slate-700 dark:text-gray-200 font-bold py-3 px-4 rounded-xl transition-all">
            {{ $t('modals.delete.cancel') }}
          </button>
          <button @click="confirmDeleteBuild" class="flex-1 bg-red-500 hover:bg-red-600 text-white font-bold py-3 px-4 rounded-xl transition-all shadow-md">
            {{ $t('modals.delete.confirm') }}
          </button>
        </div>
      </div>
    </div>

    <!-- Уведомления (Toasts) -->
    <transition name="toast-fade">
      <div v-if="toast.show" class="fixed bottom-6 right-6 px-6 py-4 rounded-2xl shadow-2xl z-[999] flex items-center gap-3 transition-all duration-300" :class="toast.type === 'error' ? 'bg-red-500/95 text-white backdrop-blur-md' : 'bg-slate-800/95 dark:bg-orange-600/95 text-white backdrop-blur-md'">
        <svg v-if="toast.type === 'success'" class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
        <svg v-else class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
        <span class="font-medium tracking-wide">{{ toast.message }}</span>
      </div>
    </transition>

  </div>
</template>

<script setup>
import { reactive, computed, onMounted, watch, ref } from 'vue';
import { useI18n } from 'vue-i18n';
import CustomSelect from './components/CustomSelect.vue';

const { t, locale } = useI18n();

const API = 'http://127.0.0.1:8000/api/v1';

// --- ЛОГИКА ТЕМЫ (Dark/Light) ---
const isDarkMode = ref(
  localStorage.getItem('theme') === 'dark' || 
  (!localStorage.getItem('theme') && window.matchMedia('(prefers-color-scheme: dark)').matches)
);

const applyTheme = () => {
  if (isDarkMode.value) {
    document.documentElement.classList.add('dark');
  } else {
    document.documentElement.classList.remove('dark');
  }
};

const toggleTheme = () => {
  isDarkMode.value = !isDarkMode.value;
  localStorage.setItem('theme', isDarkMode.value ? 'dark' : 'light');
  applyTheme();
};

const changeLanguage = (lang) => {
  locale.value = lang;
  localStorage.setItem('lang', lang);
};

// --- УВЕДОМЛЕНИЯ (Toasts) ---
const toast = reactive({ show: false, message: '', type: 'success' });
const showToast = (msg, type = 'success') => {
  toast.message = msg;
  toast.type = type;
  toast.show = true;
  setTimeout(() => { toast.show = false; }, 3000);
};

// --- СОСТОЯНИЕ КОНСТРУКТОРА ---
const isRestoring = ref(false); 
const buildToDelete = ref(null);
const currentBuildId = ref(null); // ID текущей редактируемой сборки

const options = reactive({ cpus: [], mbs: [], coolers: [], rams: [], gpus: [], psus: [], cases: [] });
const selected = reactive({ cpu: null, mb: null, cooler: null, ram: null, gpu: null, psu: null, case: null });

const systemTdp = ref(0);
const recommendedPsu = ref(0);

const filters = reactive({
  cpu: { brand: null, minPrice: null, maxPrice: null, sort: 'default' },
  mb: { brand: null, minPrice: null, maxPrice: null, sort: 'default' },
  cooler: { brand: null, minPrice: null, maxPrice: null, sort: 'default' },
  ram: { brand: null, minPrice: null, maxPrice: null, sort: 'default' },
  gpu: { brand: null, minPrice: null, maxPrice: null, sort: 'default' },
  psu: { brand: null, minWatt: null, minPrice: null, maxPrice: null, sort: 'default' },
  case: { brand: null, minPrice: null, maxPrice: null, sort: 'default' }
});

const auth = reactive({
  isAuthenticated: !!localStorage.getItem('token'),
  username: localStorage.getItem('username') || '',
  token: localStorage.getItem('token') || null
});

const showAuthModal = ref(false);
const isLoginMode = ref(true);
const authError = ref('');
const authForm = reactive({ username: '', email: '', password: '' });

// Переменные для новой модалки сохранения
const showSaveModal = ref(false);
const newBuildName = ref('Моя сборка');

const currentView = ref('builder'); 
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

const clearBuilder = () => {
  selected.cpu = null; selected.mb = null; selected.cooler = null;
  selected.ram = null; selected.gpu = null; selected.psu = null; selected.case = null;
  currentBuildId.value = null; // Сбрасываем ID сборки, теперь это новая сборка
  newBuildName.value = 'Моя сборка';
  showToast('Сборка сброшена', 'success');
};

// --- АВТОРИЗАЦИЯ И ПРОФИЛЬ ---
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
        body: JSON.stringify({ username: authForm.username, email: authForm.email, password: authForm.password })
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
      showToast(t('alerts.saveSuccess') || 'Успешный вход!', 'success');
    } else {
      showToast('Регистрация успешна! Теперь вы можете войти.', 'success');
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
      await fetch(`${API}/pass/logout`, { method: 'POST', headers: { 'Authorization': `Bearer ${auth.token}` } });
    } catch (e) { console.error(e); }
  }
  localStorage.removeItem('token');
  localStorage.removeItem('username');
  auth.isAuthenticated = false;
  auth.token = null;
  auth.username = '';
  currentView.value = 'builder';
};

const openProfile = () => {
  currentView.value = 'profile';
  fetchUserBuilds();
};

const fetchUserBuilds = async () => {
  const userId = getUserIdFromToken();
  if (!userId) return;

  try {
    const res = await fetch(`${API}/build/${userId}`, { headers: { 'Authorization': `Bearer ${auth.token}` } });
    const data = await res.json();
    
    // ДОБАВЛЕНА СТРОКА ДЛЯ ДЕБАГА
    console.log("ДАННЫЕ СБОРКИ С БЭКЕНДА (СМОТРИ КЛЮЧИ):", data); 
    
    if (res.ok) {
      if (Array.isArray(data)) userBuilds.value = data;
      else if (data && Array.isArray(data.data)) userBuilds.value = data.data;
      else userBuilds.value = [];
    }
  } catch (e) { console.error(e); }
};

const confirmDeleteBuild = async () => {
  if (!buildToDelete.value) return;
  
  try {
    const res = await fetch(`${API}/build/${buildToDelete.value}`, { 
      method: 'DELETE', 
      headers: { 'Authorization': `Bearer ${auth.token}` } 
    });
    
    if (res.ok) {
      userBuilds.value = userBuilds.value.filter(b => b.id !== buildToDelete.value);
      if (currentBuildId.value === buildToDelete.value) currentBuildId.value = null;
      showToast('Збірку успішно видалено', 'success');
    } else {
      throw new Error();
    }
  } catch (e) { 
    showToast('Помилка видалення', 'error'); 
  } finally {
    buildToDelete.value = null; // Закрываем модалку в любом случае
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
      headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${auth.token}` },
      body: JSON.stringify(payload)
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail);

    showToast(data.message || 'Профиль обновлен', 'success');
    
    if (payload.updated_username) {
      auth.username = payload.updated_username;
      localStorage.setItem('username', payload.updated_username);
    }
    if (payload.updated_password) {
      showToast("Пароль изменен. Пожалуйста, войдите заново.", "success");
      logout();
    }
    profileForm.username = '';
    profileForm.password = '';
  } catch (e) {
    showToast(e.message, 'error');
  }
};

// Открытие модалки сохранения
const openSaveModal = () => {
  if (!auth.isAuthenticated) {
    showToast("Пожалуйста, войдите в аккаунт!", 'error');
    showAuthModal.value = true;
    return;
  }
  if (!selected.cpu || !selected.mb || !selected.ram || !selected.psu || !selected.case) {
    showToast("Соберите базовую конфигурацию!", 'error');
    return;
  }
  if (!currentBuildId.value) newBuildName.value = 'Моя сборка';
  showSaveModal.value = true;
};

// Сохранение / Обновление сборки
const confirmSaveBuild = async (saveAsNew = false) => {
  if (!newBuildName.value.trim()) {
    showToast("Введите название сборки!", 'error');
    return;
  }

  const payload = {
    build_name: newBuildName.value.trim(), 
    cpu_id: selected.cpu.id, 
    motherboard_id: selected.mb.id,
    ram_id: selected.ram.id, 
    gpu_id: selected.gpu?.id || null,
    psu_id: selected.psu.id,
    case_id: selected.case.id, 
    cooler_id: selected.cooler?.id || null
  };

  const isUpdating = currentBuildId.value && !saveAsNew;
  
  const url = isUpdating ? `${API}/build/${currentBuildId.value}` : `${API}/build/`;

  const method = isUpdating ? 'PATCH' : 'POST';

  try {
    const res = await fetch(url, {
      method: method,
      headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${auth.token}` },
      body: JSON.stringify(payload)
    });
    const data = await res.json();
    if (!res.ok) {
      const errorMsg = Array.isArray(data.detail) ? JSON.stringify(data.detail) : (data.detail || "Ошибка");
      throw new Error(errorMsg);
    }
    
    showToast(isUpdating ? "Сборка успешно обновлена!" : "Новая сборка сохранена!", 'success');
    showSaveModal.value = false;
    
    // Если сохранили как новую, запоминаем её новый ID, чтобы дальше редактировать её же
    if (saveAsNew && data.build_id) {
      currentBuildId.value = data.build_id;
    }
    
    fetchUserBuilds();
  } catch (e) {
    showToast(e.message, 'error');
  }
};

const loadBuild = async (build) => {
  isRestoring.value = true;
  currentView.value = 'builder'; 
  
  // Запоминаем ID и имя редактируемой сборки
  currentBuildId.value = build.id;
  newBuildName.value = build.build_name;
  
  try {
    await Promise.all([
      fetchMBs(build.cpu_id), fetchCoolers(build.cpu_id),
      fetchRAMs(build.motherboard_id), fetchCases(build.motherboard_id),
      fetchPSUs(build.cpu_id, build.gpu_id)
    ]);
    selected.cpu = options.cpus.find(c => c.id == build.cpu_id) || null;
    selected.mb = options.mbs.find(m => m.id == build.motherboard_id) || null;
    selected.cooler = options.coolers.find(c => c.id == build.cooler_id) || null;
    selected.ram = options.rams.find(r => r.id == build.ram_id) || null;
    selected.gpu = options.gpus.find(g => g.id == build.gpu_id) || null;
    selected.psu = options.psus.find(p => p.id == build.psu_id) || null;
    selected.case = options.cases.find(c => c.id == build.case_id) || null;
    Object.keys(filters).forEach(key => { filters[key].brand = null; });
  } catch (e) {
    showToast("Не удалось загрузить сборку", 'error');
  } finally {
    setTimeout(() => { isRestoring.value = false; }, 100);
  }
};

// --- ФОРМАТИРОВАНИЕ ДЛЯ CUSTOM SELECT ---
const getBrandOptions = (brandsArr) => {
  return brandsArr.map(b => ({ id: b, name: b }));
};

const formatOption = (item, type) => {
  if (!item) return '';
  if (type === 'cpu') return `${getField(item, 'cpu', 'name')} (${item.socket_cpu}) — ${getField(item, 'cpu', 'price')} ₴`;
  if (type === 'mb') return `${getField(item, 'mb', 'name')} (${item.ram_type}) — ${getField(item, 'mb', 'price')} ₴`;
  if (type === 'cooler') return `${getField(item, 'cooler', 'name')} (TDP: ${item.max_tdp}W) — ${getField(item, 'cooler', 'price')} ₴`;
  if (type === 'ram') return `${getField(item, 'ram', 'name')} (${item.frequency_mhz} MHz) — ${getField(item, 'ram', 'price')} ₴`;
  if (type === 'gpu') return `${getField(item, 'gpu', 'name')} — ${getField(item, 'gpu', 'price')} ₴`;
  if (type === 'psu') return `${getField(item, 'psu', 'name')} (${item.wattage}W) — ${getField(item, 'psu', 'price')} ₴`;
  if (type === 'case') return `${getField(item, 'case', 'name')} — ${getField(item, 'case', 'price')} ₴`;
  return '';
};

// --- УМНАЯ ФИЛЬТРАЦИЯ ДУБЛИКАТОВ ---
const deduplicate = (arr, category) => {
  const seen = new Set();
  return arr.filter(item => {
    const name = getField(item, category, 'name');
    if (!name) return true;
    if (seen.has(name)) return false;
    seen.add(name);
    return true;
  });
};

// --- ВЫЧИСЛЯЕМЫЕ СВОЙСТВА ---
const availableBrands = computed(() => {
  const getUniqueBrands = (list, category) => {
    return [...new Set(list.map(item => getField(item, category, 'brand')))].filter(Boolean).sort();
  };
  return {
    cpu: getUniqueBrands(options.cpus, 'cpu'), mb: getUniqueBrands(options.mbs, 'mb'),
    cooler: getUniqueBrands(options.coolers, 'cooler'), ram: getUniqueBrands(options.rams, 'ram'),
    gpu: getUniqueBrands(options.gpus, 'gpu'), psu: getUniqueBrands(options.psus, 'psu'),
    case: getUniqueBrands(options.cases, 'case')
  };
});

const applySort = (arr, category, sortType) => {
  const sorted = [...arr]; // Делаем копию, чтобы не мутировать исходный массив Vue
  if (sortType === 'asc') {
    return sorted.sort((a, b) => getField(a, category, 'price') - getField(b, category, 'price'));
  }
  if (sortType === 'desc') {
    return sorted.sort((a, b) => getField(b, category, 'price') - getField(a, category, 'price'));
  }
  return sorted;
};

const filteredOptions = computed(() => {
  return {
    cpus: applySort(deduplicate(options.cpus, 'cpu').filter(item => {
      if (filters.cpu.brand && getField(item, 'cpu', 'brand') !== filters.cpu.brand.id) return false;
      if (filters.cpu.minPrice && getField(item, 'cpu', 'price') < Number(filters.cpu.minPrice)) return false;
      if (filters.cpu.maxPrice && getField(item, 'cpu', 'price') > Number(filters.cpu.maxPrice)) return false;
      return true;
    }), 'cpu', filters.cpu.sort),

    mbs: applySort(deduplicate(options.mbs, 'mb').filter(item => {
      if (filters.mb.brand && getField(item, 'mb', 'brand') !== filters.mb.brand.id) return false;
      if (filters.mb.minPrice && getField(item, 'mb', 'price') < Number(filters.mb.minPrice)) return false;
      if (filters.mb.maxPrice && getField(item, 'mb', 'price') > Number(filters.mb.maxPrice)) return false;
      return true;
    }), 'mb', filters.mb.sort),

    coolers: applySort(deduplicate(options.coolers, 'cooler').filter(item => {
      if (filters.cooler.brand && getField(item, 'cooler', 'brand') !== filters.cooler.brand.id) return false;
      if (filters.cooler.minPrice && getField(item, 'cooler', 'price') < Number(filters.cooler.minPrice)) return false;
      if (filters.cooler.maxPrice && getField(item, 'cooler', 'price') > Number(filters.cooler.maxPrice)) return false;
      return true;
    }), 'cooler', filters.cooler.sort),

    rams: applySort(deduplicate(options.rams, 'ram').filter(item => {
      if (filters.ram.brand && getField(item, 'ram', 'brand') !== filters.ram.brand.id) return false;
      if (filters.ram.minPrice && getField(item, 'ram', 'price') < Number(filters.ram.minPrice)) return false;
      if (filters.ram.maxPrice && getField(item, 'ram', 'price') > Number(filters.ram.maxPrice)) return false;
      return true;
    }), 'ram', filters.ram.sort),

    gpus: applySort(deduplicate(options.gpus, 'gpu').filter(item => {
      if (filters.gpu.brand && getField(item, 'gpu', 'brand') !== filters.gpu.brand.id) return false;
      if (filters.gpu.minPrice && getField(item, 'gpu', 'price') < Number(filters.gpu.minPrice)) return false;
      if (filters.gpu.maxPrice && getField(item, 'gpu', 'price') > Number(filters.gpu.maxPrice)) return false;
      return true;
    }), 'gpu', filters.gpu.sort),

    psus: applySort(deduplicate(options.psus, 'psu').filter(item => {
      if (filters.psu.brand && getField(item, 'psu', 'brand') !== filters.psu.brand.id) return false;
      if (filters.psu.minWatt && (item?.wattage || 0) < Number(filters.psu.minWatt)) return false;
      if (filters.psu.minPrice && getField(item, 'psu', 'price') < Number(filters.psu.minPrice)) return false;
      if (filters.psu.maxPrice && getField(item, 'psu', 'price') > Number(filters.psu.maxPrice)) return false;
      return true;
    }), 'psu', filters.psu.sort),

    cases: applySort(deduplicate(options.cases, 'case').filter(item => {
      if (filters.case.brand && getField(item, 'case', 'brand') !== filters.case.brand.id) return false;
      if (filters.case.minPrice && getField(item, 'case', 'price') < Number(filters.case.minPrice)) return false;
      if (filters.case.maxPrice && getField(item, 'case', 'price') > Number(filters.case.maxPrice)) return false;
      return true;
    }), 'case', filters.case.sort)
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
    if (!res.ok) throw new Error(`Ошибка! Код: ${res.status}`);
    const json = await res.json();
    return Object.values(json).find(val => Array.isArray(val)) || [];
  } catch (e) {
    console.error(`Ошибка при загрузке ${endpoint}:`, e);
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
    if (!res.ok) throw new Error();
    const data = await res.json();
    options.psus = data.data || [];
    systemTdp.value = data.system_tdp || 0;
    recommendedPsu.value = data.recommended_wattage || 0;
  } catch (e) {}
};

watch(() => selected.cpu, (newCpu) => {
  if (isRestoring.value) return; 
  selected.mb = null; selected.cooler = null;
  options.mbs = []; options.coolers = [];
  filters.mb.brand = null; filters.mb.minPrice = null; filters.mb.maxPrice = null;
  filters.cooler.brand = null; filters.cooler.minPrice = null; filters.cooler.maxPrice = null;
  
  if (newCpu) { fetchMBs(newCpu.id); fetchCoolers(newCpu.id); }
  fetchPSUs(newCpu?.id, selected.gpu?.id);
});

watch(() => selected.mb, (newMb) => {
  if (isRestoring.value) return;
  selected.ram = null; selected.case = null;
  options.rams = []; options.cases = [];
  filters.ram.brand = null; filters.ram.minPrice = null; filters.ram.maxPrice = null;
  filters.case.brand = null; filters.case.minPrice = null; filters.case.maxPrice = null;
  
  if (newMb) { fetchRAMs(newMb.id); fetchCases(newMb.id); }
});

watch(() => selected.gpu, (newGpu) => {
  if (isRestoring.value) return;
  fetchPSUs(selected.cpu?.id, newGpu?.id);
});

onMounted(() => {
  applyTheme();
  fetchCPUs(); fetchGPUs(); fetchPSUs(null, null);
  fetchMBs(''); fetchRAMs(''); fetchCases(''); fetchCoolers('');
});
</script>

<style>
/* Убираем стрелочки из input type="number" для всех браузеров */
input[type="number"]::-webkit-outer-spin-button,
input[type="number"]::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}
input[type="number"] {
  -moz-appearance: textfield;
}

/* Анимация для Toasts */
.toast-fade-enter-active,
.toast-fade-leave-active {
  transition: opacity 0.4s ease, transform 0.4s ease;
}
.toast-fade-enter-from,
.toast-fade-leave-to {
  opacity: 0;
  transform: translateY(20px);
}
</style>