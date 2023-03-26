<template>
  <n-config-provider :theme="theme" :hljs="hljs">
    <n-message-provider>
      <n-dialog-provider>
        <n-layout position="absolute">
          <n-space vertical justify="space-around" size="large">
            <n-layout-header bordered style="padding: 8px">
              <n-grid :x-gap="8" :y-gap="0" :cols="12">
                <n-grid-item :span="10">
                  <n-menu
                    v-model:value="activeKey"
                    mode="horizontal"
                    :options="menuOptions"
                    default-value="home"
                    :on-update:value="func"
                  />
                </n-grid-item>
                <n-grid-item :span="2">
                  <n-space justify="end"> </n-space>
                </n-grid-item>
              </n-grid>
            </n-layout-header>
            <n-layout-content content-style="padding: 24px;">
              <router-view
            /></n-layout-content>
          </n-space>
        </n-layout>
      </n-dialog-provider>
    </n-message-provider>
  </n-config-provider>
</template>

<script>
import { defineComponent, ref } from "vue";
import {
  darkTheme,
  NConfigProvider,
  NLayout,
  NLayoutHeader,
  NLayoutContent,
  NMenu,
  NGrid,
  NGridItem,
  NDialogProvider,
  NMessageProvider,
  NSpace,
} from "naive-ui";

import hljs from "highlight.js/lib/core";
import json from "highlight.js/lib/languages/json";

hljs.registerLanguage("json", json);

export default defineComponent({
  components: {
    NConfigProvider,
    NLayout,
    NLayoutHeader,
    NLayoutContent,
    NMenu,
    NGrid,
    NGridItem,
    NDialogProvider,
    NMessageProvider,
    NSpace,
  },
  setup() {
    return {
      hljs,
      theme: darkTheme,
      activeKey: ref(null),
      menuOptions: ref([
        {
          label: "首页",
          key: "home",
          disabled: false,
        },
        {
          label: "单次函数执行",
          key: "run_once",
          disabled: false,
        },
        {
          label: "运行模块",
          key: "run_module",
          disabled: false,
        },
        {
          label: "流式函数订阅",
          key: "run_fluent",
          disabled: false,
        },
      ]),
      railStyle: ({ focused, checked }) => {
        const style = {};
        if (checked) {
          style.background = "#111111";
          if (focused) {
            style.boxShadow = "0 0 0 2px #d0305040";
          }
        } else {
          style.background = "#dddddd";
          if (focused) {
            style.boxShadow = "0 0 0 2px #2080f040";
          }
        }
        return style;
      },
    };
  },
  methods: {
    func(key, item) {
      console.log(item);
      if (key == "home") {
        this.$router.push({ path: "/" });
      }
      if (key == "run_fluent") {
        this.$router.push({ path: "/run_fluent" });
      }
      if (key == "run_once") {
        this.$router.push({ path: "/run_once" });
      }
      if (key == "run_module") {
        this.$router.push({ path: "/run_module" });
      }
    },
  },
});
</script>
