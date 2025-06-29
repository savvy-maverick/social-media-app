<template>
    <!-- <div class="mb-6 flex items-center justify-between">
        <div class="flex items-center space-x-6">
            <img :src="comment.created_by.get_avatar" class="w-[40px] rounded-full">
            
            <p>
                <strong>
                    <RouterLink :to="{name: 'profile', params:{'id': comment.created_by.id}}"> {{ comment.created_by.name }} </RouterLink>
                </strong>
            </p>
        </div>

        <p class="text-gray-600">{{comment.created_at_formatted  }} ago</p>
    </div>

    <p>{{ Comment.body }}</p>
     -->
</template>

<script>
import axios from 'axios'
import { RouterLink } from 'vue-router'
export default {
    props: {
        comment: Object
    },

    components: { RouterLink }

    // methods: {
    //     likePost(id) {
    //         console.log('likePost', id)

    //         axios
    //             .post(`/api/posts/${id}/like/`)
    //             .then(response => {
    //                 console.log(response.data)
    //                 if (response.data.message == 'like created') {
    //                     this.post.likes_count += 1
    //                 }
    //             })
    //             .catch(error => {
    //                 console.log('error', error)
    //             })
    //     }
    // }
}

</script>