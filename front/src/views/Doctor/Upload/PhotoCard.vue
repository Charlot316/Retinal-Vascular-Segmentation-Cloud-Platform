<template>
  <el-card shadow="hover">
    <!-- 卡片头栏 -->
    <template #header>
      <div class="card-header">
        <span>
          <span>{{ singleImage.photo_realname }}</span>
          <!-- 修改名字 -->
          <el-popover placement="right" width="400" trigger="click">
            <template #reference>
              <el-button
                style="margin-right:10px"
                icon="el-icon-edit"
                type="text"
                circle
                @click="myProps.newName = singleImage.photo_realname"
              ></el-button>
            </template>
            <el-input
              v-model="myProps.newName"
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
        <span>
          <!-- 下载图片 -->
          <el-button
            @click="downloadASetOfImage(singleImage)"
            style="margin-right:10px"
            icon="el-icon-download"
            >下载全部</el-button
          >
          <!-- 删除图片 -->
          <el-button
            @click="deleteAGroupOfImage(singleImage)"
            type="danger"
            icon="el-icon-delete"
            >删除全部</el-button
          >
        </span>
      </div>
    </template>
    <!-- 三张图片 -->
    <el-row>
      <el-col :span="8">
        <single-photo
          :singleImage="singleImage"
          index="origin"
        />
      </el-col>
      <el-col :span="8">
        <single-photo
          :singleImage="singleImage"
          index="upload"
        />
      </el-col>
      <el-col :span="8">
        <single-photo
          :singleImage="singleImage"
          index="promap"
        />
      </el-col>
    </el-row>
  </el-card>
</template>
<script>
import { ElMessageBox, ElMessage } from "element-plus";
import SinglePhoto from "./SinglePhoto.vue";
export default {
  props: ["props", "singleImage"],
  components: {
    SinglePhoto,
  },
  data() {
    return {
      myProps: this.props,
    };
  },
  methods: {
    downloadASetOfImage(singleImage) {
      this.downloadIamge(
        singleImage.photo_origin,
        singleImage.photo_realname + "_origin"
      );
      this.downloadIamge(
        singleImage.photo_promap,
        singleImage.photo_realname + "_promap"
      );
      this.downloadIamge(
        singleImage.photo_upload,
        singleImage.photo_realname + "_bytemap"
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
    getImageList() {
      this.$emit("getImageList");
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
      if (this.props.newName.trim().length == 0)
        return this.$message.error("图片命名不能为空");
      await new Promise((resolve) => {
        this.$http
          .post(
            "/revisePictureName/",
            JSON.stringify({
              photoID: singleImage.photo_id,
              newName: this.props.newName,
            })
          )
          .then((res) => {
            {
              if (res.data.message === "修改成功") {
                singleImage.photo_realname = this.props.newName;
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
