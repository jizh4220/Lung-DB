<template>
  <el-checkbox class="app-checkbox" separator="/">
    <head>
      <title>Vue Js Get Checked Value of Checkbox If Use Array As A Model - Tutsmake.com</title>
    </head>
    <body class="bg-dark">
      <div class="container">
        <div class="col-md-7 offset-md-2  ">
          <div class="card mt-5">
            <div class="card-header">
              <h5>Vue Js Get Checked Value of Checkbox If Use Array As A Model - Tutsmake.com</h5>
            </div>
            <div class="card-body">
              <div id="checkbox">
                <!-- Check All -->
                <input v-model="isCheckAll" type="checkbox" @click="checkAll()"> Check All
                <!-- Checkboxes list -->
                <ul>
                  <el-checkbox-item v-for="lang in langsdata" :key="lang">
                    <input v-model="languages" type="checkbox" :value="lang" @change="updateCheckall()">{{ lang }}
                  </el-checkbox-item>
                </ul>
                <!-- Print -->
                <input type="button" value="Print Selected Values" @click="printValues()">
                <br>
                Selected items : {{ selectedlang }}
              </div>
            </div>
          </div>
        </div>
      </div>
    </body>
  </el-checkbox>
</template>

<script>
export default {
  data() {
    return {
      isCheckAll: false,
      langsdata: ['PHP', 'Vue.js', 'AngularJS', 'jQuery', 'JavaScript'],
      languages: [],
      selectedlang: ''
    }
  },
  watch: {
    $route() {
      this.getCheckbox()
    }
  },
  created() {
    this.getCheckbox()
  },
  methods: {
    getCheckbox() {
      // only show routes with meta.title
      let matched = this.$route.matched.filter(item => item.meta && item.meta.title)
      const first = matched[0]

      if (!this.isCheckbox(first)) {
        matched = [{ path: '/checkbox', meta: { title: 'Checkbox' }}].concat(matched)
      }

      this.levelList = matched.filter(item => item.meta && item.meta.title && item.meta.checkbox !== false)
    },
    checkAll() {
      this.isCheckAll = !this.isCheckAll
      this.languages = []
      if (this.isCheckAll) {
        // Check all
        for (var key in this.langsdata) {
          this.languages.push(this.langsdata[key])
        }
      }
    },
    updateCheckall() {
      if (this.languages.length === this.langsdata.length) {
        this.isCheckAll = true
      } else {
        this.isCheckAll = false
      }
    },
    printValues() {
      this.selectedlang = ''
      // Read Checked checkboxes value
      for (var key in this.languages) {
        this.selectedlang += this.languages[key] + ', '
      }
    }
  }
}
</script>
