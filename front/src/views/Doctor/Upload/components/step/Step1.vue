<template>
  <div>
    <el-card class="box-card">
      <el-input
        v-model="myParams.name"
        @keyup.enter="submit"
        placeholder="请输入患者姓名"
        clearable
      >
        <template #append>
          <el-button @click="submit" icon="el-icon-search"></el-button>
        </template>
      </el-input>
    </el-card>
  </div>
</template>

<script>
export default {
  props: ["params"],
  data() {
    return {
      myParams: this.params,
    };
  },
  updated() {
    //console.log(this.method);
  },
  methods: {
    submit() {
      if (this.myParams.name.trim().length > 0) {
        this.$emit("next-step");
      } else {
        this.$message({
          title: "错误",
          message: "请输入患者姓名",
          type: "error",
        });
      }
    },
  },
};
</script>

<style scoped>
.box-card {
  width: 900px;
  margin: 0 auto;
}
</style>
