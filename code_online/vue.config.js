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
                target: 'http://192.168.210.128:8899'
            }
        }
    }
}

