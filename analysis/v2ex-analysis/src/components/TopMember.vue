<script setup lang="ts">
import Member from "@/components/base/Member.vue";
import { UserBy, type TopMember } from '@/types/F'
import { ref, watchEffect } from "vue";


const selected = ref<UserBy>(UserBy.topic_count);
const datas = ref<TopMember[]>();

const a = {
  comment_count: '评论数',
  topic_count: '发帖数',
};
const b = {
  topic_count: 'top-user-by-topic_count.json',
  comment_count: 'top-user-by-comment_count.json',
};

watchEffect(() => {
  let url = b[selected.value]

  fetch(url)
    .then((r) => r.json())
    .then((r) => {
      datas.value = r;
      console.log(r);
    });
})

</script>

<template>
  <div class="overflow-x-auto mt-4">
    <div class="flex justify-between">
      <div class="flex items-center">
        评论数 | 发帖数 最多的用户
      </div>
      <div class="flex items-center">
        <div>
          Order by
        </div>
        <select v-model="selected" class="select select-bordered">
          <option selected>topic_count</option>
          <option>comment_count</option>
        </select>
      </div>
    </div>
    <table class="table">
      <thead>
        <tr>
          <th></th>
          <th>用户名</th>
          <th>{{ a[selected] }}</th>
        </tr>
      </thead>
      <tbody v-for="(d, i) in datas">
        <tr class="hover">
          <th>{{ i + 1 }}</th>
          <td>
            <Member :username="d.username"></Member>
          </td>
          <td>{{ d[selected] }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
