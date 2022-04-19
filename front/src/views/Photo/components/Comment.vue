<template>
  <div class="comment-box">
    <div>
      <user-icon :user="comment.doctor" />
      {{comment.content}}
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
  methods:{
      getPhotoInfo() {
      this.$emit("getPhotoInfo");
    },
  }
};
</script>

<style scope>
.comment-box{
    width:100%;
    background-color: white;
}
</style>
