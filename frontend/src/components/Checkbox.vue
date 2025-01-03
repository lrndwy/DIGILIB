<template>
  <label class="inline-flex items-center cursor-pointer">
    <input 
      type="checkbox" 
      :checked="isChecked"
      @change="handleChange"
      class="sr-only peer"
    >
    <div 
      class="relative w-5 h-5 border border-border-light dark:border-border-dark 
             rounded peer 
             peer-checked:bg-background-dark dark:peer-checked:bg-background-light
             peer-checked:border-background-dark dark:peer-checked:border-background-light
             after:content-[''] 
             after:absolute 
             after:opacity-0
             after:top-[2px]
             after:left-[6px]
             after:w-[6px]
             after:h-[10px]
             after:border-r-2
             after:border-b-2
             after:border-white
             dark:after:border-black
             after:rotate-45
             peer-checked:after:opacity-100
             transition-all duration-200"
    ></div>
    <span class="ms-3 text-sm font-medium text-text-light-primary dark:text-text-dark-primary">
      <slot></slot>
    </span>
  </label>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  modelValue: {
    type: [Boolean, Array, String],
    default: false
  },
  value: {
    type: [String, Number, Boolean],
    default: ''
  },
  trueValue: {
    type: [String, Boolean],
    default: true
  },
  falseValue: {
    type: [String, Boolean],
    default: false
  }
})

const emit = defineEmits(['update:modelValue'])

const isChecked = computed(() => {
  if (Array.isArray(props.modelValue)) {
    return props.modelValue.includes(props.value)
  }
  if (props.trueValue && props.falseValue) {
    return props.modelValue === props.trueValue
  }
  return props.modelValue
})

const handleChange = (event) => {
  const checked = event.target.checked
  if (Array.isArray(props.modelValue)) {
    const newValue = [...props.modelValue]
    if (checked) {
      newValue.push(props.value)
    } else {
      const index = newValue.indexOf(props.value)
      if (index > -1) {
        newValue.splice(index, 1)
      }
    }
    emit('update:modelValue', newValue)
  } else if (props.trueValue !== undefined && props.falseValue !== undefined) {
    emit('update:modelValue', checked ? props.trueValue : props.falseValue)
  } else {
    emit('update:modelValue', checked)
  }
}
</script>
