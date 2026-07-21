<template>
  <div class="relative w-full text-sm" ref="dropdownRef">
    <!-- Кнопка селекта -->
    <div
      @click="toggleDropdown"
      class="flex items-center justify-between w-full p-3 bg-slate-50 dark:bg-[#121212] border rounded-xl cursor-pointer transition-colors duration-300 select-none"
      :class="[
        disabled ? 'opacity-50 cursor-not-allowed border-slate-200 dark:border-[#333]' : 'hover:border-blue-400 dark:hover:border-orange-500 border-slate-200 dark:border-[#333]',
        isOpen ? 'border-blue-500 dark:border-orange-500 ring-1 ring-blue-500 dark:ring-orange-500' : ''
      ]"
    >
      <span v-if="modelValue" class="text-slate-800 dark:text-gray-200 truncate pr-2 font-medium">
        {{ labelFunc(modelValue) }}
      </span>
      <span v-else class="text-slate-400 dark:text-gray-500 truncate pr-2">
        {{ placeholder }}
      </span>
      
      <div class="flex items-center gap-1.5 flex-shrink-0">
        <!-- Кнопка очистки (крестик) -->
        <button
          v-if="modelValue && !disabled"
          @click.stop="clearSelection"
          class="text-slate-400 hover:text-red-500 transition-colors p-0.5 rounded-md hover:bg-slate-200 dark:hover:bg-[#333]"
          title="Очистить"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
        </button>
        <!-- Галочка (стрелочка) -->
        <svg
          class="w-4 h-4 text-slate-400 transition-transform duration-300"
          :class="{ 'rotate-180': isOpen, 'text-blue-500 dark:text-orange-500': isOpen }"
          fill="none" stroke="currentColor" viewBox="0 0 24 24"
        >
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
        </svg>
      </div>
    </div>

    <!-- Выпадающий список -->
    <transition
      enter-active-class="transition duration-200 ease-out"
      enter-from-class="transform scale-95 opacity-0 -translate-y-2"
      enter-to-class="transform scale-100 opacity-100 translate-y-0"
      leave-active-class="transition duration-150 ease-in"
      leave-from-class="transform scale-100 opacity-100 translate-y-0"
      leave-to-class="transform scale-95 opacity-0 -translate-y-2"
    >
      <ul
        v-if="isOpen && !disabled"
        class="absolute z-[100] w-full mt-2 bg-white dark:bg-[#1a1a1a] border border-slate-200 dark:border-[#333] rounded-xl shadow-xl max-h-60 overflow-y-auto py-1.5 custom-scrollbar"
      >
        <li v-if="options.length === 0" class="px-4 py-3 text-slate-400 dark:text-gray-500 text-center italic text-xs">
          Нет доступных вариантов
        </li>
        
        <!-- Обрати внимание на isSelected(option) -->
        <li
          v-for="(option, index) in options"
          :key="option.id || index"
          @click="selectOption(option)"
          class="px-4 py-2.5 cursor-pointer transition-colors duration-200 flex items-center justify-between group hover:bg-slate-100 dark:hover:bg-[#2a2a2a]"
          :class="{ 'bg-blue-50/50 dark:bg-[#222]': isSelected(option) }"
        >
          <span
            class="truncate group-hover:text-blue-600 dark:group-hover:text-orange-500 transition-colors"
            :class="isSelected(option) ? 'text-blue-600 dark:text-orange-500 font-bold' : 'text-slate-700 dark:text-gray-300 font-medium'"
          >
            {{ labelFunc(option) }}
          </span>
          <svg v-if="isSelected(option)" class="w-4 h-4 text-blue-600 dark:text-orange-500 flex-shrink-0 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7"></path></svg>
        </li>
      </ul>
    </transition>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';

const props = defineProps({
  modelValue: {
    type: Object,
    default: null
  },
  options: {
    type: Array,
    default: () => []
  },
  placeholder: {
    type: String,
    default: 'Выберите...'
  },
  disabled: {
    type: Boolean,
    default: false
  },
  labelFunc: {
    type: Function,
    default: (opt) => opt ? opt.name : ''
  }
});

const emit = defineEmits(['update:modelValue']);

const isOpen = ref(false);
const dropdownRef = ref(null);

const toggleDropdown = () => {
  if (!props.disabled) {
    isOpen.value = !isOpen.value;
  }
};

const selectOption = (option) => {
  emit('update:modelValue', option);
  isOpen.value = false;
};

const clearSelection = () => {
  emit('update:modelValue', null);
  isOpen.value = false;
};

// УМНАЯ ФУНКЦИЯ ПРОВЕРКИ ВЫБОРА
const isSelected = (option) => {
  if (!props.modelValue || !option) return false;
  
  // 1. Проверяем по ID (если он точно существует)
  if (props.modelValue.id !== undefined && option.id !== undefined) {
    return props.modelValue.id === option.id;
  }
  
  // 2. Если ID нет, сравниваем объекты напрямую или по тексту (Label)
  return props.modelValue === option || props.labelFunc(props.modelValue) === props.labelFunc(option);
};

const handleClickOutside = (event) => {
  if (dropdownRef.value && !dropdownRef.value.contains(event.target)) {
    isOpen.value = false;
  }
};

onMounted(() => {
  document.addEventListener('click', handleClickOutside);
});

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside);
});
</script>

<style scoped>
.custom-scrollbar::-webkit-scrollbar {
  width: 6px;
}
.custom-scrollbar::-webkit-scrollbar-track {
  background: transparent;
}
.custom-scrollbar::-webkit-scrollbar-thumb {
  background-color: #cbd5e1;
  border-radius: 10px;
}
:global(.dark) .custom-scrollbar::-webkit-scrollbar-thumb {
  background-color: #4b5563;
}
.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background-color: #94a3b8;
}
:global(.dark) .custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background-color: #6b7280;
}
</style>