import { inject } from 'vue'

export function useNotifications() {
  const notifications = inject('notifications')
  
  if (!notifications) {
    throw new Error('Notifications plugin not found')
  }

  const notify = ({ type = 'info', title, message, duration = 5000 }) => {
    notifications.addNotification({ type, title, message, duration })
  }

  return {
    notify
  }
} 
