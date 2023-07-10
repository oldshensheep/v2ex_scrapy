<script setup lang="ts">
import Topic from "@/components/base/Topic.vue";
import { type TopTopic, TopicBy } from '@/types/F'
import { ref, watchEffect } from "vue";

const selected = ref<TopicBy>(TopicBy.thank_count);
const datas = ref<TopTopic[]>();


const a = {
  clicks: '点击数',
  favorite_count: '收藏数',
  thank_count: '感谢数',
  votes: '投票数',
};

const b = {
  clicks: 'top-topic-by-clicks.json',
  favorite_count: 'top-topic-by-favorite_count.json',
  thank_count: 'top-topic-by-thank_count.json',
  votes: 'top-topic-by-votes.json',
};
watchEffect(() => {
  const url = b[selected.value]

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
        点击数 | 收藏数| 感谢数 | 投票数 最高的主题
      </div>
      <div class="flex items-center">
        <div>
          Order by 
        </div>
        <select v-model="selected" class="select select-bordered  ">
          <option selected>clicks</option>
          <option>favorite_count</option>
          <option>thank_count</option>
          <option>votes</option>
        </select>
      </div>

    </div>


    <table class="table">
      <thead>
        <tr>
          <th></th>
          <th>主题标题</th>
          <th>{{ a[selected] }}</th>
        </tr>
      </thead>
      <tbody v-for="(d, i) in datas">
        <tr class="hover">
          <th>{{ i + 1 }}</th>
          <td>
            <Topic :id="d.id" :title="d.title"></Topic>
          </td>
          <td>{{ d[selected] }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
