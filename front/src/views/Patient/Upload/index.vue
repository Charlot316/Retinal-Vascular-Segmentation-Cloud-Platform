<template>
  <div>
    <div class="container">
      <el-upload
        class="upload-demo inline-block"
        action="http://10.251.0.251:8000/receive/"
        :data="{pic_title:title,user_id:$store.state.user_id}"
        :on-success="handleAvatarSuccess"
        list-type=false
        :show-file-list="false"
        :before-upload="setName"
        name="pic_img"
      >
        <el-button
          show-file-list=false
          type="primary"
        >上传图片</el-button>
      </el-upload>
      <el-button
        type="success"
        @click="downloadAllImage()"
      >下载所有图片</el-button>
      <el-button
        style="margin-left:25px"
        @click="deleteAllImage(singleImage)"
        type="danger"
      >清空本页图片</el-button>
      <!-- <el-button
        type="success"
        @click="download()"
      >测试下载图片</el-button> -->
      <div
        v-for="singleImage in imageList"
        :key="singleImage"
        style="margin-top: 20px"
      >
        <el-card shadow="hover">
          <template #header>
            <div class="card-header">
              <span>{{singleImage.name}}</span>
              <span>
                <el-button
                  @click="downloadASetOfImage(singleImage)"
                  type="primary"
                  style="margin-right:10px"
                >下载全部图片</el-button>
                <el-button
                  @click="deleteAGroupOfImage(singleImage)"
                  type="danger"
                >删除全部图片</el-button>
              </span>
            </div>
          </template>
          <el-row>
            <el-col :span="8">

              <el-card :body-style="{ padding: '0px' }">
                <el-image
                  style="width: 100%;"
                  :src="singleImage.origin"
                  class="image"
                  :preview-src-list="[singleImage.origin,singleImage.bytemap,singleImage.promap]"
                >
                  <template #error>
                    <div class="image-slot">
                      <el-image
                        style="width: 100%;"
                        :src="require('../../../assets/img/loading.gif')"
                        class="image"
                      />
                      <h3 style="text-align:center">图片加载中，请稍后刷新</h3>
                    </div>
                  </template>
                </el-image>
                <div style="padding: 14px">
                  <span>原始图片</span>
                  <div class="bottom">
                    <el-button
                      type="text"
                      class="button"
                      @click="downloadIamge(singleImage.promap, singleImage.name+'_origin')"
                    >下载图片</el-button>
                  </div>
                </div>
              </el-card>

            </el-col>
            <el-col :span="8">

              <el-card :body-style="{ padding: '0px' }">
                <el-image
                  style="width: 100%;"
                  :src="singleImage.bytemap"
                  class="image"
                  :preview-src-list="[singleImage.bytemap,singleImage.promap,singleImage.origin]"
                >
                  <template #error>
                    <div class="image-slot">
                      <el-image
                        style="width: 100%;"
                        :src="require('../../../assets/img/loading.gif')"
                        class="image"
                      />
                      <h3 style="text-align:center">图片加载中，请稍后刷新</h3>
                    </div>
                  </template>
                </el-image>
                <div style="padding: 14px">
                  <span>bytemap</span>
                  <div class="bottom">
                    <el-button
                      type="text"
                      class="button"
                      @click="downloadIamge(singleImage.promap, singleImage.name+'_bytemap')"
                    >下载图片</el-button>
                  </div>
                </div>
              </el-card>

            </el-col>
            <el-col :span="8">

              <el-card :body-style="{ padding: '0px' }">
                <el-image
                  style="width: 100%;"
                  :src="singleImage.promap"
                  class="image"
                  :preview-src-list="[singleImage.promap,singleImage.origin,singleImage.bytemap]"
                >
                  <template #error>
                    <div class="image-slot">
                      <el-image
                        style="width: 100%;"
                        :src="require('../../../assets/img/loading.gif')"
                        class="image"
                      />
                      <h3 style="text-align:center">图片加载中，请稍后刷新</h3>
                    </div>
                  </template>
                </el-image>
                <div style="padding: 14px">
                  <span>promap</span>
                  <div class="bottom">
                    <el-button
                      type="text"
                      class="button"
                      @click="downloadIamge(singleImage.promap, singleImage.name+'_promap')"
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
import { ElMessageBox, ElMessage } from 'element-plus'
export default {
  name: "Upload",
  data() {
    return {
      form: {
        pic_title: "测试",
        pic_img: "",
      },
      title: "",
      imageList: [],
    };
  },
  created() {
    this.getImageList();
  },
  methods: {

    setName(file) {
      var fileExtension = file.name.substring(file.name.lastIndexOf('.') + 1);
      if (fileExtension === "gif") {
        alert("不支持上传gif图片")
        return false
      }
      this.title = file.name;
    },
    downloadAllImage() {
      var i, len;
      for (i = 0, len = this.imageList.length; i < len; i++) {
        this.downloadASetOfImage(this.imageList[i])
      }
    },
    downloadASetOfImage(singleImage) {
      this.downloadIamge(singleImage.origin, singleImage.name + "_origin")
      this.downloadIamge(singleImage.bytemap, singleImage.name + "_bytemap")
      this.downloadIamge(singleImage.promap, singleImage.name + "_promap")
    },
    deleteAllImage() {
      ElMessageBox.confirm(
        '本操作无法撤回，您确认要清空本页图片吗？',
        'Warning',
        {
          confirmButtonText: 'OK',
          cancelButtonText: 'Cancel',
          type: 'warning',
        }
      )
        .then(() => {
          var i, len;
          for (i = 0, len = this.imageList.length; i < len; i++) {
            this.deleteASetOfImage(this.imageList[i])
          }
          ElMessage({
            type: 'success',
            message: '删除成功',
          })
        })
        .catch(() => {
          ElMessage({
            type: 'info',
            message: '删除被取消',
          })
        })
    },
    deleteAGroupOfImage(singleImage) {
      ElMessageBox.confirm(
        '本操作无法撤回，您确认要清空这三张图片吗？',
        'Warning',
        {
          confirmButtonText: 'OK',
          cancelButtonText: 'Cancel',
          type: 'warning',
        }
      )
        .then(() => {
          this.deleteASetOfImage(singleImage)
          ElMessage({
            type: 'success',
            message: '删除成功',
          })
        })
        .catch(() => {
          ElMessage({
            type: 'info',
            message: '删除被取消',
          })
        })
    },
    async deleteASetOfImage(singleImage) {
       await new Promise((resolve) => {
        this.$http
          .post("/deletePicture/", JSON.stringify({ name:singleImage.name }))
          .then((res) => {
            {
              if (res.data.message === "删除成功") {
                this.getImageList()
              }
              else {
                alert("删除失败")
              }
            }
          });
        resolve();
      }).then(() => {
      });
      
    },
    async getImageList() {
      await new Promise((resolve) => {
        this.$http
          .post("/getList/", JSON.stringify({ user_id: this.$store.state.user_id }))
          .then((res) => {
            console.log(res);
            {
              console.log(res);
              if (res.data.message === "返回list成功") {
                this.imageList = res.data.imageList
              }
              else {
                alert("获取列表失败")
              }
            }
          });
        resolve();
      }).then(() => {
        console.log("成功啦post啦");
      });
    },
    handleAvatarSuccess() {
      this.$message({
        message: "上传成功",
        type: "success",
      });
      this.getImageList();
      // setTimeout(() => {
      //   this.imageList[this.imageList.length - 1] = {}
      //   this.getImageList();
      // }, 15000)
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
