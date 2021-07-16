<template>
  <div class="login-wrap">
    <div class="ms-login">
      <div class="ms-title">图书馆信息管理系统</div>
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
              <el-button icon="el-icon-user"></el-button>
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
              <el-button icon="el-icon-lock"></el-button>
            </template>
          </el-input>
        </el-form-item>
        <div class="login-btn">
          <el-button type="primary" @click="submitForm()">登录</el-button>
        </div>
        <h class="login-tips">当前还未注册？</h>
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
        password: [{ required: true, message: "请输入密码", trigger: "blur" }],
      },
    };
  },
  created() {
    this.$store.commit("clearTags");
  },
  methods: {
    submitForm() {
      this.$refs.login.validate(async (valid) => {
        if (!valid) {
          return;
        }
        const { data: res } = await this.$http.post("login", this.param);
        if (res.status !== 200){
          return this.$message.error("请输入正确的帐号名称或密码");
        }
        this.$message.success("登录成功");
        this.$store.commit("login", this.param.username);
        this.$store.commit("storeId", res.user_id);
        this.$store.commit("setRole", res.role);
        console.log(res.user_id);
        this.$router.push({ path: "/user" });
      });
    },
  },
};
</script>

<style scoped>
.login-wrap {
  position: relative;
  width: 100%;
  height: 100%;
  background-image: url(../assets/img/login.jpg);
  background-size: 100%;
}
.ms-title {
  width: 100%;
  line-height: 50px;
  text-align: center;
  font-size: 20px;
  color: rgb(141, 139, 151);
  border-bottom: 1px solid rgb(87, 107, 163);
}
.ms-login {
  position: absolute;
  left: 50%;
  top: 50%;
  width: 350px;
  margin: -190px 0 0 -175px;
  border-radius: 5px;
  background: rgba(30, 30, 32, 0.3);
  overflow: hidden;
}
.ms-content {
  padding: 30px 30px;
}
.login-btn {
  text-align: center;
}
.login-btn button {
  width: 100%;
  height: 36px;
  margin-bottom: 10px;
}
.login-tips {
  font-size: 12px;
  line-height: 30px;
  color: #fff;
}
</style>