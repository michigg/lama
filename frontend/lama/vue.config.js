module.exports = {
  pwa: {
    name: 'LAMa - Ldap Account Manager',
    themeColor: '#e97e2e',
    msTileColor: '#ffefd9',
    appleMobileWebAppCapable: 'yes',
    appleMobileWebAppStatusBarStyle: 'black',
    manifestOptions: {
      short_name: 'LAMa',
      background_color: '#ffefd9'
    },
    // configure the workbox plugin
    workboxPluginMode: 'InjectManifest',
    workboxOptions: {
      // swSrc is required in InjectManifest mode.
      swSrc: 'dev/sw.js'
      // ...other Workbox options...
    }
  }
}
