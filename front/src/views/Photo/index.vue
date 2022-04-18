<template>
  <div>
    <div class="body">
      <!-- 左侧的固定快捷按钮 -->
      <div class="left">
      
      </div>
      <!-- 中间主体部分 -->
      <div class="middle">
        <middle-content/>
      </div>
      <!-- 右边的分页 -->
      <div class="right">
        
      </div>
    </div>
  </div>
</template>

<script>
import MiddleContent from "./componets/Middle.vue";
export default {
  
  name: "Upload",
  components: {
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
