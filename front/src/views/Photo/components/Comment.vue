<template>
  <div class="comment-box">
    <div class="comment-content">
      <div class="comment-content inner">
        <user-icon :user="comment.doctor" />
        <span>{{ myComment.content }}</span>
      </div>
      <div>
        <el-button
          v-if="comment.doctor.id == $store.state.user_id"
          type="text"
          size="mini"
          @click="deleteComment"
        >
          删除
        </el-button>
      </div>
    </div>
  </div>
</template>

<script>
import UserIcon from "@/components/Public/Icon.vue";
export default {
  props: ["comment"],
  components: {
    UserIcon,
  },
  data() {
    return {
      myComment: this.comment,
    };
  },
  methods: {
    getPhotoInfo() {
      this.$emit("getPhotoInfo");
    },
    async deleteComment() {
      await new Promise((resolve) => {
        this.$http
          .post(
            "/deleteComment/",
            JSON.stringify({
              comment_id:this.comment.id,
              doctor_id: this.$store.state.user_id,
            })
          )
          .then((res) => {
            {
              if (res.data.success == true) {
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
.comment-content {
  display: flex;
  align-items: center;
  padding:10px;
}
.comment-content .inner {
  width:90%;
}

</style>
