<template>
  <div>
    <el-card class="box-card">
      <el-upload
        class="upload-demo"
        drag
        :on-error="handleError"
        :on-success="handleSuccess"
        show-file-list
        action="https://jsonplaceholder.typicode.com/posts/"
        list-type="picture"
        multiple
      >
        <i class="el-icon-upload"></i>
        <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
        <div class="el-upload__tip">只能上传jpg/png文件，且不超过500kb</div>
      </el-upload>
    </el-card>
  </div>
</template>

<script>
  export default {
    type: "user",
    data() {
      return {};
    },
    methods: {
      handleSuccess() {
        this.$message.success("上传成功");
      },
      handleError() {
        this.$message.error("上传失败");
      },
    },
    computed: {},
  };
</script>

<style scoped>
  @import "style.css";
</style>
