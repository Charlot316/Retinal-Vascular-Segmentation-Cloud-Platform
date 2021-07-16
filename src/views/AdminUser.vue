<template>
  <div>
    <el-button type="text" @click="goback">返回</el-button>
    <div class="crumbs">
      <el-breadcrumb separator="/">
        <el-breadcrumb-item>
          <i class="el-icon-lx-cascades"></i> 用户信息表
        </el-breadcrumb-item>
      </el-breadcrumb>
    </div>
    <div class="container">
      <div class="handle-box">
        <h1>操作用户</h1>
        <el-input
          @keyup.enter="handleSearch"
          v-model="searchparam.username"
          placeholder="请输入用户名的关键词"
          class="handle-input mr10"
        ></el-input>
        <el-button type="primary" icon="el-icon-search" @click="handleSearch"
          >搜索</el-button
        >
        <el-button
          type="primary"
          icon="el-icon-circle-plus-outline"
          @click="handleadd"
          >新增用户</el-button
        >
        <el-button
          v-if="Role===3"
          type="primary"
          icon="el-icon-circle-plus-outline"
          @click="handleaddStaff"
          >新增工作人员</el-button
        >
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
          label="用户 id"
          width="100"
          align="center"
        ></el-table-column>

        <el-table-column
          prop="username"
          label="用户名"
          align="center"
        ></el-table-column>
        <el-table-column
          prop="password"
          label="密码"
          align="center"
        >
        <template #default="scope">
            <span v-if="!(Role<=scope.row.role&&userid!==scope.row.user_id)">{{scope.row.password}}</span>
            <span v-else>无权查看</span>
        </template>
        </el-table-column>
        <el-table-column
          prop="role"
          label="身份"
          align="center"
        >
          <template #default="scope">
            <span v-if="scope.row.role == 1">普通用户</span>
            <span v-if="scope.row.role == 2">工作人员</span>
            <span v-if="scope.row.role == 3">管理员</span>
          </template>
        </el-table-column>
        <el-table-column prop="email" label="邮箱" align="center">
        </el-table-column>
        <el-table-column
          prop="sex"
          label="性别"
          align="center"
        >
          <template #default="scope">
            <span v-if="scope.row.sex == 1">男</span>
            <span v-if="scope.row.sex == 0">女</span>
          </template>
        </el-table-column>

        <el-table-column
          prop="uLendCount"
          label="借阅数量"
          align="center"
        ></el-table-column>
        <el-table-column label="操作" width="300" align="center">
          <template #default="scope">
            <el-button
              type="text"
              icon="el-icon-edit"
              @click="handleEditInfo(scope.$index)"
              >修改信息</el-button
            >
            <el-button
              type="text"
              icon="el-icon-delete"
              class="red"
              @click="handleDelete(scope.$index, scope.row)"
              >删除</el-button
            >
          </template>
        </el-table-column>
      </el-table>
      
      <!-- <div class="pagination">
        <el-pagination
          background
          layout="total, prev, pager, next"
          :current-page="query.pageIndex"
          :page-size="pageTotal"
          :total="pageTotal"
          @current-change="handlePageChange"
        ></el-pagination>
      </div> -->
    </div>
   
    <!-- 新增弹出框 -->
    <el-dialog title="新增用户" v-model="addVisible" width="30%">
      <el-form ref="form" :model="form" label-width="30%">
        <el-form-item label="用户名">
          <el-input v-model="form.username"></el-input>
        </el-form-item>
        <el-form-item label="密码">
          <el-input v-model="form.password"></el-input>
        </el-form-item>
        <el-form-item label="邮箱">
          <el-input v-model="form.email"></el-input>
        </el-form-item>
        <el-form-item label="性别">
          <el-radio-group v-model="form.sex">
            <el-radio :label="1">男</el-radio>
            <el-radio :label="0">女</el-radio>
          </el-radio-group>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="addVisible = false">取 消</el-button>
          <el-button type="primary" @click="saveadd">确 定</el-button>
        </span>
      </template>
    </el-dialog>
      <!-- 新增工作人员弹出框 -->
    <el-dialog title="新增工作人员" v-model="addStaffVisible" width="30%">
      <el-form ref="form" :model="form" label-width="30%">
        <el-form-item label="用户名">
          <el-input v-model="form.username"></el-input>
        </el-form-item>
        <el-form-item label="密码">
          <el-input v-model="form.password"></el-input>
        </el-form-item>
        <el-form-item label="邮箱">
          <el-input v-model="form.email"></el-input>
        </el-form-item>
        <el-form-item label="性别">
          <el-radio-group v-model="form.sex">
            <el-radio :label="1">男</el-radio>
            <el-radio :label="0">女</el-radio>
          </el-radio-group>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="addStaffVisible = false">取 消</el-button>
          <el-button type="primary" @click="saveaddStaff">确 定</el-button>
        </span>
      </template>
    </el-dialog>
    <!-- 编辑弹出框 -->
    <el-dialog title="编辑" v-model="editVisible" width="30%">
      <el-form ref="form" :model="form" label-width="30%">
        <el-form-item label="用户名">
          <el-input v-model="form.username"></el-input>
        </el-form-item>
        <el-form-item label="密码">
          <el-input v-model="form.password"></el-input>
        </el-form-item>
        <el-form-item label="邮箱">
          <el-input v-model="form.email"></el-input>
        </el-form-item>
        <el-form-item label="性别">
          <el-radio-group v-model="form.sex">
            <el-radio :label="1">男</el-radio>
            <el-radio :label="0">女</el-radio>
          </el-radio-group>
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
.handle-box {
  margin-bottom: 20px;
}

.handle-select {
  width: 120px;
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
        pageIndex: 1,
        pageSize: 50,
      },
      searchparam: { username: "" },
      tableData: [],
      multipleSelection: [],
      editVisible: false,
      addVisible: false,
      addStaffVisible:false,
      pageTotal: 0,
      form: {},
      idx: -1,
      id: -1,
    };
  },
  created() {this.getData();},
  methods: {
    // 获取 easy-mock 的模拟数据
    async getData() {
      const { data: res } = await this.$http.post(
        "getUserInformation",
        this.searchparam
      );
      console.log(res);
      if (res.status !== 200) return this.$message.error(res.message);
      this.tableData = res.result;
    },
    // 触发搜索按钮
    async handleSearch() {
       const { data: res } = await this.$http.post(
        "getUserInformation",
        this.searchparam
      );
      console.log(res);
      if (res.status !== 200) return this.$message.error(res.message);
      this.$message.success("获取用户信息成功");
      this.tableData = res.result;
    },
    // 删除操作
    handleDelete(index) {
      this.form = JSON.parse(JSON.stringify(this.tableData[index]));
      if(this.Role<=this.form.role&&this.userid!==this.form.user_id){
        return this.$message.error("无权删除其它工作人员或管理员的信息");
      }
      if(this.userid===this.form.user_id){
        return this.$message.error("不允许删除自己");
      }
      // 二次确认删除
      this.$confirm("确定要删除吗？", "提示", {
        type: "warning",
      })
        .then(async () => {
          const { data: res } = await this.$http.post("deleteUser", this.form);
          //this.$message.success(JSON.stringify(this.form));
          console.log(res);
          if (res.status !== 200) {
            return this.$message.error(res.message);
          } else {
            this.$message.success("删除用户成功");
            this.tableData.splice(index, 1);
          }
        })
        .catch(() => {});
    },

    async handleEditInfo(index) {
      this.idx = index;
      this.form = JSON.parse(JSON.stringify(this.tableData[index]));
      if(this.Role<=this.form.role&&this.userid!==this.form.user_id){
        return this.$message.error("无权修改其它工作人员或管理员的信息");
      }
      this.editVisible = true;
    },
    // 保存编辑
    async saveEdit() {
      const { data: res } = await this.$http.post("updateUserInfo", this.form);
      //this.$message.success(JSON.stringify(this.form));
      console.log(res);
      if (res.status !== 200) {
        if(res.status===422){
          return this.$message.error("用户名已存在");
        }
        return this.$message.error(res.message);
      } else {
        this.$message.success("修改用户信息成功");
        this.tableData[this.idx] = JSON.parse(JSON.stringify(this.form));
      }
      this.editVisible = false;
    },
    // 分页导航
    handlePageChange(val) {
      this.$set(this.query, "pageIndex", val);
      this.getData();
    },
    goback() {
      this.$router.push({ path: "/User" });
    },
    handleadd() {
      this.form = {};
      this.form.username="";
      this.form.password="";
      this.addVisible = true;
    },
    handleaddStaff(){
      this.form = {};
      this.form.username="";
      this.form.password="";
      this.addStaffVisible = true;
    },
    async saveaddStaff() {
      if(this.form.username==="") return this.$message.error("用户名不能为空");
      if(this.form.password==="") return this.$message.error("密码不能为空");
      const { data: res } = await this.$http.post("createStaff", this.form);
      //this.$message.success(JSON.stringify(this.form));
      console.log(res);
      if (res.status !== 200) {
        if(res.status===422){
          return this.$message.error("用户名已存在");
        }
        return this.$message.error(res.message+"请勿输入中文字符");
      } else {
        this.$message.success("新增工作人员成功");
        this.addStaffVisible = false;
        this.form.user_id = res.user_id;
        this.getData();
      }
    },
    async saveadd() {
      if(this.form.username==="") return this.$message.error("用户名不能为空");
      if(this.form.password==="") return this.$message.error("密码不能为空");
      const { data: res } = await this.$http.post("addStaff", this.form);
      //this.$message.success(JSON.stringify(this.form));
      console.log(res);
      if (res.status !== 200) {
        if(res.status===422){
          return this.$message.error("用户名已存在");
        }
        return this.$message.error(res.message+"请勿输入中文字符");
      }else {
        this.$message.success("新增用户成功");
        this.form.user_id = res.user_id;
        this.addVisible = false;
        this.getData();
      }
    },
  },
   computed: {
    Role() {
      let role = this.$store.state.role;
      return role;
    },
    userid() {
      let userid = this.$store.state.user_id;
      return userid;
    },
  },
};
</script>