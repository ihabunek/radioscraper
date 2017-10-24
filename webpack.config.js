const path = require('path')
const webpack = require('webpack')
const ExtractTextPlugin = require('extract-text-webpack-plugin')

module.exports = {
    entry: {
        "main": ['./ui/scripts/main.js'],
        "plays": ['./ui/scripts/plays.js'],
        "stats": ['./ui/scripts/stats.js'],
    },
    output: {
        path: path.join(__dirname, 'ui/dist'),
        filename: '[name].min.js',
    },
    module: {
        loaders: [{
            test: /\.scss$/,
            loader: ExtractTextPlugin.extract(["css-loader", "sass-loader"]),
        }, {
            test: /\.css$/,
            loader: ExtractTextPlugin.extract(["css-loader"]),
        }, {
            test: /\.js$/,
            exclude: /node_modules/,
            loader: 'babel-loader',
            query: {
                presets: ['env'],
            },
        }, {
            test: /\.(png|woff|woff2|eot|otf|ttf|svg)$/,
            loader: 'file-loader',
        }],
    },
    devtool: 'source-map',
    resolve: {
        alias: {
            jquery: "jquery/src/jquery",
        },
    },
    plugins: [
        new ExtractTextPlugin("styles.css"),
        new webpack.optimize.CommonsChunkPlugin({
            name: "commons",
        }),
        new webpack.optimize.UglifyJsPlugin({
            compress: {
                warnings: false,
            },
        }),
        new webpack.ProvidePlugin({
            jQuery: "jquery",
            $: "jquery",
        }),
    ],
}
