<template>
  <div style="text-align:center">
    <el-card class="box-card">
      <el-upload
        action="http://localhost:8000/receive/"
        :data="{ user_id: $store.state.user_id, id: params.id }"
        :on-success="handleAvatarSuccess"
        class="upload-demo"
        drag
        :before-upload="checkFile"
        :on-error="handleUploadError"
        name="pic_img"
        style="width: 100%"
      >
        <i class="el-icon-upload"></i>
        <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
      </el-upload>
    </el-card>
  </div>
</template>

<script>
export default {
  props: ["params", "props"],
  data() {
    return {
      code: "",
      errorCode: false,
      clicked: false,
      myProps: this.props,
    };
  },
  updated() {
    //console.log(this.method);
  },
  methods: {
    getImageList() {
      this.$emit("getImageList");
    },
    handleUploadError() {
      this.myProps.loadingNewPicture = false;
      this.$message.error("上传失败");
    },
    checkFile(file) {
      this.myProps.loadingNewPicture = true;
      var fileExtension = file.name.substring(file.name.lastIndexOf(".") + 1);
      if (file.type.startsWith("image")) {
        if (fileExtension === "gif") {
          this.$message.error("不支持上传gif图片");
          this.myProps.loadingNewPicture = false;
          return false;
        }
      } else {
        this.$message.error("请上传图片");
        this.myProps.loadingNewPicture = false;
        return false;
      }
    },
    handleAvatarSuccess() {
      this.$message({
        message: "上传成功",
        type: "success",
      });
      this.myProps.loadingNewPicture = true;
      this.myProps.visible = false;
      this.$emit("back-step");
      setTimeout(() => {
        this.myProps.imageList = [];
        this.getImageList();
      }, 10000);
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
