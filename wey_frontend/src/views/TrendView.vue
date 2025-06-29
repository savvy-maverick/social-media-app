<template>
    <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
        

        <div class="main-center col-span-3 space-y-4">
            <div class="bg-white border border-gray-200 rounded-lg">
            
            </div>

           
            <div class="p-4 bg-white border border-gray-200 rounded-lg">
                <h2 class="text-xl">Trend: #{{ trend.hashtag }}</h2>
            </div>
            

            <div class="p-4 bg-white border border-gray-200 rounded-lg"
                v-for="post in posts"
                v-bind:key="post.id"
            >
                <FeedItem v-bind:post="post"/>  
            </div>
        </div>

        <div class="main-right col-span-1 space-y-4">
            <PeopleYouMayKnow />

            <Trends />
        </div>
    </div>
</template>

<script>
import FeedItem from '../components/FeedItem.vue'
import PeopleYouMayKnow from '../components/PeopleYouMayKnow.vue'
import Trends from '../components/Trends.vue'
import { useUserStore } from '@/stores/user'
import axios from 'axios'

export default {
    name: 'FeedView',
    setup() {
            const userStore = useUserStore()

            return {
                userStore
            }
        },
    components: {
        PeopleYouMayKnow,
        Trends,
        FeedItem,
    },

    data() {
        return {
            posts: [],
            trend: {}
            
        }
    },

    mounted () {
        this.getFeed()
    },

    watch: {
      '$route.params.id': {
         handler: function() {
            console.log('kkkkkk')
            this.getFeed()
         },
         deep: true,
         immediate: true
    }
   },

    methods: {
        getFeed() {
            axios
                // .get(`/api/posts/?trend=${this.$route.params.id}`)
                 .get(`/api/posts/trends/${this.$route.params.id}`)
                .then(response => {
                    console.log(response.data)
                     this.posts = response.data.posts
                     this.trend = response.data.trend
                })
                .catch(error => {
                    console.log('error', error)
                })
        },

        
    }
}
</script>