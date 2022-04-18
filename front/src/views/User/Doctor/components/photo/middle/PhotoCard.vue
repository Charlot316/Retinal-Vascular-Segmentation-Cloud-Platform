<template>
  <el-card shadow="hover">
    <!-- 卡片头栏 -->
    <template #header>
      <div
        style="display: flex;
  justify-content: space-between;
  align-items: center;"
      >
        <span>{{ singleImage.photo_realname }}</span>
        <span>
          <!-- 下载图片 -->
          <el-button
            @click="downloadASetOfImage(singleImage)"
            style="margin-right:10px"
            icon="el-icon-download"
            >下载全部</el-button
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
          <el-card :body-style="{ padding: '0px' }">
            <el-image
              lazy
              style="width: 100%;height:230px;"
              src="https://img0.baidu.com/it/u=101714381,3578597708&fm=253&fmt=auto&app=138&f=JPEG?w=667&h=500"
              class="image"
            >
            </el-image>
            <div style="padding: 14px">
              <span>金标准</span>
              <div class="bottom">
                <el-button type="text" class="button">暂未上传</el-button>
              </div>
            </div>
          </el-card>
        </div>
      </el-col>
      <el-col :span="8">
        <single-photo :singleImage="singleImage" index="promap" />
      </el-col>
    </el-row>
  </el-card>
</template>
<script>
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
  },
};
</script>
