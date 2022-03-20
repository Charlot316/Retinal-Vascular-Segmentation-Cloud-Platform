<template>
  <el-card :body-style="{ padding: '0px' }">
    <el-image
      lazy
      style="width: 100%;"
      :src="src"
      class="image"
      :preview-src-list="list"
    >
      <!-- 图片加载出错的情况 -->
      <template #error>
        <div class="image-slot">
          <el-image
            lazy
            style="width: 100%;"
            :src="require('../../../../../assets/img/loading.gif')"
            class="image"
          />
          <div style="text-align:center;">
            <h3 style="text-align:center">
              图片加载中，请稍后刷新
            </h3>
            <el-button @click="getImageList">强制刷新</el-button>
          </div>
        </div>
      </template>
    </el-image>
    <div style="padding: 14px">
      <span>{{ name }}</span>
      <div class="bottom">
        <el-button
          type="text"
          class="button"
          @click="downloadIamge(src, singleImage.photo_realname + type)"
          >下载图片</el-button
        >
      </div>
    </div>
  </el-card>
</template>

<script>
export default {
  props: ["singleImage", "index"],
  components: {},
  data() {
    return {
      myProps: this.props,
      list: [],
      name: "",
      type: "",
      src: "",
    };
  },
  created() {
    this.initialize();
  },
  methods: {
    initialize() {
      if (this.index == "origin") {
        this.list = [
          this.singleImage.photo_origin,
          this.singleImage.photo_upload,
          this.singleImage.photo_promap,
        ];
        this.name = "原始图片";
        this.type = "_origin";
        this.src = this.singleImage.photo_origin;
      } else if (this.index == "upload") {
        this.list = [
          this.singleImage.photo_upload,
          this.singleImage.photo_promap,
          this.singleImage.photo_origin,
        ];
        this.name = "上传图片";
        this.type = "_upload";
        this.src = this.singleImage.photo_upload;
      } else {
        this.list = [
          this.singleImage.photo_promap,
          this.singleImage.photo_origin,
          this.singleImage.photo_upload,
        ];
        this.name = "生成图片";
        this.type = "_promap";
        this.src = this.singleImage.photo_promap;
      }
    },
    getImageList() {
      this.$emit("getImageList");
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
