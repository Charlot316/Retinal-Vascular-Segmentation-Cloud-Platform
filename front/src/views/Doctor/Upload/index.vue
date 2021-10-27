<template>
  <div>
    <div class="body">
      <el-row>
        <el-col :span="4">
          <el-affix :offset="120">
            <div style="margin-left:5vw;">
              <el-row>
                <el-tooltip
                  class="item"
                  effect="dark"
                  content="上传新的眼底血管图片"
                  placement="right"
                >
                  <el-upload
                    class="upload-demo"
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
                      icon="el-icon-upload"
                      circle
                    ></el-button>
                  </el-upload>
                </el-tooltip>

              </el-row>
              <el-row>
                <el-tooltip
                  class="item"
                  effect="dark"
                  content="下载本页所有图片"
                  placement="right"
                >
                  <el-button
                    style="margin-top:25px"
                    type="success"
                    icon="el-icon-download"
                    @click="downloadAllImage()"
                    circle
                  ></el-button>
                </el-tooltip>
              </el-row>
              <el-row>
                <el-tooltip
                  class="item"
                  effect="dark"
                  content="清空本页所有图片"
                  placement="right"
                >
                  <el-button
                    style="margin-top:25px"
                    @click="deleteAllImage(singleImage)"
                    type="danger"
                    icon="el-icon-delete"
                    circle
                  ></el-button>
                </el-tooltip>
              </el-row>
              <el-row>
                <el-tooltip
                  class="item"
                  effect="dark"
                  content="搜索图片"
                  placement="right"
                >
                  <div>
                    <el-popover
                      placement="right"
                      :width="400"
                      trigger="click"
                    >

                      <template #reference>

                        <el-button
                          style="margin-top:25px"
                          type="info"
                          icon="el-icon-search"
                          circle
                        ></el-button>

                      </template>
                      <div>
                        <el-input
                          v-model="searchTitle"
                          @keyup.enter="getImageList"
                          placeholder="请输入图片名"
                          clearable
                        >
                          <template #append>
                            <el-button
                              @click="getImageList"
                              icon="el-icon-search"
                            ></el-button>
                          </template>
                        </el-input>
                      </div>
                    </el-popover>
                  </div>
                </el-tooltip>
              </el-row>
            </div>
          </el-affix>
        </el-col>
        <el-col :span="16">
          <div class="container">
            <div>
              <el-tooltip
                class="item"
                effect="dark"
                content="上传新的眼底血管图片"
                placement="top"
              >
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
                    icon="el-icon-upload"
                  >上传</el-button>
                </el-upload>
              </el-tooltip>
              <el-tooltip
                class="item"
                effect="dark"
                content="下载本页所有图片"
                placement="top"
              >
                <el-button
                  type="success"
                  @click="downloadAllImage()"
                  icon="el-icon-download"
                >下载</el-button>
              </el-tooltip>
              <el-tooltip
                class="item"
                effect="dark"
                content="清空本页所有图片"
                placement="top"
              >
                <el-button
                  style="margin-left:30px"
                  @click="deleteAllImage(singleImage)"
                  type="danger"
                  icon="el-icon-delete"
                >清空</el-button>
              </el-tooltip>
              <el-input
                v-model="searchTitle"
                @keyup.enter="getImageList"
                placeholder="请输入图片名"
                clearable
                style=" margin-left:50px;width:300px"
              >
                <template #append>
                  <el-button
                    @click="getImageList"
                    icon="el-icon-search"
                  ></el-button>
                </template>
              </el-input>
            </div>
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
                        style="margin-right:10px"
                        icon="el-icon-download"
                      >下载全部</el-button>
                      <el-button
                        @click="deleteAGroupOfImage(singleImage)"
                        type="danger"
                        icon="el-icon-delete"
                      >删除全部</el-button>
                    </span>
                  </div>
                </template>
                <el-row>
                  <el-col :span="8">

                    <el-card :body-style="{ padding: '0px' }">
                      <el-image
                        lazy
                        style="width: 100%;"
                        :src="singleImage.origin"
                        class="image"
                        :preview-src-list="[singleImage.origin,singleImage.bytemap,singleImage.promap]"
                      >
                        <template #error>
                          <div class="image-slot">
                            <el-image
                              lazy
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
                            @click="downloadIamge(singleImage.origin, singleImage.name+'_origin')"
                          >下载图片</el-button>
                        </div>
                      </div>
                    </el-card>

                  </el-col>
                  <el-col :span="8">

                    <el-card :body-style="{ padding: '0px' }">
                      <el-image
                        lazy
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
                            @click="downloadIamge(singleImage.bytemap, singleImage.name+'_bytemap')"
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
        </el-col>
        <el-col :span="4">
          <el-affix :offset="120">
            <div style="margin-left:2vw;">
              <el-row>
                <el-select
                  v-model="pagesize"
                  placeholder="Select"
                  style="width:100px;margin-left:5px"
                  @change="handleSizeChange(pagesize)"
                >
                  <el-option
                    label="1条/页"
                    :value="1"
                  >
                  </el-option>
                  <el-option
                    label="3条/页"
                    :value="3"
                  >
                  </el-option>
                  <el-option
                    label="5条/页"
                    :value="5"
                  >
                  </el-option>
                  <el-option
                    label="10条/页"
                    :value="10"
                  >
                  </el-option>
                </el-select>
              </el-row>
              <el-row style="margin-left:5px;">
                <el-button-group>
                  <el-button
                    style="width:50px;"
                    icon="el-icon-arrow-left"
                    :disabled="pagenum<=1"
                    @click="handleCurrentChange(pagenum-1)"
                  ></el-button>
                  <el-button
                    style="width:50px;"
                    icon="el-icon-arrow-right"
                    :disabled="pagenum>=(total/pagesize)"
                    @click="handleCurrentChange(pagenum+1)"
                  >
                  </el-button>
                </el-button-group>
              </el-row>
              <el-row>
                <el-pagination
                  :currentPage="pagenum"
                  :page-size="pagesize"
                  layout="pager"
                  :total="total"
                  :pager-count="10"
                  @current-change="handleCurrentChange"
                >
                </el-pagination>
              </el-row>
            </div>
          </el-affix>
        </el-col>
      </el-row>
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
      pagenum: 1,
      pagesize: 5,
      searchTitle: "",
      total: 0,
      title: "",
      imageList: [],
    };
  },
  created() {
    this.getImageList();
  },
  methods: {

    handleSizeChange(size) {
      this.pagesize = size;
      this.getImageList();
    },
    handleCurrentChange(current) {
      this.pagenum = current;
      this.getImageList();
    },
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
          .post("/deletePicture/", JSON.stringify({ name: singleImage.name }))
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
          .post("/getList/", JSON.stringify({ title: this.searchTitle, user_id: this.$store.state.user_id, pagenum: this.pagenum, pagesize: this.pagesize }))
          .then((res) => {
            {
              if (res.data.message === "返回list成功") {
                this.imageList = res.data.imageList
                this.total = res.data.total
              }
              else {
                alert("获取列表失败")
              }
            }
          });
        resolve();
      }).then(() => {
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
    downloadIamge(imgsrc, name) {//下载图片地址和图片名
      let image = new Image();
      // 解决跨域 Canvas 污染问题
      image.setAttribute("crossOrigin", "anonymous");
      image.onload = function () {
        let canvas = document.createElement("canvas");
        canvas.width = image.width;
        canvas.height = image.height;
        let context = canvas.getContext("2d");
        context.drawImage(image, 0, 0, image.width, image.height);
        let url = canvas.toDataURL("image/png"); //得到图片的base64编码数据
        let a = document.createElement("a"); // 生成一个a元素
        let event = new MouseEvent("click"); // 创建一个单击事件
        a.download = name || "photo"; // 设置图片名称
        a.href = url; // 将生成的URL设置为a.href属性
        a.dispatchEvent(event); // 触发a的单击事件
      };
      image.src = imgsrc;
    },
  },
};
</script>

<style scoped>
@import "style.css";
</style>
