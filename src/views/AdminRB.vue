<template>
  <div>
    <el-button type="text" @click="goback">返回</el-button>

    <div class="crumbs">
      <el-breadcrumb separator="/">
        <el-breadcrumb-item>
          <i class="el-icon-lx-cascades"></i> 借阅信息
        </el-breadcrumb-item>
      </el-breadcrumb>
    </div>
    <div class="container">
      <div class="handle-box">
        <h1>借还书操作</h1>
        <div class="returnborrow">
          <el-select
            v-model="operationType"
            placeholder="下拉选择"
            class="handle-select mr10"
            id="selecter"
          >
            <el-option key="1" label="借书" value="借书"></el-option>
            <el-option key="2" label="还书" value="还书"></el-option>
          </el-select>
          <el-input
            @keyup.enter="handleRB"
            v-model="query.user_id"
            placeholder="请输入用户ID"
            class="handle-input mr10"
          ></el-input>
          <el-input
            @keyup.enter="handleRB"
            v-model="query.book_id"
            placeholder="请输入图书ID"
            class="handle-input mr10"
          ></el-input>
          <el-button type="primary" icon="el-icon-s-tools" @click="handleRB"
            >操作</el-button
          >
        </div>
      </div>
    </div>
    <div class="container">
      <div class="handle-box">
        <h1>查询</h1>
        <div class="reserve">
          <el-select
            v-model="searchType"
            placeholder="下拉选择"
            class="handle-select mr10"
            id="selecter"
            @change="selectChanged"
          >
            <el-option key="1" label="借书情况" value="借书情况"></el-option>
            <el-option key="2" label="预约情况" value="预约情况"></el-option>
          </el-select>
          <el-input
            @keyup.enter="handleSearch"
            v-model="form.user_id"
            placeholder="请输入用户id"
            class="handle-input mr10"
          ></el-input>
          <el-input
           @keyup.enter="handleSearch"
            v-model="form.book_id"
            placeholder="请输入图书id"
            class="handle-input mr10"
          ></el-input>
          <el-button type="primary" icon="el-icon-search" @click="handleSearch"
            >搜索</el-button
          >
        </div>
      </div>
      <el-table
        :data="tableData"
        border
        class="table"
        ref="multipleTable"
        header-cell-class-name="table-header"
        @selection-change="handleSelectionChange"
      >
        <el-table-column
          prop="user_id"
          label="用户id"
          width="100"
          align="center"
        ></el-table-column>

        <el-table-column
          prop="book_id"
          label="图书id"
          align="center"
        ></el-table-column>

        <el-table-column
          prop="lDate"
          label="借书日期"
          align="center"
          v-if="searchType==='借书情况'"
        ></el-table-column>

        <el-table-column
          prop="dDate"
          label="应还日期"
          align="center"
          v-if="searchType==='借书情况'"
        ></el-table-column>

        <el-table-column label="操作" width="180" align="center">
          <template #default="scope">
            <el-button
              v-if="searchType === '借书情况'"
              type="text"
              icon="el-icon-delete"
              class="red"
              @click="handleDelete(scope.$index, scope.row)"
              >删除</el-button
            >
            <el-button
              v-if="searchType === '借书情况'"
              type="text"
              icon="el-icon-success"
              class="blue"
              @click="handleReturn(scope.$index)"
              >还书</el-button
            >
            <el-button
              v-if="searchType === '预约情况'"
              type="text"
              icon="el-icon-success"
              class="blue"
              @click="handleDelete(scope.$index, scope.row)"
              >预约取书</el-button
            >
          </template>
        </el-table-column>
      </el-table>
      <!-- <div class="pagination">
        <el-pagination
          background
          layout="total, prev, pager, next"
          :current-page="query.pageIndex"
          :page-size="query.pageSize"
          :total="pageTotal"
          @current-change="handlePageChange"
        ></el-pagination>
      </div> -->
    </div>
    <!-- 新增弹出框 -->
    <el-dialog title="新增" v-model="addVisible" width="30%">
      <el-form ref="form" :model="form" label-width="30%">
        <el-form-item label="用户id">
          <el-input v-model="form.user_id"></el-input>
        </el-form-item>
        <el-form-item label="图书id">
          <el-input v-model="form.book_id"></el-input>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="addVisible = false">取 消</el-button>
          <el-button type="primary" @click="saveadd">确 定</el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 编辑弹出框 -->
    <el-dialog title="编辑" v-model="editVisible" width="30%">
      <el-form ref="form" :model="form" label-width="30%">
        <el-form-item label="用户id">
          <el-input v-model="form.user_id"></el-input>
        </el-form-item>
        <el-form-item label="图书id">
          <el-input v-model="form.book_id"></el-input>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="editVisible = false">取 消</el-button>
          <el-button type="primary" @click="saveEdit">确 定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<style scoped>
.container {
  margin: 10px;
}
.handle-box {
  margin-bottom: 20px;
}

.handle-select {
  width: 120px;
}
.returnborrow {
  margin: 20px 0px;
}
.reserve {
  margin: 20px 0px;
}
.handle-input {
  width: 300px;
  display: inline-block;
}
.table {
  width: 100%;
  font-size: 14px;
}
.red {
  color: #ff0000;
}
.mr10 {
  margin-right: 10px;
}
.table-td-thumb {
  display: block;
  margin: auto;
  width: 40px;
  height: 40px;
}
</style>


<script>
export default {
  data() {
    return {
      query: {
        address: "",
        name: "",
        user_id:"",
        book_id:"",
        pageIndex: 1,
        pageSize: 10,
      },
      tableData: [],
      multipleSelection: [],
      editVisible: false,
      addVisible: false,
      pageTotal: 0,
      form: {
        user_id:"",
        book_id:"",
      },
      temp:{},
      tempforborrow:{},
      tempforborrow2:{},
      idx: -1,
      id: -1,
      operationType: "",
      searchType: "",
    };
  },
  created() {
    this.getData();
  },
  methods: {
    // 获取 easy-mock 的模拟数据
    async getData() {
      if (this.searchType === "借书情况") {
        const { data: res } = await this.$http.post(
          "getBookLending",
          this.form
        );
        console.log(res);
        if (res.status !== 200) return this.$message.error(res.message);
        this.$message.success("获取借阅信息成功");
        this.temp = res.result;
        this.tableData=[];
        this.tableData[0]=this.temp;
      } else if (this.searchType === "预约情况") {
        const { data: res } = await this.$http.post(
          "queryReservedBook",
          this.form
        );
        console.log(res);
        if (res.status !== 200) return this.$message.error(res.message);
        this.$message.success("获取预约信息成功");
        this.tableData=[];
        this.temp = res.result;
        this.tableData[0]=this.temp;
      }
    },
    // 触发搜索按钮
    handleSearch() {
      if(this.searchType === "借书情况"||this.searchType === "预约情况"){
        this.getData();
      }else{
        this.$message.error("请先在下拉框中选择操作");
      }
      
    },
    //下拉选择修改
    async selectChanged(){
      this.tableData= [];
      if (this.searchType === "借书情况") {
      const { data: res } = await this.$http.post(
              "getAllLendingInf",
            );
            //this.$message.success(JSON.stringify(this.form));
            console.log(res);
            if (res.status !== 200) {
              return this.$message.error(res.message);
            } else {
              this.tableData=res.result;
            }
      }
      else if (this.searchType === "预约情况") {
            const { data: res } = await this.$http.post(
              "getAllReserveInf",
            );
            //this.$message.success(JSON.stringify(this.form));
            console.log(res);
            if (res.status !== 200) {
              return this.$message.error(res.message);
            } else {
              this.tableData=res.result;
            }
      }
    },
    // 删除操作
    handleDelete(index) {
      if (this.searchType === "借书情况") {
        this.form = JSON.parse(JSON.stringify(this.tableData[index]));
        // 二次确认删除
        this.$confirm("确定要删除吗？", "提示", {
          type: "warning",
        })
          .then(async () => {
            const { data: res } = await this.$http.post(
              "deleteBookLending",
              this.form
            );
            //this.$message.success(JSON.stringify(this.form));
            console.log(res);
            if (res.status !== 200) {
              return this.$message.error(res.message);
            } else {
              this.$message.success("删除借阅信息成功");
              this.tableData.splice(index, 1);
            }
          })
          .catch(() => {});
      } else if (this.searchType === "预约情况") {
        this.form = JSON.parse(JSON.stringify(this.tableData[index]));
        // 二次确认删除
        this.$confirm("确定要预约取书吗？", "提示", {
          type: "inf",
        })
          .then(async () => {
            const { data: res } = await this.$http.post(
              "addReservedBookLending",
              this.form
            );
            //this.$message.success(JSON.stringify(this.form));
            console.log(res);
            if (res.status !== 200) {
              return this.$message.error(res.message);
            } else {
              this.$message.success("已完成预约取书");
              this.tableData.splice(index, 1);
            }
          })
          .catch(() => {});
      }
    },

    // 编辑操作
    handleEdit(index) {
      this.idx = index;
      this.form = JSON.parse(JSON.stringify(this.tableData[index]));
      this.editVisible = true;
    },
    // 保存编辑
    saveEdit() {
      this.editVisible = false;
      this.$message.success(`修改第 ${this.idx + 1} 行成功`);
      this.tableData[this.idx] = JSON.parse(JSON.stringify(this.form));
    },
    // 分页导航
    handlePageChange(val) {
      this.$set(this.query, "pageIndex", val);
      this.getData();
    },
    async handleReturn(index){
       this.temp = JSON.parse(JSON.stringify(this.tableData[index]));
      const { data: res } = await this.$http.post(
        "addBookReturned",
        this.temp
      );
      console.log(res);
      if (res.status !== 200) {
        return this.$message.error(res.message);
      } else {
        this.$message.success("还书成功");
        this.tableData=[];
        const { data: res } = await this.$http.post(
              "getAllLendingInf",
            );
            //this.$message.success(JSON.stringify(this.form));
            console.log(res);
            if (res.status !== 200) {
              return this.$message.error(res.message);
            } else {
              this.tableData=res.result;
            }
      }
    },
    async handleRB() {
      if (this.operationType === "借书") {
        const { data: userRes } = await this.$http.post("showUserInfo", {
        user_id: this.query.user_id,
        });
        this.tempforborrow=userRes;
        const { data: loginRes } = await this.$http.post("login", this.tempforborrow);
        this.tempforborrow2=loginRes;
        if(this.tempforborrow2.role!==1) return this.$message.error("工作人员与管理员不允许借书，请使用私人账号");
        const { data: res } = await this.$http.post(
          "addBookLending",
          this.query
        );
        console.log(res);
        if (res.status !== 200) {
          return this.$message.error(res.message);
        } else {
          this.$message.success(res.message);
          if (this.searchType === "借书情况") 
          {
            const { data: res } = await this.$http.post(
                  "getAllLendingInf",
                );
                //this.$message.success(JSON.stringify(this.form));
                console.log(res);
                if (res.status !== 200) {
                  return this.$message.error(res.message);
                } else {
                  this.tableData=res.result;
                }
          }
        }
      } else if (this.operationType === "还书") {
        const { data: res } = await this.$http.post(
          "addBookReturned",
          this.query
        );
        console.log(res);
        if (res.status !== 200) {
          return this.$message.error(res.message);
        } else {
          this.$message.success(res.message);
          if (this.searchType === "借书情况") 
          {
            const { data: res } = await this.$http.post(
                  "getAllLendingInf",
                );
                //this.$message.success(JSON.stringify(this.form));
                console.log(res);
                if (res.status !== 200) {
                  return this.$message.error(res.message);
                } else {
                  this.tableData=res.result;
                }
          }
        }
      }else{
        this.$message.error("请先在下拉框中选择操作");
      }
    },
    goback() {
      this.$router.push({ path: "/User" });
    },
    handleadd() {
      this.form = {};
      this.addVisible = true;
    },
    saveadd() {
      this.tableData.push(this.form);
      this.addVisible = false;
      this.$message.success("新增预约成功");
    },
  },
};
</script>