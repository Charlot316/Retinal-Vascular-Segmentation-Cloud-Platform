<template>
  <div>
    <div class="prop-name">姓名</div>
    <div class="prop-value">
      {{ thisUser.name ? thisUser.name : "未填写姓名" }}
    </div>

    <div class="prop-name">性别</div>
    <el-radio-group v-model="thisUser.sex" class="prop-value" disabled>
      <el-radio :label="1">男</el-radio>
      <el-radio :label="0">女</el-radio>
    </el-radio-group>

    <div class="prop-name">身高:</div>
    <div class="prop-special-value">
      {{ thisUser.height ? thisUser.height : "未填写身高" }}
    </div>
    <div class="prop-name">体重:</div>
    <div class="prop-special-value">
      {{ thisUser.weight ? thisUser.weight : "未填写体重" }}
    </div>
    <div class="prop-name">年龄:</div>
    <div class="prop-special-value">
      {{ thisUser.age ? thisUser.age : "未填写年龄" }}
    </div>

    <div class="prop-name">手机号</div>
    <div class="prop-value">
      {{ thisUser.phone ? thisUser.phone : "未填写手机号" }}
    </div>
    <div class="prop-name">邮箱</div>
    <div class="prop-value">
      {{ thisUser.email ? thisUser.email : "未填写邮箱" }}
    </div>
    <div class="prop-name">地址</div>
    <div class="prop-value">
      {{ thisUser.address ? thisUser.address : "未填写地址" }}
    </div>
  </div>
</template>
<script>
export default {
  props: ["user"],
  data() {
    return {
      thisUser: this.user,
    };
  },
  created() {},
  methods: {},
  watch: {
    user() {
      this.thisUser = this.user;
    },
  },
};
</script>
<style scoped>
.prop-name {
  margin-top: 15px;
  margin-bottom: 6px;
  font-weight: bold;
  font-size: 20px;
  font-family: "等线";
}
.prop-special-value {
  margin-left: 10px;
  font-family: Serif;
  font-size: 18px;
  color: #304683;
}
.prop-value {
  font-size: 18px;
  font-family: "等线";
}
</style>
