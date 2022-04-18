<template>
  <div>
    <div class="body">
      <!-- 左侧的固定快捷按钮 -->
      <div class="left">
      
      </div>
      <!-- 中间主体部分 -->
      <div class="middle">
        <head-content/>
        <middle-content/>
      </div>
      <!-- 右边的分页 -->
      <div class="right">
        
      </div>
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
    MiddleContent
  },
  data() {
    return {

    };
  },
  created() {
    
  },
  methods: {
   
  },
};
</script>

<style>
@import "style.css";
</style>
