const MonacoWebpackPlugin = require('monaco-editor-webpack-plugin');
module.exports = {
    configureWebpack: {
        plugins: [
            new MonacoWebpackPlugin()
        ]
    },
    devServer:{
        proxy:{
            '/':{
                target: 'http://127.0.0.1:8899'
            }
        }
    }
}

