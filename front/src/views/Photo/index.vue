<template>
  <div>
    <div class="body">
      <!-- 左侧的固定快捷按钮 -->
      <div class="left"></div>
      <!-- 中间主体部分 -->
      <div class="middle">
        <head-content v-if="initial" :image="photo" style="margin-bottom:50px;"/>
        <middle-content v-if="initial" :image="photo" @getPhotoInfo="getPhotoInfo"/>
      </div>
      <!-- 右边的分页 -->
      <div class="right"></div>
    </div>
  </div>
</template>

<script>
import HeadContent from "./components/Head.vue";
import MiddleContent from "./components/Middle.vue";
export default {
  name: "Upload",
  components: {
    HeadContent,
    MiddleContent,
  },
  data() {
    return {
      photo: {
      },
      initial:false
    };
  },
  created() {
    this.getPhotoInfo();
  },
  methods: {
    async getPhotoInfo() {
      await new Promise((resolve) => {
        this.$http
          .post(
            "/getPhotoInfo/",
            JSON.stringify({ photo_id: this.$route.query.id,id:this.$store.state.user_id })
          )
          .then((res) => {
            if (res.data.success === false)
              return this.$message.error(res.data.message);
            this.photo = res.data.photo;
            this.initial=true
            console.log(JSON.stringify(this.photo));
          });
        resolve();
      }).then(() => {});
    },
  },
};
</script>

<style>
@import "style.css";
</style>
