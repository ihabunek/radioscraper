var ExtractTextPlugin = require('extract-text-webpack-plugin');
var path = require('path');
var webpack = require('webpack');

module.exports = {
    entry: {
        "main": ['./ui/scripts/main.jsx'],
        "plays": ['./ui/scripts/plays.jsx'],
        "stats": ['./ui/scripts/stats.jsx'],
    },
    output: {
        path: path.join(__dirname, 'ui/dist'),
        filename: '[name].min.js'
    },
    module: {
        loaders: [{
            test: /\.scss$/,
            loader: ExtractTextPlugin.extract(["css-loader", "sass-loader"]),
        }, {
            test: /\.css$/,
            loader: ExtractTextPlugin.extract(["css-loader"]),
        }, {
            test: /\.jsx$/,
            exclude: /node_modules/,
            loader: 'babel-loader',
            query: {
                presets: ['es2015']
            }
        }, {
          test: /\.(png|woff|woff2|eot|otf|ttf|svg)$/,
          loader: 'file-loader',
        }]
    },
    devtool: 'source-map',
    resolve: {
        alias: {
            jquery: "jquery/src/jquery"
        }
    },
    plugins: [
        new ExtractTextPlugin("styles.css"),
        new webpack.optimize.CommonsChunkPlugin({
            name: "commons"
        }),
        new webpack.optimize.UglifyJsPlugin({
            compress: {
                warnings: false
            }
        }),
        new webpack.ProvidePlugin({
            jQuery: "jquery",
            $: "jquery",
        }),
    ]
}
