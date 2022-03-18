<template>
  <div class="login-wrap">
    <div class="ms-login">
      <div class="ms-title">眼底血管分割云平台</div>
      <el-form
        :model="param"
        :rules="rules"
        ref="login"
        label-width="0px"
        class="ms-content"
      >
        <el-form-item prop="username">
          <el-input v-model="param.username" placeholder="username">
            <template #prepend>
              <i class="el-icon-user">用户名</i>
            </template>
          </el-input>
        </el-form-item>
        <el-form-item prop="password">
          <el-input
            type="password"
            placeholder="password"
            v-model="param.password"
            @keyup.enter="submitForm()"
          >
            <template #prepend>
              <i class="el-icon-lock">密码</i>
            </template>
          </el-input>
        </el-form-item>
        <div class="login-btn">
          <el-button type="primary" @click="submitForm()">登录</el-button>
        </div>
        <h>当前还未注册？</h>
        <h class="login-tips"
          ><router-link to="/register">前往注册</router-link></h
        >
      </el-form>
    </div>
  </div>
</template>

<script>
  export default {
    data() {
      return {
        param: {
          username: "",
          password: "",
        },
        rules: {
          username: [
            { required: true, message: "请输入用户名", trigger: "blur" },
          ],
          password: [
            { required: true, message: "请输入密码", trigger: "blur" },
          ],
        },
      };
    },
    created() {
      this.$store.commit("clearTags");
    },
    methods: {
      submitForm() {
        this.$refs.login.validate(async (valid) => {
          if (valid) {
            await new Promise((resolve) => {
              this.$http
                .post("/login/", JSON.stringify(this.param))
                .then((res) => {
                  if (res.data.success === false)
                    return this.$message.error(res.data.message);
                  this.$message.success("登录成功");
                  this.$store.commit("login", this.param.username);
                  this.$store.commit("storeId", res.data.userID);
                  console.log(res.data.userID);
                  this.$router.push({ path: "/doctor/upload" });
                });
              resolve();
            }).then(() => {
              console.log("成功啦post啦");
            });
          } else {
            return;
          }
        });
      },
    },
  };
</script>

<style scoped>
  @import "style.css";
</style>
