
<template>
    <n-space justify="end">
      <n-button strong round type="success" @click="show">{{ username }}</n-button>
      <n-button strong round type="warning" @click="logout">logout</n-button>
    </n-space>
    <n-modal
      class="custom-card"
      v-model:show="showModal"
      preset="card"
      :style="bodyStyle"
      title="input change"
      size="huge"
      :bordered="false"
      :segmented="segmented"
    >
      <template #header-extra></template>
      <n-form :label-width="80" :model="insert_value" size="medium">
        <n-form-item label="username">
          <n-input placeholder="inpurt username" v-model:value="user.username" />
        </n-form-item>
        <n-form-item label="password">
          <n-input
            type="password"
            placeholder="input password"
            v-model:value="user.password"
          />
        </n-form-item>
      </n-form>
      <template #footer
        ><n-button @click="login" attr-type="button">login</n-button>
      </template>
    </n-modal>
  </template>
  <script>
  import { defineComponent, ref } from "vue";
  import { NSpace, NButton, NModal, NForm, NFormItem, NInput } from "naive-ui";
  
  import axios from "axios";
  
  export default defineComponent({
    components: {
      NSpace,
      NButton,
      NModal,
      NForm,
      NFormItem,
      NInput,
    },
    data() {
      return {
        bodyStyle: {
          width: "600px",
        },
        segmented: {
          content: "soft",
          footer: "soft",
        },
        username: "click login",
        user: {
          username: "",
          password: "",
        },
      };
    },
    setup() {
      return {
        showModal: ref(false),
      };
    },
    mounted() {
      this.login_test();
    },
    methods: {
      login_test() {
        axios
          .get("/user/login_test")
          .then((response) => {
            this.username = response.data;
          })
          .catch(function (error) {
            console.log(error);
            this.username = "click login";
          });
      },
      show() {
        this.showModal = true;
      },
      login() {
        var params = this.user;
        axios
          .post("/user/login", params)
          .then((response) => {
            alert(response.data);
            this.login_test();
            this.showModal = false;
          })
          .catch(function (error) {
            console.log(error);
          });
      },
      logout() {
        axios
          .get("/user/logout")
          .then((response) => {
            alert(response.data);
            this.username = "click login";
          })
          .catch(function (error) {
            console.log(error);
          });
      },
    },
  });
  </script>
  