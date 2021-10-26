<template>
  <div class="register-wrap">
    <el-scrollbar style="height:100%">
      <div class="ms-register">
        <div class="ms-title">眼底血管分割云平台</div>
        <el-form
          :model="param"
          :rules="rules"
          ref="register"
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
          <el-form-item prop="password">
            <el-input
              type="password"
              placeholder="password"
              v-model="param.tempPassword"
              @keyup.enter="submitForm()"
            >
              <template #prepend>
                <i class="el-icon-lock">确认密码</i>
              </template>
            </el-input>
          </el-form-item>
          <el-form-item prop="email">
            <el-input v-model="param.email" placeholder="email">
              <template #prepend>
                <i class="el-icon-lock">邮箱</i>
              </template>
            </el-input>
          </el-form-item>
          <el-form-item prop="phone">
            <el-input v-model="param.phone" placeholder="phone">
              <template #prepend>
                <el-button icon="el-icon-lock">手机号</el-button>
              </template>
            </el-input>
          </el-form-item>
          <el-form-item label="" prop="sex">
            <el-radio-group v-model="param.sex" size="medium">
              <el-radio border label="男"></el-radio>
              <el-radio border label="女"></el-radio>
            </el-radio-group>
          </el-form-item>
          <div class="register-btn">
            <el-button type="primary" @click="submitForm()">注册</el-button>
          </div>
          <h>已有帐号？</h>
          <h class="h"><router-link to="/login">立即登录</router-link></h>
        </el-form>
      </div>
    </el-scrollbar>
  </div>
</template>

<script>
  export default {
    data() {
      var checkEmail = (rule, value, callback) => {
        const regEmail = /^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+((.[a-zA-Z0-9_-]{2,3}){1,2})$/;
        if (regEmail.test(value)) {
          return callback();
        }
        callback(new Error("请输入合法的邮箱"));
      };
      var checkPhone = (rule, value, callback) => {
        const regPhone = /^[0-9]+$/;
        if (regPhone.test(value)) {
          return callback();
        }
        callback(new Error("请输入合法的手机号"));
      };
      return {
        param: {
          username: "",
          password: "",
          email: "",
          phone: "",
          sex: "",
        },
        rules: {
          username: [
            { required: true, message: "请输入用户名", trigger: "blur" },
            {
              min: 1,
              max: 20,
              message: "用户名长度在1到20个字符",
              trigger: "blur",
            },
          ],
          password: [
            { required: true, message: "请输入密码", trigger: "blur" },
            {
              min: 6,
              max: 15,
              message: "密码长度在6到15个字符",
              trigger: "blur",
            },
          ],
          email: [
            { required: true, message: "请输入邮箱", trigger: "blur" },
            {
              validator: checkEmail,
              trigger: "blur",
            },
          ],
          phone: [
            { required: true, message: "请输入手机号", trigger: "blur" },
            {
              validator: checkPhone,
              trigger: "blur",
            },
          ],
          sex: [{ requierd: true, message: "请选择性别", trigger: "blur" }],
        },
      };
    },
    created() {
      this.$store.commit("clearTags");
    },
    methods: {
      submitForm() {
        this.$refs.register.validate(async (valid) => {
          if (valid) {
            if (this.param.password !== this.param.tempPassword) {
              return alert("输入的两次密码不一致");
            }
            if (this.param.sex === "") {
              alert("请选择性别");
            } else {
              await new Promise((resolve) => {
                this.$http
                  .post("/register/", JSON.stringify(this.param))
                  .then((res) => {
                    console.log(res);
                    if (res.data.message === "用户名已存在")
                      return this.$message.error("该用户名已被注册！");
                    this.$message.success("注册成功");
                    this.$router.push({ path: "/login" });
                  });
                resolve();
              }).then(() => {
                console.log("成功啦post啦");
              });
            }
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
