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
                target: 'http://localhost:8899'
            }
        }
    }
}

