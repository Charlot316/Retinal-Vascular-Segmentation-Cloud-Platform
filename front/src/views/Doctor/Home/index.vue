<template>
  <div class="about">
    <v-header />
      <div class="content">
        <router-view v-slot="{ Component }">
          <transition name="move" mode="out-in">
            <keep-alive :include="tagsList">
              <component :is="Component" />
            </keep-alive>
          </transition>
        </router-view>
        <!-- <el-backtop target=".content"></el-backtop> -->
      </div>
  </div>
</template>
<script>
  import vHeader from "../../../components/Doctor/Header";
  import vSidebar from "../../../components/Doctor/Sidebar";
  export default {
    components: {
      vHeader,
      vSidebar,
    },
    computed: {
      tagsList() {
        return this.$store.state.tagsList.map((item) => item.name);
      },
      collapse() {
        return this.$store.state.collapse;
      },
    },
  };
</script>
