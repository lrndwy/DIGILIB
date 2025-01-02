<template>
  <Transition
    enter-active-class="ease-out duration-300"
    enter-from-class="opacity-0"
    enter-to-class="opacity-100"
    leave-active-class="ease-in duration-200"
    leave-from-class="opacity-100"
    leave-to-class="opacity-0"
  >
    <div v-if="modelValue" class="fixed inset-0 bg-black bg-opacity-50 transition-opacity z-50">
      <div class="fixed inset-0 z-50 overflow-y-auto">
        <div class="flex min-h-full items-center justify-center p-4 text-left">
          <!-- Modal Panel -->
          <Transition
            enter-active-class="ease-out duration-300"
            enter-from-class="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95"
            enter-to-class="opacity-100 translate-y-0 sm:scale-100"
            leave-active-class="ease-in duration-200"
            leave-from-class="opacity-100 translate-y-0 sm:scale-100"
            leave-to-class="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95"
          >
            <div 
              v-if="modelValue"
              class="relative transform overflow-hidden rounded-lg bg-background-light dark:bg-background-dark text-text-light-primary dark:text-text-dark-primary w-full sm:max-w-lg transition-all"
            >
              <!-- Header -->
              <div class="border-b border-border-light dark:border-border-dark p-4">
                <div class="flex items-center justify-between">
                  <div class="text-lg font-medium">
                    <slot name="header"></slot>
                  </div>
                  <button
                    @click="$emit('update:modelValue', false)"
                    class="rounded-lg p-1.5 hover:bg-gray-100 dark:hover:bg-surface-dark transition-colors"
                  >
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                    </svg>
                  </button>
                </div>
              </div>

              <!-- Body -->
              <div class="p-6">
                <slot name="body"></slot>
              </div>

              <!-- Footer -->
              <div 
                v-if="$slots.footer"
                class="border-t border-border-light dark:border-border-dark p-4 flex justify-end space-x-2"
              >
                <slot name="footer"></slot>
              </div>
            </div>
          </Transition>
        </div>
      </div>
    </div>
  </Transition>
</template>

<script setup>
defineProps({
  modelValue: {
    type: Boolean,
    required: true
  }
})

defineEmits(['update:modelValue'])
</script> 
