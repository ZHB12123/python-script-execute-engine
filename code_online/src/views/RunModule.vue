<template>
  <n-grid x-gap="12" :cols="10">
    <n-grid-item :span="6">
      <n-upload
        multiple
        directory-dnd
        action="https://www.mocky.io/v2/5e4bafc63100007100d8b70f"
        :max="5"
      >
        <n-upload-dragger>
          <div style="margin-bottom: 12px">
            <n-icon size="48" :depth="3">
              <archive-icon />
            </n-icon>
          </div>
          <n-text style="font-size: 16px"> 点击或者拖动文件到该区域来上传 </n-text>
          <n-p depth="3" style="margin: 8px 0 0 0"> 请上传zip压缩包 </n-p>
        </n-upload-dragger>
      </n-upload>
      <n-data-table
        :columns="columns"
        :data="data"
        :pagination="pagination"
        :bordered="false"
      />
    </n-grid-item>
    <n-grid-item :span="4"></n-grid-item>
  </n-grid>
  <n-modal
    v-model:show="showModal"
    class="custom-card"
    preset="card"
    :style="{
      width: '600px',
    }"
    title="更新运行参数"
    size="huge"
    :bordered="false"
    :segmented="{
      content: 'soft',
      footer: 'soft',
    }"
  >
    <template #header-extra></template>
    <n-space vertical>
      <n-form :rules="rules">
        <n-form-item path="package_name" label="模块名">
          <n-input
            v-model:value="run_data.package_name"
            type="text"
            placeholder="请输入模块名"
          />
        </n-form-item>
        <n-form-item path="enter_func" label="入口函数">
          <n-input
            v-model:value="run_data.enter_func"
            type="text"
            placeholder="请输入入口函数"
          />
        </n-form-item>
        <n-form-item path="params" label="运行参数">
          <n-input
            v-model:value="run_data.params"
            type="textarea"
            :autosize="{
              minRows: 3,
              maxRows: 20,
            }"
            placeholder="请输入运行参数"
          />
        </n-form-item>
      </n-form>
    </n-space>
    <template #footer>
      <n-space justify="end">
        <n-button type="success" @click="renew_confirm"> 更新运行数据 </n-button>
      </n-space>
    </template>
  </n-modal>
</template>

<script>
import { defineComponent, ref, createVNode } from "vue";
import { ArchiveOutline as ArchiveIcon } from "@vicons/ionicons5";
import {
  NUpload,
  NUploadDragger,
  NIcon,
  NText,
  NP,
  NGrid,
  NGridItem,
  NDataTable,
  NButton,
  NModal,
  NSpace,
  NInput,
  NForm,
  NFormItem,
  useMessage,
} from "naive-ui";

const createColumns = (renew, run) => {
  return [
    {
      title: "压缩包名",
      key: "name",
    },
    {
      title: "上传时间",
      key: "upload_time",
    },
    {
      title: "模块名",
      key: "package_name",
    },
    {
      title: "入口函数",
      key: "enter_func",
    },
    {
      title: "运行参数",
      key: "params",
      width: 100,
      ellipsis: {
        tooltip: true,
      },
    },
    {
      title: "更新信息",
      key: "renew_info",
      render(row) {
        return createVNode(
          NButton,
          {
            strong: true,
            tertiary: true,
            size: "small",
            onClick: () => renew(row),
          },
          { default: () => "RENEW" }
        );
      },
    },
    {
      title: "点击运行",
      key: "run",
      render(row) {
        return createVNode(
          NButton,
          {
            strong: true,
            tertiary: true,
            size: "small",
            onClick: () => run(row),
          },
          { default: () => "RUN" }
        );
      },
    },
  ];
};

const data = [
  { name: 3, upload_time: "4:18", params: "123132165465841563489654132515321321" },
  { name: 3, upload_time: "4:18" },
  { name: 3, upload_time: "4:18" },
];

export default defineComponent({
  components: {
    ArchiveIcon,
    NUpload,
    NUploadDragger,
    NIcon,
    NText,
    NP,
    NGrid,
    NGridItem,
    NDataTable,
    NButton,
    NModal,
    NSpace,
    NInput,
    NForm,
    NFormItem,
  },
  setup() {
    const message = useMessage();
    return {
      warning(msg) {
        message.warning(msg);
      },
      error(msg) {
        message.error(msg);
      },
      showModal: ref(false),
      pagination: ref(false),
      rules: {
        package_name: {
          required: true,
          message: "请输入姓名",
          trigger: "blur",
        },
        enter_func: {
          required: true,
          message: "请输入姓名",
          trigger: "blur",
        },
        params: {
          required: false,
          message: "请输入姓名",
          trigger: "blur",
        },
      },
    };
  },
  data() {
    return {
      data,
      columns: createColumns(this.renew, this.run),
      run_data: {
        package_name: null,
        enter_func: null,
        params: null,
      },
      selected_row: null,
    };
  },
  methods: {
    renew(row) {
      this.run_data.package_name = row.package_name;
      this.run_data.enter_func = row.enter_func;
      this.run_data.params = row.params;
      console.log(row);
      this.showModal = true;
      this.selected_row = row;
    },
    renew_confirm() {
      if (!this.run_data.package_name || !this.run_data.enter_func) {
        this.error("必填项未填！");
        return;
      }
      this.selected_row.package_name = this.run_data.package_name;
      this.selected_row.enter_func = this.run_data.enter_func;
      this.selected_row.params = this.run_data.params;
    },
    run(row) {
      console.log(row);
    },
  },
});
</script>
