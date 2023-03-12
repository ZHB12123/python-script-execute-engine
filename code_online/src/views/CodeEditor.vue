<template>
  <div ref="container" class="monaco-editor" :style="`height: ${height}px`"></div>
</template>

<script>
import * as monaco from "monaco-editor";
export default {
  name: "AcMonaco",
  props: {
    opts: {
      type: Object,
      default() {
        return {};
      },
    },
    height: {
      type: Number,
      default: 1000,
    },
  },
  data() {
    return {
      // 主要配置
      defaultOpts: {
        value: "",
        theme: "vs-dark", // 编辑器主题：vs, hc-black, or vs-dark
        language: "python",
        folding: true, // 是否折叠
        foldingHighlight: true, // 折叠等高线
        foldingStrategy: "indentation", // 折叠方式  auto | indentation
        showFoldingControls: "always", // 是否一直显示折叠 always | mouseover
        disableLayerHinting: true, // 等宽优化
        emptySelectionClipboard: false, // 空选择剪切板
        selectionClipboard: false, // 选择剪切板
        automaticLayout: true, // 自动布局
        codeLens: false, // 代码镜头
        scrollBeyondLastLine: false, // 滚动完最后一行后再滚动一屏幕
        colorDecorators: true, // 颜色装饰器
        accessibilitySupport: "off", // 辅助功能支持  "auto" | "off" | "on"
        lineNumbers: "on", // 行号 取值： "on" | "off" | "relative" | "interval" | function
        lineNumbersMinChars: 5, // 行号最小字符   number
        readOnly: false, //是否只读  取值 true | false
        minimap: {
          enabled: true, // 不要小地图
        },
      },
    };
  },
  watch: {
    opts: {
      handler(n) {
        console.log(n);
        this.init();
      },
      deep: true,
    },
  },
  mounted() {
    this.init();
  },
  methods: {
    init() {
      // 初始化container的内容，销毁之前生成的编辑器
      this.$refs.container.innerHTML = "";

      this.editorOptions = Object.assign(this.defaultOpts, this.opts);
      // 生成编辑器对象
      this.monacoEditor = monaco.editor.create(this.$refs.container, this.editorOptions);

      // 编辑器内容发生改变时触发
      this.monacoEditor.onDidChangeModelContent(() => {
        this.$emit("change", this.monacoEditor.getValue());
      });
    },
    // 供父组件调用手动获取值
    getVal() {
      return this.monacoEditor.getValue();
    },
  },
};
</script>

<style scoped>
#app {
  height: 1000px;
}
</style>
