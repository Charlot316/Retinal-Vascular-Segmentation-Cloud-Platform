<template>
  <div class="container">
    <h1>个人信息</h1>
    <div class="title-liner"></div>
    <el-row>
      <el-col :span="16">
        <my-info :user="user" />
      </el-col>
      <el-col :span="2"> </el-col>
      <el-col :span="6">
        <div class="icon">
          <right-tab
            @getInfo="getInfo"
            @fatherChangeEditMode="fatherChangeEditMode"
            :user="user"
          />
        </div>
      </el-col>
    </el-row>
  </div>
</template>
<script>
import RightTab from "./RightTab";
import MyInfo from "./Info";
export default {
  props: ["user"],
  data() {
    return {
      mode: 0, //0:展示信息的状态 1:编辑信息的状态
    };
  },
  components: {
    RightTab,
    MyInfo,
  },
  created() {
    this.getInfo();
  },
  activated() {
    this.getInfo();
  },
  methods: {
    fatherChangeEditMode(mode) {
      this.mode = mode;
    },
    getInfo() {
      this.$emit("getInfo");
    },
  },
  watch: {
    user() {
      this.thisUser = this.user;
    },
  },
};
</script>
<style scoped>
.container {
  padding: 30px;
  background: #fff;
  border: 1px solid #ddd;
  border-radius: 5px;
  width: 100%;
}
.title-liner {
  border: 1px solid rgb(230, 230, 230);
  background-color: rgb(230, 230, 230);
  width: 100%;
}
.icon {
  margin-top: 30px;
  text-align: center;
}
</style>
