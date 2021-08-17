<template>
  <div class="container">
    <el-form ref="form" :model="form" label-width="80px">
      <el-form-item label="图片名称">
        <el-input
          v-model="form.pic_title"
          placeholder="请输入图片名称"
        ></el-input>
      </el-form-item>
      <el-form-item label="图片">
        <input type="file" @change="getImageFile" id="img" />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="onSubmit">确认上传</el-button>
        <el-button type="success">重置</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
export default {
  name: "Upload",
  data() {
    return {
      form: {
        pic_title: "",
        pic_img: "",
      },
    };
  },
  methods: {
    getImageFile: function (e) {
      let file = e.target.files[0];
      this.form.pic_img = file;
    },
    onSubmit() {
      let formData = new FormData();
      formData.append("pic_title", this.form.pic_title);
      formData.append("pic_img", this.form.pic_img);
      this.$http
        .post("/receive/", formData)
        .then((res) => {
          console.log(res);
          this.$message({
            message: "上传成功",
            type: "success",
          });
        })
        .catch((err) => {
          console.log(err);
        });
    },
  },
};
</script>

<style scoped>
@import "style.css";
</style>
