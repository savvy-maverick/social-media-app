<template>
    <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
        

        <div class="main-center col-span-3 space-y-4">
            <div class="bg-white border border-gray-200 rounded-lg">
              <form v-on:submit.prevent="submitForm" method="post" >
                <div class="p-4">  
                    <textarea v-model="body" class="p-4 w-full bg-gray-100 rounded-lg" placeholder="What are you thinking about?"></textarea>
                </div>

                <div class="p-4 border-t border-gray-100 flex justify-between">
                    <a href="#" class="inline-block py-4 px-6 bg-gray-600 text-white rounded-lg">Attach image</a>

                    <input type="file" ref="file">

                    <button class="inline-block py-4 px-6 bg-purple-600 text-white rounded-lg">Post</button>
                </div>
              </form>
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
            body: '',
        }
    },

    mounted () {
        this.getFeed()
    },

    methods: {
        getFeed() {
            axios
                .get('/api/posts/')
                .then(response => {
                    console.log('data', response.data)
                    this.posts = response.data
                })
                .catch(error => {
                    console.log('error', error)
                })
        },

        submitForm() {
            

            axios
                .post('/api/posts/create/', {
                    'body': this.body
                })
                .then( response => {
                    console.log('data:', response.data)
                    
                    this.posts.unshift(response.data)
                    this.body = ''
                })
                .catch(error => {
                    console.log('error', error)
                })
        }
    }
}
</script>