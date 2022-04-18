<template>
  <el-card style="width:940px;" shadow="hover">
    <!-- 卡片头栏 -->
    <template #header>
      <div class="card-header">
        <span
          style="display: flex;justify-content: space-between;align-items: center; width:500px;"
        ><span style="display: flex;justify-content: space-between;align-items: center; width:350px;">
          <user-icon :user="singleImage.patient"></user-icon>
          <user-icon :user="singleImage.doctor"></user-icon>
          </span>
          <span>
            <span>{{ singleImage.photo_realname }}</span>
            <!-- 修改名字 -->
            <el-popover v-if="singleImage.doctor.id == $store.state.user_id" placement="right" width="400" trigger="click">
              <template #reference>
                <el-button
                  icon="el-icon-edit"
                  type="text"
                  circle
                  @click="newName = singleImage.photo_realname"
                ></el-button>
              </template>
              <el-input
                v-model="newName"
                @keyup.enter="revisePictureName(singleImage)"
                placeholder="请输入修改后的图片名称"
                clearable
              >
                <template #append>
                  <el-button
                    @click="revisePictureName(singleImage)"
                    icon="el-icon-check"
                  ></el-button>
                </template>
              </el-input>
            </el-popover>
          </span>
        </span>
        <span>
          <!-- 下载图片 -->
          <el-button
            @click="downloadASetOfImage(singleImage)"
            icon="el-icon-download"
            >下载</el-button
          >
          <!-- 删除图片 -->
          <el-button
            @click="deleteAGroupOfImage(singleImage)"
            type="danger"
            icon="el-icon-delete"
            v-if="singleImage.doctor.id == $store.state.user_id"
            >删除</el-button
          >
          <el-button
            type="primary"
            icon="el-icon-search"
            >详情</el-button
          >
        </span>
      </div>
    </template>
    <!-- 三张图片 -->
    <el-row>
      <el-col :span="8">
        <single-photo :singleImage="singleImage" index="origin" />
      </el-col>
      <el-col :span="8">
        <single-photo
          v-if="singleImage.photo_upload && singleImage.photo_upload.length > 0"
          :singleImage="singleImage"
          index="upload"
        />
        <div v-else>
          <el-upload
            class="avatar-uploader"
            :action="'http://localhost:8000/upload/'"
            :data="{ photo_id: singleImage.photo_id, id: $store.state.user_id }"
            :show-file-list="false"
            :on-success="handleAvatarSuccess"
            :before-upload="checkFile"
            :on-error="handleUploadError"
            list-type="false"
            name="pic_img"
          >
            <el-card :body-style="{ padding: '0px' }">
              <el-image
                lazy
                style="width: 297px;height:297px;"
                src="https://img0.baidu.com/it/u=101714381,3578597708&fm=253&fmt=auto&app=138&f=JPEG?w=667&h=500"
                class="image"
              >
              </el-image>
              <div style="padding: 14px">
                <span>金标准</span>
                <div class="bottom">
                  <el-button type="text" class="button">点击上传</el-button>
                </div>
              </div>
            </el-card>
          </el-upload>
        </div>
      </el-col>
      <el-col :span="8">
        <single-photo :singleImage="singleImage" index="promap" />
      </el-col>
    </el-row>
  </el-card>
</template>
<script>
import UserIcon from "@/components/Public/Icon";
import { ElMessageBox, ElMessage } from "element-plus";
import SinglePhoto from "./SinglePhoto.vue";
export default {
  props: ["props", "singleImage"],
  components: {
    SinglePhoto,
    UserIcon,
  },
  data() {
    return {
      myProps: this.props,
      newName: "",
    };
  },
  created() {
    console.log(this.singleImage);
  },
  methods: {
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
      setTimeout(() => {
        this.myProps.imageList = [];
        this.getImageList();
      }, 2000);
    },
    getImageList() {
      this.$emit("getImageList");
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
    deleteAGroupOfImage(singleImage) {
      ElMessageBox.confirm(
        "本操作无法撤回，您确认要清空这三张图片吗？",
        "Warning",
        {
          confirmButtonText: "OK",
          cancelButtonText: "Cancel",
          type: "warning",
        }
      )
        .then(() => {
          this.deleteASetOfImage(singleImage);
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
    async revisePictureName(singleImage) {
      if (this.newName.trim().length == 0)
        return this.$message.error("图片命名不能为空");
      await new Promise((resolve) => {
        this.$http
          .post(
            "/revisePictureName/",
            JSON.stringify({
              photoID: singleImage.photo_id,
              newName: this.newName,
            })
          )
          .then((res) => {
            {
              if (res.data.message === "修改成功") {
                singleImage.photo_realname = this.newName;
                this.$message.success("图片名修改成功");
              } else {
                this.$message.error("修改失败");
              }
            }
          });
        resolve();
      }).then(() => {});
    },
  },
};
</script>
<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>
