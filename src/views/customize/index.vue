<template>
  <div class="app-container">
    <div style="display: flex">
      <span v-for="(item,index) in obj" :key="item.name" @click="test($event,index);cur=index">
        <input v-model="list" type="checkbox" :label="item.name" :value="item.name">
        {{ item.name }}
        <input v-if="cur==index" v-model="item.price" type="test" style="border:0px;border-bottom:1px solid black;width:30px">
      </span>
      <button @click="show">Submission</button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'CustomizeUserSelection',
  props: {
    msg: String
  },
  data() {
    return {
      cur: -1,
      checkList: ['Choose and block', 'Double check A'],
      list: [],
      obj: [
        { name: '1', price: '' },
        { name: '100', price: '' },
        { name: '44', price: '' },
        { name: '32', price: '' }
      ],
      oklist: []
    }
  },
  watch: {
    list: function(val) {
      console.log(this.list)
      if (this.list.length < 1) {
        this.cur = 50
      } else {
        for (const val in this.obj) {
          if (this.obj[val]['price'] !== '') {
            this.oklist.push(this.obj[val])
            console.log(this.oklist)
          }
        }
      }
    }
  },
  methods: {
    show() {
      console.log(this.obj)
    },
    test(e, index) {
      console.log('Select Object: ', index)
      console.log('List length', this.list.length)
      console.log(index, e)
      this.list.push(e.srcElement.value)
    }
  }
}
</script>
