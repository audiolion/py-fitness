'use strict';

var path = require('path');

module.exports = {
  entry: path.resolve(__dirname, './entry.js'),
  output: {
    path: path.resolve(__dirname, 'py_fitness/static/js'),
    filename: 'bundle.sourcemap.js'
  },
  devtool: "inline-source-map",
  module: {
    loaders: [
      {
        test: /\.scss$/,
        loaders: ["style", "css?sourceMap", "sass?sourceMap"]
      }
    ]
  },
};
