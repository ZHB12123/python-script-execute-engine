<template>
  <n-grid x-gap="12" :cols="10">
    <n-grid-item :span="6">
      <code-editor ref="CodeEditor" :opts="opts" @change="changeValue"></code-editor>
    </n-grid-item>
    <n-grid-item :span="4">
      <n-card>
        <n-space vertical>
          <n-button type="success" @click="runCode"> RUN </n-button>
          <n-card title="运行结果">
            <n-code :code="code" language="json" word-wrap />
          </n-card>
        </n-space>
      </n-card>
    </n-grid-item>
  </n-grid>
</template>

<script>
import axios from "axios";
import { defineComponent, ref } from "vue";

import { NGrid, NGridItem, NButton, NSpace, NCard, NCode } from "naive-ui";

import CodeEditor from "./CodeEditor.vue";

export default defineComponent({
  components: { CodeEditor, NGrid, NGridItem, NButton, NSpace, NCard, NCode },
  setup() {
    return {
      a: ref(null),
    };
  },
  data() {
    return {
      code: "",
      opts: {
        value: "",
        readOnly: false, // 是否可编辑
        language: "python", // 语言类型
        theme: this.$store.state.monacoTheme, // 编辑器主题
      },
    };
  },
  methods: {
    //monaco输入框代码改变的时候触发的逻辑
    changeValue(val) {
      console.log(val);
    },
    runCode() {
      var value = this.$refs.CodeEditor.getVal();
      console.log(value);
      let params = {
        entrance_func: "main",
        code: value,
      };
      axios
        .post("/execute", params)
        .then((response) => {
          this.code = JSON.stringify(response.data, null, 2);
        })
        .catch(function (error) {
          console.log(error);
        });
    },
  },
});
</script>

<style scoped>
.hljs {
  white-space: pre-wrap;
  word-wrap: break-word;
}
</style>
