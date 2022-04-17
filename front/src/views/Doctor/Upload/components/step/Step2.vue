<template>
  <div>
    <el-card class="box-card">
      <el-input
        v-model="myParams.name"
        @keyup.enter="getPatientList"
        placeholder="请输入患者姓名"
        clearable
        style="width:calc(100% - 130px)"
      >
        <template #append>
          <el-button @click="getPatientList" icon="el-icon-search"></el-button>
        </template>
      </el-input>
      <el-button @click="addPatient" type="primary">新增为新患者</el-button>
    </el-card>
    <el-card class="box-card" v-loading="loading">
      <div v-if="patientList.length > 0">
        <div v-for="patient in patientList" :key="patient">
          <div
            style="display: flex;justify-content: space-between;align-items: center;padding:5px;"
          >
            <user-icon :user="patient"></user-icon>
            <el-button @click="submit(patient)" type="primary">选择</el-button>
          </div>
        </div>
      </div>
      <div v-else>
        <el-empty description="未查询到患者" />
      </div>
    </el-card>
  </div>
</template>

<script>
import UserIcon from "@/components/Public/Icon";
export default {
  props: ["params"],
  components: {
    UserIcon,
  },
  data() {
    return {
      myParams: this.params,
      patientList: [],
      loading: false,
    };
  },
  mounted() {
    this.getPatientList();
  },
  methods: {
    async getPatientList() {
      this.loading = true;
      await new Promise((resolve) => {
        this.$http
          .post("/findPatient/", JSON.stringify({ name: this.myParams.name }))
          .then((res) => {
            {
              if (res.data.success == true) {
                this.patientList = res.data.p_list;
                this.loading = false;
              } else {
                this.$message.error(res.data.message);
                this.loading = false;
              }
            }
          });
        resolve();
      }).then(() => {});
    },
    async addPatient() {
      await new Promise((resolve) => {
        this.$http
          .post("/addPatient/", JSON.stringify({ name: this.myParams.name }))
          .then((res) => {
            {
              if (res.data.success == true) {
                this.myParams.id = res.data.patient_ID;
                this.$message.success(res.data.message);
                this.$emit("next-step");
              } else {
                this.$message.error(res.data.message);
              }
            }
          });
        resolve();
      }).then(() => {});
    },
    submit(patient) {
      this.myParams.id = patient.patient_ID;
      this.$emit("next-step");
    },
  },
};
</script>

<style scoped>
.box-card {
  width: 900px;
  margin: 0 auto;
}
.identify-choose {
  display: inline-block;
  width: 230px;
  height: 120px;
  margin: 30px;
  border: solid 1px rgb(116, 179, 242);
  border-radius: 4px;
  display: flex;
  justify-content: center;
  align-items: center;
}
.identify-choose :hover {
  cursor: pointer;
}
.hint:hover {
  cursor: pointer;
}
.error-tip {
  color: red;
  font-size: 12px;
  padding-top: 10px;
}
</style>
