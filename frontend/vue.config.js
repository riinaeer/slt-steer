const { defineConfig } = require("@vue/cli-service")
module.exports = defineConfig({
  configureWebpack: {
    entry: "./src/main.js",
    watch: true,
    watchOptions: {
      ignored: /node_modules/,
      poll: 1000,
    },
  },
  transpileDependencies: true,
  devServer: {
    historyApiFallback: true, // Fixes refresh issues with Vue Router
    hot: true,
  },
})
