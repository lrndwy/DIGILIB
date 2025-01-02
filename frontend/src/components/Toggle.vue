<template>
  <label class="inline-flex items-center cursor-pointer">
    <input 
      type="checkbox" 
      :value="modelValue"
      @input="$emit('update:modelValue', $event.target.checked)"
      class="sr-only peer"
    >
    <div 
      class="relative w-11 h-6 bg-surface-light dark:bg-surface-dark 
             peer-focus:outline-none peer-focus:ring-4 
             peer-focus:ring-secondary-300 dark:peer-focus:ring-secondary-700 
             rounded-full peer 
             peer-checked:after:translate-x-full 
             rtl:peer-checked:after:-translate-x-full 
             peer-checked:after:border-white 
             after:content-[''] 
             after:absolute 
             after:top-[2px] 
             after:start-[2px] 
             after:bg-white 
             after:border-secondary-200 
             dark:after:border-secondary-600 
             after:border 
             after:rounded-full 
             after:h-5 
             after:w-5 
             after:transition-all 
             peer-checked:bg-background-dark 
             dark:peer-checked:bg-background-light"
    ></div>
    <span class="ms-3 text-sm font-medium text-text-light-primary dark:text-text-dark-primary">
      <slot>Toggle</slot>
    </span>
  </label>
</template>

<script setup>
defineProps({
  modelValue: {
    type: Boolean,
    default: false
  }
})

defineEmits(['update:modelValue'])
</script>
