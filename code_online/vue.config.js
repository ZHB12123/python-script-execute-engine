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
                target: 'http://192.168.1.6:8899'
            }
        }
    }
}

