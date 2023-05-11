<template>
  <n-grid x-gap="12" :cols="10">
    <n-grid-item :span="6">
      <n-space vertical>
        <n-card title="模块压缩包上传">
          <n-form :rules="rules">
            <n-form-item label="模块名">
              <n-input
                v-model:value="run_data.package_name"
                type="text"
                placeholder="请输入模块名"
              />
            </n-form-item>
            <n-form-item label="入口函数">
              <n-input
                v-model:value="run_data.enter_func"
                type="text"
                placeholder="请输入入口函数"
              />
            </n-form-item>
            <n-form-item label="运行参数">
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
            <n-form-item show-require-mark="true" label="模块压缩包">
              <n-upload
                action="/upload_module"
                :default-upload="true"
                :custom-request="selectFileNew"
              >
                <n-button>选择文件</n-button>
              </n-upload>
            </n-form-item>
          </n-form>

          <n-button type="success" @click="uploadFile"> 提交 </n-button>
        </n-card>
        <n-data-table
          :columns="columns"
          :data="data"
          :pagination="pagination"
          :bordered="false"
        />
      </n-space>
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
        <n-button type="success" @click="renewConfirm"> 更新运行数据 </n-button>
      </n-space>
    </template>
  </n-modal>
</template>

<script>
import { defineComponent, ref, createVNode } from "vue";
import axios from "axios";
import {
  NUpload,
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
  NCard,
} from "naive-ui";

const createColumns = (renew, run, deletePackage) => {
  return [
    {
      title: "删除",
      key: "renew_info",
      render(row) {
        return createVNode(
          NButton,
          {
            size: "small",
            type: "warning",
            circle: true,
            onClick: () => deletePackage(row),
          },
          { default: () => "X" }
        );
      },
    },
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

const data = [];

export default defineComponent({
  components: {
    NUpload,
    NGrid,
    NGridItem,
    NDataTable,
    NButton,
    NModal,
    NSpace,
    NInput,
    NForm,
    NFormItem,
    NCard,
  },
  setup() {
    const message = useMessage();
    const fileListLengthRef = ref(0);
    const uploadRef = ref(null);
    return {
      warning(msg) {
        message.warning(msg);
      },
      error(msg) {
        message.error(msg);
      },
      upload: uploadRef,
      fileListLength: fileListLengthRef,

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
      file: null,
      upload_action: null,
      data,
      columns: createColumns(this.renew, this.run, this.deletePackage),
      run_data: {
        package_name: null,
        enter_func: null,
        params: null,
      },
      selected_row: null,
    };
  },
  mounted() {
    this.queryAll();
  },
  methods: {
    uploadFile() {
      let headers = { "Content-type": "multipart/form-data" };
      let params = new FormData();
      let action = this.upload_action;

      if (!this.file) {
        this.error("未选择文件！");
        return;
      }

      params.append("file", this.file);

      params.append("package_name", this.run_data.package_name);
      params.append("enter_func", this.run_data.enter_func);
      params.append("params", this.run_data.params);

      axios
        .post(action, params, headers)
        .then((response) => {
          console.log(response.data);
          this.queryAll();
        })
        .catch((error) => {
          console.log(error);
        });
    },
    selectFileNew(options) {
      this.upload_action = options.action;
      this.file = options.file.file;
    },
    queryAll() {
      axios
        .get("/query_all_modules")
        .then((response) => {
          console.log(response.data);
          let modules_info = response.data;
          this.data = [];
          for (var i = 0; i < modules_info.length; i++) {
            this.data.push({
              id: modules_info[i].id,
              enter_func: modules_info[i].enter_func,
              name: modules_info[i].name,
              package_name: modules_info[i].package_name,
              params: modules_info[i].params,
              upload_time: modules_info[i].upload_time,
            });
          }
          console.log(this.data);
        })
        .catch((error) => {
          console.log(error);
        });
    },
    deletePackage(row) {
      console.log(row);
    },
    renew(row) {
      this.run_data.package_name = row.package_name;
      this.run_data.enter_func = row.enter_func;
      this.run_data.params = row.params;
      console.log(row);
      this.showModal = true;
      this.selected_row = row;
    },
    renewConfirm() {
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

      let headers = { "Content-Type": "application/json" };
      let params = row;
      axios
        .post("/run_module", params, headers)
        .then((response) => {
          console.log(response.data);
          //this.queryAll();
        })
        .catch((error) => {
          console.log(error);
        });
    },
  },
});
</script>
