const path = require('path');
const webpack = require('webpack');
const common = require('./webpack.config.common');

module.exports = {
  entry: common.entry,

  output: common.output,

  plugins: common.plugins,

  module: common.module,

  externals: {
      'Config': JSON.stringify( {
          serverUrl: "http://127.0.0.1:5000",
      })
  }
};
