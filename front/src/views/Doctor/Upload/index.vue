<template>
  <div>
    <div class="body" style="width:1200px">
      <el-row>
        <!-- 左侧的固定快捷按钮 -->
        <el-col :span="4">
          <el-affix :offset="120">
            <upload-left
              :props="props"
              @downloadAllImage="downloadAllImage"
              @deleteAllImage="deleteAllImage"
              @getImageList="getImageList"
            />
          </el-affix>
        </el-col>
        <!-- 中间主体部分 -->
        <el-col :span="16" style="min-width:600px;">
          <upload-middle
            :props="props"
            @downloadAllImage="downloadAllImage"
            @deleteAllImage="deleteAllImage"
            @getImageList="getImageList"
          />
        </el-col>
        <!-- 右边的分页 -->
        <el-col :span="4">
          <el-affix :offset="120">
            <div style="margin-left:4vw;">
              <el-row>
                <el-select
                  v-model="props.pagesize"
                  placeholder="Select"
                  style="width:100px;margin-left:5px"
                  @change="handleSizeChange(props.pagesize)"
                >
                  <el-option label="1条/页" :value="1"> </el-option>
                  <el-option label="3条/页" :value="3"> </el-option>
                  <el-option label="5条/页" :value="5"> </el-option>
                  <el-option label="10条/页" :value="10"> </el-option>
                </el-select>
              </el-row>
              <el-row style="margin-left:5px; inline-block;">
                <el-button-group>
                  <el-button
                    style="width:50px; inline-block;"
                    icon="el-icon-arrow-left"
                    :disabled="props.pagenum <= 1"
                    @click="handleCurrentChange(props.pagenum - 1)"
                  ></el-button>
                  <el-button
                    style="width:50px; inline-block;"
                    icon="el-icon-arrow-right"
                    :disabled="props.pagenum >= props.total / props.pagesize"
                    @click="handleCurrentChange(props.pagenum + 1)"
                  >
                  </el-button>
                </el-button-group>
              </el-row>
              <el-row>
                <el-pagination
                  :currentPage="props.pagenum"
                  :page-size="props.pagesize"
                  layout="pager"
                  :total="props.total"
                  @current-change="handleCurrentChange"
                >
                </el-pagination>
              </el-row>
            </div>
          </el-affix>
        </el-col>
      </el-row>
    </div>
    <el-dialog v-model="props.visible" title="图片上传" width="1200px">
      <my-uploader @getImageList="getImageList" :props="props"/>
    </el-dialog>
  </div>
</template>

<script>
import { ElMessageBox, ElMessage } from "element-plus";
import UploadMiddle from "./components/Middle.vue";
import UploadLeft from "./components/Left.vue";
import MyUploader from "./components/Uploader.vue";
export default {
  name: "Upload",
  components: {
    UploadLeft,
    UploadMiddle,
    MyUploader,
  },
  data() {
    return {
      props: {
        loadingNewPicture: false,
        pagenum: 1,
        pagesize: 5,
        searchTitle: "",
        total: 0,
        imageList: [],
        newName: "",
        visible: false,
        baseURL: "http://localhost:8000/",
        //baseURL:"http://10.251.0.251:8000/"
      },
    };
  },
  created() {
    this.getImageList();
  },
  methods: {
    handleSizeChange(size) {
      this.props.pagesize = size;
      this.getImageList();
    },
    handleCurrentChange(current) {
      this.props.pagenum = current;
      this.getImageList();
    },
    downloadAllImage() {
      var i, len;
      for (i = 0, len = this.props.imageList.length; i < len; i++) {
        this.downloadASetOfImage(this.props.imageList[i]);
      }
    },
    downloadASetOfImage(singleImage) {
      this.downloadIamge(
        singleImage.photo_origin,
        singleImage.photo_realname + "_origin"
      );
      this.downloadIamge(
        singleImage.photo_upload,
        singleImage.photo_realname + "_upload"
      );
      this.downloadIamge(
        singleImage.photo_promap,
        singleImage.photo_realname + "_promap"
      );
    },
    deleteAllImage() {
      ElMessageBox.confirm(
        "本操作无法撤回，您确认要清空本页图片吗？",
        "Warning",
        {
          confirmButtonText: "OK",
          cancelButtonText: "Cancel",
          type: "warning",
        }
      )
        .then(() => {
          var i, len;
          for (i = 0, len = this.props.imageList.length; i < len; i++) {
            this.deleteASetOfImage(this.props.imageList[i]);
          }
          ElMessage({
            type: "success",
            message: "删除成功",
          });
        })
        .catch(() => {
          ElMessage({
            type: "info",
            message: "删除被取消",
          });
        });
    },

    async deleteASetOfImage(singleImage) {
      await new Promise((resolve) => {
        this.$http
          .post(
            "/deletePicture/",
            JSON.stringify({ photoID: singleImage.photo_id })
          )
          .then((res) => {
            {
              if (res.data.message === "删除成功") {
                this.getImageList();
              } else {
                this.$message.error("删除失败");
              }
            }
          });
        resolve();
      }).then(() => {});
    },
    async getImageList() {
      this.props.loadingNewPicture = true;
      await new Promise((resolve) => {
        this.$http
          .post(
            "/getList/",
            JSON.stringify({
              title: this.props.searchTitle,
              user_id: this.$store.state.user_id,
              pagenum: this.props.pagenum,
              pagesize: this.props.pagesize,
            })
          )
          .then((res) => {
            {
              if (res.data.message === "返回list成功") {
                this.props.imageList = res.data.imageList;
                this.props.total = res.data.total;
              } else {
                this.$message.error("获取列表失败");
              }
              this.props.loadingNewPicture = false;
            }
          });
        resolve();
      }).then(() => {});
    },
    downloadIamge(imgsrc, name) {
      //下载图片地址和图片名
      let image = new Image();
      // 解决跨域 Canvas 污染问题
      image.setAttribute("crossOrigin", "anonymous");
      image.onload = function() {
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

<style>
@import "style.css";
</style>
