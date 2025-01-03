export default {
  install(app) {
    if (import.meta.env.PROD) {
      ['log', 'error', 'warn', 'info', 'debug'].forEach((method) => {
        console[method] = () => {}
      })
      
      window.console = {
        log: () => {},
        error: () => {},
        warn: () => {},
        info: () => {},
        debug: () => {}
      }
    }
  }
} 
