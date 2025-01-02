<template>
  <transition
    enter-active-class="animate-enter"
    leave-active-class="animate-leave"
    appear
  >
    <div>
      <slot></slot>
    </div>
  </transition>
</template>

<script setup>
// Tidak ada logika yang diperlukan
</script>

<style scoped>
.animate-enter {
  animation: fadeInUp 0.7s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.animate-leave {
  animation: fadeOutDown 0.6s cubic-bezier(0.34, 1.56, 0.64, 1);
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px) scale(0.99);
    filter: blur(5px);
  }
  
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
    filter: blur(0);
  }
}

@keyframes fadeOutDown {
  from {
    opacity: 1;
    transform: translateY(0) scale(1);
    filter: blur(0);
  }

  to {
    opacity: 0;
    transform: translateY(20px) scale(0.99);
    filter: blur(5px);
  }
}
</style> 
