<script setup lang="ts">
import Comment from "@/components/base/Comment.vue";
import Topic from "@/components/base/Topic.vue";
import { type TopComment } from '@/types/F'
import { ref } from "vue";

const datas = ref<TopComment[]>();

fetch("./top-comment.json")
  .then((r) => r.json())
  .then((r) => {
    datas.value = r;
    console.log(r);
  });
</script>

<template>
  <div class="overflow-x-auto">
    感谢数最高的评论
    <table class="table">
      <thead>
        <tr>
          <th></th>
          <th>评论</th>
          <th>主题标题</th>
          <th>感谢数</th>
        </tr>
      </thead>
      <tbody v-for="(d, i) in datas">
        <tr class="hover">
          <th>{{ i + 1 }}</th>
          <td>
            <Comment :id="d.id" :topic-id="d.topic_id" :no="d.no" :content="d.content"></Comment>
          </td>
          <td>
            <Topic :id="d.topic_id" :title="d.title"></Topic>
          </td>
          <td>{{ d.thank_count }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
