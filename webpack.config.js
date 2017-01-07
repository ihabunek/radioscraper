var ExtractTextPlugin = require('extract-text-webpack-plugin');
var path = require('path');

module.exports = {
    entry: {
        "index": ['./ui/index.js'],
    },
    output: {
        path: path.join(__dirname, 'static'),
        filename: '[name].js'
    },
    module: {
        loaders: [{
            test: /\.scss$/,
            loader: ExtractTextPlugin.extract('css!sass'),
        }]
    },
    devtool: 'source-map',
    plugins: [
        new ExtractTextPlugin("styles.css")
    ]
}
