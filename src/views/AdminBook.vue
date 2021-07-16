<template>
  <div>
    <el-button type="text" @click="goback">返回</el-button>

    <div class="crumbs">
      <el-breadcrumb separator="/">
        <el-breadcrumb-item>
          <i class="el-icon-lx-cascades"></i> 图书信息表
        </el-breadcrumb-item>
      </el-breadcrumb>
    </div>

    <div class="container">
      <div class="handle-box">
        <h1>操作图书</h1>
        <el-input
          @keyup.enter="handleSearch"
          v-model="searchparam.bName"
          placeholder="请输入书名的关键词"
          class="handle-input mr10"
          prob="bName"
        ></el-input>
        <el-button type="primary" icon="el-icon-search" @click="handleSearch"
          >搜索</el-button
        >
        <el-button
          type="primary"
          icon="el-icon-circle-plus-outline"
          @click="handleadd"
          >新增</el-button
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
          prop="bName"
          label="图书名"
          width="100"
          align="center"
        ></el-table-column>
        <el-table-column
          prop="book_index"
          label="图书索引号"
          width="100"
          align="center"
        ></el-table-column>

        <el-table-column prop="bAuthor" label="图书作者" align="center">
        </el-table-column>
        <el-table-column prop="bType" label="图书类型" align="center">
        </el-table-column>
        <el-table-column
          prop="bPublisher"
          label="图书出版社"
          align="center"
        ></el-table-column>

        <el-table-column
          prop="bAllCount"
          label="图书馆藏书量"
          width="50px"
          align="center"
        ></el-table-column>
        <el-table-column
          prop="bInCount"
          label="图书在馆数量"
          width="50px"
          align="center"
        ></el-table-column>
        <el-table-column
          prop="bLendCount"
          width="50px"
          label="图书被借次数"
          align="center"
        ></el-table-column>
        <el-table-column
          prop="bIntroduction"
          width="800px"
          label="图书简介"
          align="center"
        ></el-table-column>
        <el-table-column label="操作" width="180" align="center">
          <template #default="scope">
            <el-button
              type="text"
              icon="el-icon-edit"
              @click="handleEdit(scope.$index)"
              >编辑</el-button
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
          :current-page="pageIndex"
          :page-size="pageSize"
          :total="pageTotal"
          @current-change="handlePageChange"
        ></el-pagination>
      </div> -->
    </div>
    <!-- 新增弹出框 -->
    <el-dialog title="新增" v-model="addVisible" width="30%">
      <el-form ref="form" :model="form" label-width="30%">
        <el-form-item label="图书名">
          <el-input @keyup.enter="saveadd" v-model="form.bName"></el-input>
        </el-form-item>
        <el-form-item label="图书作者">
          <el-input @keyup.enter="saveadd" v-model="form.bAuthor"></el-input>
        </el-form-item>
        <el-form-item label="图书类型">
          <el-select
            v-model="form.bType"
            placeholder="下拉选择"
            class="handle-select mr10"
            id="selecter"
          >
            <el-option key="1" label="航空航天" value="航空航天"></el-option>
            <el-option key="2" label="数理科学和化学" value="数理科学和化学"></el-option>
            <el-option key="3" label="文学" value="文学"></el-option>
            <el-option key="4" label="历史" value="历史"></el-option>
            <el-option key="5" label="计算机" value="计算机"></el-option>
            <el-option key="6" label="社会科学" value="社会科学"></el-option>
            <el-option key="7" label="军事" value="军事"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="图书出版社">
          <el-input @keyup.enter="saveadd" v-model="form.bPublisher"></el-input>
        </el-form-item>
        <el-form-item label="图书馆藏书量">
          <el-input-number v-model="form.bAllCount" :min="0" :max="10000" ></el-input-number>
        </el-form-item>
        <el-form-item label="图书在馆数量">
          <el-input-number v-model="form.bInCount" :min="0" :max="10000" ></el-input-number>
        </el-form-item>
        <el-form-item label="图书被借次数">
          <el-input-number v-model="form.bLendCount" :min="0" :max="10000" ></el-input-number>
        </el-form-item>
        <el-form-item label="图书简介">
          <el-input
                @keyup.enter="saveadd"
                v-model="form.bIntroduction"
                type="textarea"
                :rows="7"
          ></el-input>
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
        <el-form-item label="图书名">
          <el-input @keyup.enter="saveEdit" v-model="form.bName"></el-input>
        </el-form-item>
        <el-form-item label="图书作者">
          <el-input @keyup.enter="saveEdit" v-model="form.bAuthor"></el-input>
        </el-form-item>
        <el-form-item label="图书类型">
          <el-select
            v-model="form.bType"
            placeholder="下拉选择"
            class="handle-select mr10"
            id="selecter"
          >
            <el-option key="1" label="航空航天" value="航空航天"></el-option>
            <el-option key="2" label="数理科学和化学" value="数理科学和化学"></el-option>
            <el-option key="3" label="文学" value="文学"></el-option>
            <el-option key="4" label="历史" value="历史"></el-option>
            <el-option key="5" label="计算机" value="计算机"></el-option>
            <el-option key="6" label="社会科学" value="社会科学"></el-option>
            <el-option key="7" label="军事" value="军事"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="图书出版社">
          <el-input @keyup.enter="saveEdit" v-model="form.bPublisher"></el-input>
        </el-form-item>
        <el-form-item label="图书简介">
          <el-input
                @keyup.enter="saveEdit"
                v-model="form.bIntroduction"
                type="textarea"
                :rows="7"
          ></el-input>
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
      queryInfo: {
        bName: "", //搜索的关键词
        pageNum: 1, //第几页
        pageSize: 50, //每页显示多少个
      },
      searchtype: "",
      searchparam: { bName: "" },
      pageIndex: 1,
      pageSize: 100,
      tableData: [],
      multipleSelection: [],
      editVisible: false,
      addVisible: false,
      pageTotal: 0,
      form: {},
      tempform:{},
      idx: -1,
      id: -1,
      res: [],
      tempmessage:"",
    };
  },
  created() {
    this.getBooksList();
  },
  methods: {
    // 获取 easy-mock 的模拟数据
    async getBooksList() {
      const { data: res } = await this.$http.post(
        "showAllBookInfo",
        this.queryInfo
      );
      this.tableData = res.bookList;
    },
    async getData() {
      const { data: res } = await this.$http.post(
        "getBookInformation",
        this.searchparam
      );
      console.log(res);
      if (res.status !== 200) return this.$message.error(res.message);
      this.$message.success("获取图书信息成功");
      this.tableData = res.result;
    },
    handleSizeChange(newSize) {
      this.queryInfo.pageSize = newSize;
      this.handleSearch();
    },
    handleCurrentChange(newpage) {
      this.queryInfo.pageNum = newpage;
      this.handleSearch();
    },
    // 触发搜索按钮
    handleSearch() {
      this.pageIndex = 1;
      this.getData();
    },
    // 删除操作
    handleDelete(index) {
      this.form = JSON.parse(JSON.stringify(this.tableData[index]));
      // 二次确认删除
      this.$confirm("确定要删除吗？", "提示", {
        type: "warning",
      })
        .then(async () => {
          const { data: res } = await this.$http.post("deleteBook", this.form);
          //this.$message.success(JSON.stringify(this.form));
          console.log(res);
          if (res.status !== 200) {
            return this.$message.error(res.message);
          } else {
            this.$message.success("删除图书成功");
            this.tableData.splice(index, 1);
          }
        })
        .catch(() => {});
    },

    // 编辑操作
    handleEdit(index) {
      this.idx = index;
      this.form = JSON.parse(JSON.stringify(this.tableData[index]));
      this.editVisible = true;
    },
    // 保存编辑
    async saveEdit() {
      if(this.form.bName==="") return this.$message.error("书名不准为空");
      if(this.form.bAuthor==="") return this.$message.error("作者名不准为空");
      if(this.form.bType==="") return this.$message.error("书的类型不准为空");
      if(this.form.bPublisher==="") return this.$message.error("出版社不准为空");
      const { data: res } = await this.$http.post("updateBookInfo", this.form);
      //this.$message.success(JSON.stringify(this.form));
      console.log(res);
      if (res.status !== 200) {
        if(res.status===422){
          return this.$message.error("未做任何更改或图书已存在");
        }
        return this.$message.error(res.message);
      } else {
        this.$message.success("修改图书信息成功");
        this.tableData[this.idx] = JSON.parse(JSON.stringify(this.form));
      }
      this.editVisible = false;
    },
    // 分页导航
    handlePageChange(val) {
      this.pageIndex = val;
      this.getData();
    },
    goback() {
      this.$router.push({ path: "/User" });
    },
    handleadd() {
      this.form = {};
      this.form.bName="";
      this.form.bAuthor="";
      this.form.bType="";
      this.form.bPublisher="";
      this.addVisible = true;
    },
    async saveadd() {
      if(this.form.bName==="") return this.$message.error("书名不准为空");
      if(this.form.bAuthor==="") return this.$message.error("作者名不准为空");
      if(this.form.bType==="") return this.$message.error("书的类型不准为空");
      if(this.form.bPublisher==="") return this.$message.error("出版社不准为空");
      this.form.bIntroduction="";
      var numReg = /^[0-9]*$/
      var numRe = new RegExp(numReg)
      if (!numRe.test(this.form.bAllCount)||!numRe.test(this.form.bInCount)||!numRe.test(this.form.bLendCount)) {
        return this.$message.error("请确认“藏书量”、“在馆数量”、“被借次数”输入的是数字");
      }
      const { data: res } = await this.$http.post("addBook", this.form);
      console.log(res);
      if (res.status !== 200) {
        if(res.status===422){
          return this.$message.error("图书已存在");
        }
        return this.$message.error(res.message);
      } else {
        this.$message.success("新增图书成功");
        this.tempmessage="图书馆上新图书：《"+this.form.bName+"》,欢迎大家阅读！";
        const { data: res } = await this.$http.post("sendMessage", {"message":this.tempmessage});
        //this.$message.success(JSON.stringify(this.form));
        console.log(res);
        this.getBooksList();
        this.addVisible = false;
      }
    },
  },
};
</script>