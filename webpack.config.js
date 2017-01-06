var ExtractTextPlugin = require('extract-text-webpack-plugin');
var path = require('path');

module.exports = {
    entry: path.join(__dirname, 'ui/index.js'),
    output: {
        path: path.join(__dirname, 'static'),
        filename: 'bundle.js'
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
