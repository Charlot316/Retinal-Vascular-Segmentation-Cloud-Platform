<template>
  <div>
    <div :style="{ margin: '20px auto', width: '1000px' }">
      <el-steps :active="curStep" simple>
        <el-step
          title="检索患者名字"
          :status="getStatus('1')"
          @click="clickStep('1')"
        ></el-step>
        <el-step
          title="患者选择"
          :status="getStatus('2')"
          @click="clickStep('2')"
        ></el-step>
        <el-step
          title="上传图像"
          :status="getStatus('3')"
          @click="clickStep('3')"
        ></el-step>
      </el-steps>
    </div>
    <div>
    <step-1
      v-if="curStep == 1"
      @next-step="nextStep"
      :params="params"
    />
    <step-2
      v-if="curStep == 2"
      @next-step="nextStep"
      :params="params"
    />
    <step-3
      v-if="curStep == 3"
      @next-step="nextStep"
      @back-step="backStep"
      :params="params"
      :props="props"
      @getImageList="getImageList"
    />
    </div>
  </div>
</template>

<script>
import Step1 from "./step/Step1.vue";
import Step2 from "./step/Step2.vue";
import Step3 from "./step/Step3.vue";
export default {
  props: ["props"],
  components: {
    Step1,
    Step2,
    Step3,
  },
  data() {
    return {
      myProps: this.props,
      curStep: 1,
      params: {
        name:"",
        id: "",
      },
    };
  },
  methods: {
    getStatus(step) {
      if (this.curStep === step) {
        return "process";
      } else if (this.curStep < step) {
        return "wait";
      } else if (this.curStep > step) {
        return "success";
      }
    },
    nextStep() {
      this.curStep++;
    },
    clickStep(step) {
      if (step < this.curStep) this.curStep = step;
    },
    getImageList() {
      this.$emit("getImageList");
    },
    backStep() {
      this.curStep=1
      this.params={
        name:"",
        id: "",
      }
    },
  },
};
</script>
<style scoped>
.el-step:hover {
  cursor: pointer;
}
</style>