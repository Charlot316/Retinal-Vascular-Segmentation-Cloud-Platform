<template>
  <div>
    <div class="container">
      <el-upload
        class="upload-demo inline-block"
        action="http://10.251.0.251:8000/receive/"
        :data="{pic_title:'test.tif'}"
        :on-success="handleAvatarSuccess"
        list-type=false
        :show-file-list="false"
        name="pic_img"
      >
        <el-button
          show-file-list=false
          type="primary"
        >上传图片</el-button>
      </el-upload>
      <el-button
        type="success"
        @click="download"
      >下载结果</el-button>
      <div
        v-for="singleImage in imageList"
        :key="singleImage"
        style="margin-top: 20px"
      >
        <el-card shadow="hover">
          <template #header>
            <div class="card-header">
              <span>{{singleImage.name}}</span>
              <el-button @click="download">下载全部图片</el-button>
            </div>
          </template>
          <el-row>
            <el-col :span="8">

              <el-card :body-style="{ padding: '0px' }">
                <img
                  style="width: 100%;"
                  :src="singleImage.origin"
                  class="image"
                />
                <div style="padding: 14px">
                  <span>原始图片</span>
                  <div class="bottom">
                    <el-button
                      type="text"
                      class="button"
                    >下载图片</el-button>
                  </div>
                </div>
              </el-card>

            </el-col>
            <el-col :span="8">

              <el-card :body-style="{ padding: '0px' }">
                <img
                  style="width: 100%;"
                  :src="singleImage.bytemap"
                  class="image"
                />
                <div style="padding: 14px">
                  <span>bytemap</span>
                  <div class="bottom">
                    <el-button
                      type="text"
                      class="button"
                    >下载图片</el-button>
                  </div>
                </div>
              </el-card>

            </el-col>
            <el-col :span="8">

              <el-card :body-style="{ padding: '0px' }">
                <img
                  style="width: 100%;"
                  :src="singleImage.promap"
                  class="image"
                />
                <div style="padding: 14px">
                  <span>promap</span>
                  <div class="bottom">
                    <el-button
                      type="text"
                      class="button"
                    >下载图片</el-button>
                  </div>
                </div>
              </el-card>

            </el-col>

          </el-row>
        </el-card>
      </div>
    </div>
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
      imageList: [],
    };
  },
  created() {
    this.getImageList();
  },
  methods: {
    getImageList() {
      this.imageList = [
        {
          name: "一个图片",
          origin: "https://gimg2.baidu.com/image_search/src=http%3A%2F%2Fhbimg.b0.upaiyun.com%2Ff8107c953b8e05b262b2bab62c44acbcb238a7b79ece0-Deltbt_fw658&refer=http%3A%2F%2Fhbimg.b0.upaiyun.com&app=2002&size=f9999,10000&q=a80&n=0&g=0n&fmt=jpeg?sec=1637657441&t=0d1d0ae8ae31dd257cfb6c985390351a",
          bytemap: "https://gimg2.baidu.com/image_search/src=http%3A%2F%2Fc-ssl.duitang.com%2Fuploads%2Fitem%2F201705%2F20%2F20170520200616_HN2jR.thumb.1000_0.jpeg&refer=http%3A%2F%2Fc-ssl.duitang.com&app=2002&size=f9999,10000&q=a80&n=0&g=0n&fmt=jpeg?sec=1637657441&t=bdd770537b2bff7e58737481c3bb331e",
          promap: "https://gimg2.baidu.com/image_search/src=http%3A%2F%2Fb-ssl.duitang.com%2Fuploads%2Fitem%2F201705%2F20%2F20170520200604_txGEW.thumb.700_0.jpeg&refer=http%3A%2F%2Fb-ssl.duitang.com&app=2002&size=f9999,10000&q=a80&n=0&g=0n&fmt=jpeg?sec=1637657441&t=ed45db0968503fa01e0359a76e2b6970",
        },
        {
          name: "一个图片",
          origin: "https://gimg2.baidu.com/image_search/src=http%3A%2F%2Fhbimg.b0.upaiyun.com%2Ff8107c953b8e05b262b2bab62c44acbcb238a7b79ece0-Deltbt_fw658&refer=http%3A%2F%2Fhbimg.b0.upaiyun.com&app=2002&size=f9999,10000&q=a80&n=0&g=0n&fmt=jpeg?sec=1637657441&t=0d1d0ae8ae31dd257cfb6c985390351a",
          bytemap: "https://gimg2.baidu.com/image_search/src=http%3A%2F%2Fc-ssl.duitang.com%2Fuploads%2Fitem%2F201705%2F20%2F20170520200616_HN2jR.thumb.1000_0.jpeg&refer=http%3A%2F%2Fc-ssl.duitang.com&app=2002&size=f9999,10000&q=a80&n=0&g=0n&fmt=jpeg?sec=1637657441&t=bdd770537b2bff7e58737481c3bb331e",
          promap: "https://gimg2.baidu.com/image_search/src=http%3A%2F%2Fb-ssl.duitang.com%2Fuploads%2Fitem%2F201705%2F20%2F20170520200604_txGEW.thumb.700_0.jpeg&refer=http%3A%2F%2Fb-ssl.duitang.com&app=2002&size=f9999,10000&q=a80&n=0&g=0n&fmt=jpeg?sec=1637657441&t=ed45db0968503fa01e0359a76e2b6970",
        },
      ]
    },
    handleAvatarSuccess() {
      this.$message({
        message: "上传成功",
        type: "success",
      });
    },
    getImageFile: function (e) {
      let file = e.target.files[0];
      this.form.pic_img = file;
      this.form.pic_title = 'test.tif'
    },
    // onSubmit() {
    //   let formData = new FormData();
    //   formData.append("pic_title", this.form.pic_title);
    //   formData.append("pic_img", this.form.pic_img, 'test.tif');
    //   this.$http
    //     .post("/receive/", formData)
    //     .then((res) => {
    //       console.log(res);
    //       this.$message({
    //         message: "上传成功",
    //         type: "success",
    //       });
    //     })
    //     .catch((err) => {
    //       console.log(err);
    //     });
    // },
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
