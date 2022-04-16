<template>
  <div>
    <div class="prop-name">姓名</div>
    <el-input v-model="thisUser.name" class="prop-value" />

    <div class="prop-name">性别</div>
    <el-radio-group v-model="thisUser.sex" class="prop-value">
      <el-radio :label="1">男</el-radio>
      <el-radio :label="0">女</el-radio>
    </el-radio-group>

    <div class="prop-name">
      <span>身高:</span>
      <el-input-number
        v-model="thisUser.height"
        class="prop-special-value"
        :min="1"
        :max="300"
      />
      <span>体重:</span>
      <el-input-number
        v-model="thisUser.height"
        class="prop-special-value"
        :min="1"
        :max="500"
      />
      <span>年龄:</span>
      <el-input-number
        v-model="thisUser.height"
        class="prop-special-value"
        :min="1"
        :max="150"
      />
    </div>

    <div class="prop-name">手机号</div>
    <el-input v-model="thisUser.phone" class="prop-value" />

    <div class="prop-name">邮箱</div>
    <el-input v-model="thisUser.email" class="prop-value" />

    <div class="prop-name">地址</div>
    <el-input v-model="thisUser.address" class="prop-value" />
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
