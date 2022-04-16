<template>
  <div>
    <div class="prop-name">姓名</div>
    <el-input v-model="thisUser.name" class="prop-value" readonly/>

    <div class="prop-name">性别</div>
    <el-radio-group v-model="thisUser.sex" class="prop-value" disabled>
      <el-radio :label="1">男</el-radio>
      <el-radio :label="0">女</el-radio>
    </el-radio-group>

    <div class="prop-name">
      <span>身高:</span>
      <span  class="prop-special-value">{{thisUser.height}}</span>
      <span>体重:</span>
      <span  class="prop-special-value">{{thisUser.weight}}</span>
      <span>年龄:</span>
      <span  class="prop-special-value">{{thisUser.age}}</span>
    </div>

    <div class="prop-name">手机号</div>
    <div class="prop-value">{{thisUser.phone}}</div>
    <div class="prop-name">邮箱</div>
    <div class="prop-value">{{thisUser.email}}</div>
    <div class="prop-name">地址</div>
    <div class="prop-value">{{thisUser.address}}</div>
  </div>
</template>
<script>
export default {
  props: ['user'],
  data() {
    return {
      thisUser: this.user,
    };
  },
  created() {
  },
  methods: {
    getEducation(index) {
      if (index == 1) return "博士后"
      if (index == 2) return "博士"
      if (index == 3) return "硕士"
      if (index == 4) return "本科"
      if (index == 5) return "大专"
      if (index == 6) return "高中及以下"
    }
  },
  watch: {
    user() {
      this.thisUser = this.user
    }
  }
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