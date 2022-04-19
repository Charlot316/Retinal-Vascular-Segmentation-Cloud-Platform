<template>
  <div>
    <v-header />
    <div class="photo-body">
      <!-- 左侧的固定快捷按钮 -->
      <div class="left"></div>
      <!-- 中间主体部分 -->
      <div class="middle">
        <head-content v-if="initial" :image="photo" />
        <middle-content
          v-if="initial"
          :image="photo"
          @getPhotoInfo="getPhotoInfo"
        />
        <div v-for="comment in photo.comments" :key="comment">
          <my-comment :comment="comment"  @getPhotoInfo="getPhotoInfo"/>
        </div>
        <send-comment :image="photo"  @getPhotoInfo="getPhotoInfo"/>
      </div>
      <!-- 右边的分页 -->
      <div class="right"></div>
    </div>
  </div>
</template>

<script>
import HeadContent from "./components/Head.vue";
import MiddleContent from "./components/Middle.vue";
import MyComment from "./components/Comment.vue";
import SendComment from "./components/SendComment.vue";
import vHeader from "@/components/Doctor/Header";
export default {
  name: "Upload",
  components: {
    HeadContent,
    MiddleContent,
    vHeader,
    MyComment,
    SendComment,
  },
  data() {
    return {
      photo: {},
      initial: false,
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
            JSON.stringify({
              photo_id: this.$route.query.id,
              id: this.$store.state.user_id,
            })
          )
          .then((res) => {
            if (res.data.success === false)
              return this.$message.error(res.data.message);
            this.photo = res.data.photo;
            this.initial = true;
            console.log(JSON.stringify(this.photo));
          });
        resolve();
      }).then(() => {});
    },
  },
};
</script>

<style scope>
@import "style.css";
</style>
