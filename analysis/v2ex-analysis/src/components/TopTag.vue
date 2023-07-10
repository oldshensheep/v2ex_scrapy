<script setup lang="ts">
import Tag from "@/components/base/Tag.vue";
import { type TopTag } from '@/types/F'
import { ref } from "vue";

const datas = ref<TopTag[]>();

fetch("./tag-usage-count.json")
  .then((r) => r.json())
  .then((r) => {
    datas.value = r;
    console.log(r);
  });

</script>

<template>
  <div class="overflow-x-auto mt-4">
    使用次数最高的Tag（Tag为V2ex自动生成）
    <table class="table">
      <thead>
        <tr>
          <th></th>
          <th>Tag</th>
          <th>使用次数</th>
        </tr>
      </thead>
      <tbody v-for="(d, i) in datas">
        <tr class="hover">
          <th>{{ i + 1 }}</th>
          <td>
            <Tag :tag="d.tag"></Tag>
          </td>
          <td>{{ d.count }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
