<template>
    <el-tabs class="container">
        <el-tab-pane label="系统通知">
            <el-table :data="message" :show-header="false" style="width: 100%">
                <el-table-column type="index"></el-table-column>
                <el-table-column width="700px">
                    <template #default="scope">
                        <span class="message-title">{{scope.row.message}}</span>
                    </template>
                </el-table-column>
                <el-table-column width="200px" v-model="tmp"></el-table-column>
                <el-table-column prop="sendDate" class="col"></el-table-column>
            </el-table>
        </el-tab-pane>
  </el-tabs>
</template>
<script>
    export default {
        data() {
            return {
                message: [],
                tmp:""
            };
        },
        methods: {
            async getMessage(){
                const { data: res } = await this.$http.post("getMessage");
                this.message = res.result;
            }
        },
        created() {
            this.getMessage();
        }
    };
</script>
<style scoped>
.container {
    padding: 30px;
    background: #fff;
    border: 1px solid #ddd;
    border-radius: 5px;
}
.message-title{
    cursor: pointer;
}
.col{
    width:200px;
}
</style>
