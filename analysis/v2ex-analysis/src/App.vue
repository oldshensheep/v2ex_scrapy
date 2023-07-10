<script setup lang="ts">
import { onMounted } from "vue";

// @ts-ignore
import Plotly from 'plotly.js-dist-min'

import TopCommentVue from "./components/TopComment.vue";
import TopTopicVue from "./components/TopTopic.vue";
import TopMemberVue from "./components/TopMember.vue";
import TopTagVue from "./components/TopTag.vue";


onMounted(() => {
  fetch('new-topic-every-month.json')
    .then(r => r.json())
    .then(r => {
      console.log(r);
      Plotly.newPlot("new-topic",
        [{ "x": Object.values(r.date), "y": Object.values(r.topic_count) }],
        {
          title: '每月新增帖子',
          yaxis: {
            tickformat: 'd'
          }, dragmode: 'pan'
        },
        { scrollZoom: true },
      )
    })
  fetch('new-comment-every-month.json')
    .then(r => r.json())
    .then(r => {
      console.log(r);
      Plotly.newPlot("new-comment",
        [{ "x": Object.values(r.date), "y": Object.values(r.comment_count) }],
        {
          title: '每月新增评论',
          yaxis: {
            tickformat: 'd'
          },
          dragmode: 'pan'
        },
        { scrollZoom: true },
      )
    })
  fetch('new-member-every-month.json')
    .then(r => r.json())
    .then(r => {
      console.log(r);
      Plotly.newPlot("new-member",
        [{ "x": Object.values(r.date).slice(1,), "y": Object.values(r.member_count) }],
        {
          title: '每月新增用户（部分用户404，不能获取注册时间）',
          yaxis: {
            tickformat: 'd'
          },
          dragmode: 'pan'
        },
        { scrollZoom: true },
      )
    })
})


</script>

<template>
  <main>
    <div>
      <div>
        <TopCommentVue></TopCommentVue>
        <TopTopicVue></TopTopicVue>
        <TopMemberVue></TopMemberVue>
        <TopTagVue></TopTagVue>
        <div id="new-topic"></div>
        <div id="new-comment"></div>
        <div id="new-member"></div>
      </div>
    </div>
  </main>
</template>

<style scoped></style>
