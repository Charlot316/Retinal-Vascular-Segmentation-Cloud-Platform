<template>
  <div class="comment-box">
    <div>
      <el-input
        v-model="content"
        autosize
        placeholder="请输入评论"
        @keyup.enter="submit"
      >
      <template #append>
        <el-button @click="submit" icon="el-icon-s-comment" />
      </template>
      </el-input>
    </div>
  </div>
</template>

<script>
export default {
  props: ["image"],
  data() {
    return {
      content: "",
    };
  },
  methods: {
    getPhotoInfo() {
      this.$emit("getPhotoInfo");
    },
    async submit() {
      if (this.content.trim().length == 0)
        return this.$message.error("评论不能为空");
        console.log(this.$store.state.user_id)
      await new Promise((resolve) => {
        this.$http
          .post(
            "/sendComment/",
            JSON.stringify({
              photo_id: this.image.photo_id,
              content: this.content,
              doctor_id: this.$store.state.user_id
            })
          )
          .then((res) => {
            {
              if (res.data.success ==true) {
                this.$message.success("评论发布成功");
                this.getPhotoInfo();
              } else {
                this.$message.error("发布失败");
              }
            }
          });
        resolve();
      }).then(() => {});

    },
  },
};
</script>

<style scope>
.comment-box {
  width: 100%;
  background-color: white;
}
</style>
