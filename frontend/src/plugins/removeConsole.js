export default {
  install(app) {
    if (import.meta.env.PROD) {
      const noop = () => {}
      window.console.log = noop
      window.console.error = noop
      window.console.warn = noop
      window.console.info = noop
      window.console.debug = noop
    }
  }
} 
