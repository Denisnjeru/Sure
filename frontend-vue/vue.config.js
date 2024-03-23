const path = require("path");

module.exports = {
  chainWebpack: config => {    
    config.plugin('html').tap(args => {
      args[0].title = 'Tendersure'
      return args
    })
    config.plugins.delete('prefetch')
  },
  pluginOptions: {
    "style-resources-loader": {
      preProcessor: "scss",
      patterns: [path.resolve(__dirname, "./src/styles/main.scss")]
    },
  },
  devServer: {
    host: 'localhost',
  },
  pwa: {
    themeColor: '#f5f6f7'  
  },
  
};