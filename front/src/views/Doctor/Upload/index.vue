<template>
  <div class="container">
    <el-form
      ref="form"
      :model="form"
      label-width="80px"
    >
      <!--      <el-form-item label="图片名称">-->
      <!--        <el-input-->
      <!--          v-model="form.pic_title"-->
      <!--          placeholder="请输入图片名称"-->
      <!--        ></el-input>-->
      <!--      </el-form-item>-->
      <el-form-item label="图片">
        <input
          type="file"
          @change="getImageFile"
          id="img"
        />
      </el-form-item>
      <el-form-item>
        <el-button
          type="primary"
          @click="onSubmit"
        >确认上传</el-button>
        <el-button
          type="success"
          @click="download"
        >下载结果</el-button>
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
        pic_title: "测试",
        pic_img: "",
      },
    };
  },
  methods: {

    getImageFile: function (e) {
      let file = e.target.files[0];
      this.form.pic_img = file;
      this.form.pic_title = 'test.tif'
    },
    onSubmit() {
      let formData = new FormData();
      formData.append("pic_title", this.form.pic_title);
      formData.append("pic_img", this.form.pic_img, 'test.tif');
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
    download() {
      this.$http.post("/download/", this.form.pic_title, {
        responseType: "blob",
      })
        .then((res) => {
          // console.log(res);
          if (res.data.success === false) {
            this.$message.error("出现错误");
            return;
          }
          console.log(res, '看一下res是啥');
          const data = res.data;
          const url = window.URL.createObjectURL(
            new Blob([data], {
              type: "application/octet-stream",
            })
          );
          console.log(url, '看一下url是啥')
          console.log("**********");
          console.log(res.headers['content-disposition']);
          let fileName = 'test.png'
          const a = document.createElement("a");
          document.body.appendChild(a);
          a.style.display = "none";
          a.href = url;
          let filename = fileName;
          a.download = filename;
          console.log(filename)
          a.click();
          document.body.removeChild(a);
          window.URL.revokeObjectURL(url);
        })
    },
  },
};
</script>

<style scoped>
@import "style.css";
</style>
