<template>
  <div class="comment-box">
    <div class="comment-content">
      <user-icon :user="comment.doctor" />
      <span>{{ myComment.content }}</span>
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
  justify-content: center;
  align-items: center;
}
</style>
